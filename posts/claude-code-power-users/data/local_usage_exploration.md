# Local Claude Code Usage Data Exploration

**Date:** 2026-03-07
**Machine:** OSC Pitzer (rf15@pitzer)
**Usage period:** 2026-02-20 to 2026-03-07 (15 active days)

---

## 1. Data Sources Overview

Three distinct data stores exist locally:

| Source | Location | Files | Coverage |
|--------|----------|-------|----------|
| **JSONL session logs** | `~/.claude/projects/-users-PAS2022-rf15/*.jsonl` | 196 JSONL files | Every session (raw conversation) |
| **Session-meta (from /insights)** | `~/.claude/usage-data/session-meta/*.json` | 193 JSON files | Per-session summary metrics |
| **Facets (from /insights)** | `~/.claude/usage-data/facets/*.json` | 50 JSON files | LLM-generated qualitative analysis |
| **Insights report** | `~/.claude/usage-data/report.html` | 1 HTML file | Pre-rendered narrative report |
| **ccusage (CLI tool)** | `npx ccusage` | N/A (reads JSONL) | Token/cost aggregation |

Additionally, 162 per-session directories exist under `~/.claude/projects/-users-PAS2022-rf15/<session-id>/` containing:
- `subagents/` -- JSONL logs for sub-agent (Task tool) conversations
- `tool-results/` -- stored tool output (file paths, command output)

The KD-GAT and Map-Visualizations project directories (`~/.claude/projects/-users-PAS2022-rf15-KD-GAT/` and `-Map-Visualizations/`) contain only a `memory/` subdirectory (MEMORY.md), no separate session files.

**Total disk usage:** ~540 MB for the main projects directory.

---

## 2. Session-Meta Schema (193 files)

Each file is `<session-uuid>.json` with this schema:

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | string | UUID |
| `project_path` | string | Working directory (e.g., `/users/PAS2022/rf15`) |
| `start_time` | ISO 8601 | Session start timestamp |
| `duration_minutes` | int | Wall-clock session duration |
| `user_message_count` | int | Number of user messages |
| `assistant_message_count` | int | Number of assistant messages |
| `tool_counts` | object | `{tool_name: count}` -- every tool call tallied |
| `languages` | object | `{language: count}` -- languages detected in code blocks |
| `git_commits` | int | Commits made during session |
| `git_pushes` | int | Pushes made during session |
| `input_tokens` | int | Total input tokens (appears to be non-cache tokens only) |
| `output_tokens` | int | Total output tokens |
| `first_prompt` | string | Truncated first user message |
| `user_interruptions` | int | Times user interrupted assistant |
| `user_response_times` | array | Per-turn response times (seconds) |
| `tool_errors` | int | Number of tool errors |
| `tool_error_categories` | object | `{error_type: count}` |
| `uses_task_agent` | bool | Whether Task/Agent tool was used |
| `uses_mcp` | bool | Whether any MCP tool was used |
| `uses_web_search` | bool | Whether WebSearch was used |
| `uses_web_fetch` | bool | Whether WebFetch was used |
| `lines_added` | int | Lines of code added |
| `lines_removed` | int | Lines of code removed |
| `files_modified` | int | Number of files modified |
| `message_hours` | array[int] | Hour-of-day for each user message (local time) |
| `user_message_timestamps` | array[string] | ISO timestamps for each user message |

### Aggregate Stats (from session-meta)

- **192 sessions** parsed (1 file malformed)
- **Total input tokens:** 371,415
- **Total output tokens:** 1,414,663
- **Total duration:** 4,460 minutes (~74.3 hours)
- **Average session duration:** 23.2 minutes
- **Git commits:** 23
- **Lines added:** 44,263
- **Lines removed:** 4,177
- **Files modified:** 722
- **Unique tools used:** 47

**Note on token counts:** The session-meta `input_tokens` field appears to undercount vs. ccusage because it excludes cache tokens. ccusage reports 1.63 billion total tokens including cache read/creation.

---

## 3. Facets Schema (50 files)

Each file is `<session-uuid>.json` with LLM-generated qualitative analysis:

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | string | UUID (matches session-meta) |
| `underlying_goal` | string | Natural-language description of what user was trying to do |
| `goal_categories` | object | `{category: 1}` -- multi-label categorization of goals |
| `outcome` | enum | `fully_achieved`, `mostly_achieved`, `partially_achieved`, `unclear_from_transcript` |
| `user_satisfaction_counts` | object | `{satisfaction_level: count}` per user turn |
| `claude_helpfulness` | enum | `essential`, `very_helpful`, `moderately_helpful`, `slightly_helpful` |
| `session_type` | enum | `single_task`, `multi_task`, `exploration`, `iterative_refinement` |
| `friction_counts` | object | `{friction_type: count}` |
| `friction_detail` | string | Natural-language description of friction points |
| `primary_success` | string | What went well (e.g., `good_debugging`, `good_explanations`) |
| `brief_summary` | string | 1-2 sentence session summary |

### Aggregate Stats (from facets)

**Outcomes:** mostly_achieved (23), fully_achieved (17), partially_achieved (8), unclear (2)

