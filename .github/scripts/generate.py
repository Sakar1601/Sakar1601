#!/usr/bin/env python3
"""Generates the SVG assets used by README.md.

banner + skills are static (edit the data below); the stats card is rebuilt from the GitHub API.
Fonts are embedded as base64 so the SVGs render with the same typography inside <img> tags on GitHub.
Run locally:  GH_TOKEN=$(gh auth token) python3 .github/scripts/generate.py
"""
import base64, datetime, json, os, subprocess, textwrap
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"
FONTS = Path(__file__).resolve().parent / "fonts"
LOGIN = "Sakar1601"
# Legacy uploads that would skew the language bar.
EXCLUDE_LANGS_FROM = {"College-management-system"}

THEMES = {
    "dark": dict(bg1="#0A0F1E", bg2="#131B35", text="#F8FAFC", muted="#94A3B8", a1="#38BDF8", a2="#818CF8", a3="#F472B6",
                 grid="#94A3B8", gridop=".07", card="#0F172A", border="#334155", chip="#1E293B", name1="#F8FAFC", name2="#7DD3FC"),
    "light": dict(bg1="#F8FAFC", bg2="#EEF2FF", text="#0F172A", muted="#475569", a1="#0284C7", a2="#4F46E5", a3="#DB2777",
                  grid="#64748B", gridop=".10", card="#FFFFFF", border="#CBD5E1", chip="#F1F5F9", name1="#0F172A", name2="#4338CA"),
}

def font_css(use):
    def b64(f): return base64.b64encode((FONTS / f).read_bytes()).decode()
    faces = [("Space Grotesk", 700, "space-grotesk-700.woff2"), ("Inter", 400, "inter-400.woff2"), ("Inter", 600, "inter-600.woff2"),
             ("JetBrains Mono", 400, "jetbrains-mono-400.woff2"), ("JetBrains Mono", 500, "jetbrains-mono-500.woff2")]
    return "".join(f"@font-face{{font-family:'{n}';font-weight:{w};src:url(data:font/woff2;base64,{b64(f)}) format('woff2');}}" for n, w, f in faces if f in use)

SANS = "Inter,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
DISPLAY = "'Space Grotesk',Inter,-apple-system,'Segoe UI',sans-serif"
MONO = "'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace"

def svg_open(w, h, label, t, use):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">'
            f'<style>{font_css(use)}</style>')

# ---------------------------------------------------------------- banner
ROLES = ["FinOps for AI  @ Prama", "AI products with a human in the loop", "Multi-cloud data pipelines"]

def banner(name):
    t = THEMES[name]; W, H = 1280, 360
    s = svg_open(W, H, "Sakar Joshi: Software Engineer, full-stack and cloud data", t, {"space-grotesk-700.woff2", "jetbrains-mono-400.woff2", "jetbrains-mono-500.woff2"})
    s += f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
