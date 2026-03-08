# 2026 AI Coding Tool Dataset Search Results

Search conducted: 2026-03-07

---

## TIER 1: Downloadable Raw Data Available

### 1. AIDev Dataset (HF + GitHub)
- **What:** 932,791 agent-authored PRs across 116,211 repos from 5 AI coding agents (OpenAI Codex, Devin, GitHub Copilot, Cursor, Claude Code), plus 72,189 human developers
- **Curated subset (AIDev-pop):** 33,596 PRs from 2,807 repos with 100+ stars, enriched with comments, reviews, commits, linked issues
- **Agent breakdown:** Codex 814,522 | Copilot 50,447 | Cursor 32,941 | Devin 29,744 | Claude Code 5,137
- **Format:** Parquet (965 MB total), CC-BY-4.0 license
- **Schema (core tables):**
  - `all_pull_request` (933K rows): id, number, title, body, user, state, created_at, closed_at, merged_at, repo_url, agent
  - `all_repository` (116K rows): id, url, full_name, language, license, stars, forks
  - `all_user` (72K rows): id, login, followers, following, created_at
  - `pr_timeline` (326K rows): event history
  - `pr_comments` (39K), `pr_reviews` (29K), `pr_review_comments_v2` (27K)
  - `pr_commits` (89K), `pr_commit_details` (712K): file-level changes (additions, deletions, patch, status)
  - `pr_task_type` (34K): auto-classified PR purpose (Conventional Commits taxonomy)
  - `human_pull_request` (6.6K): comparison baseline
- **Download:** `pip install datasets && datasets.load_dataset("hao-li/AIDev")`
- **HF:** https://huggingface.co/datasets/hao-li/AIDev
- **GitHub replication package:** https://github.com/SAILResearch/AI_Teammates_in_SE3
- **Papers:** arXiv 2507.15003 (Jul 2025), arXiv 2602.09185 (Feb 2026)
- **Recency:** Data collected through late 2025; dataset last modified Feb 2026
- **Usefulness for clustering:** HIGH -- per-PR granularity with agent labels, repo metadata, task types, review outcomes. Could cluster by agent, task type, repo size, merge rate, review friction.

### 2. SWE-bench Family (HF)
- **What:** Benchmark datasets testing AI systems' ability to solve real GitHub issues
- **Variants:**
  - `princeton-nlp/SWE-bench` -- 2,294 Issue-PR pairs from 12 Python repos (600K downloads)
  - `SWE-bench/SWE-bench_Verified` -- 500 human-validated subset (98K downloads)
  - `ScaleAI/SWE-bench_Pro` -- 1,865 problems from 41 repos, 123 languages (80K downloads)
  - `SWE-bench/SWE-smith-py` -- 50,908 synthetic task instances from 131 repos (31K downloads)
  - `SWE-bench-Live/SWE-bench-Live` -- continuously updated (11.5K downloads)
- **Format:** Parquet, MIT license
- **Schema:** Issue descriptions, gold patches, test cases, repo metadata
- **Download:** HuggingFace datasets library
- **Recency:** SWE-bench Pro updated Feb 2026; SWE-smith Dec 2025
- **Usefulness for clustering:** MODERATE -- benchmarks agent capability, not real-world developer usage. No individual developer behavior data. Useful for measuring which tasks AI handles well vs. poorly.

### 3. Stack Overflow Developer Survey 2025
- **What:** Annual developer survey covering tools, AI adoption, demographics, career
- **Sample:** 49,000+ respondents from 177 countries, 62 questions, 314 technologies
- **AI findings:** 84% use AI tools; only 31% use coding agents; 60% positive sentiment (down from 70%+)
- **Format:** Historically CSV (anonymized individual responses). 2025 raw data likely available but exact download URL not confirmed -- check https://survey.stackoverflow.co/2025/ or https://insights.stackoverflow.com/survey
- **Recency:** Published Dec 2025
- **Usefulness for clustering:** HIGH if raw data available -- individual respondent level with tool choices, experience, demographics, satisfaction. Good for developer persona clustering.

### 4. JetBrains Developer Ecosystem Survey 2025
- **What:** Annual developer survey, 500+ questions covering languages, tools, AI, work/life
- **Sample:** 24,534 developers from 194 countries (after cleaning)
- **AI findings:** 85% regularly use AI tools; 62% use at least one AI coding assistant/agent/editor
- **Format:** ZIP download with anonymized responses (format not confirmed, likely CSV)
- **Download:** Available from methodology page at https://lp.jetbrains.com/developer-ecosystem-2025-methedology/
- **AI section:** https://devecosystem-2025.jetbrains.com/artificial-intelligence
- **Recency:** Survey ran Apr-Jun 2025, published Oct 2025
- **Usefulness for clustering:** HIGH -- individual respondent level, broad coverage of AI tool usage alongside language/framework preferences. 500+ columns.

---

## TIER 2: Report Data (Aggregate Stats, Not Per-Developer)

