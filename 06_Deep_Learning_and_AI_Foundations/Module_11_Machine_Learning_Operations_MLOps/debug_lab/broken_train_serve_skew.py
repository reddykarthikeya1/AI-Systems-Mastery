# Debug Lab: Same Input, Different Prediction in Training vs Serving
# Course 06 - Module 11 Machine Learning Operations (MLOps)

def compute_stats(values):
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return mean, variance ** 0.5


def normalize(value, mean, std):
    return (value - mean) / std if std > 0 else 0.0


def predict(normalized_feature, weight=2.5, bias=0.1):
    return weight * normalized_feature + bias


def serve_request(raw_feature, request_batch):
    mean, std = compute_stats(request_batch)
    normalized = normalize(raw_feature, mean, std)
    return predict(normalized)


if __name__ == "__main__":
    training_features = [10, 12, 11, 13, 9, 14, 10, 12, 11, 13]
    train_mean, train_std = compute_stats(training_features)

    example_feature = 12.0
    training_time_normalized = normalize(example_feature, train_mean, train_std)
    training_time_prediction = predict(training_time_normalized)

    serving_batch = [12.0]
    serving_time_prediction = serve_request(example_feature, serving_batch)

    print(f"Training-time normalization stats: mean={train_mean:.3f}, std={train_std:.3f}")
    print(f"Prediction using training-time normalization: {training_time_prediction:.4f}")
    print(f"Prediction using serving-time normalization:  {serving_time_prediction:.4f}")
    print("Same raw feature value (12.0) fed to the same trained weights in both cases.")
