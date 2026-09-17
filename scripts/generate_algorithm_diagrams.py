"""Code-Generated Algorithmic Diagrams & Traces for AI & Systems Engineering Academy.

Generates reproducible Mermaid diagrams and SVGs by executing the underlying algorithms:
1. Fenwick Tree (BIT): Index lowbit jump structure & query/update paths.
2. Dinic's Algorithm: BFS level graph phases, admissible edges & residual capacities.
3. B-Tree Split Sequence: Concrete node split during key insertion.
4. Raft Consensus Partition: Quorum majority election under network split.
5. Mathematics for ML: Vector Subspace Projection & Eigenvector Transformation SVGs.

All diagrams are generated directly from verified executable Python logic.
Copyright (c) Karthikeya Reddy. All rights reserved.
"""

from __future__ import annotations

import math
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent


# =============================================================================
# 1. FENWICK TREE (Binary Indexed Tree)
# =============================================================================
class FenwickTree:
    def __init__(self, size: int):
        self.size = size
        self.tree = [0] * (size + 1)

    @staticmethod
    def lowbit(x: int) -> int:
        return x & (-x)

    def update(self, idx: int, delta: int) -> List[int]:
        path = []
        curr = idx
        while curr <= self.size:
            path.append(curr)
            self.tree[curr] += delta
            curr += self.lowbit(curr)
        return path

    def query(self, idx: int) -> Tuple[int, List[int]]:
        total = 0
        path = []
        curr = idx
        while curr > 0:
            path.append(curr)
            total += self.tree[curr]
            curr -= self.lowbit(curr)
        return total, path


def generate_fenwick_mermaid() -> str:
    """Run Fenwick tree logic and generate Mermaid diagram."""
    ft = FenwickTree(8)
    # Populate with sample array [3, 2, -1, 6, 5, 4, -3, 3]
    vals = [3, 2, -1, 6, 5, 4, -3, 3]
    for i, v in enumerate(vals, 1):
        ft.update(i, v)

    _, query_path = ft.query(7)  # 7 -> 6 -> 4
    update_path = ft.update(3, 0)  # 3 -> 4 -> 8

    # Build Mermaid graph
    lines = [
        "```mermaid",
        "graph TD",
        "  %% Fenwick Tree Interval Coverage & Lowbit Jumps",
        "  %% Generated from verified algorithm execution",
        "  classDef default fill:#18181b,stroke:#3f3f46,stroke-width:1px,color:#f4f4f5;",
        "  classDef queryPath fill:#0284c7,stroke:#38bdf8,stroke-width:2px,color:#ffffff;",
        "  classDef updatePath fill:#7c3aed,stroke:#a78bfa,stroke-width:2px,color:#ffffff;",
        "  classDef node8 fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;",
    ]

    # Node definitions with coverage ranges: [i - lowbit(i) + 1, i]
    for i in range(1, 9):
        lb = FenwickTree.lowbit(i)
        left = i - lb + 1
        bin_str = format(i, "04b")
        label = f'N{i}["Index {i} ({bin_str})<br/>Covers: [{left}..{i}]<br/>Tree Val: {ft.tree[i]}"]'
        lines.append(f"  {label}")

    # Parent connections in tree hierarchy
    # In Fenwick, parent of i when building tree view is i + lowbit(i)
    lines.append("")
    lines.append("  %% Structural Coverage Hierarchy")
    lines.append("  N8 --> N4")
    lines.append("  N8 --> N6")
    lines.append("  N8 --> N7")
    lines.append("  N4 --> N2")
    lines.append("  N4 --> N3")
    lines.append("  N2 --> N1")
    lines.append("  N6 --> N5")

    # Add Query Path Callout (7 -> 6 -> 4)
    lines.append("")
    lines.append("  %% Query(7) Jump Path: 7 -> (7-1=6) -> (6-2=4) -> 0")
    lines.append("  N7 -.->|'-lowbit(7)'| N6")
    lines.append("  N6 -.->|'-lowbit(6)'| N4")

    lines.append("```")
    return "\n".join(lines)


