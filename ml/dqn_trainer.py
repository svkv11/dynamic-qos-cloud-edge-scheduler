
import os
import sys

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import numpy as np

from ml.dqn_agent import DQNAgent
from ml.dqn_environment import DQNCloudEdgeEnvironment
from ml.replay_buffer import ReplayBuffer


class DQNTrainer:
    def __init__(
        self,
        episodes=1000,
        replay_capacity=10000,
        batch_size=64,
        seed=42
    ):
        self.episodes = episodes
        self.seed = seed

        self.env = DQNCloudEdgeEnvironment(
            seed=seed
        )

        self.agent = DQNAgent(
            state_size=self.env.state_size,
            action_size=self.env.action_size,
            batch_size=batch_size
        )

        self.replay_buffer = ReplayBuffer(
            capacity=replay_capacity
        )

        self.episode_rewards = []
        self.episode_losses = []
        self.episode_deadline_success = []
        self.episode_actions = []
        self.episode_epsilons = []

    def train(self):
        for episode in range(1, self.episodes + 1):
            state = self.env.reset()

            total_reward = 0.0
            losses = []
            deadlines_met = 0
            completed_tasks = 0
            actions = []

            while True:
                action_mask = self.env.get_action_mask()

                if not action_mask.any():
                    break

                action = self.agent.select_action(
                    state,
                    action_mask,
                    training=True
                )

                next_state, reward, done, info = self.env.step(
                    action
                )

                if done:
                    next_action_mask = np.zeros(
                        self.env.action_size,
                        dtype=bool
                    )
                else:
                    next_action_mask = self.env.get_action_mask()

                self.replay_buffer.push(
                    state,
                    action,
                    reward,
                    next_state,
                    done,
                    next_action_mask
                )

                loss = self.agent.train_step(
                    self.replay_buffer
                )

                if loss is not None:
                    losses.append(loss)

                total_reward += reward
                completed_tasks += 1

                if info["deadline_met"]:
                    deadlines_met += 1

                actions.append(action)

                state = next_state

                if done:
                    break

            deadline_success = (
                deadlines_met / completed_tasks
                if completed_tasks > 0
                else 0.0
            )

            average_loss = (
                float(np.mean(losses))
                if losses
                else None
            )

            self.episode_rewards.append(
                total_reward
            )

            self.episode_losses.append(
                average_loss
            )

            self.episode_deadline_success.append(
                deadline_success
            )

            self.episode_actions.append(
                actions
            )

            self.episode_epsilons.append(
                self.agent.epsilon
            )

            if episode == 1 or episode % 100 == 0:
                print(
                    f"Episode {episode}/{self.episodes} | "
                    f"Reward: {total_reward:.3f} | "
                    f"Deadline Success: "
                    f"{deadline_success:.3f} | "
                    f"Epsilon: "
                    f"{self.agent.epsilon:.4f} | "
                    f"Loss: "
                    f"{average_loss}"
                )

        return {
            "episode_rewards": self.episode_rewards,
            "episode_losses": self.episode_losses,
            "episode_deadline_success": (
                self.episode_deadline_success
            ),
            "episode_actions": self.episode_actions,
            "episode_epsilons": self.episode_epsilons
        }


if __name__ == "__main__":
    trainer = DQNTrainer(
        episodes=10,
        batch_size=4,
        seed=42
    )

    results = trainer.train()

    print()
    print("Training smoke test complete.")
    print(
        "Episodes completed:",
        len(results["episode_rewards"])
    )
    print(
        "Final epsilon:",
        trainer.agent.epsilon
    )
    print(
        "Epsilon history entries:",
        len(results["episode_epsilons"])
    )
    print(
        "First recorded epsilon:",
        results["episode_epsilons"][0]
    )
    print(
        "Last recorded epsilon:",
        results["episode_epsilons"][-1]
    )