<linearGradient id="nm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t['name1']}"/><stop offset="1" stop-color="{t['name2']}"/></linearGradient>
<linearGradient id="ac" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t['a1']}"/><stop offset=".55" stop-color="{t['a2']}"/><stop offset="1" stop-color="{t['a3']}"/></linearGradient>
<pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse"><path d="M44 0H0V44" fill="none" stroke="{t['grid']}" stroke-opacity="{t['gridop']}"/></pattern>
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="55"/></filter>
<clipPath id="r"><rect width="{W}" height="{H}" rx="24"/></clipPath></defs>
<g clip-path="url(#r)"><rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#grid)"/>
<circle cx="1040" cy="70" r="170" fill="{t['a2']}" opacity=".38" filter="url(#blur)"><animateTransform attributeName="transform" type="translate" values="0 0;-50 34;0 0" dur="14s" repeatCount="indefinite"/></circle>
<circle cx="170" cy="340" r="150" fill="{t['a1']}" opacity=".30" filter="url(#blur)"><animateTransform attributeName="transform" type="translate" values="0 0;60 -30;0 0" dur="17s" repeatCount="indefinite"/></circle>
<circle cx="760" cy="360" r="110" fill="{t['a3']}" opacity=".18" filter="url(#blur)"><animateTransform attributeName="transform" type="translate" values="0 0;-30 -24;0 0" dur="19s" repeatCount="indefinite"/></circle>
<rect x="80" y="62" width="72" height="5" rx="2.5" fill="url(#ac)"/>
<text x="80" y="108" font-family="{MONO}" font-size="17" fill="{t['muted']}" letter-spacing="1">~/sakar-joshi</text>
<rect x="{80 + 13 * 11.2 + 8:.0f}" y="94" width="9" height="18" fill="{t['a1']}"><animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;.5;.5;.99;1" dur="1.1s" repeatCount="indefinite"/></rect>
<text x="76" y="192" font-family="{DISPLAY}" font-size="86" font-weight="700" fill="url(#nm)" letter-spacing="-2">Sakar Joshi</text>
<text x="80" y="238" font-family="{MONO}" font-size="24" font-weight="500" fill="{t['muted']}">Software Engineer <tspan fill="{t['a2']}">·</tspan> full-stack <tspan fill="{t['a2']}">·</tspan> cloud data <tspan fill="{t['a2']}">·</tspan> applied AI</text>'''
    n = len(ROLES)
    for i, r in enumerate(ROLES):
        st, en = i / n, (i + 1) / n
        pts = [(0, 1 if i == 0 else 0)]
        if i: pts += [(st, 0), (st + .02, 1)]
        pts += [(en - .02, 1), (en, 0)] if i < n - 1 else [(1, 1)]
        if i < n - 1: pts.append((1, 0))
        kt = ";".join(f"{p[0]:.3f}" for p in pts); vals = ";".join(str(p[1]) for p in pts)
        s += f'<text x="80" y="282" font-family="{MONO}" font-size="22" fill="{t["a1"]}" opacity="{1 if i == 0 else 0}"><tspan fill="{t["muted"]}">&gt; </tspan>{escape(r)}<animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="12s" repeatCount="indefinite"/></text>'
    x = 80
    for label in ["Phoenix, AZ", "Prama AI", "M.S. IT · ASU"]:
        w = len(label) * 9.6 + 34
        s += f'<rect x="{x}" y="304" width="{w:.0f}" height="34" rx="17" fill="{t["chip"]}" fill-opacity=".7" stroke="{t["border"]}"/><text x="{x + w / 2:.0f}" y="326" text-anchor="middle" font-family="{MONO}" font-size="16" fill="{t["text"]}">{escape(label)}</text>'
        x += w + 12
    s += '</g></svg>\n'
    return s

# ---------------------------------------------------------------- skills
SKILLS = [
    ("Languages", ["TypeScript", "JavaScript", "Python", "SQL"]),
    ("Frontend", ["React", "Next.js", "Angular", "Redux Toolkit", "TanStack Query", "Tailwind CSS", "shadcn/ui", "Framer Motion", "Vite"]),
    ("Backend & data", ["Supabase", "PostgreSQL", "Row-Level Security", "FastAPI", "Node.js", ".NET (C#)", "REST", "JWT / SSO"]),
    ("Data engineering & FinOps", ["AWS Glue", "PySpark", "Apache Iceberg", "Athena", "Medallion architecture", "FOCUS billing model"]),
    ("Cloud & DevOps", ["AWS", "Azure", "Oracle Cloud", "Alibaba Cloud", "Terraform", "HashiCorp Vault", "Ansible", "Docker", "GitHub Actions", "Vercel"]),
    ("AI / LLM", ["Anthropic API", "Groq", "Structured output + Zod", "Tool-use agents", "Human-in-the-loop", "Prompt evals"]),
    ("Quality", ["Vitest", "Playwright", "pytest", "CodeQL", "Dependabot"]),
    ("AI-assisted dev", ["Claude Code", "GitHub Copilot", "Cursor", "Kiro"]),
]

def skills(name):
    t = THEMES[name]; W, pad, maxw, ch, gap, fs = 1000, 40, 920, 34, 10, 14
    cw = fs * 0.6
    y = 44; body = ""
    palette = [t["a1"], t["a2"], t["a3"]]
    for gi, (label, items) in enumerate(SKILLS):
        col = palette[gi % 3]
        body += f'<circle cx="{pad + 4}" cy="{y - 4}" r="4" fill="{col}"/><text x="{pad + 18}" y="{y}" font-family="{MONO}" font-size="13" font-weight="500" fill="{t["muted"]}" letter-spacing="1.5">{escape(label.upper())}</text>'
        y += 16; x = pad
        for it in items:
            w = len(it) * cw + 30
            if x + w > pad + maxw: x = pad; y += ch + gap
            body += f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{ch}" rx="10" fill="{t["chip"]}" stroke="{t["border"]}"/><text x="{x + w / 2:.0f}" y="{y + 22}" text-anchor="middle" font-family="{MONO}" font-size="{fs}" fill="{t["text"]}">{escape(it)}</text>'
            x += w + gap
        y += ch + 30
    H = y - 6
    s = svg_open(W, H, "Skills and tools", t, {"jetbrains-mono-400.woff2", "jetbrains-mono-500.woff2"})
    s += f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="22" fill="{t["card"]}" stroke="{t["border"]}"/>' + body + '</svg>\n'
    return s

# ---------------------------------------------------------------- stats (live)
QUERY = """query($login:String!){user(login:$login){
 followers{totalCount}
 pullRequests(states:MERGED){totalCount}
 repositories(privacy:PUBLIC,ownerAffiliations:OWNER,isFork:false,first:100){totalCount nodes{name stargazerCount languages(first:8,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}
 contributionsCollection{contributionCalendar{totalContributions}}}}"""

def fetch_stats():
    out = subprocess.run(["gh", "api", "graphql", "-f", f"query={QUERY}", "-F", f"login={LOGIN}"], capture_output=True, text=True, check=True).stdout
    u = json.loads(out)["data"]["user"]
    repos = u["repositories"]["nodes"]; langs = {}
    for r in repos:
        if r["name"] in EXCLUDE_LANGS_FROM: continue
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]; langs.setdefault(n, [0, e["node"]["color"] or "#8B949E"]); langs[n][0] += e["size"]
    tot = sum(v[0] for v in langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1][0])[:6]
    return dict(repos=u["repositories"]["totalCount"], stars=sum(r["stargazerCount"] for r in repos), prs=u["pullRequests"]["totalCount"],
                contrib=u["contributionsCollection"]["contributionCalendar"]["totalContributions"],
                langs=[(n, c, v / tot) for n, (v, c) in top])

def stats(name, d):
    t = THEMES[name]; W, H, pad = 1000, 270, 40
    s = svg_open(W, H, "GitHub activity", t, {"space-grotesk-700.woff2", "inter-400.woff2", "jetbrains-mono-400.woff2", "jetbrains-mono-500.woff2"})
    s += f'<defs><clipPath id="bar"><rect x="{pad}" y="168" width="{W - 2 * pad}" height="12" rx="6"/></clipPath></defs><rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="22" fill="{t["card"]}" stroke="{t["border"]}"/>'
    cols = [("Public repos", d["repos"], t["a1"]), ("Stars earned", d["stars"], t["a2"]), ("Merged pull requests", d["prs"], t["a3"]), ("Contributions, last year", d["contrib"], t["a1"])]
    cw = (W - 2 * pad) / 4
    for i, (lab, val, col) in enumerate(cols):
        x = pad + i * cw
        s += f'<text x="{x:.0f}" y="84" font-family="{DISPLAY}" font-size="46" font-weight="700" fill="{col}">{val:,}</text><text x="{x:.0f}" y="112" font-family="{SANS}" font-size="14" fill="{t["muted"]}">{escape(lab)}</text>'
    s += f'<text x="{pad}" y="152" font-family="{MONO}" font-size="12" font-weight="500" fill="{t["muted"]}" letter-spacing="1.5">TOP LANGUAGES · PUBLIC REPOS</text><g clip-path="url(#bar)"><rect x="{pad}" y="168" width="{W - 2 * pad}" height="12" fill="{t["chip"]}"/>'
    x = pad
    for n, c, f in d["langs"]:
        w = f * (W - 2 * pad); s += f'<rect x="{x:.1f}" y="168" width="{w:.1f}" height="12" fill="{c}"/>'; x += w
    s += '</g>'
    lx = pad
    for n, c, f in d["langs"]:
        label = f"{n} {f * 100:.1f}%"; w = len(label) * 7.9 + 34
        s += f'<circle cx="{lx + 6}" cy="208" r="5" fill="{c}"/><text x="{lx + 18}" y="212" font-family="{MONO}" font-size="13" fill="{t["text"]}">{escape(label)}</text>'
        lx += w
    s += f'<text x="{W - pad}" y="248" text-anchor="end" font-family="{MONO}" font-size="11" fill="{t["muted"]}">updated {datetime.date.today().isoformat()} · generated from the GitHub API</text></svg>\n'
    return s

if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for n in THEMES:
        (ASSETS / f"banner-{n}.svg").write_text(banner(n), encoding="utf-8")
        (ASSETS / f"skills-{n}.svg").write_text(skills(n), encoding="utf-8")
    if os.environ.get("SKIP_STATS") != "1":
        d = fetch_stats()
        for n in THEMES: (ASSETS / f"stats-{n}.svg").write_text(stats(n, d), encoding="utf-8")
        print("stats:", {k: v for k, v in d.items() if k != "langs"}, [(n, round(f * 100, 1)) for n, c, f in d["langs"]])
    print("assets written:", sorted(p.name for p in ASSETS.glob("*.svg")))
