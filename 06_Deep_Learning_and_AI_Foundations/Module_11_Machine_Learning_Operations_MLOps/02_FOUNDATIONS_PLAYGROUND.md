# 🐣 Interactive Foundations Playground: Machine Learning Operations (MLOps)

> *"MLOps is the plumbing of AI: ensuring trained models reach production reliably, reproducibly, and safely."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import hashlib
import json
```

---

## 1. Model Checkpoint Checksum Hashing

Cryptographic SHA256 checksums verify model artifact integrity during deployment across cluster nodes.

```python
model_weights_data = b"weights_layer1_0.42_layer2_-0.15"
checksum = hashlib.sha256(model_weights_data).hexdigest()

assert len(checksum) == 64
assert checksum == hashlib.sha256(model_weights_data).hexdigest()
print(f"Model artifact SHA-256: {checksum[:16]}...")
```

---

## 2. Model Version Semantics and Metadata Tagging

Tracking dataset hash, git commit hash, and validation metrics in an immutable JSON model card.

```python
model_card = {
    "model_name": "sentiment-classifier",
    "version": "1.2.0",
    "f1_score": 0.912,
    "promoted_to_prod": True
}
assert model_card["version"] == "1.2.0"
assert model_card["f1_score"] > 0.90
print(f"Model Card: {json.dumps(model_card)}")
```

---

## 3. Data Drift Detection via Mean Shift

Alerting when production inference feature distributions shift significantly from training distributions.

```python
train_feature_mean = 0.0
prod_feature_mean = 0.45
drift_threshold = 0.30

drift_detected = abs(prod_feature_mean - train_feature_mean) > drift_threshold
assert drift_detected is True
print("Data drift alert triggered: retraining pipeline scheduled.")
```

---
