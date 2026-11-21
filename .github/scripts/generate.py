#!/usr/bin/env python3
"""Generates the SVG assets used by README.md (hero, impact, project cards, experience, capabilities, GitHub numbers, buttons).

Content is static data below, except the GitHub numbers, which come from the GitHub API.
Fonts (Sora, Inter, JetBrains Mono) are embedded as base64 so the SVGs keep their typography inside <img> tags.
Run locally:  GH_TOKEN=$(gh auth token) python3 .github/scripts/generate.py     (SKIP_STATS=1 to skip the API)
"""
import base64, datetime, json, os, subprocess, textwrap
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"
FONTS = Path(__file__).resolve().parent / "fonts"
LOGIN = "Sakar1601"
EXCLUDE_LANGS_FROM = {"College-management-system"}  # legacy upload that would skew the language bar

THEMES = {
    "dark": dict(bg="#0A0A10", surface="#12121C", surface2="#191926", border="#2A2A3C", text="#F5F5FA", muted="#9D9DB5", g1="#FF7A45", g2="#FF4D8D", g3="#8B5CF6",
                 ok="#3DDC97", glow1=".16", glow3=".34", dot="#FFFFFF", dotop=".10", onacc="#FFFFFF"),
    "light": dict(bg="#FBFBFD", surface="#FFFFFF", surface2="#F3F3F8", border="#E1E1EC", text="#0B0B12", muted="#5B5B73", g1="#F0591E", g2="#E11D74", g3="#7C3AED",
                  ok="#12A150", glow1=".10", glow3=".16", dot="#0B0B12", dotop=".10", onacc="#FFFFFF"),
}
SANS = "Inter,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
DISPLAY = "Sora,Inter,-apple-system,'Segoe UI',sans-serif"
MONO = "'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace"
F_S8, F_S7, F_I4, F_I6, F_J5 = "sora-800.woff2", "sora-700.woff2", "inter-400.woff2", "inter-600.woff2", "jetbrains-mono-500.woff2"

def font_css(use):
    faces = [("Sora", 800, F_S8), ("Sora", 700, F_S7), ("Inter", 400, F_I4), ("Inter", 600, F_I6), ("JetBrains Mono", 500, F_J5)]
    return "".join(f"@font-face{{font-family:'{n}';font-weight:{w};src:url(data:font/woff2;base64,{base64.b64encode((FONTS / f).read_bytes()).decode()}) format('woff2');}}" for n, w, f in faces if f in use)

def defs(t, horizontal=True):
    x2, y2 = ("1", "0") if horizontal else ("0", "1")
    return (f'<linearGradient id="g" x1="0" y1="0" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="{t["g1"]}"/><stop offset=".5" stop-color="{t["g2"]}"/><stop offset="1" stop-color="{t["g3"]}"/></linearGradient>'
            f'<linearGradient id="gd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["g1"]}"/><stop offset=".5" stop-color="{t["g2"]}"/><stop offset="1" stop-color="{t["g3"]}"/></linearGradient>')

def svg(w, h, label, use, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}"><style>{font_css(use)}</style>{body}</svg>\n')

def panel(t, x, y, w, h, r=28, fill=None):
    return f'<rect x="{x + .75}" y="{y + .75}" width="{w - 1.5}" height="{h - 1.5}" rx="{r}" fill="{fill or t["surface"]}" stroke="{t["border"]}" stroke-width="1.5"/>'

def lines(text, width, x, y, lh, **attrs):
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return "".join(f'<text x="{x}" y="{y + i * lh}" {a}>{escape(l)}</text>' for i, l in enumerate(textwrap.wrap(text, width)))

# ------------------------------------------------------------------ hero
SOURCES = ["AWS", "Azure", "OCI", "Alibaba", "AI vendors"]

