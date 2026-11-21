#!/usr/bin/env python3
"""Generates the SVG assets used by README.md, in the visual language of my portfolio (sakar-portfolio-pearl.vercel.app)
(warm paper, near-black ink, one yellow, pastel stickers, thick borders, hard offset shadows).

Everything but the numbers is static data below; the numbers come from the GitHub API.
Fonts are embedded as base64 so the SVGs keep their typography inside <img> tags on GitHub.
Run locally:  GH_TOKEN=$(gh auth token) python3 .github/scripts/generate.py     (SKIP_STATS=1 to skip the API)
"""
import base64, colorsys, datetime, json, math, os, re, subprocess, textwrap
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
STICKERS = [("AI PRODUCTS", "pink", -6, 930, 112, 200), ("CLOUD DATA", "blue", 5, 1010, 198, 184), ("FINOPS", "green", -4, 842, 214, 112),
            ("FULL-STACK", "orange", 4, 958, 292, 178)]
INTRO = "At Prama AI I make FinOps for AI real: what teams actually spend on Claude, OpenAI, Gemini and Bedrock. In my own products, the AI proposes and a human decides."

def banner(n):
    t = THEMES[n]; W, H = 1200, 456
    hlop = 1 if n == "light" else .55
    stickers = ""
    for label, pop, rot, cx, cy, tw in STICKERS:
        w = tw + 48
        stickers += f'<g transform="translate({cx} {cy}) rotate({rot})">{nb(t, -w / 2, -32, w, 64, 16, t[pop], 3, 6)}<text x="0" y="10" text-anchor="middle" font-family="{DISPLAY}" font-size="30" font-weight="800" fill="{t["ink"]}" letter-spacing="-.3">{label}</text></g>'
    badge = f"""<g transform="translate(1092 376)"><circle cx="5" cy="5" r="62" fill="{t['line']}"/><circle r="62" fill="{t['yellow']}" stroke="{t['line']}" stroke-width="3"/>
<g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="22s" repeatCount="indefinite"/><path id="cp" d="M-42 0 a42 42 0 1 1 84 0 a42 42 0 1 1 -84 0" fill="none"/>
<text font-family="{MONO}" font-size="12" font-weight="500" fill="{t['ink']}" letter-spacing="3.2"><textPath href="#cp">• SAY HELLO • LET'S TALK • SAY HELLO • LET'S TALK </textPath></text></g>
<path d="M-11 11 L11 -11 M-9 -11 H11 V9" fill="none" stroke="{t['ink']}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></g>"""
    body = f"""<defs><pattern id="grid" width="56" height="56" patternUnits="userSpaceOnUse"><path d="M56 0H0V56" fill="none" stroke="{t['grid']}" stroke-opacity="{t['gridop']}"/></pattern>
<radialGradient id="glow" cx=".25" cy=".35" r=".5"><stop offset="0" stop-color="{t['yellow']}" stop-opacity=".28"/><stop offset="1" stop-color="{t['yellow']}" stop-opacity="0"/></radialGradient>
<clipPath id="c"><rect x="3" y="3" width="{W - 6}" height="{H - 6}" rx="26"/></clipPath></defs>
<rect width="{W}" height="{H}" rx="28" fill="{t['bg']}"/><g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="url(#grid)"/><rect width="{W}" height="{H}" fill="url(#glow)"/></g>
<rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="27" fill="none" stroke="{t['line']}" stroke-width="3"/>
<text x="76" y="86" font-family="{MONO}" font-size="16" font-weight="500" fill="{t['muted']}" letter-spacing="4.5">PHOENIX, AZ</text><rect x="236" y="81" width="250" height="1.6" fill="{t['muted']}" opacity=".6"/>
<text x="72" y="176" font-family="{DISPLAY}" font-size="88" font-weight="800" fill="{t['text']}" letter-spacing="-3">Sakar Joshi</text>
<rect x="{76 + 269}" y="214" width="156" height="13" fill="{t['hl']}" opacity="{hlop}"/><rect x="76" y="250" width="272" height="13" fill="{t['hl']}" opacity="{hlop}"/>
<text x="76" y="238" font-family="{SANS}" font-size="28" fill="{t['text']}">Hi, I'm Sakar. I build <tspan font-weight="600">AI products</tspan> and the</text>
<text x="76" y="274" font-family="{SANS}" font-size="28" fill="{t['text']}"><tspan font-weight="600">cloud data pipelines</tspan> behind them.</text>
{lines(INTRO, 62, 76, 332, 32, font_family=SANS, font_size=22, fill=t['muted'])}
{stickers}{badge}"""
    return svg(W, H, "Sakar Joshi, full-stack software engineer in Phoenix. I build AI products and the cloud data pipelines behind them. At Prama AI I make FinOps for AI real: what teams actually spend on Claude, OpenAI, Gemini and Bedrock. In my own products, the AI proposes and a human decides.", {F_BG, F_I4, F_I6, F_J5}, body)

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
BUTTONS = {"portfolio": ("Portfolio", True), "linkedin": ("LinkedIn", False)}

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

