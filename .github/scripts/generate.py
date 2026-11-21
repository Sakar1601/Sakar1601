#!/usr/bin/env python3
"""Generates the SVG assets used by README.md, in the visual language of sakar-portfolio-pearl.vercel.app
(warm paper, near-black ink, one yellow, pastel stickers, thick borders, hard offset shadows).

Everything but the numbers is static data below; the numbers come from the GitHub API.
Fonts are embedded as base64 so the SVGs keep their typography inside <img> tags on GitHub.
Run locally:  GH_TOKEN=$(gh auth token) python3 .github/scripts/generate.py     (SKIP_STATS=1 to skip the API)
"""
import base64, colorsys, datetime, json, math, os, subprocess, textwrap
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"
FONTS = Path(__file__).resolve().parent / "fonts"
LOGIN = "Sakar1601"
EXCLUDE_LANGS_FROM = {"College-management-system"}  # legacy upload that would skew the language bar

def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100); return "#%02X%02X%02X" % (round(r * 255), round(g * 255), round(b * 255))

THEMES = {
    "light": dict(bg=hsl(48, 33, 95), card="#FFFFFF", ink=hsl(0, 0, 9), line=hsl(0, 0, 9), text=hsl(0, 0, 9), muted=hsl(0, 0, 38), soft=hsl(48, 20, 90),
                  yellow=hsl(49, 100, 49), hl=hsl(49, 100, 72), pink=hsl(336, 88, 78), blue=hsl(204, 90, 70), green=hsl(148, 58, 64), orange=hsl(24, 96, 67), lilac=hsl(262, 82, 80),
                  grid="#171717", gridop=".06", term="#161616", termtext="#EDEBE0", termdim="#8F8C80"),
    "dark": dict(bg=hsl(40, 8, 8), card=hsl(40, 8, 12), ink=hsl(0, 0, 9), line=hsl(40, 6, 38), text=hsl(48, 33, 93), muted=hsl(40, 8, 64), soft=hsl(40, 6, 16),
                 yellow=hsl(49, 100, 52), hl=hsl(49, 82, 30), pink=hsl(338, 52, 72), blue=hsl(205, 52, 66), green=hsl(152, 36, 60), orange=hsl(25, 60, 64), lilac=hsl(262, 42, 74),
                 grid="#F4F1E6", gridop=".045", term="#0B0A09", termtext="#EDEBE0", termdim="#8F8C80"),
}
SANS = "Inter,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
DISPLAY = "'Bricolage Grotesque','Arial Black',Inter,-apple-system,sans-serif"
MONO = "'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace"
F_BG, F_I4, F_I6, F_J4, F_J5 = "bricolage-grotesque-wght.woff2", "inter-400.woff2", "inter-600.woff2", "jetbrains-mono-400.woff2", "jetbrains-mono-500.woff2"

def font_css(use):
    faces = [("Bricolage Grotesque", "200 800", F_BG), ("Inter", "400", F_I4), ("Inter", "600", F_I6), ("JetBrains Mono", "400", F_J4), ("JetBrains Mono", "500", F_J5)]
    return "".join(f"@font-face{{font-family:'{n}';font-weight:{w};src:url(data:font/woff2;base64,{base64.b64encode((FONTS / f).read_bytes()).decode()}) format('woff2');}}" for n, w, f in faces if f in use)

def svg(w, h, label, use, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}"><style>{font_css(use)}</style>{body}</svg>\n')

def nb(t, x, y, w, h, r, fill, sw=3, off=6, extra=""):
    """Sticker block: hard offset shadow + thick bordered rect."""
    return (f'<rect x="{x + off}" y="{y + off}" width="{w}" height="{h}" rx="{r}" fill="{t["line"]}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{t["line"]}" stroke-width="{sw}" {extra}/>')

def lines(text, width, x, y, lh, **attrs):
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return "".join(f'<text x="{x}" y="{y + i * lh}" {a}>{escape(l)}</text>' for i, l in enumerate(textwrap.wrap(text, width)))

POPS = ["pink", "blue", "green", "orange", "lilac"]