def hero(n):
    t = THEMES[n]; W, H = 1200, 600
    ox, oy = 650, 62          # pipeline panel origin
    yc = [100, 170, 240, 310, 380]
    paths = [f"M146 {y} C192 {y} 184 240 206 240" for y in yc]
    outs = [(170, "Savings"), (310, "Dashboards")]
    opaths = [f"M302 240 C330 240 326 {y} 350 {y}" for y, _ in outs]
    pipe = f'<g transform="translate({ox} {oy})">{panel(t, 0, 0, 500, 476, 30)}'
    pipe += f'<text x="30" y="46" font-family="{MONO}" font-size="14" font-weight="500" fill="{t["muted"]}" letter-spacing="2.5">INGEST  →  ICEBERG  →  RECOMMEND</text>'
    for p in paths + opaths:
        pipe += f'<path d="{p}" fill="none" stroke="url(#g)" stroke-width="2.2" stroke-opacity=".7" stroke-dasharray="2 7" stroke-linecap="round"><animate attributeName="stroke-dashoffset" from="0" to="-18" dur="1.4s" repeatCount="indefinite"/></path>'
    for i, p in enumerate(paths + opaths):
        pipe += f'<circle r="5" fill="url(#gd)"><animateMotion dur="3.4s" begin="{i * .42:.2f}s" repeatCount="indefinite" path="{p}"/></circle>'
    for lab, y in zip(SOURCES, yc):
        pipe += f'<rect x="28" y="{y - 21}" width="118" height="42" rx="21" fill="{t["surface2"]}" stroke="{t["border"]}" stroke-width="1.5"/><circle cx="50" cy="{y}" r="5" fill="url(#gd)"/><text x="66" y="{y + 5}" font-family="{MONO}" font-size="16.5" font-weight="500" fill="{t["text"]}">{escape(lab)}</text>'
    pipe += f'<rect x="206" y="188" width="96" height="104" rx="24" fill="{t["surface2"]}" stroke="url(#g)" stroke-width="2.6"/>'
    for k in range(3): pipe += f'<rect x="{226 + k * 4}" y="{208 + k * 11}" width="{56 - k * 8}" height="7" rx="3.5" fill="url(#g)" opacity="{1 - k * .22}"/>'
    pipe += f'<text x="254" y="262" text-anchor="middle" font-family="{MONO}" font-size="15.5" font-weight="500" fill="{t["text"]}">Iceberg</text><text x="254" y="281" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{t["muted"]}">idempotent</text>'
    for y, lab in outs:
        pipe += f'<rect x="350" y="{y - 21}" width="132" height="42" rx="21" fill="{t["surface2"]}" stroke="{t["border"]}" stroke-width="1.5"/><circle cx="371" cy="{y}" r="5" fill="{t["ok"]}"/><text x="386" y="{y + 5}" font-family="{MONO}" font-size="16" font-weight="500" fill="{t["text"]}">{lab}</text>'
    pipe += f'<line x1="30" y1="430" x2="470" y2="430" stroke="{t["border"]}"/><text x="30" y="456" font-family="{MONO}" font-size="14" fill="{t["muted"]}">5 clouds + 10 AI vendors, one framework</text></g>'
    body = f'''<defs>{defs(t)}<radialGradient id="r3" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{t['g3']}" stop-opacity="{t['glow3']}"/><stop offset="1" stop-color="{t['g3']}" stop-opacity="0"/></radialGradient>
<radialGradient id="r1" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{t['g1']}" stop-opacity="{t['glow1']}"/><stop offset="1" stop-color="{t['g1']}" stop-opacity="0"/></radialGradient>
<pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="{t['dot']}" fill-opacity="{t['dotop']}"/></pattern><clipPath id="c"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="34"/></clipPath></defs>
<rect width="{W}" height="{H}" rx="34" fill="{t['bg']}"/><g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="url(#dots)"/><circle cx="1050" cy="90" r="400" fill="url(#r3)"/><circle cx="90" cy="600" r="360" fill="url(#r1)"/></g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="33" fill="none" stroke="{t['border']}" stroke-width="1.5"/>
<circle cx="84" cy="96" r="5" fill="url(#gd)"/><text x="104" y="102" font-family="{MONO}" font-size="15" font-weight="500" fill="{t['muted']}" letter-spacing="3.2">SOFTWARE ENGINEER · PHOENIX, AZ</text>
<text x="76" y="236" font-family="{DISPLAY}" font-size="122" font-weight="800" fill="{t['text']}" letter-spacing="-5">Sakar</text>
<text x="76" y="352" font-family="{DISPLAY}" font-size="122" font-weight="800" fill="url(#g)" letter-spacing="-5">Joshi</text>
<text x="80" y="418" font-family="{SANS}" font-size="27" fill="{t['muted']}">I build <tspan font-weight="600" fill="{t['text']}">AI products</tspan> and the <tspan font-weight="600" fill="{t['text']}">cloud data</tspan></text>
<text x="80" y="454" font-family="{SANS}" font-size="27" fill="{t['muted']}">pipelines behind them.</text>
<rect x="80" y="496" width="414" height="48" rx="24" fill="{t['surface']}" stroke="{t['border']}" stroke-width="1.5"/><circle cx="106" cy="520" r="5" fill="{t['ok']}"/><circle cx="106" cy="520" r="5" fill="none" stroke="{t['ok']}"><animate attributeName="r" values="5;14" dur="2.2s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".8;0" dur="2.2s" repeatCount="indefinite"/></circle>
<text x="126" y="526" font-family="{MONO}" font-size="15" font-weight="500" fill="{t['text']}">Now: FinOps for AI at Prama AI</text>
{pipe}'''
    return svg(W, H, "Sakar Joshi, software engineer in Phoenix. I build AI products and the cloud data pipelines behind them. Currently building FinOps for AI at Prama AI.", {F_S8, F_I4, F_I6, F_J5}, body)

