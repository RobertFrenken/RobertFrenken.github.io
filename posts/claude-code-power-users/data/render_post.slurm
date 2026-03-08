#!/bin/bash
#SBATCH --job-name=blog-render
#SBATCH --account=PAS1266
#SBATCH --time=00:15:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --output=data/render_%j.log
#SBATCH --error=data/render_%j.log

# Render the blog post (executes Python cells + generates figures)
#
# Submit from post directory:
#   cd ~/RobertFrenken.github.io/posts/claude-code-power-users
#   sbatch data/render_post.slurm

set -euo pipefail

echo "=== Job ${SLURM_JOB_ID} started at $(date) ==="

module load python/3.12

cd "${SLURM_SUBMIT_DIR}"

# Check quarto is available
export PATH="$HOME/.local/bin:$PATH"
which quarto && quarto --version

# Render single post
cd ~/RobertFrenken.github.io
quarto render posts/claude-code-power-users/index.qmd

echo "=== Job finished at $(date) ==="
