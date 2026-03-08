# JetBrains Developer Ecosystem 2025 -- AI Column Exploration

**Data source:** https://resources.jetbrains.com/storage/products/research/DevEco2025/RawData.zip
**Survey period:** April--June 2025
**License:** See LICENSE.txt in ZIP

## Overview

- **Total respondents:** 24,534
- **Total columns:** 4,740 (wide format, one-hot encoded multi-select)
- **AI-specific question groups:** 43 (528 columns)
- **Data format:** CSV (202 MB wide, plus narrow format ZIP)
- **Files in download:** wide CSV, narrow CSV (zipped), questions metadata CSV, survey logic PDF, README, LICENSE

## Column Encoding

Multi-select questions use one column per option. Selected = option text repeated as value; not selected = empty string. Single-select and Likert questions use a single column with the response text as value. Empty/NA indicates the question was not shown to that respondent (survey logic branching).

## AI Question Groups (43 groups, 528 columns)

### Tool Adoption & Usage

| Group | Columns | Description |
|-------|---------|-------------|
| `usage_ai_coding` | 46 | Which AI tools do you regularly use? (multi-select) |
| `ai_models_copilot` | 30 | LLMs used in GitHub Copilot |
| `ai_models_cursor` | 28 | LLMs used in Cursor |
| `ai_models_jb_ai` | 28 | LLMs used in JetBrains AI Assistant |
| `ai_models_windsurf` | 15 | LLMs used in Windsurf |
| `ai_models_windsurf_plugin` | 11 | LLMs used in Windsurf Plugin |
| `ai_models_tabnine` | 3 | LLMs used in Tabnine |
| `ai_llms_use_coding_at_work` | 31 | LLMs used via provider websites/apps/APIs for coding at work |
| `ai_access_how` | 28 | How do you access these LLMs? (API, app, website, self-hosted, etc.) |
| `best_ai_llm_for_coding` | 1 | Best LLM for coding (single-select) |

### Attitudes & Sentiment

| Group | Columns | Description |
|-------|---------|-------------|
| `ai_agents_try` | 1 | Likelihood of trying AI coding agents in next 12 months |
| `ai_agents_company_try` | 1 | Company likelihood of trying AI coding agents |
| `ai_agents_company_why_not` | 12 | Why company unlikely to try agents |
| `ai_third_party_policy` | 1 | Company policy on USE of third-party AI tools |
| `ai_third_party_policy_access` | 1 | Company policy on ACCESS to third-party AI tools |
| `ai_prevent_use` | 18 | What prevents you from using AI tools? |
| `ai_consider_future` | 17 | What would make you consider AI tools in future? |
| `concerns_ai_coding` | 1 | Biggest concern about AI in coding |
| `emotions_about_ai_society` | 1 | Feeling about AI's role in society |
| `creativity_changed_since_ai` | 1 | How has creativity changed since AI adoption? |
| `trust_ai_decisions_perslife` | 1 | Trust AI for personal life decisions (1--5 scale) |
| `trust_ai_courts_in_country` | 1 | Trust AI to replace courts? |
| `ethical_concerns_ai` | 9 | Most important ethical concerns about AI |

### Usage Patterns & Behaviors

| Group | Columns | Description |
|-------|---------|-------------|
| `ai_coding_tasks_freq` | 25 | How often do you use AI for each task? (6-point frequency scale) |
| `ai_coding_aspects_imp` | 16 | Importance of AI tool aspects (4-point Likert) |
| `ai_benefits` | 10 | Benefits from AI tools (multi-select) |
| `ai_time_saving` | 1 | Hours saved per week |
| `ai_coding_delegate` | 24 | Would you delegate this task to AI? (3-point: delegate/unsure/myself) |
| `areas_want_ai_assist` | 37 | Where do you want AI assistance? (multi-select) |
| `ai_non_code_related_usage` | 12 | Non-code AI agents used at work |
| `ai_agents_areas` | 16 | Work areas where AI agents are used |
| `media_ai_news` | 26 | Information sources for AI coding news |

### Future & Speculation

| Group | Columns | Description |
|-------|---------|-------------|
| `expect_coding_change_due_ai` | 14 | Expected workflow changes in 1--3 years |
| `ai_coding_statements_future` | 7 | Agreement with future statements (Agree/Disagree/Neutral) |
| `ai_bci_when` | 1 | When will brain-computer coding be possible? |
| `ai_agi_when` | 1 | When will AGI arrive? |
| `ai_agi_outcome` | 1 | Most likely outcome of AGI |

### Organization-Level