# ------------------------------------------------------------------ impact
IMPACT = [("10+", "AI vendors tracked", "FinOps-for-AI dashboards for Claude, OpenAI, Gemini, Bedrock, Copilot and more"),
          ("5", "clouds ingested", "AWS, Azure, Azure China, OCI and Alibaba through one framework into Iceberg"),
          ("20+", "PRs, one pattern", "per-provider TokenOps dashboards on a single reusable design"),
          ("12", "features in 3 sprints", "for a cyber-insurance underwriting portal used by QBE")]

def impact(n):
    t = THEMES[n]; W, H = 1200, 262; cw = W / 4
    body = f'<defs>{defs(t)}</defs>' + panel(t, 0, 0, W, H, 30)
    for i, (num, lab, cap) in enumerate(IMPACT):
        x = i * cw + 44
        if i: body += f'<line x1="{i * cw:.0f}" y1="42" x2="{i * cw:.0f}" y2="{H - 42}" stroke="{t["border"]}" stroke-width="1.5"/>'
        body += f'<text x="{x:.0f}" y="112" font-family="{DISPLAY}" font-size="78" font-weight="800" fill="url(#g)" letter-spacing="-3">{num}</text>'
        body += f'<text x="{x:.0f}" y="152" font-family="{SANS}" font-size="22" font-weight="600" fill="{t["text"]}">{escape(lab)}</text>'
        body += lines(cap, 27, round(x), 184, 24, font_family=SANS, font_size=17.5, fill=t["muted"])
    return svg(W, H, "Impact: 10+ AI vendors tracked, 5 clouds ingested, 20+ PRs on one pattern, 12 features shipped in 3 sprints", {F_S8, F_I6, F_I4}, body)

# ------------------------------------------------------------------ section headers
def header(n, label):
    t = THEMES[n]; W, H = 1200, 70
    tw = len(label) * 14.4 + 4
    body = f'<defs>{defs(t)}</defs><rect x="0" y="30" width="40" height="5" rx="2.5" fill="url(#g)"/><text x="58" y="38" font-family="{MONO}" font-size="17" font-weight="500" fill="{t["text"]}" letter-spacing="4.5">{escape(label)}</text><line x1="{58 + tw + 20:.0f}" y1="32" x2="{W}" y2="32" stroke="{t["border"]}" stroke-width="1.5"/>'
    return svg(W, H, label.title(), {F_J5}, body)

# ------------------------------------------------------------------ project cards
PROJECTS = {
    "monotask": ("AI PRODUCT · PWA", "Monotask", "Tasks, calendar and habits with Claude-powered capture, as an installable PWA.", "RLS at the database · every AI write is human-approved", ["React", "Supabase", "Claude"]),
    "cloudsentry": ("AI AGENTS · AWS", "Cloudsentry", "Your AWS account as a live graph, watched by three AI agents.", "The model only records intent · a human approves every action", ["FastAPI", "boto3", "Next.js"]),
    "resume": ("AI PRODUCT · WEB APP", "ResumeBuilder", "ATS-friendly resumes with live preview and AI bullet rewriting.", "Zod-validated output, auto-retry · never invents metrics", ["Next.js", "Supabase", "Groq"]),
    "portal": ("PLATFORM · DEVOPS", "Employee Portal", "A directory app deployed like a regulated enterprise would.", "Two Vault clusters that unseal each other · no public registries", ["Terraform", "Vault", "FastAPI"]),
}

