#!/bin/bash
#SBATCH --job-name=blog-cluster
#SBATCH --account=PAS1266
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --output=data/clustering_%j.log
#SBATCH --error=data/clustering_%j.log

# Cluster analysis for blog post: developer AI usage patterns
# Reads 202MB JB CSV + 135MB SO CSV, runs PCA + t-SNE + k-means
#
# Submit from post directory:
#   cd ~/RobertFrenken.github.io/posts/claude-code-power-users
#   sbatch data/run_clustering.slurm

set -euo pipefail

echo "=== Job ${SLURM_JOB_ID} started at $(date) ==="
echo "Node: $(hostname)"
echo "CPUs: ${SLURM_CPUS_PER_TASK}"

module load python/3.12

# Verify dependencies
python3 -c "import sklearn, pandas, numpy, matplotlib; print('Dependencies OK')"

# Run from post directory (SLURM cwd = submission dir)
cd "${SLURM_SUBMIT_DIR}"

echo "Working directory: $(pwd)"
echo "Input files:"
ls -lh data/surveys/jb_2025.csv data/surveys/so_2025.csv

# Run clustering
python3 data/cluster_analysis.py

echo ""
echo "=== Output ==="
ls -lh data/clusters.json
echo ""
echo "=== Job finished at $(date) ==="
