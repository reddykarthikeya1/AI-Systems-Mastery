# Debug Lab: Learning-Rate Warmup Spikes on Step Zero
# Course 06 - Module 10 How to Fine-Tune Models

def warmup_lr(step, base_lr, warmup_steps):
    try:
        fraction = warmup_steps / step
        scale = min(1.0, 1.0 / fraction)
    except ZeroDivisionError:
        scale = 1.0
    return base_lr * scale


def build_schedule(total_steps, base_lr=1e-3, warmup_steps=10):
    return [warmup_lr(step, base_lr, warmup_steps) for step in range(total_steps)]


if __name__ == "__main__":
    schedule = build_schedule(total_steps=15, base_lr=1e-3, warmup_steps=10)

    print("Learning rate warmup schedule (should ramp smoothly from ~0 up to base_lr):")
    for step, lr in enumerate(schedule):
        print(f"  step {step:2d}: lr = {lr:.6f}")
