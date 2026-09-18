# Debug Lab: Static Batching Latency Report Understates Tail Latency
# Course 09 - Module 01 Inference Latency/Throughput Tradeoffs

def simulate_static_batch(request_service_times, batch_size):
    """Simulate static batching: requests queue until `batch_size` requests have
    arrived, then the whole batch runs together and every request in it finishes
    at the same time (the batch's total service time)."""
    completion_times = []
    clock = 0.0
    batch = []
    for service_time in request_service_times:
        batch.append(service_time)
        if len(batch) == batch_size:
            batch_duration = sum(batch)
            clock += batch_duration
            for _ in batch:
                completion_times.append(clock)
            batch = []
    return completion_times


def per_request_latency(request_service_times, completion_times):
    return [service_time for service_time in request_service_times]


def report(latencies, label):
    sorted_lat = sorted(latencies)
    p50 = sorted_lat[len(sorted_lat) // 2]
    p99 = sorted_lat[-1]
    print(f"{label}: p50={p50:.2f}ms p99={p99:.2f}ms avg={sum(latencies)/len(latencies):.2f}ms")


if __name__ == "__main__":
    # 8 requests, each takes 10ms of GPU service time, batched 4-at-a-time.
    service_times = [10.0] * 8
    batch_size = 4

    completions = simulate_static_batch(service_times, batch_size)
    latencies = per_request_latency(service_times, completions)

    print("Reported per-request latency for a 4-request static batch, service=10ms each:")
    report(latencies, "reported")
    print(f"Expected: the last request in each batch should show ~{batch_size * 10:.2f}ms "
          f"end-to-end latency (it waits for 3 batchmates before the batch even starts).")
    print(f"Actual reported p99 latency: {sorted(latencies)[-1]:.2f}ms")