### 5. Anthropic "How AI Is Transforming Work" (Dec 2025)
- **What:** Internal study of AI usage at Anthropic
- **Sample:** 132 engineers/researchers surveyed, 53 in-depth interviews, 200,000 Claude Code transcripts analyzed
- **Key metrics:** Task categories automated (>50% work benefiting from AI), usage patterns by role, qualitative insights
- **Supplementary materials:** Survey questions PDF released for replication. NO raw survey data or transcript data released.
- **URL:** https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic
- **Usefulness for clustering:** LOW -- aggregate findings only. Survey instrument useful for designing your own study.

### 6. METR RCT Study (Jul 2025)
- **What:** Randomized controlled trial -- 16 experienced OSS developers, 246 tasks, AI allowed vs. disallowed
- **Key finding:** AI increased task completion time by 19% (contrary to expectations)
- **Tools used:** Primarily Cursor Pro with Claude 3.5/3.7 Sonnet
- **Data availability:** Paper on arXiv (2507.09089). NO public raw task-level data found. Paper includes "DO NOT TRAIN ON THIS DATA" canary. Appendix D discusses methodology. Screen recordings were collected but not published.
- **URL:** https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
- **Usefulness for clustering:** LOW -- too small (n=16) for clustering. Valuable as a reference point for expert developer behavior.

### 7. Faros AI "AI Productivity Paradox" Report (Jun 2025)
- **What:** Engineering telemetry analysis (not survey) of AI tool impact
- **Sample:** 10,000+ developers across 1,255 enterprise teams
- **Key metrics:** Task completion (+21%), PR merge rate (+98%), PR review time (+91%), code quality indicators
- **Data availability:** GATED behind lead-gen form at https://www.faros.ai/ai-productivity-paradox. Requires business email. Likely contains charts/tables in PDF but no raw data export.
- **Usefulness for clustering:** LOW -- aggregate team-level statistics, not individual developer data.

### 8. DX Q4 2025 AI Impact Report
- **What:** AI coding assistant adoption and impact measurement
- **Sample:** 435 companies, 135,000+ developers (Jul-Oct 2025)
- **Key metrics:** 91% adoption, 22% AI-authored code, time savings, code quality (change failure rate, maintainability)
- **Tools tracked:** GitHub Copilot, Cursor, Claude Code (via system telemetry + self-report)
- **Data availability:** Report freely accessible at https://getdx.com/blog/ai-assisted-engineering-q4-impact-report-2025/. AI Measurement Framework whitepaper may require form. NO raw data download.
- **Usefulness for clustering:** LOW -- aggregate stats across companies. Good for benchmarking but not developer-level clustering.

### 9. GitClear "Comparing Developer AI Use Cohorts" (2026)
- **What:** Correlation analysis of AI tool use vs code quality metrics
- **Sample:** 2,172 developer-weeks; tools tracked: Cursor, GitHub Copilot, Claude Code
- **Key metrics:** Commit count, durable code output, code review time, code churn, code block duplication (7 dimensions)
- **Data availability:** GATED behind form at https://www.gitclear.com/developer_ai_productivity_analysis_tools_research_2026. Previous report (2025): https://gitclear-public.s3.us-west-2.amazonaws.com/AI-Copilot-Code-Quality-2025.pdf
- **Historical context:** 211 million lines analyzed 2020-2024; 4x code cloning increase; code churn projected to double
- **Usefulness for clustering:** MODERATE if you could get per-developer data (unlikely). Published as aggregate cohort comparisons.

### 10. SemiAnalysis "Claude Code Is the Inflection Point" (Feb 2026)
- **What:** Analysis of Claude Code's growth and GitHub commit share
- **Key stats:** 4% of GitHub public commits by Claude Code (Feb 2 2026); projected 20%+ by end of 2026; 42,896x growth in 13 months; 135,000+ commits/day
- **Data availability:** PAYWALLED (SemiAnalysis subscriber newsletter). No methodology published for the 4% figure. No raw data. References internal "SemiAnalysis Tokenomics Model."
- **URL:** https://newsletter.semianalysis.com/p/claude-code-is-the-inflection-point
- **Usefulness for clustering:** NONE -- high-level industry statistics only.

---

## TIER 3: Tools / Infrastructure (No Shared Data, but Useful for Collection)

### 11. ccusage (CLI tool)
- **What:** CLI for analyzing Claude Code usage from local JSONL files (~/.claude/projects/)
- **Metrics:** Daily/monthly token usage, costs, model breakdown, 5-hour block monitoring
- **Data format:** Reads JSONL session logs; outputs terminal tables or JSON
- **Shared data:** NONE -- purely local analysis tool. No centralized data sharing or anonymized aggregate dataset exists.
- **Anonymized data shared by others:** NOT FOUND. No public repos or datasets with ccusage-exported data.
- **URL:** https://github.com/ryoppippi/ccusage
- **Usefulness for clustering:** N/A as data source. USEFUL as a methodology for collecting your own usage data.

