---
title: Does Your AI Agent Need a Map?
subtitle: Comparing graph-based and traditional code exploration for LLM-driven codebase consolidation
date: 2026-03-07
draft: true
---

## The Question

When an LLM agent needs to understand a codebase, does giving it a pre-built structural map (dependency graph, health scores, module summaries) actually help? Or is the tried-and-true approach of `grep`, `glob`, and `read` just as effective?

I ran a controlled experiment: two Claude Opus 4.6 agents analyzing the same codebase for consolidation opportunities, using different exploration strategies. One navigated via a graph-view system I built (manifests, codebase graphs, health/smell detectors). The other used traditional file exploration.

The results surprised me.

## Background

### The Graph-View System

Over the past few months, I've built a layered knowledge architecture for my codebases:

- **Layer 1 (Code Structure):** Tree-sitter-based property graphs (GitNexus/KuzuDB) indexing functions, classes, and call relationships
- **Layer 2 (Data Flow):** Hand-curated YAML graphs capturing how data artifacts flow through the system — which scripts produce which files, database dependencies, cross-project edges
- **Layer 3 (Knowledge):** A persistent knowledge bank of learnings, conventions, and debugging patterns

On top of these, a manifest generator produces navigable YAML files with per-module summaries, health scores (based on fan-in/fan-out and cycles), dependency lists, and entry files. A smell detector flags god modules, orphaned nodes, and circular dependencies.

The hypothesis: giving an LLM agent this structured context should let it find issues faster, with fewer tokens, and surface architectural problems that raw grep would miss.

### The Codebase

KD-GAT is a PyTorch/PyG research project for CAN bus intrusion detection. At the time of this experiment:

- ~48 Python files, ~13,000 lines across 8 modules
- 89 nodes and 214 edges in the data-flow graph
- Had just undergone a major cleanup (193K lines deleted in 5 prior commits)
- The question: what consolidation opportunities remain?

## Experimental Design

### Setup

Both agents were launched simultaneously as background sub-agents from the same Claude Code session, on the same commit (`5cb4faf`), with symmetric prompt structures. The key difference was the exploration instructions:

**Graph-View Agent** was told to:

1. Read the project manifest
2. Read module summaries
3. Read the codebase graph
4. Run health and smell detection
5. Use dataflow queries for suspicious nodes
6. Only then read specific files

**Traditional Agent** was told to:

1. List directories and explore the file tree
2. Glob for all Python files
3. Grep for patterns (dead imports, TODOs, duplicates, large files)
4. Read suspicious files
5. Cross-reference findings

Both were asked to produce structured reports with findings ranked by impact.

### Controlled Variables

| Variable   | Value                                        |
|------------|----------------------------------------------|
| Model      | Claude Opus 4.6                              |
| Agent type | general-purpose sub-agent                    |
| Codebase   | KD-GAT @ `5cb4faf`                           |
| Task       | "Find remaining consolidation opportunities" |
| Execution  | Background, parallel, same session           |

### Limitations

- Single codebase, single trial — no statistical power yet
- Prompts differ by necessity (different method instructions)
- Token counts include tool results, not just generation
- Graph infrastructure has upfront build cost not captured in trial timing
- Finding "quality" is subjectively categorized

## Results: Trial 1

### Efficiency Metrics

| Metric               | Graph-View | Traditional |
|----------------------|-----------:|------------:|
| Total tokens         |     76,951 |     142,602 |
| Tool calls           |         51 |          80 |
| Wall-clock (seconds) |        218 |         219 |
| Tokens per finding   |      8,550 |      12,964 |

Graph-view used **46% fewer tokens** while taking the same wall-clock time. It also made **36% fewer tool calls**.

### What Each Method Found

| Priority   | Graph-View | Traditional |
|------------|-----------:|------------:|
| Critical   |          0 |           1 |
| High       |          6 |           4 |
| Medium     |          2 |           4 |
| Low        |          1 |           2 |
| **Total**  |          9 |          11 |

| Finding Type | Graph-View | Traditional |
|--------------|-----------:|------------:|
| Architectural |         3 |           1 |
| Code-level    |         6 |          10 |