def art(key, t):
    s = ""; sw = 2.6
    if key == "monotask":
        for i in range(3):
            y = 40 + i * 42; done = i == 0
            s += f'<circle cx="34" cy="{y}" r="12" fill="{"url(#gd)" if done else "none"}" stroke="{"none" if done else t["muted"]}" stroke-width="2"/>'
            if done: s += f'<path d="M28 {y} l4.5 4.5 l8 -9" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            s += f'<rect x="60" y="{y - 5}" width="{[112, 84, 98][i]}" height="10" rx="5" fill="{t["muted"]}" opacity="{.35 if done else .6}"/>'
        s += f'<rect x="52" y="116" width="150" height="40" rx="12" fill="none" stroke="url(#g)" stroke-width="2" stroke-dasharray="6 5"/><rect x="118" y="124" width="76" height="26" rx="13" fill="url(#g)"/><text x="156" y="142" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="500" fill="#fff">Approve</text>'
    elif key == "cloudsentry":
        nodes = [(30, 126), (84, 70), (136, 118), (192, 56), (54, 30), (112, 28), (200, 132)]
        for a, b in [(0, 1), (1, 2), (2, 3), (1, 4), (1, 5), (2, 6), (5, 3), (0, 2)]: s += f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{t["muted"]}" stroke-opacity=".5" stroke-width="1.8"/>'
        for i, (x, y) in enumerate(nodes):
            if i in (1, 3, 6):
                s += f'<circle cx="{x}" cy="{y}" r="12" fill="none" stroke="url(#g)" stroke-width="2"><animate attributeName="r" values="12;26" dur="2.6s" begin="{i * .4}s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".9;0" dur="2.6s" begin="{i * .4}s" repeatCount="indefinite"/></circle><circle cx="{x}" cy="{y}" r="11" fill="url(#gd)"/>'
            else: s += f'<circle cx="{x}" cy="{y}" r="6" fill="{t["surface2"]}" stroke="{t["muted"]}" stroke-width="2"/>'
    elif key == "resume":
        s += f'<rect x="46" y="6" width="150" height="156" rx="12" fill="{t["surface"]}" stroke="{t["border"]}" stroke-width="2"/><rect x="62" y="24" width="64" height="11" rx="5.5" fill="{t["text"]}" opacity=".85"/><rect x="62" y="44" width="98" height="7" rx="3.5" fill="url(#g)"/>'
        for i, w in enumerate([116, 104, 0, 108, 82]):
            y = 66 + i * 17
            if w: s += f'<rect x="62" y="{y}" width="{w}" height="7" rx="3.5" fill="{t["muted"]}" opacity=".5"/>'
            else: s += f'<rect x="56" y="{y - 5}" width="130" height="18" rx="6" fill="url(#g)" opacity=".22"/><rect x="62" y="{y}" width="112" height="7" rx="3.5" fill="url(#g)"/>'
        s += f'<path d="M206 36 l4 12 l12 4 l-12 4 l-4 12 l-4 -12 l-12 -4 l12 -4z" fill="url(#gd)"><animateTransform attributeName="transform" type="rotate" from="0 206 52" to="360 206 52" dur="10s" repeatCount="indefinite"/></path>'
    else:
        for x0, lab in [(22, "A"), (146, "B")]:
            s += f'<rect x="{x0}" y="24" width="84" height="84" rx="20" fill="{t["surface"]}" stroke="url(#g)" stroke-width="2.6"/><circle cx="{x0 + 42}" cy="58" r="11" fill="none" stroke="{t["text"]}" stroke-width="2.6"/><rect x="{x0 + 37}" y="62" width="10" height="20" rx="4" fill="{t["text"]}"/>'
        s += f'<path d="M110 52 H142 M134 44 L142 52 L134 60" fill="none" stroke="url(#g)" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><animate attributeName="stroke-opacity" values="1;.35;1" dur="2s" repeatCount="indefinite"/></path><path d="M142 78 H110 M118 70 L110 78 L118 86" fill="none" stroke="url(#g)" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><animate attributeName="stroke-opacity" values=".35;1;.35" dur="2s" repeatCount="indefinite"/></path>'
        for i in range(2): s += f'<rect x="{22 + i * 124}" y="124" width="84" height="26" rx="8" fill="{t["surface2"]}" stroke="{t["border"]}" stroke-width="1.5"/><circle cx="{38 + i * 124}" cy="137" r="4" fill="{t["ok"]}"/><rect x="{50 + i * 124}" y="134" width="40" height="6" rx="3" fill="{t["muted"]}" opacity=".5"/>'
    return s