| Group | Columns | Description |
|-------|---------|-------------|
| `ai_types_tools` | 8 | Types of AI tools used in organization |
| `ai_no_usage_reasons` | 15 | Why org doesn't use AI tools |
| `percent_devs_use_ai_in_company` | 1 | % of devs using AI in company |
| `level_ai_adoption_in_company` | 1 | Company AI adoption stage |
| `devareas_ai_used_in_company` | 19 | Dev cycle areas where company uses AI |
| `org_use_ai_china` | 1 | Access to AI tools not available in Mainland China |
| `ai_llms_company_use_china` | 6 | AI/LLM tools used by org (China-specific) |

## Key Distributions

### AI Tool Adoption (usage_ai_coding, N=22,156 who answered)

| Tool | Count | % of All |
|------|-------|----------|
| ChatGPT (web/desktop/mobile) | 10,255 | 41.8% |
| GitHub Copilot | 7,605 | 31.0% |
| JetBrains AI Assistant | 4,036 | 16.5% |
| Cursor | 2,469 | 10.1% |
| None | 2,368 | 9.7% |
| Claude (web/desktop/mobile) | 2,199 | 9.0% |
| Google Gemini (web/mobile) | 2,100 | 8.6% |
| JetBrains Junie | 1,578 | 6.4% |
| DeepSeek (apps/self-hosted) | 1,472 | 6.0% |
| Claude Code | 1,029 | 4.2% |
| Perplexity | 766 | 3.1% |
| VS IntelliCode | 744 | 3.0% |
| Microsoft 365 Copilot | 669 | 2.7% |
| Windsurf | 540 | 2.2% |
| Cline | 250 | 1.0% |
| Aider | 93 | 0.4% |

### Best LLM for Coding (single-select, among 10,170 who answered)

| Model | Count | % of Respondents |
|-------|-------|-----------------|
| Claude 3.7 Sonnet | 1,070 | 10.5% |
| GPT-4o | 772 | 7.6% |
| GPT-4.1 | 768 | 7.6% |
| GPT-4.5 | 735 | 7.2% |
| Gemini 2.5 Pro | 725 | 7.1% |
| Claude 3.7 Sonnet Thinking | 625 | 6.1% |
| Claude 4 Sonnet | 464 | 4.6% |
| o4-mini | 460 | 4.5% |
| DeepSeek R1 | 331 | 3.3% |
| I don't know | 2,430 | 23.9% |

### AI Agent Adoption Intent

| Response | Count | % |
|----------|-------|---|
| Very likely | 10,947 | 44.6% |
| Somewhat likely | 4,979 | 20.3% |
| I already use AI coding agents | 2,229 | 9.1% |
| Not sure | 2,406 | 9.8% |
| Somewhat unlikely | 1,119 | 4.6% |
| Very unlikely | 1,670 | 6.8% |

### Time Saved Per Week (among 4,224 who answered)

| Range | Count | % of Respondents |
|-------|-------|-----------------|
| 2--4 hours | 1,296 | 30.7% |
| 1--2 hours | 887 | 21.0% |
| 4--8 hours | 831 | 19.7% |
| 8+ hours | 694 | 16.4% |
| Less than 1 hour | 346 | 8.2% |
| No time saved | 170 | 4.0% |

### Emotions About AI in Society (among 7,437 who answered)

| Emotion | Count | % |
|---------|-------|---|
| Hopeful | 1,880 | 25.3% |
| Uncertain | 1,613 | 21.7% |
| Excited | 1,364 | 18.3% |
| Anxious | 1,315 | 17.7% |
| Fearful | 575 | 7.7% |
| Indifferent | 448 | 6.0% |

### Creativity Change Since AI (among 7,437 who answered)

| Response | Count | % |
|----------|-------|---|
| No change | 2,547 | 34.2% |
| Somewhat more creative | 2,115 | 28.4% |
| Much more creative | 1,236 | 16.6% |
| Somewhat less creative | 757 | 10.2% |
| Haven't adopted AI | 633 | 8.5% |
| Much less creative | 149 | 2.0% |

### AGI Timeline (among 7,596 who answered)

| Response | Count | % |
|----------|-------|---|
| 5--10 years | 1,969 | 25.9% |
| 10--20 years | 1,666 | 21.9% |
| 20--50 years | 1,205 | 15.9% |
| Never | 963 | 12.7% |
| 1--3 years | 689 | 9.1% |
| 50--100 years | 603 | 7.9% |
| 100+ years | 415 | 5.5% |
| Less than 1 year | 86 | 1.1% |

## Demographic Context