**Session types:** multi_task (17), exploration (15), iterative_refinement (11), single_task (7)

**Claude helpfulness:** very_helpful (28), essential (16), moderately_helpful (5), slightly_helpful (1)

**Top friction types:** buggy_code (15), wrong_approach (14), misunderstood_request (6), user_rejected_action (1)

**Top goal categories:** implement_plan (5), git_operations (4), research_existing_tools (3), debugging (3), feature_implementation (3), documentation_update (3), bug_fix (2), architecture_analysis (2), visualization (2), planning (2)

---

## 4. JSONL Session Log Schema (196 files)

Raw conversation logs. Each line is a JSON object with a `type` field.

### Message Types

| Type | Description | Key Fields |
|------|-------------|------------|
| `user` | User message | `message.content`, `timestamp`, `cwd`, `sessionId`, `version`, `gitBranch`, `slug`, `permissionMode`, `todos` |
| `assistant` | Assistant response | `message.model`, `message.usage` (token breakdown), `message.content` (array of blocks), `timestamp`, `requestId` |
| `system` | System events | `subtype` (see below), `timestamp` |
| `progress` | Sub-agent progress | `data.message`, `toolUseID`, `parentToolUseID` |
| `file-history-snapshot` | File state tracking | `snapshot.trackedFileBackups`, `snapshot.timestamp` |

### System Message Subtypes

| Subtype | Purpose |
|---------|---------|
| `turn_duration` | Per-turn wall-clock time (`durationMs`) |
| `compact_boundary` | Context window compaction event |
| `local_command` | Local hook/command execution |

### Assistant Message Token Usage

Nested under `message.usage`:

```json
{
  "input_tokens": 10,
  "cache_creation_input_tokens": 22014,
  "cache_read_input_tokens": 10432,
  "cache_creation": {
    "ephemeral_5m_input_tokens": 0,
    "ephemeral_1h_input_tokens": 22014
  },
  "output_tokens": 6,
  "service_tier": "standard",
  "inference_geo": "not_available"
}
```

### Assistant Message Content Blocks

The `message.content` array contains blocks of type:
- `thinking` -- extended thinking (reasoning trace)
- `text` -- natural language response
- `tool_use` -- tool invocation with fields: `id`, `name`, `input`, `caller`

### Tool Use Block Schema

```json
{
  "type": "tool_use",
  "id": "toolu_01WLeGao1AcedCvTCqJpRzxV",
  "name": "Task",
  "input": {"description": "...", "prompt": "...", "subagent_type": "..."},
  "caller": "..."
}
```

### Sub-Agent Files

Per-session directories may contain `subagents/agent-<id>.jsonl` files with the same JSONL schema but `isSidechain: true` and an `agentId` field. These represent Task/Agent tool conversations.

### Tool Results

`tool-results/<hash>.txt` files store raw output from tool calls (file contents, command output).

---

## 5. ccusage CLI Output

`npx ccusage` is installed and functional. Supports: `daily`, `weekly`, `monthly`, `session`, `blocks` views.

### Daily JSON Schema

```json
{
  "daily": [
    {
      "date": "2026-02-20",
      "inputTokens": 13620,
      "outputTokens": 4264,
      "cacheCreationTokens": 303075,
      "cacheReadTokens": 3257843,
      "totalTokens": 3578802,
      "totalCost": 2.78,
      "modelsUsed": ["claude-opus-4-6", "claude-haiku-4-5-20251001"],
      "modelBreakdowns": [...]
    }
  ],
  "totals": {
    "inputTokens": 1019708,
    "outputTokens": 3067708,
    "cacheCreationTokens": 61618347,
    "cacheReadTokens": 1567828419,
    "totalCost": 1046.43,
    "totalTokens": 1633534182
  }
}
```

### Daily Cost Breakdown

| Date | Cost | Models |
|------|------|--------|
| 2026-02-20 | $2.78 | opus-4-6, haiku-4-5 |
| 2026-02-22 | $44.67 | opus-4-6, haiku-4-5, sonnet-4-6 |
| 2026-02-23 | $30.93 | opus-4-6, haiku-4-5, sonnet-4-6 |
| 2026-02-24 | $58.22 | opus-4-6, haiku-4-5 |
| 2026-02-25 | $75.95 | opus-4-6, sonnet-4-6, haiku-4-5 |
| 2026-02-26 | $44.04 | opus-4-6, haiku-4-5, sonnet-4-6 |
| 2026-02-27 | $25.45 | opus-4-6, haiku-4-5 |
| 2026-02-28 | $0.26 | opus-4-6 |
| 2026-03-01 | $48.18 | opus-4-6, sonnet-4-6, haiku-4-5 |
| 2026-03-02 | $131.07 | opus-4-6, haiku-4-5, opus-4-5, sonnet-4-6 |
| 2026-03-03 | $123.69 | opus-4-6, haiku-4-5, sonnet-4-6 |
| 2026-03-04 | $104.84 | opus-4-6, haiku-4-5, sonnet-4-6 |
| 2026-03-05 | $148.02 | opus-4-6, haiku-4-5 |
| 2026-03-06 | $132.93 | opus-4-6, haiku-4-5 |
| 2026-03-07 | $75.64 | opus-4-6, haiku-4-5 |