def card(key, n):
    t = THEMES[n]; W, H = 640, 424; label, title, desc, proof, tags = PROJECTS[key]
    body = f'<defs>{defs(t)}<radialGradient id="rg" cx="1" cy="0" r="1"><stop offset="0" stop-color="{t["g3"]}" stop-opacity="{t["glow3"]}"/><stop offset="1" stop-color="{t["g3"]}" stop-opacity="0"/></radialGradient></defs>'
    body += panel(t, 0, 0, W, H, 28) + f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="27" fill="url(#rg)"/>'
    body += f'<rect x="36" y="50" width="22" height="4" rx="2" fill="url(#g)"/><text x="68" y="58" font-family="{MONO}" font-size="14" font-weight="500" fill="{t["muted"]}" letter-spacing="2.2">{escape(label)}</text>'
    body += f'<text x="36" y="124" font-family="{DISPLAY}" font-size="40" font-weight="700" fill="{t["text"]}" letter-spacing="-1.3">{escape(title)}</text>'
    body += f'<g transform="translate(418 30) scale(.8)">{panel(t, 0, 0, 254, 176, 22, t["surface2"])}<g transform="translate(14 8)">{art(key, t)}</g></g>'
    body += lines(desc, 40, 36, 206, 32, font_family=SANS, font_size=23, fill=t["text"])
    body += f'<circle cx="42" cy="288" r="5" fill="url(#gd)"/>' + lines(proof, 42, 58, 294, 26, font_family=MONO, font_size=16.5, fill=t["muted"])
    x = 36
    for tag in tags:
        w = len(tag) * 9.6 + 32
        body += f'<rect x="{x}" y="346" width="{w:.0f}" height="40" rx="20" fill="none" stroke="{t["border"]}" stroke-width="1.8"/><text x="{x + w / 2:.0f}" y="372" text-anchor="middle" font-family="{MONO}" font-size="15.5" font-weight="500" fill="{t["text"]}">{escape(tag)}</text>'
        x += w + 9
    cx, cy = W - 66, 366
    body += f'<circle cx="{cx}" cy="{cy}" r="30" fill="url(#gd)"/><path d="M{cx - 10} {cy + 10} L{cx + 10} {cy - 10} M{cx - 4} {cy - 10} H{cx + 10} V{cy + 4}" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(W, H, f"{title}: {desc} {proof}", {F_S7, F_I4, F_J5}, body)

# ------------------------------------------------------------------ experience
EXPERIENCE = [("MAY 2026 — NOW", "Systems & DevOps Engineer", "Prama AI · Finomics, multi-cloud FinOps", "FinOps-for-AI dashboards across 10+ AI vendors. Glue and PySpark pipelines into Iceberg across 5 clouds. Rightsizing with safety guards."),
              ("SEP — DEC 2025", "Frontend Engineer Intern", "XDuce · QBE Insurance", "Built the underwriting submissions inbox: a 180+ record data grid with server-side filtering. 12 features across 3 sprints."),
              ("MAY — DEC 2025", "Web Developer", "ASU Project Humanities", "Owned two sites with 5,000+ monthly visitors. WCAG improvements, +31% email opens, +30% referral traffic."),
              ("SEP 2022 — NOV 2023", "Software Developer", "Macrosoft Creations", "Angular SPAs and .NET REST APIs for two enterprise systems, behind RBAC and ABAC authorization.")]