The most striking result: only **2 of 15 combined findings overlapped**. The methods are highly complementary (complementary score: 0.87).

### The Complementarity Effect

| Category               | Graph-View | Traditional | Both |
|------------------------|-----------:|------------:|-----:|
| Orphaned/dead scripts  |          4 |           1 |    1 |
| God module extraction  |          2 |           0 |    0 |
| Duplicate functions    |          0 |           3 |    0 |
| Missing imports (bugs) |          0 |           1 |    0 |
| Unused exports         |          0 |           2 |    0 |
| Dead migration code    |          0 |           1 |    0 |
| API clarity            |          1 |           1 |    1 |

Graph-view's structural signals (fan-out thresholds, zero fan-in/fan-out, health scores) naturally surface **architectural** issues — modules that are too large, scripts that nothing references, code that should be extracted. These are hard to find with grep because they're about *relationships*, not *text patterns*.

Traditional grep excels at **line-level** issues — a function duplicated across files, an import that references a deleted module, re-exports that nothing uses. These require cross-referencing symbol usage across files, which is exactly what grep does well.

### The Critical Bug

The traditional agent found a **runtime-crashing bug** that the graph-view agent missed entirely: `validate.py` uses `STAGE_DEPENDENCIES` without importing it. Any call to validate a stage with prerequisites would raise `NameError`.

This is instructive. The graph-view system models `validate.py` as a node with edges to `constants.py`, but it tracks *data flow* relationships, not *import correctness*. The traditional agent found it by grepping for cross-file symbol usage — a pattern the graph doesn't capture at its current granularity.

## Discussion

### When to Use Each Method

Based on this initial trial:

| Task Type                   | Recommended Method |
|-----------------------------|--------------------|
| Finding orphaned/dead code  | Graph-view         |
| Identifying god modules     | Graph-view         |
| Planning extractions/splits | Graph-view         |
| Finding duplicate functions | Traditional        |
| Detecting import bugs       | Traditional        |
| Auditing public API surface | Traditional        |
| Full consolidation review   | **Both**           |

### The Cost of the Map

The graph-view system isn't free. Building and maintaining it requires:

- Initial graph creation (hand-curated YAML, ~1–2 hours per project)
- Manifest generation scripts (~500 lines of Python)
- Health/smell detection logic
- Keeping graphs in sync with code changes (drift detection hooks)

Whether this upfront investment pays off depends on how often you need architectural-level analysis. For a research codebase undergoing active restructuring, I'd argue it does.

### Token Economics

At 46% fewer tokens for comparable results, the graph-view approach is meaningfully cheaper per session. Over many sessions, this compounds. But the traditional approach found the only critical bug — so cost savings mean nothing if you miss a `NameError`.

The optimal strategy appears to be: **graph-view for triage, traditional for verification**.

## What's Next

This is one trial on one codebase. To build confidence in these patterns, I plan to:

1. Run the same experiment on Map-Visualizations (different architecture: JS + Python, Observable Framework)
2. Vary the task type (bug hunting, feature planning, onboarding)
3. Test with different model sizes (Sonnet vs Opus)
4. Measure the graph infrastructure maintenance cost over time
5. Try a hybrid agent that uses both approaches in sequence

The dataset is accumulating at `data/trials.json` — each trial adds structured metrics for both methods plus comparison scores.

## Methodology Notes

All trials use Claude Opus 4.6 sub-agents launched in parallel from Claude Code CLI on OSC (Ohio Supercomputer Center). Agents run as background tasks with full tool access. Token counts are reported by the agent runtime and include both input (tool results) and output (generation). Wall-clock time includes tool execution latency on NFS-mounted filesystems.

The "complementary score" is defined as: `1 - (overlapping_findings / combined_unique_findings)`. A score of 1.0 means zero overlap (perfectly complementary); 0.0 means complete overlap (redundant).

---

*This post will be updated as more trials are conducted. Data is in [`data/trials.json`](https://github.com/RobertFrenken/RobertFrenken.github.io/tree/master/posts/graph-view-vs-traditional/data).*