PROJECTS = {
    "monotask": ("01", "Monotask", "Tasks, calendar and habits with Claude-powered capture, as an installable PWA.", "RLS at the database · every AI write is human-approved", ["React", "Supabase", "Claude"], "yellow"),
    "cloudsentry": ("02", "Cloudsentry", "Your AWS account as a live graph, watched by three AI agents.", "The model only records intent · a human approves every action", ["FastAPI", "boto3", "Next.js"], "blue"),
    "resume": ("03", "ResumeBuilder", "ATS-friendly resumes with live preview and AI bullet rewriting.", "Zod-validated output, auto-retry · never invents metrics", ["Next.js", "Supabase", "Groq"], "pink"),
    "portal": ("04", "Employee Portal", "A directory app deployed like a regulated enterprise would.", "Two Vault clusters that unseal each other · no public registries", ["Terraform", "Vault", "FastAPI"], "green"),
}

SHOTS = Path(__file__).resolve().parent / "shots"

def screenshot_frame(t, key, w, h):
    """Real screenshot (committed under .github/scripts/shots) clipped inside the sticker frame; None if missing."""
    f = SHOTS / f"{key}.jpg"
    if not f.exists(): return None
    pad = 10; iw, ih = w - 2 * pad, h - 2 * pad
    data = base64.b64encode(f.read_bytes()).decode()
    return (f'<defs><clipPath id="sc-{key}"><rect x="{pad}" y="{pad}" width="{iw}" height="{ih}" rx="9"/></clipPath></defs>'
            f'<image href="data:image/jpeg;base64,{data}" x="{pad}" y="{pad}" width="{iw}" height="{ih}" preserveAspectRatio="xMidYMid slice" clip-path="url(#sc-{key})"/>'
            f'<rect x="{pad}" y="{pad}" width="{iw}" height="{ih}" rx="9" fill="none" stroke="{t["line"]}" stroke-width="2.5"/>')

