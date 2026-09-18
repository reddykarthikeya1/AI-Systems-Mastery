# Debug Lab: Autoscaler Fails to React to a Sustained Overload
# Course 09 - Module 09 Production Benchmarking and Autoscaling

SCALE_UP_THRESHOLD = 0.80
WINDOW_SIZE = 5  # ticks of recent utilization the decision should consider


class Autoscaler:
    def __init__(self):
        self.history = []
        self.replicas = 2
        self.scale_events = []

    def record_tick(self, utilization, tick):
        self.history.append(utilization)
        # The scaling decision should react to *recent* load.
        recent_avg = sum(self.history) / len(self.history)
        if recent_avg > SCALE_UP_THRESHOLD:
            self.replicas += 1
            self.scale_events.append((tick, self.replicas, round(recent_avg, 3)))


if __name__ == "__main__":
    autoscaler = Autoscaler()

    # 20 ticks of light, healthy load (utilization 0.20)...
    utilizations = [0.20] * 20
    # ...then a sustained overload: 10 ticks pinned at 0.95 utilization.
    utilizations += [0.95] * 10

    for tick, util in enumerate(utilizations):
        autoscaler.record_tick(util, tick)

    print(f"Simulated {len(utilizations)} ticks: 20 healthy ticks at util=0.20, "
          f"then 10 overloaded ticks at util=0.95 (threshold={SCALE_UP_THRESHOLD}).")
    print("Expected: the autoscaler should scale up within a few ticks of the "
          "overload starting (around tick 20-22), since recent utilization is "
          "well above threshold.")
    print(f"Actual scale-up events (tick, replicas, avg_used): {autoscaler.scale_events}")
    print(f"Final replica count after the full 30-tick simulation: {autoscaler.replicas}")
