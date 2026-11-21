#!/usr/bin/env python3
"""Generates the SVG assets used by README.md (banner, project cards, timeline, tickers, stats).

Everything but the stats is static data below; stats come from the GitHub API.
Fonts are embedded as base64 so the SVGs keep their typography inside <img> tags on GitHub.
Run locally:  GH_TOKEN=$(gh auth token) python3 .github/scripts/generate.py     (SKIP_STATS=1 to skip the API)
"""
import base64, datetime, json, math, os, subprocess, textwrap
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"
FONTS = Path(__file__).resolve().parent / "fonts"
LOGIN = "Sakar1601"
EXCLUDE_LANGS_FROM = {"College-management-system"}  # legacy upload that would skew the language bar

THEMES = {
    "dark": dict(bg="#090D18", bg2="#101830", surface="#0E1424", border="#1F2842", text="#EAF0FF", muted="#8A94B0", chip="#151D33",
                 a1="#7C8CFF", a2="#3DD6F5", a3="#FFB86B", ok="#4ADE80", name1="#EAF0FF", name2="#9FB0FF", grid="#8A94B0", gridop=".06"),
    "light": dict(bg="#F7F8FC", bg2="#ECEFFB", surface="#FFFFFF", border="#DCE1F0", text="#0E1424", muted="#5B6480", chip="#F1F3FA",
                  a1="#4F5BD5", a2="#0891B2", a3="#D97706", ok="#16A34A", name1="#0E1424", name2="#4F5BD5", grid="#64748B", gridop=".09"),
}
SANS = "Inter,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
DISPLAY = "'Space Grotesk',Inter,-apple-system,'Segoe UI',sans-serif"
MONO = "'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace"
F_SG, F_I, F_JB5, F_JB4 = "space-grotesk-700.woff2", "inter-400.woff2", "jetbrains-mono-500.woff2", "jetbrains-mono-400.woff2"

def font_css(use):
    faces = [("Space Grotesk", 700, F_SG), ("Inter", 400, F_I), ("JetBrains Mono", 400, F_JB4), ("JetBrains Mono", 500, F_JB5)]
    return "".join(f"@font-face{{font-family:'{n}';font-weight:{w};src:url(data:font/woff2;base64,{base64.b64encode((FONTS / f).read_bytes()).decode()}) format('woff2');}}"
                   for n, w, f in faces if f in use)

def svg(w, h, label, use, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">'
            f'<style>{font_css(use)}</style>{body}</svg>\n')

def lines(text, width, x, y, lh, **attrs):
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return "".join(f'<text x="{x}" y="{y + i * lh}" {a}>{escape(l)}</text>' for i, l in enumerate(textwrap.wrap(text, width)))

# ------------------------------------------------------------------ banner
def banner(n):
    t = THEMES[n]; W, H, cx, cy = 1280, 400, 1010, 200
    rings = [(66, 46, [(20, "a2", 6), (200, "a3", 5)]), (116, 70, [(80, "a1", 7), (200, "a2", 5), (310, "a3", 4)]), (168, 110, [(140, "a1", 6), (290, "a2", 8)])]
    orb = ""
    for r, dur, nodes in rings:
        orb += f'<g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="{360 if r != 116 else -360} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>'
        orb += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["a1"]}" stroke-opacity=".35" stroke-dasharray="2 7" stroke-linecap="round"/>'
        for ang, col, rad in nodes:
            x, y = cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang))
            orb += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad + 7}" fill="{t[col]}" opacity=".16"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="{t[col]}"/>'
        orb += '</g>'
    body = f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
