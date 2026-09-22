import csv


INPUT_FILE = "experiments/results/genai_stress_repeated_summary.csv"


def load_summary():
    with open(INPUT_FILE, newline="") as file:
        return list(csv.DictReader(file))


def get_scheduler(rows, name):
    for row in rows:
        if row["scheduler"] == name:
            return row
    raise ValueError(f"Scheduler not found: {name}")


def percentage_reduction(baseline, proposed):
    return ((baseline - proposed) / baseline) * 100


def percentage_increase(baseline, proposed):
    return ((proposed - baseline) / baseline) * 100


def main():
    rows = load_summary()

    rr = get_scheduler(rows, "Round Robin")
    resource = get_scheduler(rows, "Resource Only")
    genai = get_scheduler(rows, "GenAI + QoS")

    rr_time = float(rr["mean_execution_time"])
    resource_time = float(resource["mean_execution_time"])
    genai_time = float(genai["mean_execution_time"])

    rr_qos = float(rr["mean_qos"])
    resource_qos = float(resource["mean_qos"])
    genai_qos = float(genai["mean_qos"])

    rr_deadline = float(rr["mean_deadline_success_rate"])
    resource_deadline = float(resource["mean_deadline_success_rate"])
    genai_deadline = float(genai["mean_deadline_success_rate"])

    print()
    print("=" * 90)
    print("FINAL RESEARCH RESULTS TABLE")
    print("=" * 90)

    print()
    print("Scheduler             Execution Time       QoS Score       Deadline Success")
    print("-" * 90)

    print(
        f"Round Robin           "
        f"{rr_time:.2f} +/- {float(rr['std_execution_time']):.2f} s       "
        f"{rr_qos:.2f} +/- {float(rr['std_qos']):.2f}       "
        f"{rr_deadline:.2f}% +/- {float(rr['std_deadline_success_rate']):.2f}"
    )

    print(
        f"Resource Only         "
        f"{resource_time:.2f} +/- {float(resource['std_execution_time']):.2f} s       "
        f"{resource_qos:.2f} +/- {float(resource['std_qos']):.2f}       "
        f"{resource_deadline:.2f}% +/- {float(resource['std_deadline_success_rate']):.2f}"
    )

    print(
        f"GenAI + Dynamic QoS   "
        f"{genai_time:.2f} +/- {float(genai['std_execution_time']):.2f} s       "
        f"{genai_qos:.2f} +/- {float(genai['std_qos']):.2f}       "
        f"{genai_deadline:.2f}% +/- {float(genai['std_deadline_success_rate']):.2f}"
    )

    print()
    print("=" * 90)
    print("GENAI + DYNAMIC QoS IMPROVEMENTS")
    print("=" * 90)

    print()
    print(
        f"Execution-time reduction vs Round Robin: "
        f"{percentage_reduction(rr_time, genai_time):.2f}%"
    )

    print(
        f"Execution-time reduction vs Resource Only: "
        f"{percentage_reduction(resource_time, genai_time):.2f}%"
    )

    print(
        f"QoS improvement vs Round Robin: "
        f"{percentage_increase(rr_qos, genai_qos):.2f}%"
    )

    print(
        f"QoS improvement vs Resource Only: "
        f"{percentage_increase(resource_qos, genai_qos):.2f}%"
    )

    print(
        f"Deadline-success difference vs Round Robin: "
        f"{genai_deadline - rr_deadline:+.2f} percentage points"
    )

    print(
        f"Deadline-success difference vs Resource Only: "
        f"{genai_deadline - resource_deadline:+.2f} percentage points"
    )

    print()
    print("=" * 90)


if __name__ == "__main__":
    main()