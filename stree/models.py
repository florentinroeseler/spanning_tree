from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class NeighborState:
    """Zustand, den *dieser* Knoten pro Nachbar führt (BPDU‑Puffer)."""

    link_cost: int           # feste Linkkosten
    root_id: int             # zuletzt erhaltene Root‑ID vom Nachbarn
    total_cost: int          # Pfadkosten des Nachbarn bis zur Root

@dataclass
class Node:
    """Repräsentiert einen Graph‑Knoten (Switch)."""

    name: str
    node_id: int
    neighbors: Dict[str, NeighborState] = field(default_factory=dict)

    # dynamische Felder während der Simulation
    next_hop: Optional[str] = None   # wohin leite ich Frames zur Root?
