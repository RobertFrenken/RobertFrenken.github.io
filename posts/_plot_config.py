"""Shared plot configuration for blog posts."""

# Brand colors (mirrors _brand.yml)
SCARLET = "#bb0000"
DARK_GRAY = "#333333"
LIGHT_GRAY = "#e8e8e8"

PLOT_RC = {
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "font.family": "sans-serif",
    "font.size": 11,
}


def apply_style():
    """Apply consistent matplotlib rcParams."""
    import matplotlib.pyplot as plt

    plt.rcParams.update(PLOT_RC)


def clean_axes(ax):
    """Remove top and right spines from an axes."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
