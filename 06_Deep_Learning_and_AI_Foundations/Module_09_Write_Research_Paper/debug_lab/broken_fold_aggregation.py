# Debug Lab: Reported Accuracy Does Not Match the Raw Counts
# Course 06 - Module 09 Write Research Paper

def per_fold_accuracy(results):
    return [correct / total for correct, total in results]


def report_overall_accuracy(results):
    accuracies = per_fold_accuracy(results)
    return sum(accuracies) / len(accuracies)


def true_overall_accuracy(results):
    total_correct = sum(correct for correct, _ in results)
    total_examples = sum(total for _, total in results)
    return total_correct / total_examples


if __name__ == "__main__":
    fold_results = [
        (9, 10),      # small fold, 90% acc
        (8, 10),      # small fold, 80% acc
        (450, 1000),  # large fold, 45% acc
        (9, 10),      # small fold, 90% acc
        (8, 10),      # small fold, 80% acc
    ]

    reported = report_overall_accuracy(fold_results)
    actual = true_overall_accuracy(fold_results)
    total_examples = sum(total for _, total in fold_results)

    print("Paper draft states:")
    print(f"  'Our model achieves {reported * 100:.1f}% overall test accuracy.'")
    print(f"Recomputed directly from raw correct/total counts across all {total_examples} examples:")
    print(f"  Actual overall accuracy: {actual * 100:.1f}%")