def card(key, n):
    t = THEMES[n]; W, H = 760, 452; num, title, desc, proof, tags, pop = PROJECTS[key]
    frame = screenshot_frame(t, key, 236, 160) or ('<g transform="translate(8 6)">' + art(key, t) + '</g>')
    body = nb(t, 4, 4, W - 18, H - 18, 22, t["card"], 3, 9)
    body += nb(t, 38, 36, 60, 60, 12, t[pop], 3, 4) + f'<text x="68" y="76" text-anchor="middle" font-family="{DISPLAY}" font-size="28" font-weight="800" fill="{t["ink"]}">{num}</text>'
    body += f'<g transform="translate(474 40) rotate({2.2 if int(num) % 2 else -2.2} 118 80)">{nb(t, 0, 0, 236, 160, 16, t[pop], 3, 6)}{frame}</g>'
    body += f'<text x="40" y="170" font-family="{DISPLAY}" font-size="52" font-weight="800" fill="{t["text"]}" letter-spacing="-1.5">{escape(title)}</text>'
    body += lines(desc, 50, 40, 250, 34, font_family=SANS, font_size=23, fill=t["text"])
    body += f'<rect x="40" y="304" width="12" height="12" rx="3" fill="{t[pop]}" stroke="{t["line"]}" stroke-width="2.2"/>' + lines(proof, 42, 64, 317, 28, font_family=MONO, font_size=17.5, fill=t["muted"])
    x = 40
    for tag in tags:
        w = len(tag) * 9.9 + 36
        body += f'<rect x="{x}" y="364" width="{w:.0f}" height="42" rx="21" fill="none" stroke="{t["line"]}" stroke-width="2.5"/><text x="{x + w / 2:.0f}" y="391" text-anchor="middle" font-family="{MONO}" font-size="16.5" font-weight="500" fill="{t["text"]}">{escape(tag)}</text>'
        x += w + 10
    cx, cy = W - 78, 386
    body += f'<circle cx="{cx + 4}" cy="{cy + 4}" r="31" fill="{t["line"]}"/><circle cx="{cx}" cy="{cy}" r="31" fill="{t["yellow"]}" stroke="{t["line"]}" stroke-width="3"/><path d="M{cx - 11} {cy + 11} L{cx + 11} {cy - 11} M{cx - 4} {cy - 11} H{cx + 11} V{cy + 4}" fill="none" stroke="{t["ink"]}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(W, H, f"{title}: {desc} {proof}", {F_BG, F_I4, F_J5}, body)

# ------------------------------------------------------------------ wide card: Kramflow
def art_kramflow(t):
    ink, paper = t["ink"], "#FFFDF4"; s = ""
    surfaces = [(18, 22, "Operator console"), (346, 22, "Phone remote"), (18, 214, "Presenter monitor"), (346, 214, "Lobby screen")]
    for x, y, lab in surfaces:
        s += f'<line x1="270" y1="150" x2="{x + 88}" y2="{y + 32}" stroke="{ink}" stroke-width="2.5" stroke-dasharray="6 5"><animate attributeName="stroke-dashoffset" from="0" to="-22" dur="1.6s" repeatCount="indefinite"/></line>'
    s += f'<rect x="188" y="108" width="164" height="84" rx="16" fill="{paper}" stroke="{ink}" stroke-width="3"/>'
    s += f'<rect x="188" y="108" width="164" height="84" rx="16" fill="none" stroke="{ink}" stroke-width="2"><animate attributeName="stroke-opacity" values="1;0" dur="2.2s" repeatCount="indefinite"/><animate attributeName="x" values="188;172" dur="2.2s" repeatCount="indefinite"/><animate attributeName="y" values="108;92" dur="2.2s" repeatCount="indefinite"/><animate attributeName="width" values="164;196" dur="2.2s" repeatCount="indefinite"/><animate attributeName="height" values="84;116" dur="2.2s" repeatCount="indefinite"/></rect>'
    s += f'<text x="270" y="146" text-anchor="middle" font-family="{MONO}" font-size="14" font-weight="500" fill="{ink}" letter-spacing="1.5">SHOW STATE</text><text x="270" y="171" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{ink}" opacity=".7">single source of truth</text>'
    for x, y, lab in surfaces:
        s += f'<rect x="{x}" y="{y}" width="176" height="64" rx="12" fill="{paper}" stroke="{ink}" stroke-width="2.5"/><circle cx="{x + 18}" cy="{y + 32}" r="5" fill="{ink}"/><text x="{x + 32}" y="{y + 37}" font-family="{MONO}" font-size="13" font-weight="500" fill="{ink}">{escape(lab)}</text>'
    return s