<linearGradient id="nm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t['name1']}"/><stop offset="1" stop-color="{t['name2']}"/></linearGradient>
<linearGradient id="ac" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t['a1']}"/><stop offset="1" stop-color="{t['a2']}"/></linearGradient>
<radialGradient id="core"><stop offset="0" stop-color="{t['a1']}" stop-opacity=".55"/><stop offset="1" stop-color="{t['a1']}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M48 0H0V48" fill="none" stroke="{t['grid']}" stroke-opacity="{t['gridop']}"/></pattern>
<mask id="fade"><rect width="{W}" height="{H}" fill="url(#gfade)"/></mask>
<linearGradient id="gfade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".55" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff"/></linearGradient>
<clipPath id="r"><rect width="{W}" height="{H}" rx="28"/></clipPath></defs>
<g clip-path="url(#r)"><rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#fade)"/>
<circle cx="{cx}" cy="{cy}" r="200" fill="url(#core)"/>{orb}
<circle cx="{cx}" cy="{cy}" r="15" fill="url(#ac)"/><circle cx="{cx}" cy="{cy}" r="15" fill="none" stroke="{t['a2']}" stroke-opacity=".6"><animate attributeName="r" values="15;34" dur="3.2s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".6;0" dur="3.2s" repeatCount="indefinite"/></circle>
<rect x="80" y="86" width="28" height="3" rx="1.5" fill="url(#ac)"/>
<text x="120" y="92" font-family="{MONO}" font-size="14" font-weight="500" fill="{t['muted']}" letter-spacing="3">SOFTWARE ENGINEER · PHOENIX, AZ</text>
<text x="76" y="196" font-family="{DISPLAY}" font-size="96" font-weight="700" fill="url(#nm)" letter-spacing="-3">Sakar Joshi</text>
<text x="80" y="252" font-family="{SANS}" font-size="25" fill="{t['text']}">I build AI products with a human in the loop,</text>
<text x="80" y="286" font-family="{SANS}" font-size="25" fill="{t['muted']}">and the data pipelines underneath them.</text>
<rect x="80" y="318" width="372" height="40" rx="20" fill="{t['surface']}" fill-opacity=".7" stroke="{t['border']}"/>
<circle cx="104" cy="338" r="4.5" fill="{t['ok']}"/><circle cx="104" cy="338" r="4.5" fill="none" stroke="{t['ok']}"><animate attributeName="r" values="4.5;12" dur="2s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".8;0" dur="2s" repeatCount="indefinite"/></circle>
<text x="124" y="343" font-family="{MONO}" font-size="14" font-weight="500" fill="{t['text']}">Building FinOps for AI at Prama AI</text></g>'''
    return svg(W, H, "Sakar Joshi, software engineer in Phoenix. I build AI products with a human in the loop, and the data pipelines underneath them.", {F_SG, F_I, F_JB5}, body)

# ------------------------------------------------------------------ project cards
PROJECTS = {
    "monotask": ("01 · PWA", "Monotask", "Tasks, calendar and habits. Claude captures, and you approve every AI suggestion.", ["React", "Supabase", "Claude"]),
    "cloudsentry": ("02 · AI AGENTS", "Cloudsentry", "Your AWS account as a live graph, watched by three AI agents you approve.", ["FastAPI", "boto3", "Next.js"]),
    "resume": ("03 · WEB APP", "ResumeBuilder", "ATS-friendly resumes with live preview and AI that never invents metrics.", ["Next.js", "Supabase", "Groq"]),
    "portal": ("04 · PLATFORM", "Employee Portal", "A directory app deployed like a regulated company: Vault, Terraform, Ansible.", ["Terraform", "Vault", "FastAPI"]),
}

def art(key, t):
    s = ""
    if key == "monotask":
        s += f'<rect width="250" height="160" rx="14" fill="{t["chip"]}" stroke="{t["border"]}"/>'
        for i, c in enumerate(["a3", "a2", "a1"]): s += f'<circle cx="{18 + i * 14}" cy="16" r="3.5" fill="{t[c]}" opacity=".85"/>'
        for i, (w, done) in enumerate([(130, True), (96, False), (146, False)]):
            y = 52 + i * 34
            if done: s += f'<circle cx="28" cy="{y}" r="9" fill="{t["a2"]}"/><path d="M23.5 {y} l3.2 3.2 l6 -6.4" fill="none" stroke="{t["surface"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
            else: s += f'<circle cx="28" cy="{y}" r="9" fill="none" stroke="{t["muted"]}" stroke-opacity=".6" stroke-width="1.6"/>'
            s += f'<rect x="50" y="{y - 4}" width="{w}" height="8" rx="4" fill="{t["muted"]}" opacity="{.28 if done else .5}"/>'
            if done: s += f'<rect x="50" y="{y - .75}" width="{w}" height="1.5" fill="{t["muted"]}"/>'
        s += f'<rect x="40" y="107" width="190" height="34" rx="10" fill="none" stroke="{t["a3"]}" stroke-dasharray="4 4"/><rect x="190" y="116" width="32" height="16" rx="8" fill="{t["a3"]}"/><text x="206" y="128" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="500" fill="{t["surface"]}">AI</text>'
    elif key == "cloudsentry":
        nodes = [(40, 120), (95, 60), (150, 110), (205, 50), (60, 28), (125, 20), (215, 125), (165, 150)]
        edges = [(0, 1), (1, 2), (2, 3), (1, 4), (1, 5), (2, 6), (2, 7), (5, 3), (0, 2)]
        for a, b in edges: s += f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{t["muted"]}" stroke-opacity=".4"/>'
        for i, (x, y) in enumerate(nodes):
            agent = {1: "a1", 3: "a2", 6: "a3"}.get(i)
            if agent:
                s += f'<circle cx="{x}" cy="{y}" r="9" fill="{t[agent]}"/><circle cx="{x}" cy="{y}" r="9" fill="none" stroke="{t[agent]}"><animate attributeName="r" values="9;24" dur="2.8s" begin="{i * .5}s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".8;0" dur="2.8s" begin="{i * .5}s" repeatCount="indefinite"/></circle>'
            else: s += f'<circle cx="{x}" cy="{y}" r="5" fill="{t["chip"]}" stroke="{t["muted"]}" stroke-opacity=".7"/>'
        s += f'<circle cx="150" cy="110" r="14" fill="none" stroke="{t["a3"]}" stroke-dasharray="3 3"/>'
    elif key == "resume":
        s += f'<rect x="62" y="2" width="150" height="150" rx="10" fill="{t["chip"]}" stroke="{t["border"]}"/>'
        s += f'<rect x="28" y="14" width="150" height="146" rx="10" fill="{t["surface"]}" stroke="{t["border"]}"/><rect x="44" y="30" width="64" height="10" rx="5" fill="{t["text"]}" opacity=".85"/><rect x="44" y="48" width="96" height="6" rx="3" fill="{t["a1"]}" opacity=".8"/>'
        for i, w in enumerate([112, 100, 0, 104, 76]):
            y = 70 + i * 14
            if w: s += f'<rect x="44" y="{y}" width="{w}" height="6" rx="3" fill="{t["muted"]}" opacity=".45"/>'
            else: s += f'<rect x="40" y="{y - 4}" width="124" height="14" rx="7" fill="{t["a3"]}" opacity=".28"/><rect x="44" y="{y}" width="108" height="6" rx="3" fill="{t["a3"]}"/>'
        s += f'<path d="M196 70 l3 9 l9 3 l-9 3 l-3 9 l-3 -9 l-9 -3 l9 -3z" fill="{t["a3"]}"><animateTransform attributeName="transform" type="scale" values="1;1.15;1" dur="2.4s" repeatCount="indefinite" additive="sum"/></path>'
    else:
        for i, c in enumerate(["a1", "a2", "a1"]):
            y = 14 + i * 46
            s += f'<rect x="6" y="{y}" width="150" height="36" rx="10" fill="{t["chip"]}" stroke="{t["border"]}"/><rect x="18" y="{y + 15}" width="54" height="6" rx="3" fill="{t["muted"]}" opacity=".5"/><circle cx="130" cy="{y + 18}" r="4" fill="{t[c]}"/><circle cx="116" cy="{y + 18}" r="4" fill="{t["muted"]}" opacity=".5"/>'
        s += f'<line x1="156" y1="50" x2="196" y2="80" stroke="{t["a3"]}" stroke-dasharray="4 4"/><line x1="156" y1="110" x2="196" y2="82" stroke="{t["a3"]}" stroke-dasharray="4 4"/>'
        s += f'<circle cx="206" cy="80" r="28" fill="{t["surface"]}" stroke="{t["a3"]}" stroke-width="2"/><circle cx="206" cy="75" r="7" fill="none" stroke="{t["a3"]}" stroke-width="2.2"/><rect x="202.5" y="79" width="7" height="14" rx="3.5" fill="{t["a3"]}"/>'
    return s

def card(key, n):
    t = THEMES[n]; W, H = 760, 372; label, title, desc, tags = PROJECTS[key]
    body = f'''<defs><radialGradient id="glow" cx="1" cy="0" r="1"><stop offset="0" stop-color="{t['a1']}" stop-opacity=".22"/><stop offset="1" stop-color="{t['a1']}" stop-opacity="0"/></radialGradient>