# ------------------------------------------------------------------ banner
def banner(n):
    t = THEMES[n]; W, H = 1200, 600
    hlop = 1 if n == "light" else .55
    term = f'''<g transform="translate(742 112) rotate(2.4)">{nb(t, 0, 0, 420, 300, 18, t["card"], 3, 9)}
<path d="M1.5 40 H418.5" stroke="{t['line']}" stroke-width="3"/><rect x="1.5" y="1.5" width="417" height="38.5" rx="17" fill="{t['soft']}"/><rect x="1.5" y="22" width="417" height="18" fill="{t['soft']}"/><path d="M1.5 40 H418.5" stroke="{t['line']}" stroke-width="3"/>
<circle cx="26" cy="21" r="6.5" fill="#FF5F57" stroke="{t['line']}" stroke-width="1.5"/><circle cx="46" cy="21" r="6.5" fill="#FEBC2E" stroke="{t['line']}" stroke-width="1.5"/><circle cx="66" cy="21" r="6.5" fill="#28C840" stroke="{t['line']}" stroke-width="1.5"/>
<text x="190" y="26" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t['muted']}">finomics · pipeline</text>
<circle cx="326" cy="21" r="4.5" fill="{t['yellow']}" stroke="{t['line']}" stroke-width="1.5"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle><text x="338" y="26" font-family="{MONO}" font-size="13" font-weight="500" fill="{t['text']}">running</text>
<g font-family="{MONO}" font-size="11" fill="{t['text']}" text-anchor="middle" letter-spacing="1.2">
<circle cx="62" cy="84" r="19" fill="{t['pink']}" stroke="{t['line']}" stroke-width="2.5"/><path d="M53 84 l6 6 l11 -12" fill="none" stroke="{t['ink']}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><text x="62" y="124">INGEST</text>
<circle cx="157" cy="84" r="19" fill="{t['blue']}" stroke="{t['line']}" stroke-width="2.5"/><path d="M148 84 l6 6 l11 -12" fill="none" stroke="{t['ink']}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><text x="157" y="124">TRANSFORM</text>
<circle cx="262" cy="84" r="19" fill="{t['card']}" stroke="{t['line']}" stroke-width="2.5"/><path d="M262 71 a13 13 0 0 1 13 13" fill="none" stroke="{t['ink'] if n == 'light' else t['text']}" stroke-width="3" stroke-linecap="round"><animateTransform attributeName="transform" type="rotate" from="0 262 84" to="360 262 84" dur="1.4s" repeatCount="indefinite"/></path><text x="262" y="124">RECOMMEND</text>
<circle cx="360" cy="84" r="19" fill="none" stroke="{t['muted']}" stroke-width="2" stroke-dasharray="4 4"/><text x="360" y="89" font-size="13" fill="{t['muted']}">4</text><text x="360" y="124" fill="{t['muted']}">REPORT</text></g>
<rect x="24" y="142" width="372" height="12" rx="6" fill="{t['card']}" stroke="{t['line']}" stroke-width="2"/><rect x="26" y="144" width="120" height="8" rx="4" fill="{t['yellow']}"><animate attributeName="width" values="90;210;90" dur="7s" repeatCount="indefinite"/></rect>
<rect x="20" y="172" width="380" height="112" rx="12" fill="{t['term']}"/>
<g font-family="{MONO}" font-size="13.5"><text x="36" y="200" fill="{t['termtext']}"><tspan fill="{t['yellow']}">$</tspan> glue run ingest_ai_usage</text><text x="52" y="220" fill="{t['termdim']}">10 vendors · 48,210 rows</text>
<text x="36" y="244" fill="{t['termtext']}"><tspan fill="{t['yellow']}">$</tspan> spark merge into iceberg.silver</text><text x="52" y="264" fill="{t['termdim']}">upserted · idempotent ✓</text></g>
<rect x="36" y="269" width="8" height="13" fill="{t['yellow']}"><animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;.5;.5;.99;1" dur="1.1s" repeatCount="indefinite"/></rect></g>'''
    badge = f'''<g transform="translate(1090 500)"><circle cx="5" cy="5" r="66" fill="{t['line']}"/><circle r="66" fill="{t['yellow']}" stroke="{t['line']}" stroke-width="3"/>
<g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="22s" repeatCount="indefinite"/><path id="cp" d="M-45 0 a45 45 0 1 1 90 0 a45 45 0 1 1 -90 0" fill="none"/>
<text font-family="{MONO}" font-size="12.5" font-weight="500" fill="{t['ink']}" letter-spacing="3.4"><textPath href="#cp">• SAY HELLO • LET'S TALK • SAY HELLO • LET'S TALK </textPath></text></g>
<path d="M-12 12 L12 -12 M-10 -12 H12 V10" fill="none" stroke="{t['ink']}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></g>'''
    body = f'''<defs><pattern id="grid" width="56" height="56" patternUnits="userSpaceOnUse"><path d="M56 0H0V56" fill="none" stroke="{t['grid']}" stroke-opacity="{t['gridop']}"/></pattern>
<radialGradient id="glow" cx=".3" cy=".4" r=".5"><stop offset="0" stop-color="{t['yellow']}" stop-opacity=".30"/><stop offset="1" stop-color="{t['yellow']}" stop-opacity="0"/></radialGradient>
<clipPath id="c"><rect x="3" y="3" width="{W - 6}" height="{H - 6}" rx="26"/></clipPath></defs>
<rect width="{W}" height="{H}" rx="28" fill="{t['bg']}"/><g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="url(#grid)"/><rect width="{W}" height="{H}" fill="url(#glow)"/></g>
<rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="27" fill="none" stroke="{t['line']}" stroke-width="3"/>
<text x="76" y="98" font-family="{MONO}" font-size="16" font-weight="500" fill="{t['muted']}" letter-spacing="4.5">PHOENIX, AZ</text><rect x="236" y="93" width="250" height="1.6" fill="{t['muted']}" opacity=".6"/>
<text x="68" y="252" font-family="{DISPLAY}" font-size="180" font-weight="800" fill="{t['text']}" letter-spacing="-7">SAKAR</text>
<text x="68" y="392" font-family="{DISPLAY}" font-size="180" font-weight="800" fill="{t['text']}" letter-spacing="-7">JOSHI</text>
<rect x="76" y="470" width="496" height="13" fill="{t['hl']}" opacity="{hlop}"/><rect x="76" y="506" width="118" height="13" fill="{t['hl']}" opacity="{hlop}"/>
<text x="76" y="458" font-family="{SANS}" font-size="27" fill="{t['text']}">Full-stack software engineer building</text>
<text x="76" y="494" font-family="{SANS}" font-size="27" font-weight="600" fill="{t['text']}">AI-integrated products and cloud data</text>
<text x="76" y="530" font-family="{SANS}" font-size="27" fill="{t['text']}"><tspan font-weight="600">pipelines</tspan> that teams can trust.</text>
{term}{badge}'''
    return svg(W, H, "Sakar Joshi, full-stack software engineer building AI-integrated products and cloud data pipelines that teams can trust. Phoenix, AZ.", {F_BG, F_I4, F_I6, F_J4, F_J5}, body)