def card_wide(n):
    t = THEMES[n]; W, H = 1536, 488; pop = "lilac"
    body = nb(t, 4, 4, W - 18, H - 18, 22, t["card"], 3, 9)
    body += nb(t, 38, 36, 60, 60, 12, t[pop], 3, 4) + f'<text x="68" y="76" text-anchor="middle" font-family="{DISPLAY}" font-size="28" font-weight="800" fill="{t["ink"]}">05</text>'
    body += f'<g transform="translate(900 40) rotate(-1.6 270 150)">{nb(t, 0, 0, 540, 300, 18, t[pop], 3, 6)}{screenshot_frame(t, "kramflow", 540, 300) or art_kramflow(t)}</g>'
    body += f'<text x="40" y="170" font-family="{DISPLAY}" font-size="52" font-weight="800" fill="{t["text"]}" letter-spacing="-1.5">Kramflow</text>'
    body += lines("A multi-tenant live-event operating system: the operator console, phone remote and every display share one real-time state.", 66, 40, 250, 34, font_family=SANS, font_size=23, fill=t["text"])
    body += f'<rect x="40" y="338" width="12" height="12" rx="3" fill="{t[pop]}" stroke="{t["line"]}" stroke-width="2.2"/>' + lines("I own the data layer, reliability and AI: tenant isolation, cold-start-proof rate limiting, lease-gated live sequencing.", 70, 64, 336, 28, font_family=MONO, font_size=17.5, fill=t["muted"])
    x = 40
    for tag in ["Next.js", "Supabase", "Anthropic"]:
        w = len(tag) * 9.9 + 36
        body += f'<rect x="{x}" y="396" width="{w:.0f}" height="42" rx="21" fill="none" stroke="{t["line"]}" stroke-width="2.5"/><text x="{x + w / 2:.0f}" y="423" text-anchor="middle" font-family="{MONO}" font-size="16.5" font-weight="500" fill="{t["text"]}">{escape(tag)}</text>'
        x += w + 10
    cx, cy = W - 78, 386
    body += f'<circle cx="{cx + 4}" cy="{cy + 4}" r="31" fill="{t["line"]}"/><circle cx="{cx}" cy="{cy}" r="31" fill="{t["yellow"]}" stroke="{t["line"]}" stroke-width="3"/><path d="M{cx - 11} {cy + 11} L{cx + 11} {cy - 11} M{cx - 4} {cy - 11} H{cx + 11} V{cy + 4}" fill="none" stroke="{t["ink"]}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(W, H, "Kramflow: a multi-tenant live-event operating system where the operator console, phone remote and every display share one real-time state. I own the data layer, reliability and AI features.", {F_BG, F_I4, F_J5}, body)

# ------------------------------------------------------------------ impact tiles
IMPACT = [("10+", "AI VENDORS TRACKED", "Claude, OpenAI, Gemini, Bedrock, Copilot", "pink"),
          ("5", "CLOUDS INGESTED", "AWS, Azure, Azure China, OCI and Alibaba", "blue"),
          ("20+", "PRS, ONE PATTERN", "Per-provider dashboards on one reusable design", "green"),
          ("12", "FEATURES IN 3 SPRINTS", "A QBE cyber-insurance underwriting portal", "orange")]

def impact(n):
    t = THEMES[n]; W, H = 1000, 230; cw, gap = 226, 22
    body = ""
    for i, (v, lab, cap, pop) in enumerate(IMPACT):
        x = 4 + i * (cw + gap)
        body += nb(t, x, 6, cw, 204, 16, t[pop], 3, 6)
        body += f'<text x="{x + cw / 2}" y="84" text-anchor="middle" font-family="{DISPLAY}" font-size="64" font-weight="800" fill="{t["ink"]}" letter-spacing="-2">{v}</text>'
        body += f'<text x="{x + cw / 2}" y="112" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="500" fill="{t["ink"]}" letter-spacing="1.6">{lab}</text>'
        body += f'<line x1="{x + 40}" y1="130" x2="{x + cw - 40}" y2="130" stroke="{t["ink"]}" stroke-width="2" opacity=".55"/>'
        for j, l in enumerate(textwrap.wrap(cap, 24)[:3]): body += f'<text x="{x + cw / 2}" y="{154 + j * 20}" text-anchor="middle" font-family="{SANS}" font-size="15" fill="{t["ink"]}">{escape(l)}</text>'
    return svg(W, H, "Impact: 10+ AI vendors tracked, 5 clouds ingested, 20+ PRs on one reusable pattern, 12 features shipped in 3 sprints", {F_BG, F_I4, F_J5}, body)

