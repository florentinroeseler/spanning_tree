"""Einlesen und Parsen der Textdatei."""
from __future__ import annotations
import re
from pathlib import Path
from typing import Dict

from .models import Node, NeighborState

_EDGE_RE = re.compile(r"^([A-Za-z]\w*)\s*-\s*([A-Za-z]\w*)\s*:\s*(\d+)\s*;")
_NODE_RE = re.compile(r"^([A-Za-z]\w*)\s*=\s*(\d+)\s*;")
_COMMENT_RE = re.compile(r"^\s*(//.*)?$")


def _touch(nodes: Dict[str, Node], name: str) -> Node:
    if name not in nodes:
        nodes[name] = Node(name=name, node_id=0)
    return nodes[name]


def parse_graph_file(path: str | Path) -> Dict[str, Node]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    nodes: Dict[str, Node] = {}

    with path.open(encoding="utf-8") as fp:
        for lineno, raw in enumerate(fp, 1):
            line = raw.strip()
            if _COMMENT_RE.match(line):
                continue  # leer oder Kommentar

            if m := _NODE_RE.match(line):
                name, nid = m.groups()
                _touch(nodes, name).node_id = int(nid)
                continue

            if m := _EDGE_RE.match(line):
                a, b, cost_s = m.groups()
                cost = int(cost_s)
                if cost <= 0:
                    raise ValueError(f"Edge cost must be >0 (line {lineno})")

                na = _touch(nodes, a)
                nb = _touch(nodes, b)
                _add_edge(nodes, a, b, cost)      # legt beide Richtungen korrekt an
                continue

            raise SyntaxError(f"{path}:{lineno}: ungültige Zeile: {line}")

    # Konsistenz‑Checks
    missing = [n.name for n in nodes.values() if n.node_id is None]
    if missing:
        raise ValueError(f"Keine node_id für: {', '.join(missing)}")

    return nodes

def _add_edge(nodes, name_a, name_b, cost):
    a, b = nodes[name_a], nodes[name_b]

    # ↑  Einmal für A–B …
    a.neighbors[b.name] = NeighborState(
        link_cost=cost,
        root_id=b.node_id,         #  !!!  nicht a.node_id
        total_cost=0,
    )
    # ↓  … und einmal für B–A
    b.neighbors[a.name] = NeighborState(
        link_cost=cost,
        root_id=a.node_id,
        total_cost=0,
    )

