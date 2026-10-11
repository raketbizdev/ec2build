#!/usr/bin/env python3
"""EC2Build: render the six documents into ONE self-contained HTML page.

Usage:  python3 <SKILL_DIR>/scripts/onepage.py <project-dir>
Writes <project-dir>/docs/<slug>.html: sidebar navigation, all six documents, swimlane SVGs inlined,
Mermaid diagrams rendered in the browser (code shown if offline), light/dark theme, print-friendly.
No third-party Python packages needed. Never hand-edit the HTML; re-run after any document change.
"""
import datetime, html, pathlib, re, sys
for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass

DOCS = [("PRD.md", "PRD", "Product Requirements"), ("TRD.md", "TRD", "Technical Requirements"),
        ("APP_FLOW.md", "APP_FLOW", "App Flow"), ("DESIGN_BRIEF.md", "DESIGN", "Design Brief"),
        ("DATABASE_SCHEMA.md", "SCHEMA", "Database Schema"), ("IMPLEMENTATION_PLAN.md", "PLAN", "Implementation Plan")]
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"

# ------------------------------------------------------------------ markdown (subset used by EC2Build docs)
def slugify(text):
    s = re.sub(r"<[^>]+>", "", text).lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    return re.sub(r"[\s-]+", "-", s).strip("-") or "section"

def inline(text, ctx):
    codes = []
    def keep(m):
        codes.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00{len(codes)-1}\x00"
    t = re.sub(r"`([^`]+)`", keep, text)
    t = html.escape(t, quote=False)
    def img(m):
        alt, src = m.group(1), m.group(2)
        return ctx["image"](alt, src)
    t = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", img, t)
    def link(m):
        label, href = m.group(1), m.group(2)
        if re.match(r"^[A-Za-z_]+\.md$", href.split("#")[0]):     # link to a sibling document
            target = next((k for f, k, _ in DOCS if f == href.split("#")[0]), None)
            href = f"#{target.lower()}" if target else href
        return f'<a href="{html.escape(href)}">{label}</a>'
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"(?<![\w])_(?!\s)([^_]+?)(?<!\s)_(?![\w])", r"<em>\1</em>", t)
    t = re.sub(r"(?<![\w\"'=/])(https?://[^\s<)]+)", r'<a href="\1">\1</a>', t)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], t)

def split_row(line):
    cells, cur, in_code, i = [], "", False, 0
    line = line.strip()
    if line.startswith("|"): line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"): line = line[:-1]
    while i < len(line):
        ch = line[i]
        if ch == "\\" and i + 1 < len(line) and line[i+1] == "|": cur += "|"; i += 2; continue
        if ch == "`": in_code = not in_code
        if ch == "|" and not in_code: cells.append(cur.strip()); cur = ""
        else: cur += ch
        i += 1
    cells.append(cur.strip())
    return cells

def render_md(md, ctx):
    lines = md.splitlines()
    out, i, para = [], 0, []
    def flush():
        if para:
            out.append("<p>" + inline(" ".join(para), ctx) + "</p>"); para.clear()
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if s.startswith("```"):
            flush(); lang = s[3:].strip().split()[0] if s[3:].strip() else ""
            j = i + 1; buf = []
            while j < len(lines) and not lines[j].strip().startswith("```"):
                buf.append(lines[j]); j += 1
            code = "\n".join(buf)
            if lang == "mermaid":
                out.append(f'<div class="mermaid-wrap"><pre class="mermaid">{html.escape(code)}</pre></div>')
            else:
                out.append(f'<pre class="code"><span class="lang">{html.escape(lang)}</span><code>{html.escape(code)}</code></pre>')
            i = j + 1; continue
        if s.startswith("<!--"):
            flush()
            while i < len(lines) and "-->" not in lines[i]: i += 1
            i += 1; continue
        if re.match(r"^</?(details|summary)", s):
            flush(); out.append(re.sub(r"<summary>(.*?)</summary>", lambda m: f"<summary>{inline(m.group(1), ctx)}</summary>", s)); i += 1; continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            flush(); level = len(m.group(1)); text = m.group(2)
            hid = ctx["id"](text)
            if level == 2: ctx["toc"].append((hid, re.sub(r"[`*_]", "", text)))
            out.append(f'<h{level} id="{hid}">{inline(text, ctx)}</h{level}>'); i += 1; continue
        if re.match(r"^(-{3,}|\*{3,})$", s):
            flush(); out.append("<hr>"); i += 1; continue
        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-{2,}", lines[i+1].strip()):
            flush(); head = split_row(s); rows = []; j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append(split_row(lines[j])); j += 1
            t = ['<div class="table-wrap"><table><thead><tr>' + "".join(f"<th>{inline(c, ctx)}</th>" for c in head) + "</tr></thead><tbody>"]
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c, ctx)}</td>" for c in r) + "</tr>")
            out.append("".join(t) + "</tbody></table></div>"); i = j; continue
        if s.startswith(">"):
            flush(); buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip()); i += 1
            out.append("<blockquote>" + inline(" ".join(buf), ctx) + "</blockquote>"); continue
        if re.match(r"^\s*([-*]|\d+\.)\s+", line):
            flush(); i = render_list(lines, i, out, ctx); continue
        if not s:
            flush(); i += 1; continue
        para.append(s); i += 1
    flush()
    return "\n".join(out)

