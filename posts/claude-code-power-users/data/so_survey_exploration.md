# Stack Overflow 2025 Developer Survey — AI Column Exploration

**Source:** https://survey.stackoverflow.co/datasets/stack-overflow-developer-survey-2025.zip
**Downloaded:** 2026-03-07
**Total respondents:** 49,191 (53,921 rows including header)
**Total columns:** 172

---

## All AI-Related Columns

### 1. Core AI Usage & Sentiment (highest response rates — best for clustering)

| Column | Description | Respondents | % of Total |
|--------|-------------|-------------|------------|
| `AISelect` | Do you currently use AI tools? (frequency) | 33,720 | 68.5% |
| `AISent` | Favorability toward AI tools | 33,467 | 68.0% |
| `AIAcc` | Trust in AI output accuracy | 33,297 | 67.7% |
| `AIComplex` | How well AI handles complex tasks | 33,283 | 67.7% |
| `AIThreat` | Do you believe AI threatens your job? | 36,078 | 73.3% |
| `AIAgentChange` | Have AI tools changed your dev work? | 31,678 | 64.4% |
| `AIAgents` | Are you using AI agents at work? | 31,919 | 64.9% |

### 2. AI Learning

| Column | Description | Respondents | % of Total |
|--------|-------------|-------------|------------|
| `LearnCodeAI` | Learned AI tools in past year? | 45,201 | 91.9% |
| `AILearnHow` | How did you learn AI? (multi-select) | 28,257 | 57.4% |

### 3. AI Tool Integration by Task (matrix — 5 columns, 14 tasks each)

| Column | Description | Respondents | % of Total |
|--------|-------------|-------------|------------|
| `AIToolCurrently partially AI` | Tasks currently partially AI-assisted | 21,028 | 42.7% |
| `AIToolCurrently mostly AI` | Tasks currently mostly AI-driven | 11,225 | 22.8% |
| `AIToolPlan to partially use AI` | Tasks planned for partial AI | 22,556 | 45.9% |
| `AIToolPlan to mostly use AI` | Tasks planned for mostly AI | 12,818 | 26.1% |
| `AIToolDon't plan to use AI for this task` | Tasks with no AI plans | 25,381 | 51.6% |

### 4. AI Frustrations & Human Fallback

| Column | Description | Respondents | % of Total |
|--------|-------------|-------------|------------|
| `AIFrustration` | Problems encountered with AI (multi-select) | 31,522 | 64.1% |
| `AIHuman` | When would you still ask a human? (multi-select) | 29,194 | 59.3% |
| `SOFriction` | How often AI issues send you to SO? | 30,787 | 62.6% |

### 5. AI Models Used

| Column | Description | Respondents | % of Total |
|--------|-------------|-------------|------------|
| `AIModelsChoice` | Did you use LLMs for dev? (Y/N gate) | 30,239 | 61.5% |
| `AIModelsHaveWorkedWith` | Which LLMs used (multi-select) | 16,281 | 33.1% |
| `AIModelsWantToWorkWith` | Which LLMs want to use (multi-select) | 11,845 | 24.1% |
| `AIModelsAdmired` | Which LLMs admired (multi-select) | 11,284 | 22.9% |

### 6. AI Agent Deep-Dive (lower response — agent users only)

| Column | Description | Respondents | % of Total |
|--------|-------------|-------------|------------|
| `AIAgent_Uses` | Industry/task uses for agents (multi-select) | 12,320 | 25.0% |
| `AgentUsesGeneral` | General agent capabilities used | 5,805 | 11.8% |
| `AIAgentImpact*` (5 cols) | Likert agreement on agent impact statements | 3,779–10,146 | 7.7–20.6% |
| `AIAgentChallenges*` (5 cols) | Likert agreement on agent challenges | 9,314–23,108 | 18.9–47.0% |
| `AIAgentKnowledge` | Agent memory/data tools used | 3,401 | 6.9% |
| `AIAgentOrchestration` | Agent frameworks used | 3,760 | 7.6% |
| `AIAgentObserveSecure` | Agent observability/security tools | 2,692 | 5.5% |
| `AIAgentExternal` | Out-of-the-box agents/copilots used | 8,332 | 16.9% |

### 7. Free Text (qualitative only)

| Column | Description | Respondents | % of Total |
|--------|-------------|-------------|------------|
| `AIExplain` | Is "vibe coding" part of your work? | 26,592 | 54.1% |
| `AIOpen` | Skills valuable even as AI grows? | 22,554 | 45.8% |

---

## Key Value Distributions

### AISelect — AI Tool Usage Frequency
| Value | Count | % |
|-------|-------|---|
| Yes, I use AI tools daily | 15,883 | 47.1% |
| Yes, I use AI tools weekly | 5,958 | 17.7% |
| No, and I don't plan to | 5,454 | 16.2% |
| Yes, I use AI tools monthly or infrequently | 4,628 | 13.7% |
| No, but I plan to soon | 1,797 | 5.3% |

**78.5% of respondents who answered use AI tools at least sometimes.** 47.1% are daily users.

