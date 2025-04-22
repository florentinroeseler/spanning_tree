"""Verteilte Berechnung des Spanning‑Trees."""
from __future__ import annotations
import random
import time
from typing import Dict

from .models import Node


def _step(node: Node, nodes: Dict[str, Node]) -> bool:
    """Bearbeite *einen* Knoten.  Rückgabe: hat sich etwas geändert?"""
    changed = False

    best_root = node.node_id
    best_cost = 0
    best_hop: str | None = None

    # 1) Angebote der Nachbarn prüfen
    for nb_name, nb_state in node.neighbors.items():
        offer_root = nb_state.root_id
        offer_cost = nb_state.total_cost + nb_state.link_cost
        if offer_root < best_root or (offer_root == best_root and offer_cost < best_cost):
            best_root = offer_root
            best_cost = offer_cost
            best_hop = nb_name

    # 2) Eigenen Zustand anpassen
    if best_hop is not None and node.next_hop != best_hop:
        node.next_hop = best_hop
        changed = True

    # 3) neues Angebot an alle Nachbarn senden (Broadcast)
    for nb_name, local in node.neighbors.items():
        remote = nodes[nb_name].neighbors[node.name]       # Gegenrichtung
        offer_cost = best_cost + local.link_cost           # <── KOSTEN ADDIEREN
        if remote.root_id != best_root or remote.total_cost != offer_cost:
            remote.root_id   = best_root
            remote.total_cost = offer_cost
            changed = True

    node.msg_cnt += 1
    return changed




def run_spanning_tree(nodes, *, max_rounds=1000):
    rnd = random.Random(int(time.time()))
    for _ in range(max_rounds):
        changed = False

        # jede Runde alle Knoten – aber in zufälliger Reihenfolge
        names = list(nodes.keys())
        rnd.shuffle(names)
        for name in names:
            if _step(nodes[name], nodes):
                changed = True

        if not changed:          # gesamte Matrix stabil  →  fertig
            return

    raise RuntimeError("Spanning‑Tree konvergiert nicht (max_rounds überschritten)")

def print_spanning_tree(nodes):
    root = min(nodes.values(), key=lambda n: n.node_id)
    print("Spanning-Tree {")
    print(f"  Root: {root.name}")
    for n in nodes.values():
        if n.next_hop:                       # KEIN weiterer Filter
            print(f"  {n.name} - {n.next_hop}")
    print("}")


def dump_state(nodes):
    for n in nodes.values():
        print(f"{n.name}: next={n.next_hop}  myRoot={n.node_id}")
        for nb, link in n.neighbors.items():
            print(f"   -> {nb}: root={link.root_id} cost={link.total_cost}")
    print("-" * 40)