def experience(n):
    t = THEMES[n]; W, rh = 1200, 132; H = rh * len(EXPERIENCE) + 12; rx = 262
    body = f'<defs>{defs(t, False)}</defs><line x1="{rx}" y1="30" x2="{rx}" y2="{H - 40}" stroke="url(#g)" stroke-width="2.5" stroke-linecap="round" stroke-opacity=".6"/>'
    for i, (date, role, co, impact_) in enumerate(EXPERIENCE):
        y = 6 + i * rh; now = i == 0
        if i: body += f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{t["border"]}" stroke-width="1.5"/>'
        body += f'<text x="{rx - 28}" y="{y + 58}" text-anchor="end" font-family="{MONO}" font-size="15" font-weight="500" fill="{t["text"] if now else t["muted"]}" letter-spacing="1.4">{escape(date)}</text>'
        if now: body += f'<circle cx="{rx}" cy="{y + 53}" r="9" fill="none" stroke="url(#gd)" stroke-width="2"><animate attributeName="r" values="9;20" dur="2.4s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".9;0" dur="2.4s" repeatCount="indefinite"/></circle>'
        body += f'<circle cx="{rx}" cy="{y + 53}" r="{8 if now else 6}" fill="{"url(#gd)" if now else t["bg"]}" stroke="{"none" if now else t["muted"]}" stroke-width="2.5"/>'
        body += f'<text x="{rx + 40}" y="{y + 50}" font-family="{DISPLAY}" font-size="29" font-weight="700" fill="{t["text"]}" letter-spacing="-.8">{escape(role)}</text>'
        body += f'<text x="{rx + 40}" y="{y + 84}" font-family="{SANS}" font-size="19" font-weight="600" fill="{t["muted"]}">{escape(co)}</text>'
        body += lines(impact_, 44, 780, y + 46, 26, font_family=SANS, font_size=17.5, fill=t["muted"])
    return svg(W, H, "Experience: " + "; ".join(f"{r} at {c.split(' · ')[0]}, {d.title()}" for d, r, c, _ in EXPERIENCE), {F_S7, F_I6, F_I4, F_J5}, body)

# ------------------------------------------------------------------ capabilities
CAPS = [("FRONTEND", ["React · Next.js · Angular", "TypeScript", "Tailwind · shadcn/ui", "Redux · TanStack Query", "Playwright · Vitest"]),
        ("BACKEND & DATA", ["Python · FastAPI", "PostgreSQL · SQL", "Supabase · RLS", ".NET (C#) · REST", "JWT · SSO · RBAC"]),
        ("DATA & CLOUD", ["AWS Glue · PySpark", "Apache Iceberg · Athena", "AWS · Azure · OCI", "Terraform · Vault", "Docker · GitHub Actions"]),
        ("APPLIED AI", ["Anthropic API · Groq", "Schema-validated (Zod)", "Tool-use agents", "Human-in-the-loop", "Prompt evals · quotas"])]

def capabilities(n):
    t = THEMES[n]; W, H = 1200, 290; cw = W / 4
    body = f'<defs>{defs(t)}</defs>' + panel(t, 0, 0, W, H, 30)
    for i, (title, items) in enumerate(CAPS):
        x = i * cw + 40
        if i: body += f'<line x1="{i * cw:.0f}" y1="38" x2="{i * cw:.0f}" y2="{H - 38}" stroke="{t["border"]}" stroke-width="1.5"/>'
        body += f'<rect x="{x:.0f}" y="46" width="22" height="4" rx="2" fill="url(#g)"/><text x="{x + 32:.0f}" y="53" font-family="{MONO}" font-size="14" font-weight="500" fill="{t["muted"]}" letter-spacing="2.6">{escape(title)}</text>'
        for j, it in enumerate(items): body += f'<text x="{x:.0f}" y="{104 + j * 37}" font-family="{SANS}" font-size="19.5" fill="{t["text"]}">{escape(it)}</text>'
    return svg(W, H, "Capabilities. Frontend: React, Next.js, Angular, TypeScript. Backend and data: Python, FastAPI, PostgreSQL, Supabase. Data and cloud: AWS Glue, PySpark, Iceberg, Terraform. Applied AI: Anthropic API, Groq, Zod, agents.", {F_I4, F_J5}, body)

# ------------------------------------------------------------------ github (live)
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