- **Top languages:** Java (20.4%), Python (18.3%), C# (11.2%), TypeScript (10.1%), PHP (7.0%)
- **Employment:** 62.7% full-time, 11.0% students, 10.4% self-employed
- **AI/ML involvement:** 17.2% work on "AI and AI tools", 19.1% do "AI engineering", 12.9% do "Machine learning"
- **Company size:** 20.2% at 51--500, 12.7% at 5,000+, 14.1% at 11--50

## Clustering Potential Assessment

### High-value columns for clustering AI developer archetypes:

1. **Tool portfolio** (`usage_ai_coding`): 46 binary features. Can derive: total tools used, tool category mix (IDE-integrated vs chat-based vs agentic vs self-hosted).
2. **Task frequency** (`ai_coding_tasks_freq`): 25 ordinal features (Never through Every day). Rich behavioral signal -- who uses AI for code completion vs agentic dev vs docs vs debugging.
3. **Delegation willingness** (`ai_coding_delegate`): 24 three-level features. Captures trust/autonomy spectrum.
4. **Importance weights** (`ai_coding_aspects_imp`): 16 four-level Likert features. Reveals what matters: quality vs speed vs price vs privacy.
5. **Sentiment** (`emotions_about_ai_society`, `creativity_changed_since_ai`, `ai_agi_outcome`, `trust_ai_decisions_perslife`): Psychological profile.
6. **Agent adoption intent** (`ai_agents_try`): Clean ordinal signal.
7. **LLM preferences** (`best_ai_llm_for_coding`, `ai_models_*`): Model loyalty patterns.
8. **Benefits perceived** (`ai_benefits`): 10 binary features.

### Recommended clustering approach:

- **Feature engineering:** Combine tool counts + task frequency PCA + delegation PCA + sentiment variables into ~15--20 features.
- **Method:** K-means or HDBSCAN on standardized features. Expect 4--6 natural clusters (e.g., "Power users", "Cautious adopters", "Non-adopters", "Chat-only users", "Agentic pioneers").
- **Key challenge:** ~30% of rows have heavy NA (survey logic branching means non-AI-users skip most AI questions). Need to handle missing data carefully -- impute as "not applicable" or use a two-stage approach (first classify adopter/non-adopter, then cluster within adopters).
- **Sample size is strong:** 24,534 respondents with ~22,156 answering the AI tools question.

### Potential blog post angles:

1. **"The 5 Tribes of AI-Assisted Developers"** -- cluster on tool+task+delegation features.
2. **"Claude Code Users Are Different"** -- compare the 1,029 Claude Code users against the rest on delegation, task frequency, and sentiment.
3. **"What Separates Power Users from Skeptics"** -- ordinal regression on `ai_time_saving` or `ai_agents_try`.
4. **"The Trust Gap"** -- cross-tab trust/sentiment with tool adoption intensity.

## Comparison with Stack Overflow Survey

The JetBrains survey has significantly richer AI coverage than Stack Overflow 2024:

| Dimension | JetBrains 2025 | Stack Overflow 2024 |
|-----------|---------------|-------------------|
| AI tool list | 46 tools (incl. Claude Code, Aider, Cline, Junie) | ~10 tools |
| LLM model preferences | Per-tool model breakdowns (Copilot, Cursor, JB AI, etc.) | Not asked |
| Task frequency | 25 tasks with 6-point frequency | Binary "use for X" |
| Delegation willingness | 24 tasks, 3-point scale | Not asked |
| Importance aspects | 16 aspects, 4-point Likert | Not asked |
| Agentic development | Explicit question on prompt-based agentic dev | Not asked |
| Company policy | Use + access policies separately | Not asked |
| Sentiment/philosophy | Emotions, creativity, AGI timeline, BCI timeline, trust | Broad sentiment only |
| Sample size | 24,534 | ~65,000 (but fewer AI questions) |

JetBrains 2025 is the better dataset for AI developer segmentation due to its granular behavioral and attitudinal questions. The task frequency matrix alone (25 tasks x 6 frequency levels) provides far more signal than any other public developer survey.

## Data Location

Raw data downloaded to: `/tmp/jetbrains_2025/Developer Ecosystem Survey 2025_ Raw Data Sharing 2/`
- `developer_ecosystem_2025_external.csv` -- wide format (202 MB, 24,534 rows x 4,740 cols)
- `developer_ecosystem_2025_external_questions.csv` -- question metadata
- `Developer_Ecosystem_2025_Survey_questions_logic.pdf` -- survey branching logic
- `developer_ecosystem_2025_external_narrow.csv.zip` -- narrow format (one row per response-option)