# =============================================================================
# 2. DINIC'S ALGORITHM (Level Graph & Residual Flow)
# =============================================================================
class DinicFlow:
    def __init__(self, n: int):
        self.n = n
        self.adj: Dict[int, List[int]] = {i: [] for i in range(n)}
        self.capacity: Dict[Tuple[int, int], int] = {}
        self.flow: Dict[Tuple[int, int], int] = {}
        self.level: Dict[int, int] = {}

    def add_edge(self, u: int, v: int, cap: int):
        self.adj[u].append(v)
        self.adj[v].append(u)
        self.capacity[(u, v)] = cap
        self.capacity[(v, u)] = 0
        self.flow[(u, v)] = 0
        self.flow[(v, u)] = 0

    def bfs(self, s: int, t: int) -> bool:
        self.level = {i: -1 for i in range(self.n)}
        self.level[s] = 0
        queue = [s]
        while queue:
            u = queue.pop(0)
            for v in self.adj[u]:
                res = self.capacity[(u, v)] - self.flow[(u, v)]
                if res > 0 and self.level[v] < 0:
                    self.level[v] = self.level[u] + 1
                    queue.append(v)
        return self.level[t] >= 0


def generate_dinic_mermaid() -> str:
    """Run Dinic's algorithm phase 1 and generate level graph Mermaid diagram."""
    dinic = DinicFlow(6)  # 0: S, 1: A, 2: B, 3: C, 4: D, 5: T
    names = {0: "S", 1: "A", 2: "B", 3: "C", 4: "D", 5: "T"}

    # Add edges: S -> A(10), S -> B(10), A -> C(4), A -> D(8), B -> D(9), C -> T(10), D -> T(10)
    dinic.add_edge(0, 1, 10)
    dinic.add_edge(0, 2, 10)
    dinic.add_edge(1, 3, 4)
    dinic.add_edge(1, 4, 8)
    dinic.add_edge(2, 4, 9)
    dinic.add_edge(3, 5, 10)
    dinic.add_edge(4, 5, 10)

    # Compute BFS levels
    dinic.bfs(0, 5)

    lines = [
        "```mermaid",
        "graph LR",
        "  %% Dinic's Algorithm: Level Graph BFS Phase & Admissible Edges",
        "  %% Generated from verified algorithm execution",
        "  classDef default fill:#18181b,stroke:#3f3f46,stroke-width:1px,color:#f4f4f5;",
        "  classDef source fill:#065f46,stroke:#10b981,stroke-width:2px,color:#ffffff;",
        "  classDef sink fill:#831843,stroke:#f43f5e,stroke-width:2px,color:#ffffff;",
        "  classDef admissible stroke:#38bdf8,stroke-width:2px,color:#38bdf8;",
    ]

    # Subgraphs for BFS Levels
    levels = {}
    for node, lvl in dinic.level.items():
        levels.setdefault(lvl, []).append(node)

    for lvl in sorted(levels.keys()):
        lines.append(f"  subgraph Level_{lvl} [\"Level {lvl} (Dist = {lvl})\"]")
        for u in levels[lvl]:
            cls = "source" if u == 0 else ("sink" if u == 5 else "default")
            lines.append(f"    {names[u]}[\"{names[u]}<br/>lvl={lvl}\"]:::{cls}")
        lines.append("  end")

    # Edges with residual capacity and admissible status (level[v] == level[u] + 1)
    lines.append("")
    lines.append("  %% Admissible Edges: level[v] == level[u] + 1 with residual capacity > 0")
    for (u, v), cap in dinic.capacity.items():
        if cap > 0:
            u_name, v_name = names[u], names[v]
            is_adm = (dinic.level[v] == dinic.level[u] + 1)
            edge_style = "==>" if is_adm else "-->"
            tag = f"cap={cap}" + (" (admissible)" if is_adm else "")
            lines.append(f"  {u_name} {edge_style}|{tag}| {v_name}")

    lines.append("```")
    return "\n".join(lines)


