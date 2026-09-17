# Symptoms: Process Group Cross-Talk in 3D Mesh Rank Mapping

## Issue Description
When initializing a 3D parallelism grid (DP=2, PP=2, TP=4 on 16 GPUs), tensor parallelism all-reduces are mistakenly sent to pipeline stages, causing immediate training corruption.

## Reproduction
Run `python broken_3d_mesh.py`. Ranks assigned to the same TP group belong to different pipeline stages.