### AISent — Sentiment Toward AI Tools
| Value | Count | % |
|-------|-------|---|
| Favorable | 12,311 | 36.8% |
| Very favorable | 7,677 | 22.9% |
| Indifferent | 5,880 | 17.6% |
| Unfavorable | 3,621 | 10.8% |
| Very unfavorable | 3,219 | 9.6% |
| Unsure | 759 | 2.3% |

**59.7% favorable or very favorable; 20.4% unfavorable or very unfavorable.**

### AIAcc — Trust in AI Accuracy
| Value | Count | % |
|-------|-------|---|
| Somewhat trust | 9,869 | 29.6% |
| Somewhat distrust | 8,685 | 26.1% |
| Neither trust nor distrust | 7,162 | 21.5% |
| Highly distrust | 6,533 | 19.6% |
| Highly trust | 1,048 | 3.1% |

**Only 3.1% highly trust AI accuracy. 45.7% distrust (somewhat + highly).**

### AIComplex — AI Handling of Complex Tasks
| Value | Count | % |
|-------|-------|---|
| Good, but not great | 8,384 | 25.2% |
| Bad | 7,328 | 22.0% |
| Very poor | 5,844 | 17.6% |
| Don't use / don't know | 5,582 | 16.8% |
| Neither good nor bad | 4,688 | 14.1% |
| Very well | 1,457 | 4.4% |

**39.6% rate AI as bad or very poor at complex tasks. Only 4.4% say very well.**

### AIThreat — Does AI Threaten Your Job?
| Value | Count | % |
|-------|-------|---|
| No | 22,958 | 63.6% |
| I'm not sure | 7,700 | 21.3% |
| Yes | 5,420 | 15.0% |

### AIAgents — AI Agent Usage
| Value | Count | % |
|-------|-------|---|
| No, and I don't plan to | 12,082 | 37.9% |
| No, but I plan to | 5,561 | 17.4% |
| Yes, daily | 4,509 | 14.1% |
| No, copilot/autocomplete only | 4,401 | 13.8% |
| Yes, weekly | 2,868 | 9.0% |
| Yes, monthly or infrequently | 2,498 | 7.8% |

**30.9% use AI agents at work (daily + weekly + monthly). 37.9% have no plans to use them.**

### AIAgentChange — Has AI Changed Your Dev Work?
| Value | Count | % |
|-------|-------|---|
| Not at all or minimally | 13,097 | 41.3% |
| Yes, somewhat | 11,171 | 35.3% |
| Yes, to a great extent | 5,178 | 16.3% |
| No, changed due to non-AI factors (somewhat) | 1,410 | 4.5% |
| No, changed due to non-AI factors (significantly) | 822 | 2.6% |

### AIFrustration — Problems With AI Tools
| Value | Count | % of respondents |
|-------|-------|------------------|
| Solutions almost right, but not quite | 20,806 | 66.0% |
| Debugging AI code is more time-consuming | 14,262 | 45.2% |
| I don't use AI tools regularly | 7,413 | 23.5% |
| Less confident in own problem-solving | 6,323 | 20.1% |
| Hard to understand how/why code works | 5,147 | 16.3% |
| No problems encountered | 1,247 | 4.0% |

### AIModelsHaveWorkedWith — LLM Models Used (top 10)
| Model | Count | % of respondents |
|-------|-------|------------------|
| OpenAI GPT (chatbot) | 13,424 | 82.5% |
| Anthropic Claude Sonnet | 7,063 | 43.4% |
| Gemini Flash | 5,823 | 35.8% |
| OpenAI Reasoning | 5,716 | 35.1% |
| OpenAI Image gen | 4,395 | 27.0% |
| Gemini Pro Reasoning | 4,221 | 25.9% |
| DeepSeek Reasoning | 3,848 | 23.6% |
| Meta Llama | 2,941 | 18.1% |
| DeepSeek General | 2,363 | 14.5% |
| X Grok | 1,839 | 11.3% |

### AIAgentExternal — Copilots/Assistants Used (top 10)
| Tool | Count | % of respondents |
|------|-------|------------------|
| ChatGPT | 6,807 | 81.7% |
| GitHub Copilot | 5,656 | 67.9% |
| Google Gemini | 3,952 | 47.4% |
| Claude Code | 3,398 | 40.8% |
| Microsoft Copilot | 2,603 | 31.2% |
| Perplexity | 1,353 | 16.2% |
| v0.dev | 756 | 9.1% |
| Bolt.new | 542 | 6.5% |
| Lovable.dev | 476 | 5.7% |
| AgentGPT | 419 | 5.0% |

### SOFriction — How Often AI Issues Drive You to Stack Overflow
| Value | Count | % |
|-------|-------|---|
| Rarely, almost never | 13,213 | 42.9% |
| I don't use AI tools | 6,791 | 22.1% |
| Less than half the time | 5,698 | 18.5% |
| About half the time | 2,790 | 9.1% |
| More than half the time | 2,295 | 7.5% |

