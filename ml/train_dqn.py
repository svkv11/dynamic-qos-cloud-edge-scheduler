
import os
import sys
import csv
import json

# Allow execution from the project repository.
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ml.dqn_trainer import DQNTrainer


def main():
    episodes = 1000
    seed = 42
    replay_capacity = 10000
    batch_size = 64

    trainer = DQNTrainer(
        episodes=episodes,
        replay_capacity=replay_capacity,
        batch_size=batch_size,
        seed=seed
    )

    # Capture these invariant dimensions before training.
    # The environment's state_size property currently depends
    # on the current task and fails after an episode finishes.
    state_size = trainer.env.state_size
    action_size = trainer.env.action_size

    results = trainer.train()

    output_dir = os.path.join(
        PROJECT_ROOT,
        "experiments",
        "results",
        "dqn"
    )
    os.makedirs(output_dir, exist_ok=True)

    model_path = os.path.join(
        output_dir,
        "dqn_model.pt"
    )

    import torch

    torch.save(
        {
            "model_state_dict": (
                trainer.agent.policy_net.state_dict()
            ),
            "state_size": state_size,
            "action_size": action_size,
            "seed": seed,
            "episodes": episodes
        },
        model_path
    )

    metrics_path = os.path.join(
        output_dir,
        "dqn_training_metrics.csv"
    )

    with open(
        metrics_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow([
            "episode",
            "reward",
            "average_loss",
            "deadline_success",
            "epsilon"
        ])

        for index in range(episodes):
            writer.writerow([
                index + 1,
                results["episode_rewards"][index],
                results["episode_losses"][index],
                results["episode_deadline_success"][index],
                results["episode_epsilons"][index]
            ])

    summary_path = os.path.join(
        output_dir,
        "dqn_training_summary.json"
    )

    with open(
        summary_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            {
                "episodes": episodes,
                "seed": seed,
                "state_size": state_size,
                "action_size": action_size,
                "final_epsilon": trainer.agent.epsilon,
                "replay_capacity": replay_capacity,
                "batch_size": batch_size
            },
            file,
            indent=4
        )

    print()
    print("DQN training complete.")
    print("Episodes:", episodes)
    print("State size:", state_size)
    print("Action size:", action_size)
    print("Final epsilon:", trainer.agent.epsilon)
    print()
    print("Saved model:", model_path)
    print("Saved metrics:", metrics_path)
    print("Saved summary:", summary_path)


if __name__ == "__main__":
    main()