# ------------------------------------------------------------------ experience
EXPERIENCE = [("MAY 2026 – NOW", "Systems & DevOps Engineer", "Prama AI · Finomics, multi-cloud FinOps", "FinOps-for-AI dashboards across 10+ AI vendors. Glue and PySpark pipelines into Iceberg across 5 clouds. Rightsizing with safety guards.", "yellow"),
              ("SEP – DEC 2025", "Frontend Engineer Intern", "XDuce · QBE Insurance", "Built the underwriting submissions inbox: a 180+ record data grid with server-side filtering. 12 features across 3 sprints.", "orange"),
              ("MAY – DEC 2025", "Web Developer", "ASU Project Humanities", "Owned two sites with 5,000+ monthly visitors. WCAG improvements, +31% email opens, +30% referral traffic.", "green"),
              ("SEP 2022 – NOV 2023", "Software Developer", "Macrosoft Creations", "Angular SPAs and .NET REST APIs for two enterprise systems, behind RBAC and ABAC authorization.", "lilac")]

def experience(n):
    t = THEMES[n]; W, rh, gap = 1000, 132, 20; H = len(EXPERIENCE) * (rh + gap) + 4
    body = ""
    for i, (date, role, co, impact_, pop) in enumerate(EXPERIENCE):
        y = 6 + i * (rh + gap)
        body += nb(t, 4, y, W - 16, rh, 18, t["card"], 3, 6)
        dw = len(date) * 8.7 + 26
        body += f'<rect x="30" y="{y + 22}" width="{dw:.0f}" height="30" rx="15" fill="{t[pop]}" stroke="{t["line"]}" stroke-width="2.2"/><text x="{30 + dw / 2:.0f}" y="{y + 42}" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="500" fill="{t["ink"]}" letter-spacing="1.3">{escape(date)}</text>'
        body += f'<text x="30" y="{y + 90}" font-family="{DISPLAY}" font-size="30" font-weight="800" fill="{t["text"]}" letter-spacing="-.8">{escape(role)}</text>'
        body += f'<text x="30" y="{y + 114}" font-family="{SANS}" font-size="16.5" font-weight="600" fill="{t["muted"]}">{escape(co)}</text>'
        body += f'<line x1="470" y1="{y + 24}" x2="470" y2="{y + rh - 24}" stroke="{t["line"]}" stroke-width="2" opacity=".4"/>'
        body += lines(impact_, 52, 496, y + 44, 26, font_family=SANS, font_size=17.5, fill=t["text"])
    return svg(W, H, "Experience: " + "; ".join(f"{r} at {c.split(' · ')[0]}, {d.title()}" for d, r, c, _, _ in EXPERIENCE), {F_BG, F_I4, F_I6, F_J5}, body)

# ------------------------------------------------------------------ capabilities (chips)
CAPS = [("FRONTEND", "blue", ["React", "Next.js", "Angular", "TypeScript", "Tailwind CSS", "Redux Toolkit", "TanStack Query", "Playwright"]),
        ("BACKEND & DATA", "green", ["Python", "FastAPI", "PostgreSQL", "SQL", "Supabase", "Row-Level Security", ".NET (C#)", "REST", "JWT / SSO"]),
        ("DATA & CLOUD", "orange", ["AWS Glue", "PySpark", "Apache Iceberg", "Athena", "AWS", "Azure", "OCI", "Terraform", "Vault", "Docker"]),
        ("APPLIED AI", "pink", ["Anthropic API", "Groq", "Zod-validated output", "Tool-use agents", "Human-in-the-loop", "Prompt evals"])]