**Total cost: $1,046.43** across 15 days ($69.76/day average).

---

## 6. Insights Report (report.html)

Pre-rendered HTML report with:
- **Top-line stats:** 1,142 messages, +79,348/-5,548 lines, 912 files, 15 days, 76.1 msgs/day
- Narrative sections with qualitative analysis
- "At a Glance" summary, big wins, friction categories
- Project area breakdowns
- CLAUDE.md improvement suggestions

---

## 7. Per-Session Metrics Extractable

### From session-meta (structured, easy):
- Session duration (minutes)
- Token usage (input + output; cache tokens NOT in session-meta)
- Tool call distribution (which tools, counts)
- Files modified / lines added / removed
- Git commits and pushes
- Feature flags (uses_mcp, uses_task_agent, uses_web_search, uses_web_fetch)
- Time-of-day patterns (message_hours, user_message_timestamps)
- User interruption count
- Tool error count and categories
- Languages used
- First prompt text

### From facets (qualitative, LLM-generated):
- Session goal and goal categories
- Outcome (achieved/partial/unclear)
- Claude helpfulness rating
- Session type (single_task/multi_task/exploration/iterative_refinement)
- Friction types and descriptions
- Brief natural-language summary

### From JSONL (raw, requires parsing):
- Per-turn token breakdown (input, output, cache_creation, cache_read)
- Per-turn timing (`system.turn_duration.durationMs`)
- Model used per turn (claude-opus-4-6, haiku, sonnet, etc.)
- Thinking/reasoning content (extended thinking blocks)
- Tool call inputs and outputs (full arguments)
- Context compaction events (`compact_boundary`)
- Sub-agent spawning and nesting
- Working directory changes
- Git branch per message
- Claude Code version per message
- Permission mode (`plan`, etc.)

### From ccusage (aggregated):
- Daily/weekly/monthly cost with model breakdown
- Cache token usage (creation vs. read) -- key for cost analysis
- Per-model cost split
- Cost per session (via `ccusage session`)

---

## 8. Coverage Gaps and Limitations

1. **Facets only cover 50 of 193 sessions** -- the /insights analysis is partial (likely the most recent or longest sessions).
2. **Session-meta token counts exclude cache tokens** -- must use JSONL or ccusage for cache-aware cost analysis.
3. **No project-level tagging in session-meta** -- `project_path` is always `/users/PAS2022/rf15` (the home directory), even for sessions that cd into KD-GAT or Map-Viz. Would need to parse first_prompt or JSONL cwd changes to determine actual project.
4. **ccusage treats all sessions as one "project"** -- the `sessionId` in ccusage output is `-users-PAS2022-rf15` (the directory), not per-conversation.
5. **Sub-agent data is in separate JSONL files** -- not aggregated into session-meta. Must parse `<session>/subagents/` for sub-agent tool usage and token costs.
6. **No commit message content** -- session-meta has `git_commits` count but not the commit messages or SHAs.

---

## 9. Data Quality Notes

- 1 malformed session-meta JSON file (parse error at line 32)
- JSONL files range from 588 bytes (empty/aborted sessions) to 15.4 MB (long multi-agent sessions)
- Largest session files: 15.4 MB, 13.6 MB, 9.3 MB, 9.3 MB, 6.2 MB
- Smallest: 588 bytes, 1.7 KB, 2.9 KB (aborted or very short sessions)

---

## 10. Tool Usage Distribution (Top 25)

| Tool | Total Calls |
|------|-------------|
| Read | 1,413 |
| Bash | 1,365 |
| Edit | 921 |
| TaskUpdate | 493 |
| TaskCreate | 365 |
| Write | 312 |
| Grep | 242 |
| Glob | 122 |
| Task | 111 |
| ToolSearch | 104 |
| Agent | 84 |
| WebFetch | 51 |
| mcp__playwright__browser_navigate | 39 |
| AskUserQuestion | 28 |
| mcp__playwright__browser_console_messages | 24 |
| mcp__playwright__browser_evaluate | 21 |
| mcp__playwright__browser_close | 18 |
| mcp__playwright__browser_run_code | 16 |
| mcp__playwright__browser_take_screenshot | 16 |
| WebSearch | 16 |
| TaskOutput | 14 |
| ExitPlanMode | 12 |
| mcp__context7__query-docs | 10 |
| mcp__context7__resolve-library-id | 8 |
| mcp__playwright__browser_wait_for | 7 |

---

## 11. Recommended Extraction Strategy for Blog Post

1. **ccusage daily --json** for cost trends and model usage over time
2. **session-meta** for per-session metrics (duration, tool distribution, code output)
3. **Facets** for qualitative session analysis (outcomes, friction, helpfulness)
4. **JSONL parsing** (targeted) for per-turn token/timing data and cache analysis
5. **Join session-meta + facets** on `session_id` for quantitative + qualitative per-session view (50 sessions have both)