# ------------------------------------------------------------------ marquee
MARQUEE = ["PYTHON", "AWS", "SUPABASE", "LLM AGENTS", "FINOPS", "TYPESCRIPT", "REACT", "TERRAFORM", "POSTGRESQL", "PYSPARK", "ICEBERG", "NEXT.JS", "FASTAPI", "VAULT"]

def marquee(n):
    t = THEMES[n]; W, H = 1200, 60; cw = 16 * .6 + 5
    x = 40; items = ""
    for i, w in enumerate(MARQUEE):
        col = [t["blue"], t["green"], t["orange"], t["lilac"], t["yellow"], t["pink"]][i % 6]
        items += f'<text x="{x:.0f}" y="37" font-family="{MONO}" font-size="16" font-weight="500" fill="{col}" letter-spacing="5">{escape(w)}</text><text x="{x + len(w) * cw + 34:.0f}" y="37" font-family="{MONO}" font-size="16" fill="{t["termtext"]}">✦</text>'
        x += len(w) * cw + 34 + 52
    L = x - 40
    body = f'<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs><g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="#161616"/><g><animateTransform attributeName="transform" type="translate" from="0 0" to="{-L:.0f} 0" dur="{L / 55:.0f}s" repeatCount="indefinite"/>{items}<g transform="translate({L:.0f} 0)">{items}</g></g></g><rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="13" fill="none" stroke="{t["line"]}" stroke-width="3"/>'
    return svg(W, H, "Stack: " + ", ".join(MARQUEE), {F_J5}, body)

