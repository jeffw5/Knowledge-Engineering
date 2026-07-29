"""
llm_backend.py
--------------
The seam where "agentic AI built on Claude" plugs into the pilot.

DomainMappingAgent (see domain_agent.py) never calls an LLM SDK directly --
it calls an LLMBackend. Two implementations are provided:

  * AnthropicBackend  -- real Claude call, used automatically if the
                          `anthropic` package is installed AND an
                          ANTHROPIC_API_KEY is present in the environment.
  * HeuristicBackend  -- a deterministic keyword/overlap scorer with no
                          external dependencies, used as a fallback so the
                          pilot runs standalone in any sandbox.

This is intentionally the only file that needs to change to move from the
pilot to a production agent: swap HeuristicBackend's role for a real
Claude Agent SDK agent with MCP tool access to the domain's vector DB and
ontology, per Section 3.1 of the design doc. Everything downstream
(the validation gate, KGCL commit, drift monitor) does not care which
backend produced the proposal -- it only trusts the deterministic gate.
"""

import os
import re
from typing import List, Tuple

from ontology import Concept


class LLMBackend:
    """Interface: given artifact text and candidate concepts, return ranked
    (concept, confidence, evidence) proposals. confidence is 0..1."""

    def propose(self, artifact_text: str, candidates: List[Concept]) -> List[Tuple[Concept, float, str]]:
        raise NotImplementedError


class HeuristicBackend(LLMBackend):
    """
    Pure-Python stand-in for the domain agent's reasoning step. Uses simple
    keyword-overlap scoring against each candidate concept's keyword list --
    this is the same *role* a domain vector DB + Claude reasoning step plays
    (Section 3.1: "vector search narrows candidates; the ontology decides
    which are valid"), just without an embedding model or an LLM call.
    """

    def propose(self, artifact_text: str, candidates: List[Concept]) -> List[Tuple[Concept, float, str]]:
        text_norm = re.sub(r"[^a-z0-9\s]", " ", artifact_text.lower())
        tokens = set(text_norm.split())

        scored = []
        for concept in candidates:
            hits = [kw for kw in concept.keywords if kw in text_norm]
            if not hits:
                continue
            # crude confidence: fraction of the concept's keyword vocabulary that matched,
            # boosted slightly by absolute hit count so richer matches win ties.
            confidence = min(1.0, (len(hits) / len(concept.keywords)) + 0.1 * (len(hits) - 1))
            evidence = f"matched keywords: {', '.join(hits)}"
            scored.append((concept, round(confidence, 2), evidence))

        scored.sort(key=lambda t: t[1], reverse=True)
        return scored


class AnthropicBackend(LLMBackend):
    """
    Real backend. Sends the artifact text and the domain's candidate concept
    list to Claude and asks it to rank the candidates with a confidence and
    a supporting quote. Requires `pip install anthropic` and
    ANTHROPIC_API_KEY set in the environment.
    """

    def __init__(self, model: str = "claude-sonnet-5"):
        import anthropic  # deferred import: only required if this backend is used
        self.client = anthropic.Anthropic()
        self.model = model

    def propose(self, artifact_text: str, candidates: List[Concept]) -> List[Tuple[Concept, float, str]]:
        candidate_desc = "\n".join(f"- {c.uri}: {c.label} ({', '.join(c.keywords)})" for c in candidates)
        prompt = (
            "You are a domain mapping agent scoped to exactly one ontology domain. "
            "Given the artifact below and the candidate concepts from your domain, "
            "return a JSON list of objects {uri, confidence 0-1, evidence} for every "
            "candidate that plausibly matches, most confident first. Do not invent "
            "concepts outside this list.\n\n"
            f"Artifact:\n{artifact_text}\n\nCandidates:\n{candidate_desc}"
        )
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        # Parsing left intentionally minimal -- production code should validate
        # the JSON against a schema before trusting it as a "proposal."
        import json
        text = response.content[0].text
        try:
            parsed = json.loads(text)
        except (ValueError, KeyError):
            return []
        by_uri = {c.uri: c for c in candidates}
        results = []
        for item in parsed:
            concept = by_uri.get(item.get("uri"))
            if concept:
                results.append((concept, float(item.get("confidence", 0)), item.get("evidence", "")))
        return results


def get_default_backend() -> LLMBackend:
    """Picks AnthropicBackend if usable, else falls back to the heuristic one."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            return AnthropicBackend()
        except ImportError:
            pass
    return HeuristicBackend()
