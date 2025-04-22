"""Kommandozeile: python -m stree.cli <graph-file>"""
from __future__ import annotations
import argparse

from .parser import parse_graph_file
from .spanning_tree import dump_state, run_spanning_tree, print_spanning_tree


def main() -> None:
    ap = argparse.ArgumentParser(description="Spanning‑Tree‑Simulation (Layer‑2)")
    ap.add_argument("graph_file", help="Pfad zur Input‑Datei")
    ap.add_argument("--max-rounds", type=int, default=1000, help="maximale Simulations‑Runden")
    ns = ap.parse_args()

    nodes = parse_graph_file(ns.graph_file)
    print("== Knotentabelle ==")
    for n in nodes.values():
        print(f"{n.name:2}  id={n.node_id}")
    print("kleinste node_id:", min(n.node_id for n in nodes.values()))

    run_spanning_tree(nodes, max_rounds=ns.max_rounds)
    print_spanning_tree(nodes)


if __name__ == "__main__":
    main()
