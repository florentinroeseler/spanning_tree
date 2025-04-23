# Spanning Tree Algorithmus - Dokumentation

## Voraussetzungen und Ausführung

### Voraussetzungen
- Python 3.7 oder höher
- Keine externen Abhängigkeiten/Bibliotheken erforderlich

### Ausführung
1. Wechseln Sie in das Projektverzeichnis
   ```
   cd spanning_tree
   ```
   <span style="color: red;">Achtung: Nicht in spanning_tree/stree</span>

2. Ausführung über die Kommandozeile
    ```
    python -m stree.cli <graph_file> [--max-rounds <value>]
    ```
    Das Argument --max-rounds gibt die maximale Anzahl der Iterationen an und ist optional (Default sind 1000).
    Die -m Flag weist Python an, das angegebene Modul (stree.cli) als Skript auszuführen. Dadurch kann ein Modul als standalone Programm ausgeführt werden.

    Der Aufruf könnte also z. B. so lauten:
    ```
    python -m stree.cli sample_graph.txt 
    ```
    oder etwa:
    ```
    python -m stree.cli sample_graph2.txt --max-rounds 2000
    ```


## Überblick

Dieses Python-Projekt implementiert eine Simulation des Spanning Tree Protokolls für ein Layer-2-Netzwerk. Es ermöglicht die Berechnung eines Spanning Trees in einem Netzwerk von Switches, um Schleifen zu vermeiden und gleichzeitig die Netzwerkkonnektivität zu gewährleisten.

## Projektstruktur

```
C:.
│   sample_graph.txt        # Beispiel-Graphdefinition
│   sample_graph2.txt
│   sample_graph3.txt
│
└───stree
        cli.py              # Kommandozeilen-Interface
        models.py           # Datenmodelle für Knoten und Kanten
        parser.py           # Parser für Graphdateien
        spanning_tree.py    # Implementierung des Spanning Tree Algorithmus
        __init__.py         # Öffentliche API des Pakets
```

## Datenmodelle

### NeighborState

Repräsentiert den Zustand, den ein Knoten pro Nachbar führt (BPDU-Puffer).

Attribute:
- `link_cost`: Kosten für die Verbindung zum Nachbarn
- `root_id`: Die zuletzt vom Nachbarn erhaltene Root-ID
- `total_cost`: Die gesamten Pfadkosten des Nachbarn bis zur Root

### Node

Repräsentiert einen Graphknoten (Switch) im Netzwerk.

Attribute:
- `name`: Name des Knotens
- `node_id`: Eindeutige ID des Knotens
- `neighbors`: Dictionary von Nachbarn mit ihren Zuständen
- `next_hop`: Ziel für die Weiterleitung von Frames zur Root

## Parser

Der Parser liest Graphbeschreibungen aus Textdateien ein und erstellt daraus ein Netzwerk von Knoten.

Beispiel einer Graphdatei:
```
// Node‑IDs
A = 5;
B = 1;
C = 3;
D = 7;
E = 6;
F = 4;

// Links und Kosten
A - B : 10;
A - C : 10;
B - D : 15;
B - E : 10;
C - D : 3;
C - E : 10;
D - E : 2;
D - F : 10;
E - F : 2;
```

Die Syntax:
- Knotendefinition: `<Name> = <ID>;`
- Kantendeklaration: `<Knoten1> - <Knoten2> : <Kosten>;`
- Kommentare beginnen mit `//`

## Spanning Tree Algorithmus

Der Kernalgorithmus ist in `spanning_tree.py` implementiert und folgt diesen Schritten:

1. Jeder Knoten betrachtet anfangs sich selbst als Root
2. In jeder Runde werden alle Knoten in zufälliger Reihenfolge bearbeitet
3. Jeder Knoten überprüft die Angebote seiner Nachbarn (Root-ID und Gesamtkosten)
4. Wenn ein Nachbar einen besseren Pfad zur Root anbietet, aktualisiert der Knoten seinen `next_hop` und seinen Zustand
5. Der Knoten sendet sein aktualisiertes Angebot an alle Nachbarn
6. Die Simulation endet, wenn sich keine Änderungen mehr ergeben

Die Hauptfunktionen sind:
- `_step()`: Bearbeitet einen einzelnen Knoten in einem Schritt
- `run_spanning_tree()`: Führt die Simulation durch
- `print_spanning_tree()`: Gibt den berechneten Spanning Tree aus

## Kommandozeilen-Interface

Enthält die Main-Routine und macht definiert das CLI.

## Beispielausführung

Für die Beispielgraphdatei `sample_graph.txt` sollte die Ausgabe etwa so aussehen:

```
Spanning-Tree {
  Root: B
  A - B
  C - D
  D - E
  E - B
  F - E
}
```

## API

Das Paket exportiert folgende Funktionen und Klassen über `__init__.py`:

- `Node`: Klasse für Netzwerkknoten
- `NeighborState`: Klasse für den Zustand eines Nachbarn
- `parse_graph_file`: Funktion zum Parsen einer Graphdatei
- `run_spanning_tree`: Funktion zum Ausführen der Spanning Tree Berechnung
- `print_spanning_tree`: Funktion zum Ausgeben des berechneten Spanning Trees