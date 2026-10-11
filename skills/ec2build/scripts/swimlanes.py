#!/usr/bin/env python3
"""EC2Build agent tool: render horizontal swimlanes (rows = users/systems, flow left -> right) for a project's APP_FLOW.md.

Usage:  python3 <SKILL_DIR>/scripts/swimlanes.py <project-dir>      (e.g. ec2build/my-app or projects/my-app)

Input (project output, written by the agent):  <project-dir>/docs/diagrams/flows.json
  {"format": "ec2build-swimlanes/1",
   "flows": [{"id": "FLOW-001", "part": null | "a", "title": "...",
              "lanes": [["key", "Lane label"], ...],                      # top-to-bottom rows: actors first, then systems
              "nodes": [["id", "laneKey", col, "start|task|decision|error|end", "Label"], ...],  # col = 0-based column, left to right
              "edges": [["srcId", "dstId", "label or empty"], ...]}]}     # edge to an earlier column = dashed retry arrow
Rules: one node per (lane, col); every edge endpoint must exist; list nodes in reading order (they get step numbers).

Output: <project-dir>/docs/diagrams/<FLOW-ID>[-part].svg, and the block between
  <!-- swimlane:FLOW-### --> and <!-- /swimlane:FLOW-### --> in docs/APP_FLOW.md is replaced with the image
  plus a generated Mermaid text version. Never hand-edit those outputs; edit flows.json and re-run.
"""
from __future__ import annotations
import html, pathlib, re, sys, textwrap

for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass

import json

LANE_LABEL_W, COL_W, LANE_H, TOP = 150, 200, 124, 70
BOX_W, BOX_H, DIA_W, DIA_H = 156, 66, 166, 88
COLORS = {
    "start": ("#DCFCE7", "#15803D"), "end": ("#DCFCE7", "#15803D"),
    "task": ("#FFFFFF", "#1D4ED8"), "decision": ("#FEF3C7", "#B45309"), "error": ("#FEE2E2", "#B91C1C"),
}

# ---------------------------------------------------------------- rendering
def esc(s): return html.escape(s, quote=True)

