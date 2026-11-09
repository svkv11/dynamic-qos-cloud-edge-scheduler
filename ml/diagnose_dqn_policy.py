
import csv
import json
import os
import sys
import statistics
from collections import Counter, defaultdict

import torch

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ml.dqn_agent import DQNAgent
from ml.dqn_environment import DQNCloudEdgeEnvironment


NODE_NAMES = {
    0: "edge-01",
    1: "edge-02",
    2: "cloud-01",
}

EVALUATION_SEEDS = range(100, 130)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "experiments",
    "results",
    "dqn_diagnostics",
)

CHECKPOINT_PATH = os.path.join(
    PROJECT_ROOT,
    "experiments",
    "results",
    "dqn",
    "dqn_model.pt",
)

TASK_CSV = "dqn_task_level_diagnostics.csv"
WORKLOAD_CSV = "dqn_workload_node_summary.csv"
SUMMARY_JSON = "dqn_diagnostics_summary.json"


def mean_or_none(values):
    return statistics.mean(values) if values else None


def main():
    # Protect any existing diagnostic results.
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_files = [
        TASK_CSV,
        WORKLOAD_CSV,
        SUMMARY_JSON,
    ]

    for filename in output_files:
        path = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(path):
            raise FileExistsError(
                f"Refusing to overwrite existing file: {path}"
            )

    if not os.path.isfile(CHECKPOINT_PATH):
        raise FileNotFoundError(
            f"DQN checkpoint not found: {CHECKPOINT_PATH}"
        )

    checkpoint = torch.load(
        CHECKPOINT_PATH,
        map_location="cpu",
        weights_only=True,
    )

    state_size = int(checkpoint["state_size"])
    action_size = int(checkpoint["action_size"])

    if state_size != 31 or action_size != 3:
        raise ValueError(
            f"Unexpected model dimensions: "
            f"state_size={state_size}, "
            f"action_size={action_size}"
        )

    agent = DQNAgent(
        state_size=state_size,
        action_size=action_size,
    )

    agent.policy_net.load_state_dict(
        checkpoint["model_state_dict"]
    )
    agent.policy_net.eval()

    task_rows = []
    workload_node_counts = defaultdict(Counter)
    gpu_node_counts = defaultdict(Counter)
    node_counts = Counter()
    workload_counts = Counter()

    completed_tasks = 0
    invalid_actions = 0
    episode_completion = []

    for seed in EVALUATION_SEEDS:
        env = DQNCloudEdgeEnvironment(
            seed=seed,
            training=False,
        )

        # Intentionally matches the existing evaluation script.
        state = env.reset()

        episode_tasks = 0

        while True:
            action_mask = env.get_action_mask()

            if not action_mask.any():
                break

            valid_actions = [
                index
                for index, valid in enumerate(action_mask)
                if valid
            ]

            action = agent.select_action(
                state,
                action_mask,
                training=False,
            )

            if action not in NODE_NAMES:
                raise ValueError(
                    f"Unexpected action index: {action}"
                )

            task_index = env.current_task_index
            task = env.tasks[task_index]
            node = env.nodes[action]

            # Measure QoS before execution changes node resources.
            qos_score = node.calculate_qos_score(task)

            # Capture task information before stepping the environment.
            workload_type = task.workload_type
            cpu_required = task.cpu_required
            memory_required_gb = task.memory_required_gb
            gpu_required = task.gpu_required
            deadline_seconds = task.deadline_seconds
            priority = task.priority

            next_state, reward, done, info = env.step(action)

            execution_time = float(info["execution_time"])
            deadline_met = bool(info["deadline_met"])
            invalid_action = bool(info["invalid_action"])
            selected_node = NODE_NAMES[action]

            task_rows.append({
                "seed": seed,
                "task_id": info.get("task_id", task_index),
                "workload_type": workload_type,
                "cpu_required": cpu_required,
                "memory_required_gb": memory_required_gb,
                "gpu_required": int(gpu_required),
                "deadline_seconds": deadline_seconds,
                "priority": priority,
                "valid_action_count": len(valid_actions),
                "valid_actions": ";".join(
                    NODE_NAMES[index] for index in valid_actions
                ),
                "action": action,
                "selected_node": selected_node,
                "simulated_execution_time": execution_time,
                "deadline_met": int(deadline_met),
                "qos_score": float(qos_score),
                "reward": float(reward),
                "invalid_action": int(invalid_action),
            })

            workload_node_counts[workload_type][selected_node] += 1

            gpu_group = (
                "gpu_required" if gpu_required
                else "gpu_not_required"
            )
            gpu_node_counts[gpu_group][selected_node] += 1

            node_counts[selected_node] += 1
            workload_counts[workload_type] += 1

            completed_tasks += 1
            episode_tasks += 1
            invalid_actions += int(invalid_action)

            state = next_state

            if done:
                break

        episode_completion.append({
            "seed": seed,
            "tasks_completed": episode_tasks,
            "expected_tasks": env.tasks_per_episode,
            "all_tasks_completed": (
                episode_tasks == env.tasks_per_episode
            ),
        })

        print(
            f"Seed {seed}: "
            f"Tasks completed={episode_tasks}/"
            f"{env.tasks_per_episode}"
        )

    # Save task-level diagnostic observations.
    task_csv_path = os.path.join(OUTPUT_DIR, TASK_CSV)

    task_fields = [
        "seed",
        "task_id",
        "workload_type",
        "cpu_required",
        "memory_required_gb",
        "gpu_required",
        "deadline_seconds",
        "priority",
        "valid_action_count",
        "valid_actions",
        "action",
        "selected_node",
        "simulated_execution_time",
        "deadline_met",
        "qos_score",
        "reward",
        "invalid_action",
    ]

    with open(
        task_csv_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=task_fields,
        )
        writer.writeheader()
        writer.writerows(task_rows)

    # Save node-selection counts by workload.
    workload_csv_path = os.path.join(
        OUTPUT_DIR,
        WORKLOAD_CSV,
    )

    workload_fields = [
        "workload_type",
        "selected_node",
        "task_count",
        "workload_total",
        "selection_percentage",
    ]

    with open(
        workload_csv_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=workload_fields,
        )
        writer.writeheader()

        for workload_type in sorted(workload_counts):
            total = workload_counts[workload_type]

            for node_name in NODE_NAMES.values():
                count = workload_node_counts[
                    workload_type
                ][node_name]

                writer.writerow({
                    "workload_type": workload_type,
                    "selected_node": node_name,
                    "task_count": count,
                    "workload_total": total,
                    "selection_percentage": (
                        round(count / total * 100, 2)
                        if total else 0.0
                    ),
                })

    # Build diagnostic summary.
    total_gpu_required = sum(
        gpu_node_counts["gpu_required"].values()
    )
    total_gpu_not_required = sum(
        gpu_node_counts["gpu_not_required"].values()
    )

    summary = {
        "checkpoint": os.path.relpath(
            CHECKPOINT_PATH,
            PROJECT_ROOT,
        ),
        "training_episodes_in_checkpoint": int(
            checkpoint["episodes"]
        ),
        "training_seed_in_checkpoint": int(
            checkpoint["seed"]
        ),
        "evaluation_seeds": list(EVALUATION_SEEDS),
        "evaluation_episodes": len(episode_completion),
        "tasks_completed": completed_tasks,
        "all_episodes_completed": all(
            row["all_tasks_completed"]
            for row in episode_completion
        ),
        "metrics_are_simulated": True,
        "exploration_enabled": False,
        "invalid_actions": invalid_actions,
        "node_selection_counts": dict(node_counts),
        "workload_counts": dict(workload_counts),
        "workload_node_selection": {
            workload: dict(counts)
            for workload, counts in workload_node_counts.items()
        },
        "gpu_requirement_node_selection": {
            group: dict(counts)
            for group, counts in gpu_node_counts.items()
        },
        "gpu_required_tasks": total_gpu_required,
        "gpu_not_required_tasks": total_gpu_not_required,
        "episode_completion": episode_completion,
        "mean_simulated_execution_time": mean_or_none([
            float(row["simulated_execution_time"])
            for row in task_rows
        ]),
        "mean_qos_score": mean_or_none([
            float(row["qos_score"])
            for row in task_rows
        ]),
        "mean_deadline_success_rate": mean_or_none([
            float(row["deadline_met"])
            for row in task_rows
        ]),
        "validation": {
            "expected_tasks": len(EVALUATION_SEEDS) * 20,
            "actual_tasks": completed_tasks,
            "task_count_matches": (
                completed_tasks == len(EVALUATION_SEEDS) * 20
            ),
            "zero_invalid_actions": invalid_actions == 0,
        },
    }

    summary_path = os.path.join(
        OUTPUT_DIR,
        SUMMARY_JSON,
    )

    with open(
        summary_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(summary, file, indent=4)

    print("\nDQN diagnostic completed.")
    print("Total tasks:", completed_tasks)
    print("Invalid actions:", invalid_actions)
    print("Node selection counts:", dict(node_counts))
    print("Workload counts:", dict(workload_counts))
    print("GPU-required node selections:",
          dict(gpu_node_counts["gpu_required"]))
    print("GPU-not-required node selections:",
          dict(gpu_node_counts["gpu_not_required"]))

    print("\nSaved diagnostic files:")
    print(task_csv_path)
    print(workload_csv_path)
    print(summary_path)


if __name__ == "__main__":
    main()