def github(n, d):
    t = THEMES[n]; W, H = 1200, 196; pad = 44
    body = f'<defs>{defs(t)}<clipPath id="bar"><rect x="{pad}" y="122" width="{W - 2 * pad}" height="10" rx="5"/></clipPath></defs>' + panel(t, 0, 0, W, H, 30)
    cols = [("PUBLIC REPOS", d["repos"]), ("STARS", d["stars"]), ("MERGED PRS", d["prs"]), ("CONTRIBUTIONS · 12 MO", d["contrib"])]
    cw = (W - 2 * pad) / 4
    for i, (lab, val) in enumerate(cols):
        x = pad + i * cw
        body += f'<text x="{x:.0f}" y="66" font-family="{DISPLAY}" font-size="44" font-weight="700" fill="url(#g)" letter-spacing="-1.5">{val:,}</text><text x="{x:.0f}" y="94" font-family="{MONO}" font-size="12.5" font-weight="500" fill="{t["muted"]}" letter-spacing="2">{lab}</text>'
    body += f'<g clip-path="url(#bar)"><rect x="{pad}" y="122" width="{W - 2 * pad}" height="10" fill="{t["surface2"]}"/>'
    x = pad
    for k, c, f in d["langs"]:
        w = f * (W - 2 * pad); body += f'<rect x="{x:.1f}" y="122" width="{w:.1f}" height="10" fill="{c}"/>'; x += w
    body += '</g>'
    lx = pad
    for k, c, f in d["langs"][:4]:
        lab = f"{k} {f * 100:.0f}%"; body += f'<circle cx="{lx + 5}" cy="162" r="5" fill="{c}"/><text x="{lx + 18}" y="167" font-family="{SANS}" font-size="15" fill="{t["muted"]}">{escape(lab)}</text>'; lx += len(lab) * 8.4 + 40
    body += f'<text x="{W - pad}" y="167" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t["muted"]}">public data · updated {datetime.date.today().isoformat()}</text>'
    return svg(W, H, f"GitHub: {d['repos']} public repos, {d['stars']} stars, {d['prs']} merged pull requests, {d['contrib']} contributions in the last year", {F_S7, F_I4, F_J5}, body)

# ------------------------------------------------------------------ buttons
BUTTONS = {"linkedin": ("Connect on LinkedIn", True), "portfolio": ("Portfolio", False), "kramflow": ("Kramflow", False)}

def button(key, n):
    t = THEMES[n]; label, primary = BUTTONS[key]; w = int(len(label) * 12.4 + 84); H = 60
    body = f'<defs>{defs(t)}</defs>'
    if primary: body += f'<rect x="1" y="1" width="{w}" height="56" rx="28" fill="url(#g)"/>'
    else: body += f'<rect x="1.5" y="1.5" width="{w - 1}" height="55" rx="27.5" fill="{t["surface"]}" stroke="{t["border"]}" stroke-width="1.5"/>'
    col = t["onacc"] if primary else t["text"]
    body += f'<text x="30" y="36" font-family="{SANS}" font-size="20" font-weight="600" fill="{col}">{escape(label)}</text><path d="M{w - 38} 38 L{w - 20} 20 M{w - 32} 20 H{w - 20} V32" fill="none" stroke="{col}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(w + 2, H, label, {F_I6}, body)

if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for n in THEMES:
        (ASSETS / f"hero-{n}.svg").write_text(hero(n), encoding="utf-8")
        (ASSETS / f"impact-{n}.svg").write_text(impact(n), encoding="utf-8")
        for k, lab in {"work": "SELECTED WORK", "experience": "EXPERIENCE", "capabilities": "CAPABILITIES", "github": "ON GITHUB"}.items():
            (ASSETS / f"h-{k}-{n}.svg").write_text(header(n, lab), encoding="utf-8")
        for k in PROJECTS: (ASSETS / f"card-{k}-{n}.svg").write_text(card(k, n), encoding="utf-8")
        (ASSETS / f"experience-{n}.svg").write_text(experience(n), encoding="utf-8")
        (ASSETS / f"capabilities-{n}.svg").write_text(capabilities(n), encoding="utf-8")
        for k in BUTTONS: (ASSETS / f"btn-{k}-{n}.svg").write_text(button(k, n), encoding="utf-8")
    d = fetch_stats() if os.environ.get("SKIP_STATS") != "1" else dict(repos=7, stars=4, prs=120, contrib=752, langs=[("TypeScript", "#3178c6", .74), ("JavaScript", "#f1e05a", .09), ("Python", "#3572A5", .08), ("CSS", "#563d7c", .06)])
    for n in THEMES: (ASSETS / f"github-{n}.svg").write_text(github(n, d), encoding="utf-8")
    print("assets:", len(list(ASSETS.glob("*.svg"))), {k: v for k, v in d.items() if k != "langs"})
