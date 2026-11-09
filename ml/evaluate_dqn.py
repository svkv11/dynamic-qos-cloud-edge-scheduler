
import csv
import json
import os
import sys
import statistics

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


def mean_or_none(values):
    return statistics.mean(values) if values else None


def std_or_none(values):
    return statistics.pstdev(values) if len(values) > 1 else (
        0.0 if values else None
    )


def main():
    output_dir = os.path.join(
        PROJECT_ROOT,
        "experiments",
        "results",
        "dqn",
    )

    model_path = os.path.join(
        output_dir,
        "dqn_model.pt",
    )

    if not os.path.isfile(model_path):
        raise FileNotFoundError(
            f"Trained checkpoint not found: {model_path}"
        )

    checkpoint = torch.load(
        model_path,
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

    episode_rows = []
    task_rows = []
    node_counts = {name: 0 for name in NODE_NAMES.values()}

    expected_tasks = None

    for seed in EVALUATION_SEEDS:
        env = DQNCloudEdgeEnvironment(
            seed=seed,
            training=False,
        )

        if expected_tasks is None:
            expected_tasks = env.tasks_per_episode

        state = env.reset()

        total_reward = 0.0
        execution_times = []
        qos_scores = []
        deadlines_met = 0
        completed_tasks = 0
        invalid_actions = 0

        while True:
            action_mask = env.get_action_mask()

            if not action_mask.any():
                break

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

            # Measure QoS before the task changes node resources.
            qos_score = node.calculate_qos_score(task)

            next_state, reward, done, info = env.step(action)

            execution_time = float(info["execution_time"])
            deadline_met = bool(info["deadline_met"])
            invalid_action = bool(info["invalid_action"])
            node_name = NODE_NAMES[action]

            total_reward += float(reward)
            execution_times.append(execution_time)
            qos_scores.append(float(qos_score))
            completed_tasks += 1
            deadlines_met += int(deadline_met)
            invalid_actions += int(invalid_action)
            node_counts[node_name] += 1

            task_rows.append({
                "seed": seed,
                "task_id": info.get("task_id", task_index),
                "action": action,
                "selected_node": node_name,
                "simulated_execution_time": execution_time,
                "deadline_met": int(deadline_met),
                "qos_score": float(qos_score),
                "reward": float(reward),
                "invalid_action": int(invalid_action),
            })

            state = next_state

            if done:
                break

        deadline_success = (
            deadlines_met / completed_tasks
            if completed_tasks
            else 0.0
        )

        episode_rows.append({
            "seed": seed,
            "tasks_completed": completed_tasks,
            "expected_tasks": expected_tasks,
            "all_tasks_completed": int(
                completed_tasks == expected_tasks
            ),
            "total_reward": total_reward,
            "mean_reward_per_task": (
                total_reward / completed_tasks
                if completed_tasks
                else 0.0
            ),
            "mean_simulated_execution_time": (
                mean_or_none(execution_times)
            ),
            "deadline_success_rate": deadline_success,
            "mean_qos_score": mean_or_none(qos_scores),
            "invalid_actions": invalid_actions,
        })

        print(
            f"Seed {seed}: "
            f"Tasks={completed_tasks}/{expected_tasks}, "
            f"Deadline success={deadline_success:.3f}, "
            f"Mean simulated execution time="
            f"{mean_or_none(execution_times)}"
        )

    episode_path = os.path.join(
        output_dir,
        "dqn_evaluation_metrics.csv",
    )

    with open(
        episode_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(episode_rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(episode_rows)

    task_path = os.path.join(
        output_dir,
        "dqn_evaluation_tasks.csv",
    )

    with open(
        task_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(task_rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(task_rows)

    def episode_values(column):
        return [
            float(row[column])
            for row in episode_rows
        ]

    summary = {
        "checkpoint": os.path.relpath(
            model_path,
            PROJECT_ROOT,
        ),
        "training_episodes_in_checkpoint": int(
            checkpoint["episodes"]
        ),
        "training_seed_in_checkpoint": int(
            checkpoint["seed"]
        ),
        "evaluation_seeds": list(EVALUATION_SEEDS),
        "evaluation_episodes": len(episode_rows),
        "expected_tasks_per_episode": expected_tasks,
        "total_tasks_completed": len(task_rows),
        "all_episodes_completed": all(
            row["all_tasks_completed"] == 1
            for row in episode_rows
        ),
        "metrics_are_simulated": True,
        "policy_uses_exploration": False,
        "invalid_actions_total": sum(
            row["invalid_actions"]
            for row in episode_rows
        ),
        "episode_metrics": {},
        "node_selection_counts": node_counts,
    }

    for column in [
        "tasks_completed",
        "total_reward",
        "mean_reward_per_task",
        "mean_simulated_execution_time",
        "deadline_success_rate",
        "mean_qos_score",
    ]:
        values = episode_values(column)
        summary["episode_metrics"][column] = {
            "mean": mean_or_none(values),
            "population_std": std_or_none(values),
        }

    summary_path = os.path.join(
        output_dir,
        "dqn_evaluation_summary.json",
    )

    with open(
        summary_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(summary, file, indent=4)

    print("\nDQN evaluation complete.")
    print("Evaluation episodes:", len(episode_rows))
    print("Task observations:", len(task_rows))
    print(
        "All episodes completed:",
        summary["all_episodes_completed"],
    )
    print(
        "Mean deadline success:",
        summary["episode_metrics"]["deadline_success_rate"]["mean"],
    )
    print(
        "Mean simulated execution time:",
        summary["episode_metrics"][
            "mean_simulated_execution_time"
        ]["mean"],
    )
    print("Node selection counts:", node_counts)
    print("\nSaved evaluation metrics:", episode_path)
    print("Saved task details:", task_path)
    print("Saved evaluation summary:", summary_path)


if __name__ == "__main__":
    main()
