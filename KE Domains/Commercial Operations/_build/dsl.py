"""Authoring DSL for the Commercial Operations domain specifications.

Each domain spec (spec_<domain>.py) is a plain list of these records. build_domains.py turns them into
vocabulary-domain-*, taxonomy-domain-*, ontology-domain-* and shapes-domain-* Turtle/TriG files.

References
  vocabulary terms : 'core-role/client', 'domain-sales/quota'          (…/vocabulary/<scheme>/<term>)
  ontology classes : 'core:process-step', 'sales:selling-step'          (ontology prefix : local name)
  taxonomy broader : the local id of a concept in the same taxonomy
"""
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class V:                      # vocabulary primitive
    id: str
    label: str
    definition: str
    alt: List[str] = field(default_factory=list)
    broader: Optional[str] = None      # local id in the same vocabulary
    scope: Optional[str] = None
    promote: Optional[str] = None      # reason this general primitive is a candidate for promotion to the core
    homonym: Optional[str] = None      # core term with the same label but a different sense (kept apart on purpose)


@dataclass
class C:                      # taxonomy concept
    id: str
    label: str
    definition: str
    subjects: List[str]                # primitives it is built from, in phrase order
    broader: Optional[str] = None      # None: top concept
    primary: Optional[str] = None      # head primitive (default: last subject)
    alt: List[str] = field(default_factory=list)
    formalized: Optional[str] = None   # class (required on top concepts)
    scope: Optional[str] = None


@dataclass
class K:                      # ontology class
    id: str
    label: str
    definition: str
    parents: List[str]
    primary: str
    restrictions: List[Tuple[str, str, str]] = field(default_factory=list)   # ('some'|'only', property, class)
    alt: List[str] = field(default_factory=list)
    scope: Optional[str] = None


@dataclass
class P:                      # ontology object property
    id: str
    label: str
    definition: str
    parent: str                        # a core relation, or an RO relation ('obo:RO_…') when no core relation fits
    inverse: Optional[str] = None
    scope: Optional[str] = None
    promote: Optional[str] = None      # reason this general relation is a candidate for promotion to the core


@dataclass
class S:                      # SHACL node shape
    id: str                            # without the -shape suffix
    label: str
    definition: str
    target: str
    props: List[dict] = field(default_factory=list)  # path, cls | or_cls, min, max, msg, warn