<linearGradient id="ac" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['a1']}"/><stop offset="1" stop-color="{t['a2']}"/></linearGradient></defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="26" fill="{t['surface']}" stroke="{t['border']}"/><rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="26" fill="url(#glow)"/>
<text x="40" y="62" font-family="{MONO}" font-size="16" font-weight="500" fill="{t['muted']}" letter-spacing="2.5">{escape(label)}</text>
<text x="40" y="132" font-family="{DISPLAY}" font-size="50" font-weight="700" fill="{t['text']}" letter-spacing="-1">{escape(title)}</text>
<g transform="translate(480 34) scale(1.04)">{art(key, t)}</g>
{lines(desc, 44, 40, 232, 34, font_family=SANS, font_size=23, fill=t['muted'])}'''
    x = 40
    for tag in tags:
        w = len(tag) * 9.9 + 36
        body += f'<rect x="{x}" y="292" width="{w:.0f}" height="40" rx="20" fill="{t["chip"]}" stroke="{t["border"]}"/><text x="{x + w / 2:.0f}" y="318" text-anchor="middle" font-family="{MONO}" font-size="16.5" fill="{t["text"]}">{escape(tag)}</text>'
        x += w + 10
    body += f'<circle cx="{W - 64}" cy="312" r="27" fill="url(#ac)"/><path d="M{W - 75} {323} L{W - 53} {301} M{W - 65} {301} H{W - 53} V{313}" fill="none" stroke="{t["surface"]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(W, H, f"{title}: {desc}", {F_SG, F_I, F_JB5, F_JB4}, body)

# ------------------------------------------------------------------ timeline
PATH = [("2022 – 23", "Software Developer", "Macrosoft Creations", "Angular and .NET for two enterprise systems", "a1"),
        ("2025", "Web Developer", "ASU Project Humanities", "5,000+ monthly visitors, +31% email opens", "a2"),
        ("2025", "Frontend Intern", "XDuce · QBE Insurance", "12 features shipped in 3 sprints", "a3"),
        ("2026 – NOW", "Systems & DevOps Engineer", "Prama AI", "FinOps for AI across 10+ AI vendors", "a1")]

def timeline(n):
    t = THEMES[n]; W, H = 1000, 262; y0 = 84; step = 230; x0 = 130
    body = f'<defs><linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["border"]}"/><stop offset=".55" stop-color="{t["a1"]}" stop-opacity=".7"/><stop offset="1" stop-color="{t["a2"]}"/></linearGradient></defs>'
    body += f'<line x1="20" y1="{y0}" x2="{W - 20}" y2="{y0}" stroke="url(#ln)" stroke-width="2" stroke-linecap="round"/>'
    for i, (date, role, co, line, col) in enumerate(PATH):
        x = x0 + i * step; now = i == len(PATH) - 1
        if now: body += f'<circle cx="{x}" cy="{y0}" r="9" fill="none" stroke="{t[col]}"><animate attributeName="r" values="9;24" dur="2.6s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".8;0" dur="2.6s" repeatCount="indefinite"/></circle>'
        body += f'<circle cx="{x}" cy="{y0}" r="{9 if now else 7}" fill="{t[col] if now else t["bg"]}" stroke="{t[col]}" stroke-width="2.5"/>'
        body += f'<text x="{x}" y="{y0 - 26}" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="500" fill="{t[col] if now else t["muted"]}" letter-spacing="2">{escape(date)}</text>'
        rl = textwrap.wrap(role, 19)
        for j, l in enumerate(rl): body += f'<text x="{x}" y="{y0 + 44 + j * 24}" text-anchor="middle" font-family="{DISPLAY}" font-size="20" font-weight="700" fill="{t["text"]}">{escape(l)}</text>'
        yy = y0 + 44 + len(rl) * 24 + 2
        body += f'<text x="{x}" y="{yy}" text-anchor="middle" font-family="{SANS}" font-size="15" fill="{t[col]}">{escape(co)}</text>'
        for j, l in enumerate(textwrap.wrap(line, 28)): body += f'<text x="{x}" y="{yy + 26 + j * 20}" text-anchor="middle" font-family="{SANS}" font-size="14" fill="{t["muted"]}">{escape(l)}</text>'
    return svg(W, H, "Career path: Macrosoft Creations 2022 to 2023, ASU Project Humanities 2025, XDuce 2025, Prama AI 2026 to now", {F_SG, F_I, F_JB5}, body)

# ------------------------------------------------------------------ tickers
ROWS = [["TypeScript", "React", "Next.js", "Angular", "Python", "FastAPI", "SQL", "Supabase", "PostgreSQL", "Row-Level Security", "Tailwind CSS", ".NET (C#)", "Vite"],
        ["AWS Glue", "PySpark", "Apache Iceberg", "Athena", "Terraform", "HashiCorp Vault", "Ansible", "Docker", "Anthropic API", "Groq", "Zod", "Playwright", "Vitest"]]

def ticker(n):
    t = THEMES[n]; W, H = 1000, 118; cw = 14 * 0.6
    body = f'<defs><linearGradient id="gf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".08" stop-color="#fff"/><stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient><mask id="m"><rect width="{W}" height="{H}" fill="url(#gf)"/></mask></defs><g mask="url(#m)">'
    for ri, row in enumerate(ROWS):
        y = 14 + ri * 52; x = 0; chips = ""
        for it in row:
            w = len(it) * cw + 32
            chips += f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="38" rx="19" fill="{t["chip"]}" stroke="{t["border"]}"/><text x="{x + w / 2:.0f}" y="{y + 24}" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{t["text"]}">{escape(it)}</text>'
            x += w + 12
        L = x
        frm, to = (0, -L) if ri == 0 else (-L, 0)
        body += f'<g><animateTransform attributeName="transform" type="translate" from="{frm:.0f} 0" to="{to:.0f} 0" dur="{L / 38:.0f}s" repeatCount="indefinite"/>{chips}<g transform="translate({L:.0f} 0)">{chips}</g></g>'
    body += '</g>'
    return svg(W, H, "Stack: " + ", ".join(sum(ROWS, [])), {F_JB4}, body)

# ------------------------------------------------------------------ stats (live)
QUERY = """query($login:String!){user(login:$login){
 pullRequests(states:MERGED){totalCount}
 repositories(privacy:PUBLIC,ownerAffiliations:OWNER,isFork:false,first:100){totalCount nodes{name stargazerCount languages(first:8,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}
 contributionsCollection{contributionCalendar{totalContributions}}}}"""

def fetch_stats():
    out = subprocess.run(["gh", "api", "graphql", "-f", f"query={QUERY}", "-F", f"login={LOGIN}"], capture_output=True, text=True, check=True).stdout
    u = json.loads(out)["data"]["user"]; repos = u["repositories"]["nodes"]; langs = {}
    for r in repos:
        if r["name"] in EXCLUDE_LANGS_FROM: continue
        for e in r["languages"]["edges"]:
            k = e["node"]["name"]; langs.setdefault(k, [0, e["node"]["color"] or "#8B949E"]); langs[k][0] += e["size"]
    tot = sum(v[0] for v in langs.values()) or 1
    return dict(repos=u["repositories"]["totalCount"], stars=sum(r["stargazerCount"] for r in repos), prs=u["pullRequests"]["totalCount"],
                contrib=u["contributionsCollection"]["contributionCalendar"]["totalContributions"],
                langs=[(k, c, v / tot) for k, (v, c) in sorted(langs.items(), key=lambda kv: -kv[1][0])[:5]])

def stats(n, d):
    t = THEMES[n]; W, H, pad = 1000, 150, 8
    cols = [("public repos", d["repos"], "a1"), ("stars", d["stars"], "a2"), ("merged PRs", d["prs"], "a3"), ("contributions · 12 mo", d["contrib"], "a1")]
    body = f'<defs><clipPath id="bar"><rect x="{pad}" y="100" width="{W - 2 * pad}" height="6" rx="3"/></clipPath></defs>'
    cw = (W - 2 * pad) / 4
    for i, (lab, val, c) in enumerate(cols):
        x = pad + i * cw
        body += f'<text x="{x:.0f}" y="52" font-family="{DISPLAY}" font-size="44" font-weight="700" fill="{t[c]}">{val:,}</text><text x="{x:.0f}" y="78" font-family="{MONO}" font-size="12" font-weight="500" fill="{t["muted"]}" letter-spacing="1.5">{escape(lab.upper())}</text>'
    body += f'<g clip-path="url(#bar)"><rect x="{pad}" y="100" width="{W - 2 * pad}" height="6" fill="{t["chip"]}"/>'
    x = pad
    for k, c, f in d["langs"]:
        w = f * (W - 2 * pad); body += f'<rect x="{x:.1f}" y="100" width="{w:.1f}" height="6" fill="{c}"/>'; x += w
    body += '</g>'
    lx = pad
    for k, c, f in d["langs"][:4]:
        lab = f"{k} {f * 100:.0f}%"; body += f'<circle cx="{lx + 4}" cy="130" r="4" fill="{c}"/><text x="{lx + 14}" y="134" font-family="{SANS}" font-size="13" fill="{t["muted"]}">{escape(lab)}</text>'; lx += len(lab) * 7.4 + 34
    body += f'<text x="{W - pad}" y="134" text-anchor="end" font-family="{MONO}" font-size="11" fill="{t["muted"]}" fill-opacity=".8">public data · updated {datetime.date.today().isoformat()}</text>'
    return svg(W, H, f"GitHub: {d['repos']} public repos, {d['stars']} stars, {d['prs']} merged pull requests, {d['contrib']} contributions in the last year", {F_SG, F_I, F_JB5}, body)

if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for n in THEMES:
        (ASSETS / f"banner-{n}.svg").write_text(banner(n), encoding="utf-8")
        for k in PROJECTS: (ASSETS / f"card-{k}-{n}.svg").write_text(card(k, n), encoding="utf-8")
        (ASSETS / f"timeline-{n}.svg").write_text(timeline(n), encoding="utf-8")
        (ASSETS / f"ticker-{n}.svg").write_text(ticker(n), encoding="utf-8")
    if os.environ.get("SKIP_STATS") != "1":
        d = fetch_stats()
        for n in THEMES: (ASSETS / f"stats-{n}.svg").write_text(stats(n, d), encoding="utf-8")
        print("stats:", {k: v for k, v in d.items() if k != "langs"})
    print("assets:", len(list(ASSETS.glob("*.svg"))))
