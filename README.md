<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="Sakar Joshi: Software Engineer, full-stack, cloud data and applied AI" src="assets/banner-light.svg" width="100%">
</picture>

[**LinkedIn**](https://www.linkedin.com/in/sakar-joshi/) &nbsp;·&nbsp; [**Portfolio**](https://sakar-portfolio-pearl.vercel.app) &nbsp;·&nbsp; [**Monotask**](https://monotask.vercel.app) &nbsp;·&nbsp; [**Kramflow**](https://kramflow.me) &nbsp;·&nbsp; [**Cloudsentry**](https://sakar1601.github.io/cloudsentry/)

</div>

&nbsp;

## About

I'm a full-stack engineer who likes to own the whole vertical slice: the data pipeline underneath, the logic in the middle, and the interface people actually touch.

**AI is the through-line.** At **Prama AI** I work on the FinOps-for-AI layer of *Finomics*, the part that shows companies what they really spend on Claude, OpenAI, Gemini, Bedrock and Copilot. In my own products I ship real runtime LLM features: schema-constrained extraction, tool-using agents, and a human approval gate before anything is written or executed.

<table>
<tr>
<td width="33%" valign="top">

**Applied AI**<br>
Structured output validated with Zod, anti-hallucination prompting, per-user quotas, and human review on every write.

</td>
<td width="33%" valign="top">

**Data and cloud**<br>
AWS Glue, PySpark and Apache Iceberg pipelines across AWS, Azure, OCI and Alibaba Cloud, with idempotent loads.

</td>
<td width="33%" valign="top">

**Full-stack products**<br>
React, Next.js and TypeScript on Supabase, with security enforced at the database layer (Row-Level Security).

</td>
</tr>
</table>

&nbsp;

## Featured projects

<table>
<tr>
<td width="50%" valign="top">

<a href="https://monotask.vercel.app"><img src="https://raw.githubusercontent.com/Sakar1601/Monotask/main/docs/screenshots/dashboard.png" alt="Monotask dashboard" width="100%"></a>

**[Monotask](https://github.com/Sakar1601/Monotask)**<br>
Tasks, calendar, habits and analytics in a minimal monochrome PWA. Claude turns plain English into structured tasks, and every AI suggestion is schema-validated and human-approved before it is written. Two-way Google and Outlook sync.

`React` `Supabase` `RLS` `Claude` `Edge Functions` `PWA`<br>
[Live](https://monotask.vercel.app) · [Code](https://github.com/Sakar1601/Monotask)

</td>
<td width="50%" valign="top">

<a href="https://sakar1601.github.io/cloudsentry/"><img src="https://raw.githubusercontent.com/Sakar1601/cloudsentry/main/docs/images/banner.png" alt="Cloudsentry" width="100%"></a>

**[Cloudsentry](https://github.com/Sakar1601/cloudsentry)**<br>
A real AWS account drawn as a live graph and watched by three Claude agents (cost, performance, security). The model can only record intent: a human approves before anything runs, and proposals are validated twice.

`FastAPI` `boto3` `Anthropic tool use` `Next.js` `Terraform`<br>
[Live demo](https://sakar1601.github.io/cloudsentry/) · [Code](https://github.com/Sakar1601/cloudsentry)

</td>
</tr>
<tr>
<td width="50%" valign="top">

<a href="https://github.com/Sakar1601/resume-builder-app"><img src="https://raw.githubusercontent.com/Sakar1601/resume-builder-app/main/docs/screenshots/editor.png" alt="ResumeBuilder editor with live preview" width="100%"></a>

**[ResumeBuilder](https://github.com/Sakar1601/resume-builder-app)**<br>
ATS-friendly resume builder with live preview. AI rewrites bullets or tailors a whole resume to a job description, using Zod-validated output with an automatic retry and prompts that never invent metrics.

`Next.js` `Supabase` `Groq` `Zod` `Playwright`<br>
[Live](https://resume-builder-app-phi.vercel.app) · [Code](https://github.com/Sakar1601/resume-builder-app)

</td>
<td width="50%" valign="top">

<a href="https://sakar1601.github.io/internal-employee-portal/"><img src="https://raw.githubusercontent.com/Sakar1601/internal-employee-portal/main/docs/images/banner.png" alt="Employee Portal" width="100%"></a>

**[Internal Employee Portal](https://github.com/Sakar1601/internal-employee-portal)**<br>
A small directory app deployed the way a regulated, network-isolated company would: Terraform, two HashiCorp Vault clusters that unseal each other, Ansible and AWX, with no public registries.

`Terraform` `Vault` `Ansible` `AWX` `FastAPI` `React`<br>
[Live demo](https://sakar1601.github.io/internal-employee-portal/) · [Code](https://github.com/Sakar1601/internal-employee-portal)

</td>
</tr>
</table>

**[Kramflow](https://kramflow.me)** · a multi-tenant live-event operating system where the operator console, phone remote and every display surface share one real-time state. I own the data layer, reliability and AI features: tenant isolation fixes, a rate limiter that survives serverless cold starts, lease-gated live sequencing, and human-reviewed Claude features. ([Code](https://github.com/Workflow-bench/kramflow))

&nbsp;

## Experience

<details open>
<summary><b>Systems & DevOps Engineer</b> · Prama AI &nbsp;<sub>May 2026 – present · Phoenix, AZ (remote)</sub></summary>
<br>

On **Finomics**, a multi-cloud FinOps platform whose flagship is FinOps for AI.

- Built React/TypeScript dashboards tracking AI-tool and SaaS spend across **10+ AI/LLM vendors** with org, team and member drill-down, delivered in 20+ pull requests on one reusable per-provider pattern.
- Built AWS Glue/PySpark to Iceberg pipelines that ingest vendor usage and cost data across **AWS, Azure, Azure China, OCI and Alibaba Cloud**, with MERGE INTO upserts so re-runs stay idempotent.
- Built threshold-driven rightsizing and idle-resource recommendations with live SKU pricing and annualized savings, hardened with multi-metric safety guards, a 50%-per-cycle downsizing cap and peak-utilization gating.
- Found and fixed silent data-loss bugs after live runs, and moved core metrics to 5-minute resolution with peak (max) utilization alongside the mean.

</details>

<details>
<summary><b>Frontend Engineer Intern</b> · XDuce <sub>(client: QBE Insurance)</sub> &nbsp;<sub>Sep – Dec 2025 · Remote</sub></summary>
<br>

- Built the All Submissions inbox of a cyber-insurance underwriting portal: a sortable, filterable data grid (180+ records per view) with server-side pagination and debounced search.
- Implemented predictable AND-semantics filtering across tabs, search, column filters and a My/All toggle, plus lifecycle-driven Active/Reviewed tabs with Red/Amber/Green risk indicators.
- Shipped **12 production features across 3 sprints** against JIRA user stories.

</details>

<details>
<summary><b>Web Developer</b> · ASU Project Humanities &nbsp;<sub>May – Dec 2025 · Tempe, AZ</sub></summary>
<br>

- Owned the web presence of two ASU platforms serving **5,000+ monthly visitors**, improving accessibility (WCAG) and information architecture across 10+ pages.
- Direct traffic grew **12%**, referral traffic **30%**, pledge-page engagement **20%**, and email open rates **31%** through GA4, Salesforce and Mailchimp workflows.

</details>

<details>
<summary><b>Software Developer</b> · Macrosoft Creations &nbsp;<sub>Sep 2022 – Nov 2023 · Gandhinagar, India</sub></summary>
<br>

- Built Angular SPA features and **.NET (C#) REST APIs** for two enterprise systems (Event Management and Personnel Care) behind an RBAC/ABAC authorization model.
- Delivered multi-step reactive forms, dashboards, QR/ID scanning, webcam attendance, and client-side Excel/PDF reporting, backed by SQL for filtering, pagination and exports.

</details>

&nbsp;

## Toolbox

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/skills-dark.svg">
  <img alt="Skills and tools: TypeScript, React, Next.js, Python, Supabase, PostgreSQL, AWS, Terraform, Anthropic API and more" src="assets/skills-light.svg" width="100%">
</picture>

&nbsp;

## GitHub, by the numbers

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stats-dark.svg">
  <img alt="GitHub statistics: public repositories, stars, merged pull requests and contributions, with top languages" src="assets/stats-light.svg" width="100%">
</picture>

&nbsp;

## Education

**M.S., Information Technology** · Arizona State University, Tempe, AZ &nbsp;<sub>2024 – 2025</sub><br>
**B.E., Computer Engineering** · Kadi Sarva Vishwavidyalaya, Gandhinagar, India &nbsp;<sub>2019 – 2023</sub>

&nbsp;

## Say hello

I'm happy to talk about FinOps for AI, LLM features that keep a human in the loop, or data pipelines across clouds.
Reach me on [LinkedIn](https://www.linkedin.com/in/sakar-joshi/).

<sub>The banner, toolbox and stats above are SVGs generated by [`.github/scripts/generate.py`](.github/scripts/generate.py), and the stats refresh daily through a [GitHub Action](.github/workflows/profile-assets.yml). Fonts: Space Grotesk, Inter and JetBrains Mono.</sub>
