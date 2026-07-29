"""
monitor.py
----------
Drift & Governance Monitor (design doc Section 3.6).

Tracks, per agent, a rolling window of validation outcomes and derives three
signals:

  * MTBH proxy            -- artifacts processed since the last rejection
                              (a real implementation stratifies this by
                              WHO/WHAT/WHEN/WHERE/WHY; the pilot tracks one
                              aggregate number per agent to keep the demo
                              readable, but the per-dimension breakdown is
                              the documented design -- see README).
  * Value-Drift Coefficient proxy -- rolling rejection rate over the window.
  * Circuit breaker        -- trips when the rejection rate crosses a
                              domain-specific threshold within the window.
                              A tripped agent's future proposals are
                              quarantined (not committed) until reset, but
                              no other agent is affected.
"""

from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict


@dataclass
class AgentHealth:
    agent_id: str
    window: Deque[bool] = field(default_factory=lambda: deque(maxlen=10))  # True = accepted
    since_last_rejection: int = 0
    tripped: bool = False
    trip_reason: str = ""

    def record(self, accepted: bool, threshold: float):
        self.window.append(accepted)
        if accepted:
            self.since_last_rejection += 1
        else:
            self.since_last_rejection = 0

        if len(self.window) >= 3:
            rejection_rate = 1 - (sum(self.window) / len(self.window))
            if rejection_rate > threshold and not self.tripped:
                self.tripped = True
                self.trip_reason = (
                    f"rejection rate {rejection_rate:.0%} over last {len(self.window)} "
                    f"proposals exceeds the {threshold:.0%} threshold"
                )

    @property
    def value_drift_coefficient(self) -> float:
        if not self.window:
            return 0.0
        return round(1 - (sum(self.window) / len(self.window)), 2)

    def reset_breaker(self):
        self.tripped = False
        self.trip_reason = ""
        self.window.clear()
        self.since_last_rejection = 0


class DriftMonitor:
    def __init__(self, circuit_breaker_threshold: float = 0.5):
        self.threshold = circuit_breaker_threshold
        self.health: Dict[str, AgentHealth] = {}

    def _get(self, agent_id: str) -> AgentHealth:
        if agent_id not in self.health:
            self.health[agent_id] = AgentHealth(agent_id=agent_id)
        return self.health[agent_id]

    def is_tripped(self, agent_id: str) -> bool:
        return self._get(agent_id).tripped

    def record_outcome(self, agent_id: str, accepted: bool):
        self._get(agent_id).record(accepted, self.threshold)

    def report(self) -> str:
        lines = []
        for agent_id, h in self.health.items():
            state = "TRIPPED" if h.tripped else "healthy"
            lines.append(
                f"  {agent_id:22s} state={state:8s} "
                f"value_drift={h.value_drift_coefficient:.2f}  "
                f"mtbh_proxy={h.since_last_rejection} artifacts since last rejection"
                + (f"  [{h.trip_reason}]" if h.tripped else "")
            )
        return "\n".join(lines)
