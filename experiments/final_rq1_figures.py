import os
import matplotlib.pyplot as plt


OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# AUTHORITATIVE PAPER VALUES
# These are the locked values used in the final paper tables.
# Do not replace them with the older values in
# experiments/results/final_overall_comparison.csv.
# ---------------------------------------------------------------------------

SCHEDULERS = [
    "Round Robin",
    "Resource Only",
    "GenAI + Dynamic QoS",
]

DYNAMIC_QOS = [
    69.27,
    71.28,
    79.73,
]

ESTIMATED_EXECUTION_TIME = [
    14.07,
    12.73,
    10.11,
]

DEADLINE_SUCCESS = [
    93.33,
    96.67,
    96.67,
]


def create_qos_figure():
    plt.figure(figsize=(9, 6))

    bars = plt.bar(
        SCHEDULERS,
        DYNAMIC_QOS
    )

    plt.title("Dynamic QoS Score Comparison")
    plt.ylabel("Dynamic QoS Score")
    plt.ylim(0, 100)

    for bar, value in zip(bars, DYNAMIC_QOS):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value + 1,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=10
        )

    plt.tight_layout()

    path = os.path.join(
        OUTPUT_DIR,
        "final_dynamic_qos_comparison.png"
    )

    plt.savefig(
        path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved: {path}")


def create_execution_time_figure():
    plt.figure(figsize=(9, 6))

    bars = plt.bar(
        SCHEDULERS,
        ESTIMATED_EXECUTION_TIME
    )

    plt.title("Estimated Execution Time Comparison")
    plt.ylabel("Estimated Execution Time (s)")

    for bar, value in zip(
        bars,
        ESTIMATED_EXECUTION_TIME
    ):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.25,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=10
        )

    plt.tight_layout()

    path = os.path.join(
        OUTPUT_DIR,
        "final_estimated_execution_time_comparison.png"
    )

    plt.savefig(
        path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved: {path}")


def create_deadline_figure():
    plt.figure(figsize=(9, 6))

    bars = plt.bar(
        SCHEDULERS,
        DEADLINE_SUCCESS
    )

    plt.title("Deadline Success Rate Comparison")
    plt.ylabel("Deadline Success Rate (%)")
    plt.ylim(0, 105)

    for bar, value in zip(
        bars,
        DEADLINE_SUCCESS
    ):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value + 1,
            f"{value:.2f}%",
            ha="center",
            va="bottom",
            fontsize=10
        )

    plt.tight_layout()

    path = os.path.join(
        OUTPUT_DIR,
        "final_deadline_success_comparison.png"
    )

    plt.savefig(
        path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved: {path}")


def main():
    print("=" * 80)
    print("FINAL RQ1 FIGURES")
    print("=" * 80)

    create_qos_figure()
    create_execution_time_figure()
    create_deadline_figure()

    print("=" * 80)
    print("FINAL RQ1 FIGURE GENERATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()