class Diagram:
    def __init__(self, f):
        self.f = f
        self.lane_idx = {k: i for i, (k, _) in enumerate(f["lanes"])}
        self.nodes = {n[0]: n for n in f["nodes"]}
        seen = {}
        for nid, lane, col, kind, label in f["nodes"]:
            if lane not in self.lane_idx: sys.exit(f"{f['id']}: node {nid} unknown lane {lane}")
            key = (lane, col)
            if key in seen: sys.exit(f"{f['id']}: {nid} and {seen[key]} share cell {key}")
            seen[key] = nid
        for s, d, _ in f["edges"]:
            if s not in self.nodes or d not in self.nodes: sys.exit(f"{f['id']}: bad edge {s}->{d}")
        self.ncols = max(n[2] for n in f["nodes"]) + 1
        self.width = LANE_LABEL_W + self.ncols * COL_W + 30
        self.height = TOP + len(f["lanes"]) * LANE_H + 40

    def cx(self, col): return LANE_LABEL_W + col * COL_W + COL_W / 2
    def cy(self, lane): return TOP + self.lane_idx[lane] * LANE_H + LANE_H / 2
    def size(self, kind): return (DIA_W, DIA_H) if kind == "decision" else (BOX_W, BOX_H)
    def bbox(self, nid):
        _, lane, col, kind, _ = self.nodes[nid]; w, h = self.size(kind)
        x, y = self.cx(col), self.cy(lane); return (x - w/2, y - h/2, x + w/2, y + h/2)

    def hits(self, pts, ignore):
        for nid in self.nodes:
            if nid in ignore: continue
            x0, y0, x1, y1 = self.bbox(nid)
            for (ax, ay), (bx, by) in zip(pts, pts[1:]):
                if ay == by and y0 - 2 <= ay <= y1 + 2 and max(min(ax, bx), x0) < min(max(ax, bx), x1): return True
                if ax == bx and x0 - 2 <= ax <= x1 + 2 and max(min(ay, by), y0) < min(max(ay, by), y1): return True
        return False

    def route(self, s, d):
        sl, sc, dl, dc = self.nodes[s][1], self.nodes[s][2], self.nodes[d][1], self.nodes[d][2]
        sx0, sy0, sx1, sy1 = self.bbox(s); dx0, dy0, dx1, dy1 = self.bbox(d)
        y1, y2 = self.cy(sl), self.cy(dl); ign = {s, d}
        g_after = self.cx(sc) + COL_W / 2           # gutter right of source column
        g_before = self.cx(dc) - COL_W / 2          # gutter left of destination column
        if dc > sc:
            if sl == dl:
                p = [(sx1, y1), (dx0, y2)]
                if not self.hits(p, ign): return p, False
                ch = TOP + self.lane_idx[sl] * LANE_H + 9
                return [(sx1, y1), (g_after, y1), (g_after, ch), (g_before, ch), (g_before, y2), (dx0, y2)], False
            for p in ([(sx1, y1), (g_before, y1), (g_before, y2), (dx0, y2)],
                      [(sx1, y1), (g_after, y1), (g_after, y2), (dx0, y2)]):
                if not self.hits(p, ign): return p, False
            lo = max(self.lane_idx[sl], self.lane_idx[dl])
            ch = TOP + lo * LANE_H + 9
            return [(sx1, y1), (g_after, y1), (g_after, ch), (g_before, ch), (g_before, y2), (dx0, y2)], False
        if dc == sc:
            if y2 > y1: return [(self.cx(sc), sy1), (self.cx(dc), dy0)], False
            return [(self.cx(sc), sy0), (self.cx(dc), dy1)], False
        # backward (retry / loop): run along the bottom channel of the lower lane
        lo = max(self.lane_idx[sl], self.lane_idx[dl])
        ch = TOP + (lo + 1) * LANE_H - 9
        return [(self.cx(sc), sy1), (self.cx(sc), ch), (self.cx(dc), ch), (self.cx(dc), dy1)], True

    def wrap(self, label, kind):
        width = 19 if kind == "decision" else 23
        return textwrap.wrap(label, width)[:4]

    def svg(self):
        f = self.f; o = []
        title = f"{f['id']} — {f['title']}"
        o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
                 f'viewBox="0 0 {self.width} {self.height}" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" '
                 f'role="img" aria-label="{esc(title)} swimlane">')
        o.append('<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
                 '<path d="M0,0 L10,5 L0,10 z" fill="#334155"/></marker></defs>')
        o.append(f'<rect width="{self.width}" height="{self.height}" fill="#FFFFFF"/>')
        o.append(f'<text x="16" y="34" font-size="20" font-weight="700" fill="#0F172A">{esc(title)}</text>')
        o.append(f'<text x="16" y="56" font-size="12" fill="#475569">Rows = who acts. Read left to right. '
                 f'Solid arrow = next step · dashed arrow = go back / retry · green = start/end · amber = decision · red = error.</text>')
        for i, (k, name) in enumerate(f["lanes"]):
            y = TOP + i * LANE_H
            o.append(f'<rect x="0" y="{y}" width="{self.width}" height="{LANE_H}" fill="{"#F8FAFC" if i % 2 == 0 else "#EEF2F7"}" stroke="#CBD5E1"/>')
            o.append(f'<rect x="0" y="{y}" width="{LANE_LABEL_W}" height="{LANE_H}" fill="#E2E8F0" stroke="#CBD5E1"/>')
            for j, line in enumerate(textwrap.wrap(name, 16)):
                o.append(f'<text x="14" y="{y + LANE_H/2 - 4 + j*16}" font-size="14" font-weight="700" fill="#0F172A">{esc(line)}</text>')
        labels = []
        used: dict[float, list[tuple[float, float]]] = {}   # gutter x -> vertical spans already drawn
        node_xs = {self.cx(c) for c in range(self.ncols)}
        def separate(pts):
            pts = [list(p) for p in pts]
            for i in range(len(pts) - 1):
                (ax, ay), (bx, by) = pts[i], pts[i + 1]
                if ax != bx or ax in node_xs: continue
                lo, hi = sorted((ay, by)); x = ax; k = 0
                while any(lo < h2 and l2 < hi for l2, h2 in used.get(x, [])):
                    k += 1; x = ax + (8 * ((k + 1) // 2)) * (1 if k % 2 else -1)
                used.setdefault(x, []).append((lo, hi))
                if x != ax:
                    pts[i][0] = pts[i + 1][0] = x
            return [tuple(p) for p in pts]
        for s, d, lab in f["edges"]:
            pts, back = self.route(s, d)
            pts = separate(pts)
            path = " ".join(f"{'M' if i == 0 else 'L'}{x:.0f},{y:.0f}" for i, (x, y) in enumerate(pts))
            dash = ' stroke-dasharray="6 4"' if back else ""
            o.append(f'<path d="{path}" fill="none" stroke="#334155" stroke-width="1.6"{dash} marker-end="url(#arr)"/>')
            if lab:
                segs = list(zip(pts, pts[1:]))
                (ax, ay), (bx, by) = max(segs, key=lambda sg: abs(sg[0][0]-sg[1][0]) + abs(sg[0][1]-sg[1][1]))
                labels.append(((ax + bx) / 2, (ay + by) / 2, lab))
        for idx, (nid, lane, col, kind, label) in enumerate(f["nodes"], 1):
            x, y = self.cx(col), self.cy(lane); w, h = self.size(kind); fill, stroke = COLORS[kind]
            if kind == "decision":
                o.append(f'<polygon points="{x},{y-h/2} {x+w/2},{y} {x},{y+h/2} {x-w/2},{y}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
            else:
                rx = h / 2 if kind in ("start", "end") else 8
                o.append(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
            lines = self.wrap(label, kind); fs = 12; lh = 14
            for j, line in enumerate(lines):
                ty = y - (len(lines) - 1) * lh / 2 + j * lh + 4
                o.append(f'<text x="{x}" y="{ty:.0f}" font-size="{fs}" text-anchor="middle" fill="#0F172A">{esc(line)}</text>')
            bx, by = x - w/2 + 2, y - h/2 - 2
            o.append(f'<circle cx="{bx}" cy="{by}" r="10" fill="{stroke}"/>'
                     f'<text x="{bx}" y="{by+4}" font-size="11" font-weight="700" text-anchor="middle" fill="#FFFFFF">{idx}</text>')
        for x, y, lab in labels:
            w = 7 * len(lab) + 10
            o.append(f'<rect x="{x-w/2:.0f}" y="{y-9:.0f}" width="{w}" height="17" rx="4" fill="#FFFFFF" stroke="#94A3B8"/>'
                     f'<text x="{x:.0f}" y="{y+4:.0f}" font-size="11" font-weight="600" text-anchor="middle" fill="#334155">{esc(lab)}</text>')
        o.append("</svg>")
        return "\n".join(o)

    def mermaid(self):
        f = self.f; o = ["flowchart LR"]
        for k, name in f["lanes"]:
            o.append(f'  subgraph L_{k}["{name}"]'); o.append("    direction LR")
            for nid, lane, col, kind, label in sorted(f["nodes"], key=lambda n: n[2]):
                if lane != k: continue
                t = label.replace('"', "'")
                shape = {"decision": f'{{"{t}"}}', "start": f'(["{t}"])', "end": f'(["{t}"])'}.get(kind, f'["{t}"]')
                o.append(f"    {nid}{shape}")
            o.append("  end")
        for s, d, lab in f["edges"]:
            o.append(f'  {s} -- "{lab}" --> {d}' if lab else f"  {s} --> {d}")
        return "\n".join(o)

def main():
    if len(sys.argv) != 2: sys.exit("usage: python3 swimlanes.py <project-dir>")
    project = pathlib.Path(sys.argv[1])
    OUT = project / "docs" / "diagrams"; APP_FLOW = project / "docs" / "APP_FLOW.md"
    spec = json.loads((OUT / "flows.json").read_text(encoding='utf-8'))
    if spec.get("format") != "ec2build-swimlanes/1": sys.exit("flows.json: unsupported format")
    FLOWS = [dict(id=f["id"], title=f["title"], part=f.get("part"), lanes=[tuple(l) for l in f["lanes"]],
                  nodes=[tuple(n) for n in f["nodes"]], edges=[tuple(e) for e in f["edges"]]) for f in spec["flows"]]
    blocks: dict[str, list[str]] = {}
    for f in FLOWS:
        dg = Diagram(f)
        name = f["id"] + (f"-{f['part']}" if f["part"] else "")
        (OUT / f"{name}.svg").write_text(dg.svg(), encoding='utf-8')
        blocks.setdefault(f["id"], []).append(
            f"**{f['title']}**\n\n![{f['id']} {f['title']} — horizontal swimlane](diagrams/{name}.svg)\n\n"
            f"<details><summary>Text version (Mermaid, generated)</summary>\n\n```mermaid\n{dg.mermaid()}\n```\n</details>\n")
    text = APP_FLOW.read_text(encoding='utf-8')
    for fid, parts in blocks.items():
        body = "\n".join(parts)
        pat = re.compile(rf"<!-- swimlane:{fid} -->.*?<!-- /swimlane:{fid} -->", re.S)
        new = f"<!-- swimlane:{fid} -->\n{body}<!-- /swimlane:{fid} -->"
        if not pat.search(text): sys.exit(f"marker <!-- swimlane:{fid} --> missing in APP_FLOW.md")
        text = pat.sub(lambda _: new, text)
    APP_FLOW.write_text(text, encoding='utf-8')
    print(f"wrote {sum(len(v) for v in blocks.values())} diagrams for {len(blocks)} flows")

if __name__ == "__main__":
    main()
