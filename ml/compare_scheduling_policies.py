
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
from scheduler.scheduler import QoSScheduler


EVALUATION_SEEDS = range(100, 130)

POLICY_NAMES = [
    "Round Robin",
    "Resource Only",
    "Dynamic QoS",
    "DQN",
]

ACTION_TO_NODE = {
    0: "edge-01",
    1: "edge-02",
    2: "cloud-01",
}


def mean_or_none(values):
    return statistics.mean(values) if values else None


def std_or_none(values):
    if len(values) > 1:
        return statistics.pstdev(values)
    return 0.0 if values else None


def load_dqn_agent(model_path):
    if not os.path.isfile(model_path):
        raise FileNotFoundError(
            f"Trained DQN checkpoint not found: {model_path}"
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
            f"Unexpected checkpoint dimensions: "
            f"state_size={state_size}, action_size={action_size}"
        )

    agent = DQNAgent(
        state_size=state_size,
        action_size=action_size,
    )

    agent.policy_net.load_state_dict(
        checkpoint["model_state_dict"]
    )
    agent.policy_net.eval()

    return agent, checkpoint


def select_round_robin_action(env, cursor):
    task = env.tasks[env.current_task_index]
    node_count = len(env.nodes)

    for _ in range(node_count):
        action = cursor % node_count
        cursor += 1

        if env.nodes[action].can_run_task(task):
            return action, cursor

    return None, cursor


def select_resource_only_action(env):
    task = env.tasks[env.current_task_index]
    feasible = [
        (index, node)
        for index, node in enumerate(env.nodes)
        if node.can_run_task(task)
    ]

    if not feasible:
        return None

    # Preserve the existing baseline's first-node tie-breaking behavior.
    best_action, best_node = feasible[0]
    best_score = best_node.calculate_qos_score(task)

    for action, node in feasible[1:]:
        score = node.calculate_qos_score(task)

        if score > best_score:
            best_action = action
            best_score = score

    return best_action


def select_dynamic_qos_action(env, scheduler):
    task = env.tasks[env.current_task_index]

    selected_node = scheduler.select_best_node(
        task,
        available_nodes=env.nodes,
    )

    if selected_node is None:
        return None

    for action, node in enumerate(env.nodes):
        if node.node_id == selected_node.node_id:
            return action

    raise RuntimeError(
        f"Selected node is not part of the environment: "
        f"{selected_node.node_id}"
    )


def select_dqn_action(env, agent, state):
    action_mask = env.get_action_mask()

    if not action_mask.any():
        return None

    return agent.select_action(
        state,
        action_mask,
        training=False,
    )


def run_policy(policy_name, seed, agent):
    # Each policy starts from the same seed, task-generation procedure,
    # node configurations, and evaluation-mode execution-time formula.
    env = DQNCloudEdgeEnvironment(
        tasks_per_episode=20,
        seed=seed,
        training=False,
    )

    state = env.reset(seed=seed)

    qos_scheduler = None
    if policy_name == "Dynamic QoS":
        qos_scheduler = QoSScheduler(
            nodes=env.nodes,
            mode="full",
        )

    round_robin_cursor = 0
    task_rows = []
    total_reward = 0.0
    deadline_count = 0
    invalid_actions = 0

    while env.current_task_index < len(env.tasks):
        task_index = env.current_task_index
        task = env.tasks[task_index]

        if policy_name == "Round Robin":
            action, round_robin_cursor = select_round_robin_action(
                env,
                round_robin_cursor,
            )

        elif policy_name == "Resource Only":
            action = select_resource_only_action(env)

        elif policy_name == "Dynamic QoS":
            action = select_dynamic_qos_action(
                env,
                qos_scheduler,
            )

        elif policy_name == "DQN":
            action = select_dqn_action(
                env,
                agent,
                state,
            )

        else:
            raise ValueError(f"Unknown policy: {policy_name}")

        if action is None:
            # No feasible node: record the task as unscheduled. The
            # environment cannot accept a valid node action for this task.
            invalid_actions += 1
            task_rows.append({
                "policy": policy_name,
                "seed": seed,
                "task_id": task.task_id,
                "selected_node": None,
                "simulated_execution_time": None,
                "deadline_met": 0,
                "qos_score": None,
                "reward": None,
                "invalid_action": 1,
                "task_completed": 0,
            })

            # All generated tasks should be feasible on cloud-01.
            # Stop rather than invent an execution result.
            break

        if action not in ACTION_TO_NODE:
            raise ValueError(f"Unexpected action: {action}")

        node = env.nodes[action]

        # Score before env.step changes the environment.
        qos_score = node.calculate_qos_score(task)

        next_state, reward, done, info = env.step(action)

        total_reward += float(reward)
        deadline_count += int(info["deadline_met"])
        invalid_actions += int(info["invalid_action"])

        task_rows.append({
            "policy": policy_name,
            "seed": seed,
            "task_id": info["task_id"],
            "selected_node": info["selected_node"],
            "simulated_execution_time": info["execution_time"],
            "deadline_met": int(info["deadline_met"]),
            "qos_score": float(qos_score),
            "reward": float(reward),
            "invalid_action": int(info["invalid_action"]),
            "task_completed": 1,
        })

        state = next_state

        if done:
            break

    completed_rows = [
        row for row in task_rows
        if row["task_completed"] == 1
    ]

    execution_times = [
        float(row["simulated_execution_time"])
        for row in completed_rows
    ]
    qos_scores = [
        float(row["qos_score"])
        for row in completed_rows
    ]

    completed_count = len(completed_rows)
    expected_count = len(env.tasks)

    episode_row = {
        "policy": policy_name,
        "seed": seed,
        "tasks_completed": completed_count,
        "expected_tasks": expected_count,
        "all_tasks_completed": int(
            completed_count == expected_count
        ),
        "total_reward": total_reward,
        "mean_reward_per_completed_task": (
            total_reward / completed_count
            if completed_count else None
        ),
        "mean_simulated_execution_time": mean_or_none(
            execution_times
        ),
        "deadline_success_rate": (
            deadline_count / completed_count
            if completed_count else None
        ),
        "mean_qos_score": mean_or_none(qos_scores),
        "invalid_actions_or_unscheduled": invalid_actions,
    }

    return episode_row, task_rows


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"No rows available to write: {path}")

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)