# ------------------------------------------------------------------ buttons
BUTTONS = {"portfolio": ("See the work", True), "linkedin": ("LinkedIn", False), "kramflow": ("Kramflow", False)}

def button(key, n):
    t = THEMES[n]; label, primary = BUTTONS[key]; w = int(len(label) * 11.8 + (112 if primary else 96)); H = 76
    body = nb(t, 4, 4, w, 56, 28, t["card"], 3, 5)
    body += f'<text x="{26}" y="40" font-family="{SANS}" font-size="21" font-weight="600" fill="{t["text"]}">{escape(label)}</text>'
    cx = w - 24
    body += f'<circle cx="{cx}" cy="32" r="18" fill="{t["yellow"]}" stroke="{t["line"]}" stroke-width="2.5"/><path d="M{cx - 7} 32 H{cx + 7} M{cx + 1} 25 L{cx + 8} 32 L{cx + 1} 39" fill="none" stroke="{t["ink"]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(w + 14, H, label, {F_I6}, body)

# ------------------------------------------------------------------ section headers
def header(n, eyebrow, title):
    t = THEMES[n]; W, H = 1000, 118
    body = f'<rect x="4" y="22" width="14" height="14" fill="{t["yellow"]}" stroke="{t["line"]}" stroke-width="2.5"/><text x="30" y="34" font-family="{MONO}" font-size="15" font-weight="500" fill="{t["muted"]}" letter-spacing="3.5">{escape(eyebrow)}</text>'
    body += f'<text x="2" y="96" font-family="{DISPLAY}" font-size="62" font-weight="800" fill="{t["text"]}" letter-spacing="-2">{escape(title)}</text>'
    return svg(W, H, title, {F_BG, F_J5}, body)

# ------------------------------------------------------------------ project cards
PROJECTS = {
    "monotask": ("01", "Monotask", "Tasks, calendar and habits. Claude captures, and you approve every AI suggestion.", ["React", "Supabase", "Claude"], "yellow"),
    "cloudsentry": ("02", "Cloudsentry", "Your AWS account as a live graph, watched by three AI agents you approve.", ["FastAPI", "boto3", "Next.js"], "blue"),
    "resume": ("03", "ResumeBuilder", "ATS-friendly resumes with live preview and AI that never invents metrics.", ["Next.js", "Supabase", "Groq"], "pink"),
    "portal": ("04", "Employee Portal", "A directory app deployed like a regulated company: Vault, Terraform, Ansible.", ["Terraform", "Vault", "FastAPI"], "green"),
}