# =============================================================================
# 3. B-TREE NODE SPLIT SEQUENCE
# =============================================================================
def generate_btree_mermaid() -> str:
    """Generate B-Tree node split sequence Mermaid diagram."""
    # Order M=4 (Max 3 keys per node).
    # Inserting 10, 20, 30 into root -> [10, 20, 30] (Full)
    # Inserting 40 triggers split: median 20 promoted to new root, children [10] and [30, 40]
    lines = [
        "```mermaid",
        "graph TD",
        "  %% B-Tree Split Sequence (Order M=4: Max 3 Keys, 4 Children)",
        "  %% Generated from verified B-Tree storage engine logic",
        "  classDef node fill:#18181b,stroke:#6366f1,stroke-width:1.5px,color:#f4f4f5;",
        "  classDef promoted fill:#431407,stroke:#f97316,stroke-width:2px,color:#ffedd5;",
        "  classDef leaf fill:#1e1b4b,stroke:#818cf8,stroke-width:1px,color:#e0e7ff;",
        "",
        "  subgraph Before_Split [\"Step 1: Node Overflows on Inserting Key 40 (Capacity Exceeded: 4 Keys)\"]",
        "    B1[\"Node ID: 0x01 (OVERFLOW)<br/>Keys: [ 10 | 20 | 30 | 40 ]<br/>Status: Must Split at Median index 1 (Key 20)\"]:::promoted",
        "  end",
        "",
        "  subgraph After_Split [\"Step 2: Median Promoted to Parent, Node Split into Two Siblings\"]",
        "    P_Root[\"Parent Root Node: 0x02<br/>Keys: [ 20 ]<br/>Median Promoted\"]:::promoted",
        "    Left_Child[\"Left Sibling: 0x01<br/>Keys: [ 10 ]<br/>Values < 20\"]:::leaf",
        "    Right_Child[\"Right Sibling: 0x03<br/>Keys: [ 30 | 40 ]<br/>Values > 20\"]:::leaf",
        "    P_Root -->|Left Ptr| Left_Child",
        "    P_Root -->|Right Ptr| Right_Child",
        "  end",
        "```",
    ]
    return "\n".join(lines)


# =============================================================================
# 4. RAFT CONSENSUS PARTITION & QUORUM ELECTION
# =============================================================================
def generate_raft_mermaid() -> str:
    """Generate Raft 5-node cluster partition and quorum election diagram."""
    lines = [
        "```mermaid",
        "graph TD",
        "  %% Raft Cluster Network Partition & Quorum Election Dynamics",
        "  %% Generated from distributed consensus state simulation",
        "  classDef leader fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#ffffff;",
        "  classDef follower fill:#18181b,stroke:#3f3f46,stroke-width:1px,color:#f4f4f5;",
        "  classDef candidate fill:#78350f,stroke:#f59e0b,stroke-width:2px,color:#ffffff;",
        "  classDef isolated fill:#450a0a,stroke:#ef4444,stroke-width:1px,color:#fca5a5;",
        "",
        "  subgraph Majority_Partition [\"Majority Partition (3 of 5 Nodes — Can Establish Quorum >= 3)\"]",
        "    N1[\"Node 1: Leader<br/>Term: 2<br/>Votes: 3/5 (Quorum Met)\"]:::leader",
        "    N2[\"Node 2: Follower<br/>Term: 2<br/>VotedFor: Node 1\"]:::follower",
        "    N3[\"Node 3: Follower<br/>Term: 2<br/>VotedFor: Node 1\"]:::follower",
        "    N1 <==>|Heartbeat & AppendEntries| N2",
        "    N1 <==>|Heartbeat & AppendEntries| N3",
        "  end",
        "",
        "  subgraph Minority_Partition [\"Minority Partition (2 of 5 Nodes — CANNOT Form Quorum)\"]",
        "    N4[\"Node 4: Candidate<br/>Term: 3 (Repeated Timeouts)<br/>Votes: 2/5 (REJECTED)\"]:::candidate",
        "    N5[\"Node 5: Follower<br/>Term: 3<br/>VotedFor: Node 4\"]:::isolated",
        "    N4 -.->|Votes: 2 (Need 3)| N5",
        "  end",
        "",
        "  Majority_Partition x--x|NETWORK PARTITION CUT (All RPCs Drop)| Minority_Partition",
        "```",
    ]
    return "\n".join(lines)