def main():
    output_dir = os.path.join(
        PROJECT_ROOT,
        "experiments",
        "results",
        "dqn_comparison",
    )
    os.makedirs(output_dir, exist_ok=True)

    model_path = os.path.join(
        PROJECT_ROOT,
        "experiments",
        "results",
        "dqn",
        "dqn_model.pt",
    )

    agent, checkpoint = load_dqn_agent(model_path)

    episode_rows = []
    task_rows = []

    for policy_name in POLICY_NAMES:
        print(f"\nEvaluating policy: {policy_name}")

        for seed in EVALUATION_SEEDS:
            episode_row, per_task_rows = run_policy(
                policy_name,
                seed,
                agent,
            )

            episode_rows.append(episode_row)
            task_rows.extend(per_task_rows)

            rate = episode_row["deadline_success_rate"]
            mean_time = episode_row["mean_simulated_execution_time"]

            print(
                f"Seed {seed}: "
                f"Tasks={episode_row['tasks_completed']}/"
                f"{episode_row['expected_tasks']}, "
                f"Deadline success={rate}, "
                f"Mean simulated time={mean_time}"
            )

    episode_path = os.path.join(
        output_dir,
        "policy_comparison_episode_metrics.csv",
    )
    task_path = os.path.join(
        output_dir,
        "policy_comparison_task_details.csv",
    )
    summary_path = os.path.join(
        output_dir,
        "policy_comparison_summary.json",
    )

    write_csv(episode_path, episode_rows)
    write_csv(task_path, task_rows)

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
        "policies": POLICY_NAMES,
        "tasks_per_episode": 20,
        "episodes_per_policy": len(EVALUATION_SEEDS),
        "metrics_are_simulated": True,
        "execution_time_is_wall_clock": False,
        "same_seeded_task_generation_per_policy": True,
        "policy_exploration_enabled_for_dqn": False,
        "episode_summary": {},
        "node_selection_counts": {},
        "notes": [
            "All policy outcomes use DQNCloudEdgeEnvironment.",
            "Round Robin and Resource Only follow the existing baseline selection definitions.",
            "Dynamic QoS uses QoSScheduler in full mode.",
            "Dynamic QoS deadline ranking uses TaskExecutor estimates, while outcomes use the environment's execution-time formula.",
            "Results should be interpreted as a comparison under the shared simulator, not real-world execution measurements.",
        ],
    }

    for policy_name in POLICY_NAMES:
        policy_episodes = [
            row for row in episode_rows
            if row["policy"] == policy_name
        ]

        summary["episode_summary"][policy_name] = {}

        for metric in [
            "tasks_completed",
            "total_reward",
            "mean_reward_per_completed_task",
            "mean_simulated_execution_time",
            "deadline_success_rate",
            "mean_qos_score",
            "invalid_actions_or_unscheduled",
        ]:
            values = [
                float(row[metric])
                for row in policy_episodes
                if row[metric] is not None
            ]

            summary["episode_summary"][policy_name][metric] = {
                "mean": mean_or_none(values),
                "population_std": std_or_none(values),
            }

        counts = {
            node_name: sum(
                1
                for row in task_rows
                if row["policy"] == policy_name
                and row["selected_node"] == node_name
            )
            for node_name in ACTION_TO_NODE.values()
        }
        summary["node_selection_counts"][policy_name] = counts

    summary["all_episodes_completed"] = {
        policy_name: all(
            row["all_tasks_completed"] == 1
            for row in episode_rows
            if row["policy"] == policy_name
        )
        for policy_name in POLICY_NAMES
    }

    with open(
        summary_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(summary, file, indent=4)

    print("\nPolicy comparison complete.")
    print("Episode metrics:", episode_path)
    print("Task details:", task_path)
    print("Summary:", summary_path)

    print("\nMean metrics by policy:")
    for policy_name in POLICY_NAMES:
        metrics = summary["episode_summary"][policy_name]
        print(f"\n{policy_name}")
        print(
            "  Mean simulated execution time:",
            metrics["mean_simulated_execution_time"]["mean"],
        )
        print(
            "  Deadline success rate:",
            metrics["deadline_success_rate"]["mean"],
        )
        print(
            "  Mean QoS score:",
            metrics["mean_qos_score"]["mean"],
        )
        print(
            "  Node selection counts:",
            summary["node_selection_counts"][policy_name],
        )


if __name__ == "__main__":
    main()