def art(key, t):
    ink, paper = t["ink"], "#FFFDF4"; s = ""
    if key == "monotask":
        for i, done in enumerate([True, False, False]):
            y = 44 + i * 36
            s += f'<circle cx="34" cy="{y}" r="11" fill="{ink if done else paper}" stroke="{ink}" stroke-width="2.5"/>'
            if done: s += f'<path d="M28 {y} l4.5 4.5 l8 -9" fill="none" stroke="{paper}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            s += f'<rect x="58" y="{y - 5}" width="{[120, 90, 110][i]}" height="10" rx="5" fill="{ink}" opacity="{.35 if done else .8}"/>'
        s += f'<rect x="150" y="104" width="62" height="24" rx="12" fill="{ink}"/><text x="181" y="121" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="500" fill="{paper if False else "#FFFFFF"}">AI</text>'
        s += f'<rect x="46" y="98" width="170" height="36" rx="10" fill="none" stroke="{ink}" stroke-width="2.5" stroke-dasharray="6 5"/>'
    elif key == "cloudsentry":
        nodes = [(36, 118), (90, 62), (140, 112), (196, 54), (58, 26), (118, 24), (202, 124)]
        for a, b in [(0, 1), (1, 2), (2, 3), (1, 4), (1, 5), (2, 6), (5, 3), (0, 2)]: s += f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{ink}" stroke-width="2.5"/>'
        for i, (x, y) in enumerate(nodes):
            big = i in (1, 3, 6)
            if big: s += f'<circle cx="{x}" cy="{y}" r="11" fill="none" stroke="{ink}" stroke-width="2"><animate attributeName="r" values="11;24" dur="2.6s" begin="{i * .4}s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".9;0" dur="2.6s" begin="{i * .4}s" repeatCount="indefinite"/></circle>'
            s += f'<circle cx="{x}" cy="{y}" r="{11 if big else 6}" fill="{paper if big else ink}" stroke="{ink}" stroke-width="2.5"/>'
    elif key == "resume":
        s += f'<rect x="40" y="10" width="150" height="146" rx="10" fill="{paper}" stroke="{ink}" stroke-width="2.5"/><rect x="56" y="28" width="62" height="12" rx="6" fill="{ink}"/><rect x="56" y="48" width="96" height="7" rx="3.5" fill="{ink}" opacity=".5"/>'
        for i, w in enumerate([112, 100, 0, 104, 80]):
            y = 70 + i * 15
            if w: s += f'<rect x="56" y="{y}" width="{w}" height="7" rx="3.5" fill="{ink}" opacity=".6"/>'
            else: s += f'<rect x="52" y="{y - 4}" width="124" height="15" rx="4" fill="{t["yellow"]}" stroke="{ink}" stroke-width="2"/><rect x="58" y="{y + 1}" width="100" height="7" rx="3.5" fill="{ink}"/>'
        s += f'<path d="M206 40 l4 12 l12 4 l-12 4 l-4 12 l-4 -12 l-12 -4 l12 -4z" fill="{ink}"><animateTransform attributeName="transform" type="rotate" from="0 206 56" to="360 206 56" dur="9s" repeatCount="indefinite"/></path>'
    else:
        for i in range(3):
            y = 12 + i * 46
            s += f'<rect x="12" y="{y}" width="140" height="36" rx="10" fill="{paper}" stroke="{ink}" stroke-width="2.5"/><rect x="24" y="{y + 15}" width="50" height="7" rx="3.5" fill="{ink}" opacity=".5"/><circle cx="118" cy="{y + 18}" r="5" fill="{ink}"/><circle cx="134" cy="{y + 18}" r="5" fill="none" stroke="{ink}" stroke-width="2"/>'
        s += f'<line x1="152" y1="52" x2="186" y2="80" stroke="{ink}" stroke-width="2.5" stroke-dasharray="5 4"/><line x1="152" y1="108" x2="186" y2="82" stroke="{ink}" stroke-width="2.5" stroke-dasharray="5 4"/>'
        s += f'<circle cx="206" cy="80" r="26" fill="{t["yellow"]}" stroke="{ink}" stroke-width="3"/><circle cx="206" cy="75" r="7" fill="none" stroke="{ink}" stroke-width="3"/><rect x="201" y="79" width="10" height="13" rx="3" fill="{ink}"/>'
    return s

def card(key, n):
    t = THEMES[n]; W, H = 760, 420; num, title, desc, tags, pop = PROJECTS[key]
    body = nb(t, 4, 4, W - 18, H - 18, 22, t["card"], 3, 9)
    body += nb(t, 38, 36, 60, 60, 12, t[pop], 3, 4) + f'<text x="68" y="76" text-anchor="middle" font-family="{DISPLAY}" font-size="28" font-weight="800" fill="{t["ink"]}">{num}</text>'
    body += f'<g transform="translate(474 40) rotate({2.2 if int(num) % 2 else -2.2} 118 80)">{nb(t, 0, 0, 236, 160, 16, t[pop], 3, 6)}<g transform="translate(8 6)">{art(key, t)}</g></g>'
    body += f'<text x="40" y="170" font-family="{DISPLAY}" font-size="52" font-weight="800" fill="{t["text"]}" letter-spacing="-1.5">{escape(title)}</text>'
    body += lines(desc, 52, 40, 252, 34, font_family=SANS, font_size=23, fill=t["muted"])
    x = 40
    for tag in tags:
        w = len(tag) * 9.9 + 36
        body += f'<rect x="{x}" y="334" width="{w:.0f}" height="42" rx="21" fill="none" stroke="{t["line"]}" stroke-width="2.5"/><text x="{x + w / 2:.0f}" y="361" text-anchor="middle" font-family="{MONO}" font-size="16.5" font-weight="500" fill="{t["text"]}">{escape(tag)}</text>'
        x += w + 10
    cx, cy = W - 78, 356
    body += f'<circle cx="{cx + 4}" cy="{cy + 4}" r="31" fill="{t["line"]}"/><circle cx="{cx}" cy="{cy}" r="31" fill="{t["yellow"]}" stroke="{t["line"]}" stroke-width="3"/><path d="M{cx - 11} {cy + 11} L{cx + 11} {cy - 11} M{cx - 4} {cy - 11} H{cx + 11} V{cy + 4}" fill="none" stroke="{t["ink"]}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(W, H, f"{title}: {desc}", {F_BG, F_I4, F_J5}, body)

