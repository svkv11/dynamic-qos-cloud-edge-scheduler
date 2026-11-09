
import random

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from ml.dqn_network import DQNNetwork


class DQNAgent:
    def __init__(
        self,
        state_size,
        action_size,
        learning_rate=1e-3,
        gamma=0.99,
        epsilon_start=1.0,
        epsilon_min=0.05,
        epsilon_decay=0.995,
        batch_size=64,
        target_update_frequency=100
    ):
        self.state_size = state_size
        self.action_size = action_size

        self.gamma = gamma

        self.epsilon = epsilon_start
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        self.batch_size = batch_size
        self.target_update_frequency = target_update_frequency

        self.device = torch.device("cpu")

        self.policy_net = DQNNetwork(
            state_size,
            action_size
        ).to(self.device)

        self.target_net = DQNNetwork(
            state_size,
            action_size
        ).to(self.device)

        self.target_net.load_state_dict(
            self.policy_net.state_dict()
        )

        self.target_net.eval()

        self.optimizer = optim.Adam(
            self.policy_net.parameters(),
            lr=learning_rate
        )

        self.loss_function = nn.SmoothL1Loss()

        self.training_steps = 0

    def select_action(self, state, action_mask, training=True):
        valid_actions = [
            index
            for index, valid in enumerate(action_mask)
            if valid
        ]

        if not valid_actions:
            raise ValueError(
                "No valid actions available for the current state."
            )

        if training and random.random() < self.epsilon:
            return random.choice(valid_actions)

        state_tensor = torch.tensor(
            state,
            dtype=torch.float32,
            device=self.device
        ).unsqueeze(0)

        with torch.no_grad():
            q_values = self.policy_net(state_tensor)

        q_values = q_values.squeeze(0).cpu().numpy()

        masked_q_values = np.full(
            self.action_size,
            -np.inf,
            dtype=np.float32
        )

        for action in valid_actions:
            masked_q_values[action] = q_values[action]

        return int(np.argmax(masked_q_values))

    def train_step(self, replay_buffer):
        if len(replay_buffer) < self.batch_size:
            return None

        batch = replay_buffer.sample(
            self.batch_size
        )

        (
            states,
            actions,
            rewards,
            next_states,
            dones,
            next_action_masks
        ) = zip(*batch)

        states = torch.tensor(
            np.asarray(states),
            dtype=torch.float32,
            device=self.device
        )

        actions = torch.tensor(
            actions,
            dtype=torch.long,
            device=self.device
        ).unsqueeze(1)

        rewards = torch.tensor(
            rewards,
            dtype=torch.float32,
            device=self.device
        )

        next_states = torch.tensor(
            np.asarray(next_states),
            dtype=torch.float32,
            device=self.device
        )

        dones = torch.tensor(
            dones,
            dtype=torch.bool,
            device=self.device
        )

        next_action_masks = torch.tensor(
            np.asarray(next_action_masks),
            dtype=torch.bool,
            device=self.device
        )

        if next_action_masks.shape != (
            self.batch_size,
            self.action_size
        ):
            raise ValueError(
                "Next-state action masks have an incorrect shape."
            )

        if torch.any(
            (~dones) & (~next_action_masks.any(dim=1))
        ):
            raise ValueError(
                "A non-terminal transition has no valid next action."
            )

        current_q_values = self.policy_net(states).gather(
            1,
            actions
        ).squeeze(1)

        with torch.no_grad():
            next_q_values = torch.zeros(
                self.batch_size,
                dtype=torch.float32,
                device=self.device
            )

            non_terminal_indices = torch.where(
                ~dones
            )[0]

            if len(non_terminal_indices) > 0:
                non_terminal_states = next_states[
                    non_terminal_indices
                ]

                non_terminal_masks = next_action_masks[
                    non_terminal_indices
                ]

                target_values = self.target_net(
                    non_terminal_states
                )

                target_values = target_values.masked_fill(
                    ~non_terminal_masks,
                    -torch.inf
                )

                next_q_values[non_terminal_indices] = (
                    target_values.max(dim=1).values
                )

            target_q_values = rewards + (
                self.gamma * next_q_values
            )

        loss = self.loss_function(
            current_q_values,
            target_q_values
        )

        self.optimizer.zero_grad()

        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            self.policy_net.parameters(),
            max_norm=1.0
        )

        self.optimizer.step()

        self.training_steps += 1

        if (
            self.training_steps
            % self.target_update_frequency
            == 0
        ):
            self.target_net.load_state_dict(
                self.policy_net.state_dict()
            )

        if self.epsilon > self.epsilon_min:
            self.epsilon = max(
                self.epsilon_min,
                self.epsilon * self.epsilon_decay
            )

        return float(loss.item())