### AIHuman — When Would You Still Ask a Human?
| Value | Count | % of respondents |
|-------|-------|------------------|
| When I don't trust AI's answers | 21,980 | 75.3% |
| Ethical or security concerns | 18,010 | 61.7% |
| Want to fully understand something | 17,885 | 61.3% |
| Want best practices | 16,962 | 58.1% |
| Stuck and can't explain the problem | 15,938 | 54.6% |
| Complex or unfamiliar code | 14,537 | 49.8% |
| Compare different solutions | 12,886 | 44.1% |
| Quick troubleshooting | 8,014 | 27.5% |
| Don't think I'll need people anymore | 1,247 | 4.3% |

### LearnCodeAI — Learned AI in Past Year
| Value | Count | % |
|-------|-------|---|
| Yes, for job/career | 16,403 | 36.3% |
| Yes, for personal curiosity | 14,027 | 31.0% |
| No, learned non-AI (personal) | 5,282 | 11.7% |
| No, didn't learn anything | 4,864 | 10.8% |
| No, learned non-AI (for job) | 4,625 | 10.2% |

**67.3% actively learned AI tools in the past year.**

---

## Assessment: Columns Suitable for Clustering Developer AI Usage Patterns

### Tier 1 — Primary clustering features (high response rate, clean ordinal/categorical)

These 7 columns have 64–74% response rates with clean categorical values. They form a natural feature matrix:

1. **`AISelect`** — Usage frequency (5-level ordinal: daily → don't plan to)
2. **`AISent`** — Sentiment (5-level ordinal: very favorable → very unfavorable)
3. **`AIAcc`** — Trust in accuracy (5-level ordinal)
4. **`AIComplex`** — Perceived capability for complex tasks (6-level ordinal)
5. **`AIThreat`** — Job threat perception (3-level: Yes/No/Unsure)
6. **`AIAgentChange`** — Degree of workflow change (5-level ordinal)
7. **`AIAgents`** — Agent usage level (6-level ordinal)

**~31,000–33,000 respondents answered all of these.** After dropping rows with any NA, expect ~28,000–30,000 usable rows.

### Tier 2 — Enrichment features (lower response, deeper signal)

8. **`AIFrustration`** — Multi-select frustrations (encode as binary flags per frustration type)
9. **`AIHuman`** — When humans preferred over AI (binary flags)
10. **`AIToolCurrently partially AI` / `AIToolCurrently mostly AI`** — Which tasks are AI-assisted (14 tasks, can create task-level AI adoption score)
11. **`AIAgentExternal`** — Which tools used (binary flags — useful for tool-ecosystem clustering)
12. **`AIModelsHaveWorkedWith`** — Which LLMs (binary flags)
13. **`SOFriction`** — AI-to-SO friction frequency

### Tier 3 — Agent deep-dive (small n, for sub-analysis)

14. **`AIAgentImpact*`** — 5 Likert columns x 8 statements (matrix question, ~10K respondents)
15. **`AIAgentChallenges*`** — 5 Likert columns x 7 statements (~9K–23K respondents)
16. **`AIAgentOrchestration`** / **`AIAgentKnowledge`** / **`AIAgentObserveSecure`** — Toolchain details (3K–4K respondents, agent builders only)

---

## Obvious Natural Groupings Visible in Distributions

### Group 1: "AI Enthusiasts" (~15–20% of respondents)
- Daily AI tool users (47.1% of AISelect respondents)
- Very favorable sentiment (22.9%)
- Use agents daily (14.1%) or weekly (9.0%)
- "Great extent" workflow change (16.3%)
- But even they rarely "highly trust" accuracy (3.1%)

### Group 2: "Pragmatic Adopters" (~30–35%)
- Weekly/monthly AI use
- Favorable but cautious sentiment
- "Somewhat trust" accuracy (29.6%)
- AI is "good, but not great" at complex tasks (25.2%)
- Top frustration: "almost right, but not quite" (66.0%)

### Group 3: "Skeptics/Non-adopters" (~20–25%)
- Don't use AI and don't plan to (16.2% of AISelect)
- Unfavorable or very unfavorable sentiment (20.4% combined)
- "Highly distrust" accuracy (19.6%)
- Don't plan to use agents (37.9%)
- Not at all or minimally changed by AI (41.3%)

### Group 4: "Copilot-Only Users" (~14%)
- Use AI exclusively in copilot/autocomplete mode (13.8% of AIAgents)
- Likely daily/weekly AISelect users but NOT agentic
- Bridge between enthusiasts and pragmatists

### Key Paradox for Blog Post
**The "Adoption-Trust Gap"**: 47% use AI daily, but only 3% highly trust it. 66% say AI solutions are "almost right, but not quite." Developers have adopted AI as a tool they actively distrust — similar to how people use Google Maps but still double-check the route. This tension between heavy usage and low trust is the strongest signal in the data.

### Another Notable Pattern
**Self-reported skill erosion**: 20.1% say AI has made them "less confident in my own problem-solving." This is a minority but a substantial one — 1 in 5 active AI users reports diminished self-confidence. Cross-tabulated with experience level, this could reveal whether junior vs. senior devs are differentially affected.