def render_list(lines, i, out, ctx):
    stack = []  # (indent, tag)
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
        if not m:
            if line.strip() and stack and len(line) - len(line.lstrip()) > stack[-1][0]:   # continuation
                out[-1] = out[-1][:-5] + " " + inline(line.strip(), ctx) + "</li>"; i += 1; continue
            break
        indent, marker, text = len(m.group(1)), m.group(2), m.group(3)
        tag = "ol" if marker[0].isdigit() else "ul"
        while stack and indent < stack[-1][0]:
            out.append(f"</{stack.pop()[1]}>")
        if not stack or indent > stack[-1][0]:
            start = f' start="{marker[:-1]}"' if tag == "ol" and marker[:-1] != "1" else ""
            out.append(f"<{tag}{start}>"); stack.append((indent, tag))
        box = re.match(r"^\[( |x|X)\]\s+(.*)$", text)
        if box:
            checked = " checked" if box.group(1).lower() == "x" else ""
            out.append(f'<li class="task"><input type="checkbox" disabled{checked}> {inline(box.group(2), ctx)}</li>')
        else:
            out.append(f"<li>{inline(text, ctx)}</li>")
        i += 1
    while stack:
        out.append(f"</{stack.pop()[1]}>")
    return i

# ------------------------------------------------------------------ page
def doc_meta(md):
    def cell(name):
        m = re.search(rf"^\|\s*{name}\s*\|\s*(.+?)\s*\|\s*$", md, re.M)
        return re.sub(r"[`*]", "", m.group(1)) if m else ""
    version = cell("Version")
    parts = re.split(r"\s*·\s*", version)
    status = parts[1] if len(parts) > 1 else cell("Status")
    status = re.split(r"[\s—–(-]", status.strip(), maxsplit=1)[0] if status else "draft"
    return parts[0], status or "draft"