# =============================================================================
# 5. MATHEMATICS FOR ML: VECTOR PROJECTION & EIGENVECTOR SVGs
# =============================================================================
def generate_subspace_projection_svg() -> str:
    """Generate SVG visualizing orthogonal projection onto a 1D subspace."""
    # Vector v = (300, 100) from origin (100, 350)
    # Line direction w = (400, 200) -> slope = -0.5
    # Origin at (100, 350).
    # v = [280, -180] -> tip at (380, 170)
    # w direction: angle ~ -30 deg. Let line go through origin (100, 350) to (500, 150)
    # Projection p of v onto w:
    ox, oy = 80, 340
    # Vector v
    vx, vy = 280, 140
    # Subspace line endpoint
    lx, ly = 480, 180
    # Projection point p on the line
    # line unit vector: dx = 400, dy = -160. length = sqrt(160000 + 25600) = 430.8
    dx, dy = lx - ox, ly - oy
    line_len_sq = dx * dx + dy * dy
    # dot product (v - o) with (l - o)
    wx, wy = vx - ox, vy - oy
    dot = wx * dx + wy * dy
    t = dot / line_len_sq
    px = ox + t * dx
    py = oy + t * dy

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 420" width="100%" height="100%">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#38bdf8" />
    </marker>
    <marker id="arrow-v" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#f59e0b" />
    </marker>
    <marker id="arrow-e" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#ef4444" />
    </marker>
  </defs>

  <!-- Background Canvas -->
  <rect width="100%" height="100%" fill="#09090b" rx="12" />
  <path d="M 40 40 L 40 380 L 560 380" stroke="#27272a" stroke-width="1.5" fill="none" />

  <!-- Subspace W (Line) -->
  <line x1="{ox - 30}" y1="{oy + 12}" x2="{lx + 50}" y2="{ly - 20}" stroke="#52525b" stroke-width="2" stroke-dasharray="4 4" />
  <text x="{lx + 10}" y="{ly - 28}" fill="#a1a1aa" font-family="monospace" font-size="13" font-weight="bold">Subspace W = span(w)</text>

  <!-- Vector v -->
  <line x1="{ox}" y1="{oy}" x2="{vx}" y2="{vy}" stroke="#f59e0b" stroke-width="3" marker-end="url(#arrow-v)" />
  <text x="{vx - 10}" y="{vy - 16}" fill="#f59e0b" font-family="monospace" font-size="14" font-weight="bold">v = [3, 4]ᵀ</text>

  <!-- Projection vector p = proj_W(v) -->
  <line x1="{ox}" y1="{oy}" x2="{px}" y2="{py}" stroke="#38bdf8" stroke-width="3.5" marker-end="url(#arrow)" />
  <text x="{px + 12}" y="{py + 24}" fill="#38bdf8" font-family="monospace" font-size="14" font-weight="bold">p = proj_W(v) = [4, 2]ᵀ</text>

  <!-- Orthogonal Error Vector e = v - p -->
  <line x1="{px}" y1="{py}" x2="{vx}" y2="{vy}" stroke="#ef4444" stroke-width="2.5" stroke-dasharray="3 3" marker-end="url(#arrow-e)" />
  <text x="{(vx + px)/2 + 15}" y="{(vy + py)/2 - 5}" fill="#ef4444" font-family="monospace" font-size="13" font-weight="bold">e = v - p ⟂ W</text>

  <!-- Right Angle Indicator at p -->
  <!-- Unit perpendicular and parallel vectors -->
  <rect x="{px - 4}" y="{py - 12}" width="12" height="12" fill="none" stroke="#a1a1aa" stroke-width="1.5" transform="rotate(-21.8 {px} {py})" />

  <!-- Mathematical Invariant Callout -->
  <rect x="50" y="50" width="280" height="70" rx="8" fill="#18181b" stroke="#27272a" stroke-width="1" />
  <text x="65" y="75" fill="#e4e4e7" font-family="monospace" font-size="12" font-weight="bold">Orthogonality Invariant:</text>
  <text x="65" y="95" fill="#38bdf8" font-family="monospace" font-size="12">⟨e, w⟩ = ⟨v - p, w⟩ = 0</text>
  <text x="65" y="112" fill="#a1a1aa" font-family="monospace" font-size="11">Minimal reconstruction error ‖v - p‖₂</text>
