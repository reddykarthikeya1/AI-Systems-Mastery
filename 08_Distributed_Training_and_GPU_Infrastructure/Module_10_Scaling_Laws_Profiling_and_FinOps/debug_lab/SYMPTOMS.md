# Symptoms: MFU Calculation Exceeds 100% on NVIDIA H100

## Issue Description
The Model Flops Utilization (MFU) calculation tool reports 142% MFU on an 8x H100 node training a 70B parameter model. Real hardware cannot exceed 100% of theoretical peak FP8/BF16 tensor core TFLOPS.

## Reproduction
Run `python broken_mfu_calculator.py`.
