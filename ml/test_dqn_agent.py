
import os
import sys

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import numpy as np
import torch

from ml.dqn_environment import DQNCloudEdgeEnvironment
from ml.dqn_agent import DQNAgent
from ml.replay_buffer import ReplayBuffer


def main():
    env = DQNCloudEdgeEnvironment(seed=42)

    agent = DQNAgent(
        state_size=env.state_size,
        action_size=env.action_size,
        batch_size=4,
        target_update_frequency=2
    )

    replay_buffer = ReplayBuffer(
        capacity=100
    )

    state = env.reset()

    experiences_collected = 0
    resets = 0
    terminal_experiences = 0

    # Collect real environment experiences.
    while experiences_collected < 8:
        action_mask = env.get_action_mask()

        if not action_mask.any():
            state = env.reset()
            resets += 1
            continue

        action = agent.select_action(
            state,
            action_mask,
            training=True
        )

        next_state, reward, done, info = env.step(
            action
        )

        if done:
            next_action_mask = np.zeros(
                env.action_size,
                dtype=bool
            )
            terminal_experiences += 1
        else:
            next_action_mask = env.get_action_mask()

        replay_buffer.push(
            state,
            action,
            reward,
            next_state,
            done,
            next_action_mask
        )

        experiences_collected += 1
        state = next_state

        if done:
            state = env.reset()
            resets += 1

    print(
        "Experiences collected:",
        len(replay_buffer)
    )

    print(
        "Environment resets:",
        resets
    )

    print(
        "Terminal experiences:",
        terminal_experiences
    )

    # Record parameters before training.
    parameters_before = [
        parameter.detach().clone()
        for parameter in agent.policy_net.parameters()
    ]

    epsilon_before = agent.epsilon

    loss = agent.train_step(
        replay_buffer
    )

    print(
        "Training loss:",
        loss
    )

    print(
        "Epsilon before:",
        epsilon_before
    )

    print(
        "Epsilon after:",
        agent.epsilon
    )

    if loss is None or not np.isfinite(loss):
        raise AssertionError(
            "Training loss is missing or non-finite."
        )

    parameters_changed = any(
        not torch.equal(before, after)
        for before, after in zip(
            parameters_before,
            agent.policy_net.parameters()
        )
    )

    print(
        "Policy parameters changed:",
        parameters_changed
    )

    print(
        "Training steps:",
        agent.training_steps
    )

    if not parameters_changed:
        raise AssertionError(
            "Policy network parameters did not change."
        )

    if agent.training_steps != 1:
        raise AssertionError(
            "Unexpected number of training steps."
        )

    print()
    print("DQN masked-training test passed.")


if __name__ == "__main__":
    main()