# ------------------------------------------------------------------ path
PATH = [("2022 – 23", "Software Developer", "Macrosoft Creations", "Angular and .NET for two enterprise systems", "lilac"),
        ("2025", "Web Developer", "ASU Project Humanities", "5,000+ monthly visitors, +31% email opens", "green"),
        ("2025", "Frontend Intern", "XDuce · QBE Insurance", "12 features shipped in 3 sprints", "orange"),
        ("2026 – NOW", "Systems & DevOps Engineer", "Prama AI", "FinOps for AI across 10+ AI vendors", "yellow")]

def timeline(n):
    t = THEMES[n]; W, H = 1000, 290; cw, gap = 226, 22
    body = f'<line x1="0" y1="26" x2="{W}" y2="26" stroke="{t["line"]}" stroke-width="4" stroke-linecap="round"/>'
    for i, (date, role, co, line, pop) in enumerate(PATH):
        x = 4 + i * (cw + gap); now = i == len(PATH) - 1; cx = x + cw / 2
        body += f'<rect x="{cx - 12:.0f}" y="14" width="24" height="24" rx="5" fill="{t[pop]}" stroke="{t["line"]}" stroke-width="3"/>'
        if now: body += f'<rect x="{cx - 12:.0f}" y="14" width="24" height="24" rx="5" fill="none" stroke="{t["yellow"]}" stroke-width="3"><animate attributeName="x" values="{cx - 12:.0f};{cx - 22:.0f}" dur="1.8s" repeatCount="indefinite"/><animate attributeName="y" values="14;4" dur="1.8s" repeatCount="indefinite"/><animate attributeName="width" values="24;44" dur="1.8s" repeatCount="indefinite"/><animate attributeName="height" values="24;44" dur="1.8s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values="1;0" dur="1.8s" repeatCount="indefinite"/></rect>'
        body += f'<line x1="{cx:.0f}" y1="38" x2="{cx:.0f}" y2="62" stroke="{t["line"]}" stroke-width="3"/>'
        body += nb(t, x, 62, cw, 200, 16, t["card"], 3, 6)
        dw = len(date) * 8.6 + 22
        body += f'<rect x="{x + 16}" y="80" width="{dw:.0f}" height="28" rx="14" fill="{t[pop]}" stroke="{t["line"]}" stroke-width="2"/><text x="{x + 16 + dw / 2:.0f}" y="99" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="500" fill="{t["ink"]}" letter-spacing="1.2">{escape(date)}</text>'
        rl = textwrap.wrap(role, 17)
        for j, l in enumerate(rl): body += f'<text x="{x + 16}" y="{140 + j * 27}" font-family="{DISPLAY}" font-size="21.5" font-weight="800" fill="{t["text"]}" letter-spacing="-.4">{escape(l)}</text>'
        yy = 140 + len(rl) * 27
        body += f'<text x="{x + 16}" y="{yy + 2}" font-family="{SANS}" font-size="14.5" font-weight="600" fill="{t["text"]}">{escape(co)}</text>'
        for j, l in enumerate(textwrap.wrap(line, 26)): body += f'<text x="{x + 16}" y="{yy + 26 + j * 19}" font-family="{SANS}" font-size="13.5" fill="{t["muted"]}">{escape(l)}</text>'
    return svg(W, H, "Career path: Software Developer at Macrosoft Creations 2022 to 2023; Web Developer at ASU Project Humanities 2025; Frontend Intern at XDuce 2025; Systems and DevOps Engineer at Prama AI 2026 to now", {F_BG, F_I4, F_I6, F_J5}, body)

# ------------------------------------------------------------------ numbers (tiles static, strip live)
TILES = [("4", "ROLES SHIPPED", "pink"), ("5", "AI-INTEGRATED PROJECTS", "blue"), ("10+", "AI VENDORS TRACKED", "green"), ("2", "DEGREES", "orange")]
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