def main():
    if len(sys.argv) != 2: sys.exit("usage: python3 onepage.py <project-dir>")
    project = pathlib.Path(sys.argv[1]).resolve(); docs = project / "docs"
    missing = [f for f, _, _ in DOCS if not (docs / f).exists()]
    if missing: sys.exit(f"missing documents: {', '.join(missing)}")
    prd = (docs / "PRD.md").read_text(encoding="utf-8")
    title_m = re.search(r"^#\s+(?:PRD\s+—\s+)?(.+?)(?:\s+Product Requirements Document)?\s*$", prd, re.M)
    name = title_m.group(1).strip() if title_m else project.name
    hist = re.findall(r"^\|\s*(\d+\.\d+\.\d+)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|", prd.split("Change history")[-1], re.M) if "Change history" in prd else []
    package = hist[-1][0] if hist else ""
    svg_n = [0]
    def image(alt, src):
        p = (docs / src).resolve()
        if p.suffix == ".svg" and p.exists() and docs in p.parents:
            svg_n[0] += 1; k = f"s{svg_n[0]}"
            svg = re.sub(r"<\?xml[^>]*>", "", p.read_text(encoding="utf-8"))
            svg = svg.replace('id="arr"', f'id="arr-{k}"').replace("url(#arr)", f"url(#arr-{k})")
            return f'<figure class="swimlane"><div class="svg-scroll">{svg}</div><figcaption>{html.escape(alt)} · scroll sideways ↔</figcaption></figure>'
        return f'<img alt="{html.escape(alt)}" src="{html.escape(src)}">'
    sections, nav, cards = [], [], []
    for fname, key, label in DOCS:
        md = (docs / fname).read_text(encoding="utf-8")
        used = set()
        def make_id(text, key=key, used=used):
            base = f"{key.lower()}-{slugify(text)}"; hid = base; n = 2
            while hid in used: hid = f"{base}-{n}"; n += 1
            used.add(hid); return hid
        ctx = {"toc": [], "id": make_id, "image": image}
        body = render_md(md, ctx)
        version, status = doc_meta(md)
        sections.append(f'<section class="doc" id="{key.lower()}"><div class="doc-tag">{label} · v{html.escape(version)} · {html.escape(status)}</div>{body}</section>')
        sub = "".join(f'<li><a href="#{hid}">{html.escape(t)}</a></li>' for hid, t in ctx["toc"])
        nav.append(f'<details class="nav-doc"><summary><a href="#{key.lower()}">{label}</a></summary><ul>{sub}</ul></details>')
        cards.append(f'<a class="card" href="#{key.lower()}"><span class="card-k">{key.replace("_", " ")}</span><span class="card-l">{label}</span><span class="card-v">v{html.escape(version)} · {html.escape(status)}</span></a>')
    generated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    page = TEMPLATE.format(
        title=html.escape(name), package=html.escape(package or "—"), generated=generated,
        nav="".join(nav), cards="".join(cards), sections="".join(sections), mermaid=MERMAID)
    out = docs / f"{project.name}.html"
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out} ({len(page)//1024} KB)")

TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — EC2Build specs</title>
<style>
:root{{--bg:#fff;--surface:#f6f8fb;--border:#d9dfe8;--text:#0f172a;--muted:#475569;--primary:#1d4ed8;--code:#f1f5f9;--accent:#b45309}}
@media (prefers-color-scheme:dark){{:root{{--bg:#0b1220;--surface:#111a2e;--border:#26324a;--text:#e6eaf2;--muted:#a3aec2;--primary:#6e9bff;--code:#0f1a30;--accent:#f2b13c}}}}
*{{box-sizing:border-box}} html{{scroll-behavior:smooth;scroll-padding-top:64px}}
body{{margin:0;overflow-x:hidden;background:var(--bg);color:var(--text);font:15px/1.6 Inter,"Segoe UI",system-ui,-apple-system,sans-serif}}
header{{position:sticky;top:0;z-index:5;display:flex;flex-wrap:wrap;gap:4px 16px;align-items:center;padding:10px 20px;background:var(--bg);border-bottom:1px solid var(--border)}}
header h1{{font-size:18px;margin:0}} header .meta{{color:var(--muted);font-size:13px}}
header button{{margin-left:auto;border:1px solid var(--border);background:var(--surface);color:var(--text);border-radius:8px;padding:6px 10px;cursor:pointer}}
.layout{{display:grid;grid-template-columns:280px minmax(0,1fr)}}
nav{{position:sticky;top:53px;height:calc(100vh - 53px);overflow:auto;padding:12px 10px 40px;border-right:1px solid var(--border);background:var(--surface);font-size:13.5px}}
nav input{{width:100%;padding:7px 9px;border:1px solid var(--border);border-radius:8px;background:var(--bg);color:var(--text);margin-bottom:10px}}
.nav-doc summary{{cursor:pointer;padding:5px 4px;font-weight:600}} .nav-doc ul{{list-style:none;margin:0 0 6px;padding-left:12px}}
.nav-doc li a{{display:block;padding:2px 4px;color:var(--muted);text-decoration:none;border-radius:4px}} .nav-doc li a:hover{{background:var(--bg);color:var(--text)}}
.nav-doc summary a{{color:var(--text);text-decoration:none}}
main{{padding:24px clamp(16px,4vw,48px) 80px;max-width:1200px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px;margin:8px 0 28px}}
.card{{display:flex;flex-direction:column;gap:2px;padding:12px;border:1px solid var(--border);border-radius:10px;text-decoration:none;color:var(--text);background:var(--surface)}}
.card:hover{{border-color:var(--primary)}} .card-k{{font-weight:700;color:var(--primary)}} .card-v{{font-size:12px;color:var(--muted)}}
.doc{{border-top:3px solid var(--primary);padding-top:8px;margin-top:40px;min-width:0}} main p,main li{{overflow-wrap:anywhere}} td{{overflow-wrap:break-word}}
.doc-tag{{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}}
h1,h2,h3,h4{{line-height:1.25}} .doc h1{{font-size:28px;margin:.3em 0 .6em}} h2{{font-size:22px;margin-top:2em;padding-bottom:4px;border-bottom:1px solid var(--border)}} h3{{font-size:17px;margin-top:1.6em}} h4{{font-size:15px}}
a{{color:var(--primary)}} code{{font:13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--code);padding:1px 4px;border-radius:4px}}
pre.code{{position:relative;background:var(--code);border:1px solid var(--border);border-radius:8px;padding:14px;overflow:auto;max-height:520px}}
pre.code code{{background:none;padding:0;white-space:pre}} pre .lang{{position:absolute;top:4px;right:8px;font-size:11px;color:var(--muted)}}
.table-wrap{{overflow-x:auto;margin:12px 0}} table{{border-collapse:collapse;font-size:13.5px;min-width:60%}}
th,td{{border:1px solid var(--border);padding:6px 9px;text-align:left;vertical-align:top}} th{{background:var(--surface)}}
blockquote{{margin:12px 0;padding:8px 14px;border-left:4px solid var(--accent);background:var(--surface)}}
.swimlane{{margin:14px 0}} .svg-scroll{{overflow-x:auto;border:1px solid var(--border);border-radius:8px;background:#fff}} .svg-scroll svg{{display:block;height:auto;max-width:none}}
figcaption{{font-size:12px;color:var(--muted);margin-top:4px}}
.mermaid-wrap{{overflow-x:auto;background:#fff;border:1px solid var(--border);border-radius:8px;padding:10px;margin:12px 0;color:#0f172a}}
details{{margin:8px 0}} li.task{{list-style:none;margin-left:-1.2em}}
.hidden{{display:none}}
@media (max-width:860px){{.layout{{grid-template-columns:minmax(0,1fr)}} header{{position:static}} nav{{position:static;height:auto;max-height:45vh;border-right:0;border-bottom:1px solid var(--border)}} header button{{margin-left:0}} .cards{{grid-template-columns:repeat(auto-fill,minmax(140px,1fr))}}}}
@media print{{header button,nav{{display:none}} .layout{{display:block}} .doc{{page-break-before:always}} pre.code{{max-height:none}}}}
</style></head>
<body>
<header><h1>{title}</h1><span class="meta">EC2Build specs · package {package} · generated {generated}</span><button onclick="document.querySelectorAll('details').forEach(d=>d.open=!d.open)">Expand / collapse</button></header>
<div class="layout">
<nav aria-label="Documents"><input type="search" placeholder="Filter sections…" oninput="filterNav(this.value)">{nav}</nav>
<main>
<p style="color:var(--muted);margin-top:0">All six documents on one page. Source of truth is the Markdown in <code>docs/</code>; this page is generated. Do not edit it.</p>
<div class="cards">{cards}</div>
{sections}
</main></div>
<script>
function filterNav(q){{q=q.toLowerCase();document.querySelectorAll('nav .nav-doc').forEach(function(d){{var any=false;d.querySelectorAll('li').forEach(function(li){{var hit=!q||li.textContent.toLowerCase().indexOf(q)>-1;li.classList.toggle('hidden',!hit);any=any||hit}});d.open=!!q&&any;d.classList.toggle('hidden',!!q&&!any)}})}}
</script>
<script src="{mermaid}"></script>
<script>if(window.mermaid){{mermaid.initialize({{startOnLoad:true,theme:'default',securityLevel:'strict'}})}}</script>
</body></html>
"""

if __name__ == "__main__":
    main()