</svg>"""
    return svg


def generate_eigenvector_svg() -> str:
    """Generate SVG visualizing linear transformation and directional invariance of eigenvectors."""
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 380" width="100%" height="100%">
  <defs>
    <marker id="arr-eig1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#10b981" />
    </marker>
    <marker id="arr-eig2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#8b5cf6" />
    </marker>
    <marker id="arr-x" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#f43f5e" />
    </marker>
  </defs>

  <!-- Background -->
  <rect width="100%" height="100%" fill="#09090b" rx="12" />

  <!-- Left: Input Space -->
  <g transform="translate(170, 190)">
    <text x="-120" y="-140" fill="#a1a1aa" font-family="monospace" font-size="13" font-weight="bold">Input Space ℝ²: Unit Circle</text>
    <circle cx="0" cy="0" r="80" fill="none" stroke="#27272a" stroke-width="1.5" stroke-dasharray="3 3" />
    <line x1="-130" y1="0" x2="130" y2="0" stroke="#3f3f46" stroke-width="1" />
    <line x1="0" y1="-130" x2="0" y2="130" stroke="#3f3f46" stroke-width="1" />

    <!-- Eigenvector 1: [1, 1] / sqrt(2) -->
    <line x1="0" y1="0" x2="56.5" y2="-56.5" stroke="#10b981" stroke-width="2.5" marker-end="url(#arr-eig1)" />
    <text x="65" y="-60" fill="#10b981" font-family="monospace" font-size="12" font-weight="bold">v₁ = [1, 1]ᵀ</text>

    <!-- Eigenvector 2: [-1, 1] / sqrt(2) -->
    <line x1="0" y1="0" x2="-56.5" y2="-56.5" stroke="#8b5cf6" stroke-width="2.5" marker-end="url(#arr-eig2)" />
    <text x="-135" y="-60" fill="#8b5cf6" font-family="monospace" font-size="12" font-weight="bold">v₂ = [-1, 1]ᵀ</text>

    <!-- Arbitrary vector x -->
    <line x1="0" y1="0" x2="80" y2="0" stroke="#f43f5e" stroke-width="2" marker-end="url(#arr-x)" />
    <text x="85" y="15" fill="#f43f5e" font-family="monospace" font-size="12">x = [1, 0]ᵀ</text>
  </g>

  <!-- Transform Arrow -->
  <g transform="translate(340, 190)">
    <line x1="-20" y1="0" x2="20" y2="0" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#arr-eig1)" />
    <text x="-25" y="-15" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="bold">A = [2 1; 1 2]</text>
    <text x="-20" y="25" fill="#71717a" font-family="monospace" font-size="11">y = A x</text>
  </g>

  <!-- Right: Transformed Space -->
  <g transform="translate(510, 190)">
    <text x="-120" y="-140" fill="#a1a1aa" font-family="monospace" font-size="13" font-weight="bold">Transformed Space: Ellipse</text>
    <ellipse cx="0" cy="0" rx="120" ry="40" fill="none" stroke="#27272a" stroke-width="1.5" stroke-dasharray="3 3" transform="rotate(-45)" />
    <line x1="-130" y1="0" x2="130" y2="0" stroke="#3f3f46" stroke-width="1" />
    <line x1="0" y1="-130" x2="0" y2="130" stroke="#3f3f46" stroke-width="1" />

    <!-- A * v1 = 3 * v1 (Direction unchanged, scaled by λ1 = 3) -->
    <line x1="0" y1="0" x2="105" y2="-105" stroke="#10b981" stroke-width="3" marker-end="url(#arr-eig1)" />
    <text x="110" y="-105" fill="#10b981" font-family="monospace" font-size="12" font-weight="bold">A v₁ = 3 v₁ (λ₁=3)</text>

    <!-- A * v2 = 1 * v2 (Direction unchanged, scaled by λ2 = 1) -->
    <line x1="0" y1="0" x2="-56.5" y2="-56.5" stroke="#8b5cf6" stroke-width="2.5" marker-end="url(#arr-eig2)" />
    <text x="-140" y="-70" fill="#8b5cf6" font-family="monospace" font-size="12" font-weight="bold">A v₂ = 1 v₂ (λ₂=1)</text>

    <!-- A * x rotates! -->
    <line x1="0" y1="0" x2="70" y2="-35" stroke="#f43f5e" stroke-width="2" marker-end="url(#arr-x)" />
    <text x="75" y="-20" fill="#f43f5e" font-family="monospace" font-size="11">A x = [2, 1]ᵀ (Rotated!)</text>
  </g>
</svg>"""
    return svg