def numbers(n, d):
    t = THEMES[n]; W, H = 1000, 268; cw, gap = 226, 22
    body = ""
    for i, (v, lab, pop) in enumerate(TILES):
        x = 4 + i * (cw + gap)
        body += nb(t, x, 6, cw, 128, 16, t[pop], 3, 6)
        body += f'<text x="{x + cw / 2}" y="76" text-anchor="middle" font-family="{DISPLAY}" font-size="56" font-weight="800" fill="{t["ink"]}" letter-spacing="-1.5">{v}</text>'
        for j, l in enumerate(textwrap.wrap(lab, 16)): body += f'<text x="{x + cw / 2}" y="{102 + j * 17}" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="500" fill="{t["ink"]}" letter-spacing="1.6">{l}</text>'
    body += nb(t, 4, 158, W - 16, 96, 16, t["card"], 3, 6)
    body += f'<text x="26" y="190" font-family="{MONO}" font-size="14.5" font-weight="500" fill="{t["text"]}" letter-spacing=".5"><tspan fill="{t["muted"]}">GITHUB  </tspan>{d["repos"]} public repos  ·  {d["stars"]} stars  ·  {d["prs"]} merged PRs  ·  {d["contrib"]:,} contributions / 12 mo</text>'
    body += f'<defs><clipPath id="bar"><rect x="26" y="204" width="{W - 60}" height="14" rx="7"/></clipPath></defs><g clip-path="url(#bar)"><rect x="26" y="204" width="{W - 60}" height="14" fill="{t["soft"]}"/>'
    x = 26
    for k, c, f in d["langs"]:
        w = f * (W - 60); body += f'<rect x="{x:.1f}" y="204" width="{w:.1f}" height="14" fill="{c}"/>'; x += w
    body += f'</g><rect x="26" y="204" width="{W - 60}" height="14" rx="7" fill="none" stroke="{t["line"]}" stroke-width="2.5"/>'
    lx = 26
    for k, c, f in d["langs"][:4]:
        lab = f"{k} {f * 100:.0f}%"; body += f'<circle cx="{lx + 5}" cy="238" r="5" fill="{c}" stroke="{t["line"]}" stroke-width="1.5"/><text x="{lx + 16}" y="242" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{escape(lab)}</text>'; lx += len(lab) * 7.4 + 38
    body += f'<text x="{W - 26}" y="242" text-anchor="end" font-family="{MONO}" font-size="11" fill="{t["muted"]}">public data · updated {datetime.date.today().isoformat()}</text>'
    return svg(W, H, f"4 roles shipped, 5 AI-integrated projects, 10+ AI vendors tracked, 2 degrees. GitHub: {d['repos']} public repos, {d['stars']} stars, {d['prs']} merged pull requests, {d['contrib']} contributions in the last year.", {F_BG, F_J5}, body)

if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for n in THEMES:
        (ASSETS / f"banner-{n}.svg").write_text(banner(n), encoding="utf-8")
        (ASSETS / f"marquee-{n}.svg").write_text(marquee(n), encoding="utf-8")
        for k in BUTTONS: (ASSETS / f"btn-{k}-{n}.svg").write_text(button(k, n), encoding="utf-8")
        for k, (e, ti) in {"work": ("01 / SELECTED WORK", "What I've built"), "path": ("02 / PATH", "Where I've built it"), "numbers": ("03 / NUMBERS", "By the numbers")}.items():
            (ASSETS / f"h-{k}-{n}.svg").write_text(header(n, e, ti), encoding="utf-8")
        for k in PROJECTS: (ASSETS / f"card-{k}-{n}.svg").write_text(card(k, n), encoding="utf-8")
        (ASSETS / f"timeline-{n}.svg").write_text(timeline(n), encoding="utf-8")
    d = fetch_stats() if os.environ.get("SKIP_STATS") != "1" else dict(repos=7, stars=4, prs=119, contrib=750, langs=[("TypeScript", "#3178c6", .74), ("JavaScript", "#f1e05a", .09), ("Python", "#3572A5", .08), ("CSS", "#563d7c", .06)])
    for n in THEMES: (ASSETS / f"numbers-{n}.svg").write_text(numbers(n, d), encoding="utf-8")
    print("assets:", len(list(ASSETS.glob("*.svg"))), {k: v for k, v in d.items() if k != "langs"})