### 12. Claude Code Analytics API (Official)
- **What:** Programmatic access to Claude Code team usage for API/Teams/Enterprise customers
- **Metrics:** Sessions, lines added/removed, commits, PRs, acceptance/rejection rates, costs, token usage by model
- **Export:** CSV download of contribution data; API returns JSON
- **Data availability:** Only for your own org's data. No public shared datasets.
- **URL:** https://code.claude.com/docs/en/analytics
- **Usefulness for clustering:** HIGH if you have access to your own org's data. Could cluster developers by usage intensity, acceptance rate, model preference, session patterns.

### 13. Community Claude Code Analytics Tools (GitHub)
- **kanopi/claude-dev-insights** -- Developer analytics with Google Sheets sync (3 hooks)
- **chiphuyen/sniffly** -- Usage dashboard with sharing feature
- **deshraj/Claud-ometer** -- Local-first analytics dashboard
- **aarora79/claude-code-usage-analyzer** -- Cost/token analyzer using ccusage + LiteLLM pricing
- **Maciek-roboblog/Claude-Code-Usage-Monitor** -- Real-time monitoring with ML predictions
- **Shared data from these tools:** NOT FOUND. All local-first, no public aggregated datasets.

---

## TIER 4: Related Papers with Potential Data

### 14. arXiv 2509.14745 -- "On the Use of Agentic Coding" (Watanabe et al.)
- **What:** 567 Claude Code PRs across 157 OSS projects
- **Findings:** 83.8% merged, 54.9% without modification
- **Data availability:** No companion dataset found on arXiv, GitHub, or HF
- **Usefulness:** Small but focused on Claude Code specifically. Could contact authors.

### 15. MSR 2026 Mining Challenge Papers (using AIDev)
Several papers from MSR 2026 (Apr 2026) use the AIDev dataset with replication packages:
- **"How AI Coding Agents Modify Code"** (Ogenrwot & Businge, 2601.17581) -- replication package available
- **"Code Change Characteristics and Description Alignment"** (Pham & Ghaleb, 2601.17627) -- replication at https://github.com/Taher-Ghaleb/AIAgentsAlignment-MSR2026
- **"Security in the Age of AI Teammates"** (2601.00477)
- **"Where Do AI Coding Agents Fail?"** (2601.15195) -- failed agentic PRs analysis

### 16. GitHub Copilot Controlled Experiments
- **Peng et al. (2302.06590):** 95 devs, HTTP server task, 55.8% faster with Copilot
- **MIT field experiment:** 12.9-21.8% more PRs/week at Microsoft, 7.5-8.7% at Accenture
- **ACM ICER 2025:** Students 34.9% faster on brownfield tasks
- **Data availability:** Academic papers; raw data not confirmed public

### 17. GitHub Octoverse 2025
- **What:** Annual report on GitHub platform activity
- **Key stats:** 180M+ developers, TypeScript #1 language (Aug 2025), 80% new devs use Copilot in first week
- **Data availability:** Blog posts with charts. No raw data download.
- **URL:** https://github.blog/news-insights/octoverse/

---

## Summary: Best Bets for a Data-Driven Blog Post

| Dataset | Individual-Level? | Sample Size | Downloadable? | Recency |
|---------|------------------|-------------|---------------|---------|
| **AIDev (HF)** | Per-PR (agent + dev) | 933K PRs, 72K devs | YES (Parquet) | Feb 2026 |
| **SO Survey 2025** | Per-respondent | 49K+ | Likely YES (CSV) | Dec 2025 |
| **JetBrains 2025** | Per-respondent | 24.5K | YES (ZIP) | Oct 2025 |
| **SWE-bench Pro** | Per-task | 1,865 tasks | YES (Parquet) | Feb 2026 |
| DX Q4 Report | Aggregate | 135K devs | Report only | Oct 2025 |
| GitClear 2026 | Aggregate cohorts | 2,172 dev-weeks | Gated PDF | 2026 |
| Faros AI | Aggregate | 10K devs | Gated PDF | Jun 2025 |
| METR RCT | Per-task (small) | 16 devs, 246 tasks | NO | Jul 2025 |
| Anthropic internal | Aggregate | 132 surveyed | NO | Dec 2025 |

### Recommended approach for the blog post:
1. **AIDev** is the clear winner -- massive, granular, freely downloadable, covers Claude Code specifically. Filter to Claude Code's 5,137 PRs for focused analysis, or compare across all 5 agents.
2. **Stack Overflow + JetBrains surveys** for developer demographics and AI tool sentiment (if raw data confirmed available).
3. **SWE-bench** for benchmarking which task types AI handles well.
4. **Aggregate reports** (DX, GitClear, Faros, METR, Anthropic) as narrative context and cited statistics -- not for original analysis.
5. **Claude Code Analytics API** if you want to share your own usage data as a case study.
