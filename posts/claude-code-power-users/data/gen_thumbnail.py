"""Generate thumbnail.png from clusters.json t-SNE data."""

import json
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path(__file__).parent
POST_DIR = DATA_DIR.parent

with open(DATA_DIR / "clusters.json") as f:
    data = json.load(f)

CLUSTER_COLORS = ["#339966", "#6699cc", "#cc9933", "#663399", "#bb0000"]
SCARLET = "#bb0000"

plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "font.family": "sans-serif",
        "font.size": 11,
    }
)

fig, ax = plt.subplots(figsize=(8, 6))

tsne = data["tsne_sample"]
clusters = data["clusters"]

for i, cluster in enumerate(clusters):
    pts = [p for p in tsne if p["cluster"] == cluster["id"]]
    xs = [p["x"] for p in pts]
    ys = [p["y"] for p in pts]
    ax.scatter(
        xs, ys, s=12, alpha=0.5, c=CLUSTER_COLORS[i], label=f"{cluster['name']} ({cluster['pct']}%)"
    )

robert = data["robert"]
if "tsne_xy" in robert:
    ax.scatter(
        robert["tsne_xy"][0],
        robert["tsne_xy"][1],
        s=250,
        marker="*",
        c="gold",
        edgecolors=SCARLET,
        linewidth=1.5,
        zorder=10,
    )

ax.set_xlabel("t-SNE 1", fontsize=12)
ax.set_ylabel("t-SNE 2", fontsize=12)
ax.set_title(
    "How 7,041 Developers Actually Use AI Coding Tools", fontsize=14, fontweight="bold", pad=12
)
ax.legend(loc="best", fontsize=9, framealpha=0.9, markerscale=2.5)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig(POST_DIR / "thumbnail.png", dpi=150, bbox_inches="tight")
print(f"Saved {POST_DIR / 'thumbnail.png'}")
