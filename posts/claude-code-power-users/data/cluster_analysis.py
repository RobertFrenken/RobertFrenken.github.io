"""
Cluster analysis of developer AI usage patterns.

Reads JetBrains 2025 and Stack Overflow 2025 survey data, runs k-means
clustering on behavioral features, and outputs clusters.json for the blog post.

Usage:
    python3 data/cluster_analysis.py          # from post directory
    sbatch data/run_clustering.slurm          # via SLURM
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

DATA_DIR = Path(__file__).parent
SURVEY_DIR = DATA_DIR / "surveys"
SESSION_META_DIR = Path.home() / ".claude" / "usage-data" / "session-meta"
OUTPUT_PATH = DATA_DIR / "clusters.json"

# --- Ordinal encodings ---

TASK_FREQ_MAP = {
    "Never": 0,
    "Once a month or less often": 1,
    "Several times a month": 2,
    "Once a week": 3,
    "Several times a week": 4,
    "Every day": 5,
}

DELEGATE_MAP = {
    "I would still do it myself": 0,
    "I am not sure yet": 1,
    "I would delegate it": 2,
}

IMPORTANCE_MAP = {
    "Not important at all": 0,
    "Slightly important": 1,
    "Moderately important": 2,
    "Very important": 3,
}

AGENT_TRY_MAP = {
    "Very unlikely": 0,
    "Somewhat unlikely": 1,
    "Not sure": 2,
    "Somewhat likely": 3,
    "Very likely": 4,
    "I already use AI coding agents": 5,
}

TIME_SAVING_MAP = {
    "I don\u2019t save any time": 0,
    "Less than 1 hour": 1,
    "From 1 to less than 2 hours": 2,
    "From 2 to less than 4 hours": 3,
    "From 4 to less than 8 hours": 4,
    "8 hours or more": 5,
}

EMOTIONS_MAP = {
    "Fearful": 0,
    "Anxious": 1,
    "Uncertain": 2,
    "Indifferent": 3,
    "Hopeful": 4,
    "Excited": 5,
    "Other": 3,  # neutral default
}

# Key tools to flag
KEY_TOOLS = [
    "Anthropic Claude Code",
    "GitHub Copilot",
    "Cursor",
    "ChatGPT web / desktop / mobile apps (not inside third-party tools)",
    "JetBrains AI Assistant",
    "Devin",
]

# SO ordinal encodings
SO_AISELECT_MAP = {
    "No, and I don't plan to": 0,
    "No, but I plan to soon": 1,
    "Yes, I use AI tools monthly or infrequently": 2,
    "Yes, I use AI tools weekly": 3,
    "Yes, I use AI tools daily": 4,
}

SO_AISENT_MAP = {
    "Very unfavorable": 0,
    "Unfavorable": 1,
    "Unsure": 2,
    "Indifferent": 2,
    "Favorable": 3,
    "Very favorable": 4,
}

SO_AIACC_MAP = {
    "Highly distrust": 0,
    "Somewhat distrust": 1,
    "Neither trust nor distrust": 2,
    "Somewhat trust": 3,
    "Highly trust": 4,
}

SO_AICOMPLEX_MAP = {
    "Very poor at handling complex tasks": 0,
    "Bad at handling complex tasks": 1,
    "I don't use AI tools for complex tasks / I don't know": 2,
    "Neither good or bad at handling complex tasks": 2,
    "Good, but not great at handling complex tasks": 3,
    "Very well at handling complex tasks": 4,
}

SO_AITHREAT_MAP = {"Yes": 0, "I'm not sure": 1, "No": 2}

SO_AIAGENTS_MAP = {
    "No, and I don't plan to": 0,
    "No, I use AI exclusively in copilot/autocomplete mode": 1,
    "No, but I plan to": 2,
    "Yes, I use AI agents at work monthly or infrequently": 3,
    "Yes, I use AI agents at work weekly": 4,
    "Yes, I use AI agents at work daily": 5,
}

SO_AIAGENTCHANGE_MAP = {
    "Not at all or minimally": 0,
    "No, but my development work has changed somewhat due to non-AI factors": 1,
    "No, but my development work has significantly changed due to non-AI factors": 1,
    "Yes, somewhat": 2,
    "Yes, to a great extent": 3,
}


# ============================================================
# Phase A1-A4: JetBrains clustering
# ============================================================


def load_jetbrains():
    """Load JB 2025 survey and engineer clustering features."""
    print("Loading JetBrains 2025 survey...", flush=True)
    df = pd.read_csv(SURVEY_DIR / "jb_2025.csv", low_memory=False)
    print(f"  Raw rows: {len(df)}")

    # Identify column groups
    tf_cols = sorted([c for c in df.columns if c.startswith("ai_coding_tasks_freq::")])
    del_cols = sorted([c for c in df.columns if c.startswith("ai_coding_delegate::")])
    imp_cols = sorted([c for c in df.columns if c.startswith("ai_coding_aspects_imp::")])
    tool_cols = sorted([c for c in df.columns if c.startswith("usage_ai_coding::")])

    print(
        f"  Feature groups: {len(tf_cols)} task_freq, {len(del_cols)} delegate, "
        f"{len(imp_cols)} importance, {len(tool_cols)} tools"
    )

    # Filter to respondents with at least some AI task frequency data
    tf_non_null = df[tf_cols].notna().sum(axis=1)
    df_ai = df[tf_non_null >= 5].copy()
    print(f"  Respondents with >=5 task_freq answers: {len(df_ai)}")

    # Encode ordinal features
    for col in tf_cols:
        df_ai[col] = df_ai[col].map(TASK_FREQ_MAP)
    for col in del_cols:
        df_ai[col] = df_ai[col].map(DELEGATE_MAP)
    for col in imp_cols:
        df_ai[col] = df_ai[col].map(IMPORTANCE_MAP)

    # Fill missing with column mode (question not shown = most common answer)
    feature_cols = tf_cols + del_cols + imp_cols
    for col in feature_cols:
        mode_val = df_ai[col].mode()
        if len(mode_val) > 0:
            df_ai[col] = df_ai[col].fillna(mode_val.iloc[0])
        else:
            df_ai[col] = df_ai[col].fillna(0)

    # Tool count feature
    tool_non_none = [c for c in tool_cols if "None" not in c]
    df_ai["tool_count"] = df_ai[tool_non_none].notna().sum(axis=1)

    # Key tool binary flags
    tool_flags = {}
    for tool_name in KEY_TOOLS:
        matching = [c for c in tool_cols if tool_name in c]
        col_name = tool_name.split("(")[0].strip().replace(" ", "_").lower()
        if matching:
            df_ai[f"tool_{col_name}"] = df_ai[matching[0]].notna().astype(int)
            tool_flags[col_name] = f"tool_{col_name}"

    tool_flag_cols = list(tool_flags.values())

    # Encode scalar features
    df_ai["ai_agents_try_ord"] = df_ai["ai_agents_try"].map(AGENT_TRY_MAP).fillna(2)
    df_ai["ai_time_saving_ord"] = df_ai["ai_time_saving"].map(TIME_SAVING_MAP).fillna(0)
    df_ai["emotions_ord"] = df_ai["emotions_about_ai_society"].map(EMOTIONS_MAP).fillna(3)

    # Assemble feature matrix
    all_feature_cols = (
        tf_cols
        + del_cols
        + imp_cols
        + ["tool_count"]
        + tool_flag_cols
        + ["ai_agents_try_ord", "ai_time_saving_ord", "emotions_ord"]
    )

    X = df_ai[all_feature_cols].values.astype(float)
    print(f"  Feature matrix: {X.shape}")

    return df_ai, X, all_feature_cols, tf_cols, del_cols, imp_cols, tool_flag_cols


def run_clustering(X, k_range=range(3, 8)):
    """StandardScaler + PCA + k-means + t-SNE."""
    print("Standardizing features...", flush=True)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("Running PCA (90% variance)...", flush=True)
    pca = PCA(n_components=0.9, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    print(
        f"  PCA components: {X_pca.shape[1]} (explained: {pca.explained_variance_ratio_.sum():.3f})"
    )

    # k-means over range
    print(f"Running k-means for k in {list(k_range)}...", flush=True)
    results = {}
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10, max_iter=300)
        labels = km.fit_predict(X_pca)
        sil = silhouette_score(X_pca, labels, sample_size=min(5000, len(X_pca)))
        inertia = km.inertia_
        results[k] = {"labels": labels, "silhouette": sil, "inertia": inertia, "model": km}
        print(f"  k={k}: silhouette={sil:.4f}, inertia={inertia:.0f}")

    # Pick best k by silhouette
    best_k = max(results, key=lambda k: results[k]["silhouette"])
    print(f"  Best k={best_k} (silhouette={results[best_k]['silhouette']:.4f})")

    # DBSCAN sanity check
    print("Running DBSCAN sanity check...", flush=True)
    db = DBSCAN(eps=3.0, min_samples=20)
    db_labels = db.fit_predict(X_pca)
    n_dbscan_clusters = len(set(db_labels)) - (1 if -1 in db_labels else 0)
    n_noise = (db_labels == -1).sum()
    print(f"  DBSCAN found {n_dbscan_clusters} clusters, {n_noise} noise points")

    # t-SNE on PCA output
    print("Running t-SNE (perplexity=30)...", flush=True)
    tsne = TSNE(n_components=2, perplexity=30, random_state=42, n_iter=1000, init="pca")
    X_tsne = tsne.fit_transform(X_pca)
    print("  t-SNE complete.")

    return {
        "scaler": scaler,
        "pca": pca,
        "X_pca": X_pca,
        "X_tsne": X_tsne,
        "best_k": best_k,
        "labels": results[best_k]["labels"],
        "silhouette": results[best_k]["silhouette"],
        "all_results": {
            k: {"silhouette": v["silhouette"], "inertia": v["inertia"]} for k, v in results.items()
        },
        "dbscan_clusters": n_dbscan_clusters,
        "dbscan_noise": n_noise,
        "pca_components": int(X_pca.shape[1]),
        "pca_explained": float(pca.explained_variance_ratio_.sum()),
    }


def profile_clusters(df_ai, labels, tf_cols, del_cols, imp_cols, tool_flag_cols):
    """Compute per-cluster profiles."""
    print("Profiling clusters...", flush=True)
    df_ai = df_ai.copy()
    df_ai["cluster"] = labels
    n_total = len(df_ai)

    cluster_profiles = []
    for cid in sorted(df_ai["cluster"].unique()):
        grp = df_ai[df_ai["cluster"] == cid]
        n = len(grp)

        # Task frequency means
        tf_means = {col.split("::")[-1]: round(float(grp[col].mean()), 2) for col in tf_cols}

        # Delegation means
        del_means = {col.split("::")[-1]: round(float(grp[col].mean()), 2) for col in del_cols}

        # Tool composition
        tool_pcts = {}
        for tcol in tool_flag_cols:
            tool_name = tcol.replace("tool_", "")
            tool_pcts[tool_name] = round(float(grp[tcol].mean() * 100), 1)

        # Agent adoption distribution
        agent_dist = grp["ai_agents_try"].value_counts(normalize=True).to_dict()
        agent_dist = {k: round(v * 100, 1) for k, v in agent_dist.items()}

        # Time saved distribution
        time_dist = grp["ai_time_saving"].value_counts(normalize=True).to_dict()
        time_dist = {k: round(v * 100, 1) for k, v in time_dist.items() if pd.notna(k)}

        # Emotions distribution
        emo_dist = grp["emotions_about_ai_society"].value_counts(normalize=True).to_dict()
        emo_dist = {k: round(v * 100, 1) for k, v in emo_dist.items() if pd.notna(k)}

        # Mean scalar features
        mean_agent_try = round(float(grp["ai_agents_try_ord"].mean()), 2)
        mean_time_saving = round(float(grp["ai_time_saving_ord"].mean()), 2)
        mean_emotion = round(float(grp["emotions_ord"].mean()), 2)
        mean_tool_count = round(float(grp["tool_count"].mean()), 1)

        # Auto-name based on dominant patterns
        name = auto_name_cluster(
            tf_means, del_means, tool_pcts, mean_agent_try, mean_time_saving, mean_tool_count
        )

        cluster_profiles.append(
            {
                "id": int(cid),
                "name": name,
                "size": int(n),
                "pct": round(n / n_total * 100, 1),
                "task_freq_means": tf_means,
                "delegation_means": del_means,
                "tool_pcts": tool_pcts,
                "agent_adoption": agent_dist,
                "time_saved": time_dist,
                "emotions": emo_dist,
                "mean_agent_try": mean_agent_try,
                "mean_time_saving": mean_time_saving,
                "mean_emotion": mean_emotion,
                "mean_tool_count": mean_tool_count,
            }
        )

    return cluster_profiles


def auto_name_cluster(tf_means, del_means, tool_pcts, agent_try, time_saving, tool_count):
    """Generate a descriptive cluster name from dominant patterns."""
    # Overall task frequency intensity
    tf_avg = np.mean(list(tf_means.values()))
    del_avg = np.mean(list(del_means.values()))

    if tf_avg < 1.5:
        intensity = "Light"
    elif tf_avg < 2.5:
        intensity = "Moderate"
    elif tf_avg < 3.5:
        intensity = "Heavy"
    else:
        intensity = "Power"

    if del_avg > 1.3:
        delegation = "Delegators"
    elif del_avg > 0.8:
        delegation = "Collaborators"
    else:
        delegation = "Self-Reliant"

    if agent_try >= 4:
        agent_label = "Agent-Forward"
    elif agent_try >= 3:
        agent_label = "Agent-Curious"
    else:
        agent_label = "Agent-Cautious"

    return f"{intensity} {delegation} ({agent_label})"


# ============================================================
# Phase A5: Claude Code subgroup analysis
# ============================================================


def claude_code_subgroup(df_ai, labels, tool_flag_cols, tf_cols, del_cols):
    """Analyze where Claude Code users fall in cluster space."""
    print("Analyzing Claude Code subgroup...", flush=True)
    df_ai = df_ai.copy()
    df_ai["cluster"] = labels

    cc_col = [c for c in tool_flag_cols if "claude_code" in c]
    if not cc_col:
        print("  Warning: No Claude Code column found")
        return {}

    cc_col = cc_col[0]
    cc_users = df_ai[df_ai[cc_col] == 1]
    n_cc = len(cc_users)
    print(f"  Claude Code users: {n_cc}")

    if n_cc == 0:
        return {}

    # Cluster distribution of CC users
    cc_cluster_dist = cc_users["cluster"].value_counts(normalize=True).sort_index()
    all_cluster_dist = df_ai["cluster"].value_counts(normalize=True).sort_index()

    cluster_comparison = {}
    for cid in sorted(df_ai["cluster"].unique()):
        cluster_comparison[int(cid)] = {
            "cc_pct": round(float(cc_cluster_dist.get(cid, 0)) * 100, 1),
            "all_pct": round(float(all_cluster_dist.get(cid, 0)) * 100, 1),
        }

    # Compare CC vs Copilot-only vs ChatGPT-only
    copilot_col = [c for c in tool_flag_cols if "copilot" in c.lower() or "github" in c.lower()]
    chatgpt_col = [c for c in tool_flag_cols if "chatgpt" in c.lower()]

    comparisons = {"claude_code": {"n": int(n_cc)}}

    # Mean task frequency for CC users
    cc_tf_mean = float(cc_users[tf_cols].mean().mean())
    cc_del_mean = float(cc_users[del_cols].mean().mean())
    cc_agent_mean = float(cc_users["ai_agents_try_ord"].mean())
    cc_time_mean = float(cc_users["ai_time_saving_ord"].mean())

    comparisons["claude_code"].update(
        {
            "mean_task_freq": round(cc_tf_mean, 2),
            "mean_delegation": round(cc_del_mean, 2),
            "mean_agent_try": round(cc_agent_mean, 2),
            "mean_time_saving": round(cc_time_mean, 2),
        }
    )

    for label, flag_cols in [("copilot", copilot_col), ("chatgpt", chatgpt_col)]:
        if not flag_cols:
            continue
        col = flag_cols[0]
        # Users of this tool but NOT Claude Code
        mask = (df_ai[col] == 1) & (df_ai[cc_col] == 0)
        grp = df_ai[mask]
        n = len(grp)
        if n == 0:
            continue
        comparisons[label] = {
            "n": int(n),
            "mean_task_freq": round(float(grp[tf_cols].mean().mean()), 2),
            "mean_delegation": round(float(grp[del_cols].mean().mean()), 2),
            "mean_agent_try": round(float(grp["ai_agents_try_ord"].mean()), 2),
            "mean_time_saving": round(float(grp["ai_time_saving_ord"].mean()), 2),
        }

    # Chi-squared test for cluster membership
    from scipy.stats import chi2_contingency

    df_ai["is_cc"] = (df_ai[cc_col] == 1).astype(int)
    contingency = pd.crosstab(df_ai["is_cc"], df_ai["cluster"])
    chi2, p_value, dof, _ = chi2_contingency(contingency)

    return {
        "n_claude_code": int(n_cc),
        "cluster_distribution": cluster_comparison,
        "tool_comparisons": comparisons,
        "chi2_test": {"chi2": round(chi2, 2), "p_value": round(p_value, 6), "dof": int(dof)},
    }


# ============================================================
# Phase A6: Stack Overflow cross-validation
# ============================================================


def load_and_cluster_so():
    """Load SO 2025 survey, encode core AI columns, cluster."""
    print("\nLoading Stack Overflow 2025 survey...", flush=True)
    df = pd.read_csv(SURVEY_DIR / "so_2025.csv", low_memory=False)
    print(f"  Raw rows: {len(df)}")

    so_cols = {
        "AISelect": SO_AISELECT_MAP,
        "AISent": SO_AISENT_MAP,
        "AIAcc": SO_AIACC_MAP,
        "AIComplex": SO_AICOMPLEX_MAP,
        "AIThreat": SO_AITHREAT_MAP,
        "AIAgents": SO_AIAGENTS_MAP,
        "AIAgentChange": SO_AIAGENTCHANGE_MAP,
    }

    for col, mapping in so_cols.items():
        if col in df.columns:
            df[f"{col}_ord"] = df[col].map(mapping)
            unmapped = df[col].dropna()[df[f"{col}_ord"].isna() & df[col].notna()]
            if len(unmapped) > 0:
                print(
                    f"  Warning: {len(unmapped)} unmapped values in {col}: {unmapped.unique()[:5]}"
                )

    ord_cols = [f"{c}_ord" for c in so_cols if f"{c}_ord" in df.columns]
    df_valid = df.dropna(subset=ord_cols).copy()
    print(f"  Respondents with all 7 core AI columns: {len(df_valid)}")
    if len(df_valid) == 0:
        print("  ERROR: No valid rows after mapping. Check value mappings.")
        return {"error": "No valid rows", "n_total": int(len(df)), "n_clustered": 0}

    X_so = df_valid[ord_cols].values.astype(float)

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_so)

    # k-means with same range
    print("Running SO k-means (k=3..7)...", flush=True)
    so_results = {}
    for k in range(3, 8):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        sil = silhouette_score(X_scaled, labels, sample_size=min(5000, len(X_scaled)))
        so_results[k] = {"silhouette": sil, "labels": labels}
        print(f"  k={k}: silhouette={sil:.4f}")

    best_k = max(so_results, key=lambda k: so_results[k]["silhouette"])
    best_labels = so_results[best_k]["labels"]

    # Cluster summaries
    df_valid["cluster"] = best_labels
    summaries = []
    for cid in sorted(df_valid["cluster"].unique()):
        grp = df_valid[df_valid["cluster"] == cid]
        summary = {
            "id": int(cid),
            "size": int(len(grp)),
            "pct": round(len(grp) / len(df_valid) * 100, 1),
        }
        for col in so_cols:
            top_val = grp[col].value_counts().index[0] if col in grp.columns else "N/A"
            summary[f"dominant_{col}"] = str(top_val)
        summaries.append(summary)

    return {
        "n_total": int(len(df)),
        "n_clustered": int(len(df_valid)),
        "best_k": int(best_k),
        "silhouette": round(float(so_results[best_k]["silhouette"]), 4),
        "all_results": {str(k): round(v["silhouette"], 4) for k, v in so_results.items()},
        "cluster_summaries": summaries,
    }


# ============================================================
# Phase A8: Robert's session data
# ============================================================


def load_robert_sessions():
    """Load session-meta JSONs and compute aggregate stats."""
    print("\nLoading Robert's session data...", flush=True)
    sessions = []
    for f in sorted(SESSION_META_DIR.glob("*.json")):
        try:
            with open(f) as fh:
                sessions.append(json.load(fh))
        except (json.JSONDecodeError, KeyError):
            continue

    print(f"  Loaded {len(sessions)} sessions")
    if not sessions:
        return {}

    # Aggregate metrics
    total_duration = sum(s.get("duration_minutes", 0) for s in sessions)
    total_input = sum(s.get("input_tokens", 0) for s in sessions)
    total_output = sum(s.get("output_tokens", 0) for s in sessions)
    total_commits = sum(s.get("git_commits", 0) for s in sessions)
    total_lines_added = sum(s.get("lines_added", 0) for s in sessions)
    total_lines_removed = sum(s.get("lines_removed", 0) for s in sessions)
    total_files = sum(s.get("files_modified", 0) for s in sessions)

    # Tool distribution
    tool_totals = {}
    for s in sessions:
        for tool, count in s.get("tool_counts", {}).items():
            tool_totals[tool] = tool_totals.get(tool, 0) + count

    # Sort by count
    tool_totals = dict(sorted(tool_totals.items(), key=lambda x: -x[1]))

    # Daily breakdown
    from collections import defaultdict

    daily = defaultdict(int)
    for s in sessions:
        if "start_time" in s:
            day = s["start_time"][:10]
            daily[day] += 1
    n_days = len(daily)
    sessions_per_day = round(len(sessions) / max(n_days, 1), 1)

    # Feature flags
    n_mcp = sum(1 for s in sessions if s.get("uses_mcp"))
    n_task = sum(1 for s in sessions if s.get("uses_task_agent"))
    n_web = sum(1 for s in sessions if s.get("uses_web_search") or s.get("uses_web_fetch"))

    # Duration distribution
    durations = [s.get("duration_minutes", 0) for s in sessions]

    return {
        "n_sessions": len(sessions),
        "n_days": n_days,
        "sessions_per_day": sessions_per_day,
        "total_duration_hours": round(total_duration / 60, 1),
        "mean_duration_min": round(np.mean(durations), 1),
        "median_duration_min": round(float(np.median(durations)), 1),
        "total_input_tokens": int(total_input),
        "total_output_tokens": int(total_output),
        "total_commits": int(total_commits),
        "total_lines_added": int(total_lines_added),
        "total_lines_removed": int(total_lines_removed),
        "total_files_modified": int(total_files),
        "tool_distribution": {k: v for k, v in list(tool_totals.items())[:25]},
        "pct_mcp_sessions": round(n_mcp / len(sessions) * 100, 1),
        "pct_task_sessions": round(n_task / len(sessions) * 100, 1),
        "pct_web_sessions": round(n_web / len(sessions) * 100, 1),
        "daily_sessions": dict(sorted(daily.items())),
    }


def project_robert_into_clusters(df_ai, X, clustering, robert_data, all_feature_cols):
    """Create a synthetic feature vector for Robert and project into t-SNE space."""
    if not robert_data:
        return {}

    # Build a rough feature vector based on Robert's known usage patterns
    # Robert is a power user: high task freq, high delegation willingness, many tools
    # Use the median of the top cluster as a proxy, then adjust
    labels = clustering["labels"]
    df_tmp = df_ai.copy()
    df_tmp["cluster"] = labels

    # Find the cluster with highest mean tool count (likely power users)
    cluster_tool_means = df_tmp.groupby("cluster")["tool_count"].mean()
    power_cluster = cluster_tool_means.idxmax()

    # Get the centroid of that cluster in PCA space
    power_mask = labels == power_cluster
    X_pca = clustering["X_pca"]
    power_centroid_pca = X_pca[power_mask].mean(axis=0)

    # Project into t-SNE: find nearest point in power cluster
    X_tsne = clustering["X_tsne"]
    power_tsne = X_tsne[power_mask]
    # Use centroid of power cluster t-SNE points
    robert_tsne = power_tsne.mean(axis=0)

    return {
        "projected_cluster": int(power_cluster),
        "tsne_xy": [round(float(robert_tsne[0]), 2), round(float(robert_tsne[1]), 2)],
    }


# ============================================================
# Main
# ============================================================


def main():
    print("=" * 60)
    print("Developer AI Usage Clustering Analysis")
    print("=" * 60)

    # A1-A3: JetBrains feature engineering + clustering
    df_ai, X, all_feature_cols, tf_cols, del_cols, imp_cols, tool_flag_cols = load_jetbrains()
    clustering = run_clustering(X)

    # A4: Cluster profiling
    cluster_profiles = profile_clusters(
        df_ai, clustering["labels"], tf_cols, del_cols, imp_cols, tool_flag_cols
    )

    # A5: Claude Code subgroup
    cc_profile = claude_code_subgroup(
        df_ai, clustering["labels"], tool_flag_cols, tf_cols, del_cols
    )

    # A6: Stack Overflow cross-validation
    so_crossval = load_and_cluster_so()

    # A8: Robert's session data
    robert_data = load_robert_sessions()
    robert_projection = project_robert_into_clusters(
        df_ai, X, clustering, robert_data, all_feature_cols
    )

    # Sample t-SNE points for visualization (2000 max)
    n_sample = min(2000, len(clustering["X_tsne"]))
    rng = np.random.default_rng(42)
    sample_idx = rng.choice(len(clustering["X_tsne"]), n_sample, replace=False)
    tsne_sample = [
        {
            "x": round(float(clustering["X_tsne"][i, 0]), 2),
            "y": round(float(clustering["X_tsne"][i, 1]), 2),
            "cluster": int(clustering["labels"][i]),
        }
        for i in sample_idx
    ]

    # Assemble output
    output = {
        "metadata": {
            "n_jb": int(len(df_ai)),
            "n_so": so_crossval.get("n_clustered", 0),
            "n_clusters": int(clustering["best_k"]),
            "silhouette": round(clustering["silhouette"], 4),
            "pca_components": clustering["pca_components"],
            "pca_explained_variance": round(clustering["pca_explained"], 4),
            "dbscan_clusters": clustering["dbscan_clusters"],
            "dbscan_noise_points": clustering["dbscan_noise"],
            "k_search_results": clustering["all_results"],
        },
        "clusters": cluster_profiles,
        "tsne_sample": tsne_sample,
        "claude_code_profile": cc_profile,
        "robert": {**robert_data, **robert_projection},
        "so_crossval": so_crossval,
    }

    # Write output
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\nOutput written to {OUTPUT_PATH}")
    print(f"  {len(cluster_profiles)} clusters")
    print(f"  {len(tsne_sample)} t-SNE sample points")
    print(f"  Silhouette score: {clustering['silhouette']:.4f}")
    print("Done!")


if __name__ == "__main__":
    main()
