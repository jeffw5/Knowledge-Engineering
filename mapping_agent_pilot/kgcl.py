"""
kgcl.py
-------
KGCL Commit stage (design doc Section 3.5).

Appends an accepted mapping to a JSON-lines change log carrying full
WHO/WHAT/WHEN/WHERE/WHY provenance plus which agent proposed it and which
validation checks it passed. In production this writes a real KGCL record
into the GraphDB; here it's a flat file so the pilot output is easy to
inspect after a run.
"""

import json
import os
from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class KGCLRecord:
    what: str            # concept URI the artifact was mapped to
    who: str              # agent identity that proposed it
    when: str             # timestamp
    where: str            # domain
    why: str              # rationale / confidence
    artifact_id: str
    confidence: float
    validation: str       # "passed: shacl, swrl, pep"


class KGCLCommitLog:
    def __init__(self, path: str):
        self.path = path
        # start each pilot run with a clean log so results are easy to read.
        # (truncate via 'w' rather than os.remove -- some sandboxes disallow
        # deleting a file that already exists but allow truncating it)
        with open(self.path, "w"):
            pass

    def commit(self, record: KGCLRecord):
        with open(self.path, "a") as f:
            f.write(json.dumps(asdict(record)) + "\n")

    def read_all(self):
        if not os.path.exists(self.path):
            return []
        with open(self.path) as f:
            return [json.loads(line) for line in f if line.strip()]