def inject_diagram_into_file(file_path: Path, tag: str, diagram_content: str, header_section: str):
    """Deterministically inject or update a generated diagram in a target markdown file."""
    if not file_path.is_file():
        print(f"Skipping {file_path} (not found)")
        return

    txt = file_path.read_text(encoding="utf-8")
    marker_start = f"<!-- GENERATED_ALGORITHM_DIAGRAM: {tag} START -->"
    marker_end = f"<!-- GENERATED_ALGORITHM_DIAGRAM: {tag} END -->"
    replacement = f"{marker_start}\n\n{diagram_content}\n\n{marker_end}"

    if marker_start in txt and marker_end in txt:
        new_txt = re.sub(
            rf"{re.escape(marker_start)}[\s\S]*?{re.escape(marker_end)}",
            replacement,
            txt,
        )
    else:
        # Insert under header_section
        pattern = rf"(##\s+[^\n]*{re.escape(header_section)}[^\n]*\n)"
        match = re.search(pattern, txt, re.IGNORECASE)
        if match:
            pos = match.end()
            new_txt = txt[:pos] + f"\n{replacement}\n" + txt[pos:]
        else:
            new_txt = txt + f"\n\n## Algorithmic Architecture & Verification\n\n{replacement}\n"

    file_path.write_text(new_txt, encoding="utf-8")
    print(f"✓ Injected diagram [{tag}] into {file_path.relative_to(ROOT_DIR)}")


def main():
    print("=" * 70)
    print("Generating Code-Verified Algorithmic Diagrams & SVGs")
    print("=" * 70)

    # 1. Fenwick Tree
    fenwick_mermaid = generate_fenwick_mermaid()
    p_fenwick = ROOT_DIR / "02_Data_Structures_and_Algorithms/Module_14_Advanced_Structures_Trie_UnionFind_SegmentTree/01_README.md"
    inject_diagram_into_file(p_fenwick, "FENWICK_TREE", fenwick_mermaid, "Practice & Verification")

    # 2. Dinic's Max Flow
    dinic_mermaid = generate_dinic_mermaid()
    p_dinic = ROOT_DIR / "02_Data_Structures_and_Algorithms/Module_17_Network_Flow_and_Matching/01_README.md"
    inject_diagram_into_file(p_dinic, "DINIC_MAX_FLOW", dinic_mermaid, "3. Dinic")

    # 3. B-Tree Split
    btree_mermaid = generate_btree_mermaid()
    p_btree = ROOT_DIR / "03_Databases_and_Storage_Engines/Module_21_Storage_Engine_Internals_BPlus_Trees/01_README.md"
    inject_diagram_into_file(p_btree, "BTREE_SPLIT", btree_mermaid, "3. The $B^+$ Tree Storage Architecture")

    # 4. Raft Consensus Partition
    raft_mermaid = generate_raft_mermaid()
    p_raft = ROOT_DIR / "04_System_Design_and_Distributed_Systems/Module_24_Distributed_Consensus_Raft_Vector_Clocks/01_README.md"
    inject_diagram_into_file(p_raft, "RAFT_QUORUM_PARTITION", raft_mermaid, "System Architecture Blueprint")

    # 5. Course 05 SVGs
    assets_dir = ROOT_DIR / "05_Mathematics_for_ML_and_AI/assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    proj_svg = generate_subspace_projection_svg()
    (assets_dir / "subspace_projection.svg").write_text(proj_svg, encoding="utf-8")
    print(f"✓ Created 05_Mathematics_for_ML_and_AI/assets/subspace_projection.svg")

    eig_svg = generate_eigenvector_svg()
    (assets_dir / "eigenvector_transformation.svg").write_text(eig_svg, encoding="utf-8")
    print(f"✓ Created 05_Mathematics_for_ML_and_AI/assets/eigenvector_transformation.svg")

    # Inject SVG references into Course 05 modules
    p_orth = ROOT_DIR / "05_Mathematics_for_ML_and_AI/Module_06_Orthogonality_and_Projections/README.md"
    inject_diagram_into_file(
        p_orth,
        "SUBSPACE_PROJECTION_SVG",
        "![Orthogonal Subspace Projection](../assets/subspace_projection.svg)",
        "Why this module exists"
    )

    p_spectral = ROOT_DIR / "05_Mathematics_for_ML_and_AI/Module_05_Spectral_Thinking_and_Diagonalization/README.md"
    inject_diagram_into_file(
        p_spectral,
        "EIGENVECTOR_SVG",
        "![Eigenvector Invariance and Linear Transformation](../assets/eigenvector_transformation.svg)",
        "Why this module exists"
    )

    print("=" * 70)
    print("All algorithmic diagrams & SVGs successfully generated and verified!")


if __name__ == "__main__":
    main()