def chip_layout(items, maxw):
    rows, x, y = [], 0, 0
    for it in items:
        w = len(it) * 8.6 + 30
        if x + w > maxw and x: x = 0; y += 46
        rows.append((it, x, y, w)); x += w + 10
    return rows, y + 40

def capabilities(n):
    t = THEMES[n]; W, cw, gap, pad = 1000, 484, 22, 28
    lay = [chip_layout(items, cw - 2 * pad)[0:2] for _, _, items in CAPS]
    h1 = 86 + max(lay[0][1], lay[1][1]); h2 = 86 + max(lay[2][1], lay[3][1]); H = h1 + h2 + gap + 16
    body = ""
    for k, (title, pop, items) in enumerate(CAPS):
        col, row = k % 2, k // 2
        x = 4 + col * (cw + gap); y = 6 + (0 if row == 0 else h1 + gap); h = h1 if row == 0 else h2
        body += nb(t, x, y, cw, h, 18, t["card"], 3, 6)
        body += f'<rect x="{x + pad}" y="{y + 26}" width="16" height="16" rx="4" fill="{t[pop]}" stroke="{t["line"]}" stroke-width="2.2"/><text x="{x + pad + 28}" y="{y + 40}" font-family="{MONO}" font-size="14" font-weight="500" fill="{t["text"]}" letter-spacing="3">{escape(title)}</text>'
        for it, cx, cy, w in lay[k][0]:
            body += f'<rect x="{x + pad + cx:.0f}" y="{y + 64 + cy}" width="{w:.0f}" height="38" rx="10" fill="{t["card"]}" stroke="{t["line"]}" stroke-width="1.8"/><text x="{x + pad + cx + w / 2:.0f}" y="{y + 88 + cy}" text-anchor="middle" font-family="{SANS}" font-size="15.5" font-weight="600" fill="{t["text"]}">{escape(it)}</text>'
    return svg(W, H, "Capabilities. Frontend: React, Next.js, Angular, TypeScript. Backend and data: Python, FastAPI, PostgreSQL, Supabase. Data and cloud: AWS Glue, PySpark, Apache Iceberg, Terraform. Applied AI: Anthropic API, Groq, Zod, agents.", {F_I4, F_I6, F_J5}, body)

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
    t = THEMES[n]; W, H = 1000, 130
    body = nb(t, 4, 6, W - 16, 110, 16, t["card"], 3, 6)
    body += f'<text x="28" y="44" font-family="{MONO}" font-size="15" font-weight="500" fill="{t["text"]}" letter-spacing=".4"><tspan fill="{t["muted"]}">GITHUB  </tspan>{d["repos"]} public repos  ·  {d["stars"]} stars  ·  {d["prs"]} merged PRs  ·  {d["contrib"]:,} contributions / 12 mo</text>'
    body += f'<defs><clipPath id="bar"><rect x="28" y="62" width="{W - 60}" height="14" rx="7"/></clipPath></defs><g clip-path="url(#bar)"><rect x="28" y="62" width="{W - 60}" height="14" fill="{t["soft"]}"/>'
    x = 28
    for k, c, f in d["langs"]:
        w = f * (W - 60); body += f'<rect x="{x:.1f}" y="62" width="{w:.1f}" height="14" fill="{c}"/>'; x += w
    body += f'</g><rect x="28" y="62" width="{W - 60}" height="14" rx="7" fill="none" stroke="{t["line"]}" stroke-width="2.5"/>'
    lx = 28
    for k, c, f in d["langs"][:4]:
        lab = f"{k} {f * 100:.0f}%"; body += f'<circle cx="{lx + 5}" cy="102" r="5" fill="{c}" stroke="{t["line"]}" stroke-width="1.5"/><text x="{lx + 16}" y="107" font-family="{MONO}" font-size="12.5" fill="{t["muted"]}">{escape(lab)}</text>'; lx += len(lab) * 7.6 + 38
    body += f'<text x="{W - 28}" y="107" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="{t["muted"]}">public data · updated {datetime.date.today().isoformat()}</text>'
    return svg(W, H, f"GitHub: {d['repos']} public repos, {d['stars']} stars, {d['prs']} merged pull requests, {d['contrib']} contributions in the last year", {F_J5}, body)

