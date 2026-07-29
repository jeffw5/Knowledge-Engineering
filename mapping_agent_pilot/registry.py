"""
registry.py
-----------
Agent Registry (design doc Section 3.7): a persistent identity per
Domain Mapping Agent, its bound scope, and its lifecycle state
(DEV -> STG -> PRD). This is what lets the drift monitor and circuit
breaker attach state to "this specific agent" rather than to an
anonymous function call.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict


@dataclass
class AgentRecord:
    agent_id: str
    domain: str
    lifecycle_state: str = "DEV"
    registered_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class AgentRegistry:
    def __init__(self):
        self._agents: Dict[str, AgentRecord] = {}

    def register(self, agent_id: str, domain: str) -> AgentRecord:
        record = AgentRecord(agent_id=agent_id, domain=domain)
        self._agents[agent_id] = record
        return record

    def promote(self, agent_id: str, new_state: str):
        assert new_state in ("DEV", "STG", "PRD")
        self._agents[agent_id].lifecycle_state = new_state

    def quarantine(self, agent_id: str):
        self._agents[agent_id].lifecycle_state = "QUARANTINED"

    def get(self, agent_id: str) -> AgentRecord:
        return self._agents[agent_id]

    def report(self) -> str:
        lines = []
        for agent_id, r in self._agents.items():
            lines.append(f"  {agent_id:22s} domain={r.domain:12s} state={r.lifecycle_state}")
        return "\n".join(lines)
