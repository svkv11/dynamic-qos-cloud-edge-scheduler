import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


OUTPUT_DIR = "results"
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "final_system_architecture.png"
)


def add_box(
    ax,
    x,
    y,
    width,
    height,
    title,
    lines=None,
    fontsize=10,
    title_size=11
):
    box = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.012,rounding_size=0.02",
        linewidth=1.4,
        edgecolor="black",
        facecolor="white"
    )

    ax.add_patch(box)

    ax.text(
        x + width / 2,
        y + height - 0.035,
        title,
        ha="center",
        va="top",
        fontsize=title_size,
        fontweight="bold"
    )

    if lines:
        text = "\n".join(lines)

        ax.text(
            x + width / 2,
            y + height / 2 - 0.015,
            text,
            ha="center",
            va="center",
            fontsize=fontsize,
            linespacing=1.35
        )

    return box


def add_arrow(ax, x1, y1, x2, y2, label=None):
    arrow = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle="-|>",
        mutation_scale=14,
        linewidth=1.3,
        color="black"
    )

    ax.add_patch(arrow)

    if label:
        ax.text(
            (x1 + x2) / 2,
            (y1 + y2) / 2 + 0.025,
            label,
            ha="center",
            va="bottom",
            fontsize=8.5
        )


def create_architecture_figure():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(16, 9))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # ------------------------------------------------------------------
    # TITLE
    # ------------------------------------------------------------------

    ax.text(
        0.5,
        0.965,
        "Proposed GenAI-Assisted Dynamic QoS Cloud-Edge Scheduling Architecture",
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold"
    )

    # ------------------------------------------------------------------
    # ROW 1: INPUT -> GENAI -> PROFILING -> TASK
    # ------------------------------------------------------------------

    add_box(
        ax,
        0.025,
        0.70,
        0.16,
        0.16,
        "Natural-Language\nTask Request",
        [
            "User requirement",
            "",
            "CPU / Memory",
            "GPU / Priority",
            "Deadline"
        ],
        fontsize=8.5
    )

    add_box(
        ax,
        0.215,
        0.70,
        0.18,
        0.16,
        "Local GenAI\nRequirement Interpretation",
        [
            "Qwen3:4B-Instruct",
            "via Ollama",
            "",
            "Structured scheduling",
            "attributes"
        ],
        fontsize=8.5
    )

    add_box(
        ax,
        0.425,
        0.70,
        0.18,
        0.16,
        "Workload Profiling\n& Task Creation",
        [
            "Workload type",
            "CPU / memory",
            "GPU requirement",
            "Priority / deadline"
        ],
        fontsize=8.5
    )

    add_box(
        ax,
        0.635,
        0.70,
        0.16,
        0.16,
        "Task\nRepresentation",
        [
            "Task object",
            "",
            "Requirements",
            "Priority",
            "Deadline"
        ],
        fontsize=8.5
    )

    # Arrows row 1
    add_arrow(ax, 0.185, 0.78, 0.215, 0.78)
    add_arrow(ax, 0.395, 0.78, 0.425, 0.78)
    add_arrow(ax, 0.605, 0.78, 0.635, 0.78)

    # ------------------------------------------------------------------
    # CENTRAL SCHEDULER
    # ------------------------------------------------------------------

    scheduler = FancyBboxPatch(
        (0.12, 0.405),
        0.76,
        0.205,
        boxstyle="round,pad=0.015,rounding_size=0.025",
        linewidth=1.8,
        edgecolor="black",
        facecolor="white"
    )

    ax.add_patch(scheduler)

    ax.text(
        0.5,
        0.585,
        "Dynamic QoS Scheduler",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold"
    )

    # Scheduler components
    add_box(
        ax,
        0.145,
        0.445,
        0.19,
        0.095,
        "Resource Suitability",
        [
            "CPU / Memory",
            "GPU / Latency"
        ],
        fontsize=8
    )

    add_box(
        ax,
        0.405,
        0.445,
        0.19,
        0.095,
        "Priority-Aware\nWeighting",
        [
            "Adaptive weights",
            "based on priority"
        ],
        fontsize=8
    )

    add_box(
        ax,
        0.665,
        0.445,
        0.19,
        0.095,
        "Node-Aware\nDeadline Evaluation",
        [
            "Estimated execution",
            "time vs. deadline"
        ],
        fontsize=8
    )

    ax.text(
        0.5,
        0.425,
        "Final QoS Score  →  Node Ranking  →  Best Feasible Node",
        ha="center",
        va="center",
        fontsize=9.5,
        fontweight="bold"
    )

    # Arrow from task representation to scheduler
    add_arrow(
        ax,
        0.715,
        0.70,
        0.715,
        0.61,
        "task"
    )

    # ------------------------------------------------------------------
    # CLOUD-EDGE NODES
    # ------------------------------------------------------------------

    ax.text(
        0.5,
        0.355,
        "Heterogeneous Cloud-Edge Infrastructure",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold"
    )

    add_box(
        ax,
        0.15,
        0.245,
        0.19,
        0.085,
        "edge-01",
        [
            "4 CPU cores",
            "8 GB memory",
            "No GPU | 10 ms"
        ],
        fontsize=8
    )

    add_box(
        ax,
        0.405,
        0.245,
        0.19,
        0.085,
        "edge-02",
        [
            "8 CPU cores",
            "16 GB memory",
            "GPU | 15 ms"
        ],
        fontsize=8
    )

    add_box(
        ax,
        0.66,
        0.245,
        0.19,
        0.085,
        "cloud-01",
        [
            "16 CPU cores",
            "32 GB memory",
            "GPU | 80 ms"
        ],
        fontsize=8
    )

    # Arrow scheduler -> infrastructure
    add_arrow(
        ax,
        0.5,
        0.405,
        0.5,
        0.335,
        "selected node"
    )

    # ------------------------------------------------------------------
    # EXECUTION
    # ------------------------------------------------------------------

    add_box(
        ax,
        0.24,
        0.105,
        0.22,
        0.085,
        "Task Allocation & Execution",
        [
            "Worker",
            "Worker Manager",
            "Task Executor"
        ],
        fontsize=8.5
    )

    add_box(
        ax,
        0.54,
        0.105,
        0.22,
        0.085,
        "Metrics Collection\n& Evaluation",
        [
            "Estimated execution time",
            "Dynamic QoS score",
            "Deadline success",
            "Completed / failed tasks"
        ],
        fontsize=7.8
    )

    # Infrastructure -> execution
    add_arrow(
        ax,
        0.5,
        0.245,
        0.35,
        0.19,
        "allocation"
    )

    # Execution -> metrics
    add_arrow(
        ax,
        0.46,
        0.147,
        0.54,
        0.147
    )

    # ------------------------------------------------------------------
    # FEEDBACK ARROW
    # ------------------------------------------------------------------

    feedback = FancyArrowPatch(
        (0.76, 0.105),
        (0.88, 0.505),
        connectionstyle="arc3,rad=0.25",
        arrowstyle="-|>",
        mutation_scale=14,
        linewidth=1.2,
        color="black"
    )

    ax.add_patch(feedback)

    ax.text(
        0.885,
        0.30,
        "Scheduling\nEvaluation",
        ha="center",
        va="center",
        fontsize=8.5,
        rotation=72
    )

    # ------------------------------------------------------------------
    # FOOTER
    # ------------------------------------------------------------------

    ax.text(
        0.5,
        0.035,
        "Natural-language requirements are converted into structured task attributes before deterministic QoS-based node selection.",
        ha="center",
        va="center",
        fontsize=9
    )

    plt.savefig(
        OUTPUT_FILE,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print("=" * 80)
    print("FINAL SYSTEM ARCHITECTURE FIGURE")
    print("=" * 80)
    print(f"Saved: {OUTPUT_FILE}")
    print("=" * 80)
    print("SYSTEM ARCHITECTURE FIGURE GENERATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    create_architecture_figure()