def hashify():
    """Give every asset a content-hashed filename and rewrite the README references.

    GitHub's image proxy caches by URL, so a changed image must get a new URL: banner-dark.svg -> banner-dark.1a2b3c4d.svg.
    """
    import hashlib
    keep, names = set(), {}
    for f in sorted(ASSETS.glob("*.svg")):
        if re.search(r"\.[0-9a-f]{8}\.svg$", f.name): continue
        stem = f.stem
        h = hashlib.sha1(f.read_bytes()).hexdigest()[:8]
        target = ASSETS / f"{stem}.{h}.svg"
        f.rename(target); keep.add(target.name); names[stem] = f"{stem}.{h}.svg"
    for f in ASSETS.glob("*.svg"):
        if f.name not in keep: f.unlink()
    readme = ROOT / "README.md"
    if readme.exists():
        txt = readme.read_text(encoding="utf-8")
        def sub(m):
            stem = m.group(1) + m.group(2)
            return f"assets/{names[stem]}" if stem in names else m.group(0)
        txt = re.sub(r"assets/((?:[a-z0-9]+-)+?)(?:\d{8}-)?(dark|light)(?:\.[0-9a-f]{8})?\.svg(?:\?v=\d+)?", sub, txt)
        readme.write_text(txt, encoding="utf-8")

if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for stale in ASSETS.glob("*.svg"): stale.unlink()  # everything is regenerated; nothing stale may survive
    heads = {"work": ("01 / SELECTED WORK", "What I've built"), "experience": ("02 / EXPERIENCE", "Where I've worked"), "capabilities": ("03 / CAPABILITIES", "What I work with"), "github": ("04 / GITHUB", "In numbers")}
    for n in THEMES:
        (ASSETS / f"banner-{n}.svg").write_text(banner(n), encoding="utf-8")
        (ASSETS / f"marquee-{n}.svg").write_text(marquee(n), encoding="utf-8")
        (ASSETS / f"impact-{n}.svg").write_text(impact(n), encoding="utf-8")
        for k in BUTTONS: (ASSETS / f"btn-{k}-{n}.svg").write_text(button(k, n), encoding="utf-8")
        for k, (e, ti) in heads.items(): (ASSETS / f"h-{k}-{n}.svg").write_text(header(n, e, ti), encoding="utf-8")
        for k in PROJECTS: (ASSETS / f"card-{k}-{n}.svg").write_text(card(k, n), encoding="utf-8")
        (ASSETS / "card-kramflow-{}.svg".format(n)).write_text(card_wide(n), encoding="utf-8")
        (ASSETS / f"experience-{n}.svg").write_text(experience(n), encoding="utf-8")
        (ASSETS / f"capabilities-{n}.svg").write_text(capabilities(n), encoding="utf-8")
    d = fetch_stats() if os.environ.get("SKIP_STATS") != "1" else dict(repos=7, stars=4, prs=120, contrib=752, langs=[("TypeScript", "#3178c6", .74), ("JavaScript", "#f1e05a", .09), ("Python", "#3572A5", .08), ("CSS", "#563d7c", .06)])
    for n in THEMES: (ASSETS / f"github-{n}.svg").write_text(github(n, d), encoding="utf-8")
    hashify()
    print("assets:", len(list(ASSETS.glob("*.svg"))), {k: v for k, v in d.items() if k != "langs"})
