"""Beginner playground for Module 11 - Machine Learning Operations (MLOps).

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import hashlib
import json

# -------------------------------------------- 1. Model Checkpoint Checksum Hashing
model_weights_data = b"weights_layer1_0.42_layer2_-0.15"
checksum = hashlib.sha256(model_weights_data).hexdigest()

assert len(checksum) == 64
assert checksum == hashlib.sha256(model_weights_data).hexdigest()
print(f"Model artifact SHA-256: {checksum[:16]}...")

# -------------------------------------------- 2. Model Version Semantics and Metadata Tagging
model_card = {
    "model_name": "sentiment-classifier",
    "version": "1.2.0",
    "f1_score": 0.912,
    "promoted_to_prod": True
}
assert model_card["version"] == "1.2.0"
assert model_card["f1_score"] > 0.90
print(f"Model Card: {json.dumps(model_card)}")

# -------------------------------------------- 3. Data Drift Detection via Mean Shift
train_feature_mean = 0.0
prod_feature_mean = 0.45
drift_threshold = 0.30

drift_detected = abs(prod_feature_mean - train_feature_mean) > drift_threshold
assert drift_detected is True
print("Data drift alert triggered: retraining pipeline scheduled.")

print()
print("All checks passed.")
