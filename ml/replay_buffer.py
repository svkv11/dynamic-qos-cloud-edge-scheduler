
from collections import deque
import random
import numpy as np


class ReplayBuffer:
    def __init__(self, capacity=10000):
        if capacity < 1:
            raise ValueError(
                "Replay buffer capacity must be at least 1."
            )

        self.buffer = deque(maxlen=capacity)

    def push(
        self,
        state,
        action,
        reward,
        next_state,
        done,
        next_action_mask
    ):
        state = np.asarray(
            state,
            dtype=np.float32
        ).copy()

        if next_state is None:
            next_state = np.zeros_like(
                state,
                dtype=np.float32
            )
        else:
            next_state = np.asarray(
                next_state,
                dtype=np.float32
            ).copy()

        if next_action_mask is None:
            raise ValueError(
                "Next-state action mask cannot be None."
            )

        next_action_mask = np.asarray(
            next_action_mask,
            dtype=np.bool_
        ).copy()

        if next_action_mask.ndim != 1:
            raise ValueError(
                "Next-state action mask must be one-dimensional."
            )

        self.buffer.append(
            (
                state,
                int(action),
                float(reward),
                next_state,
                bool(done),
                next_action_mask
            )
        )

    def sample(self, batch_size):
        if batch_size < 1 or batch_size > len(self.buffer):
            raise ValueError(
                "batch_size must be between 1 and the buffer length."
            )

        return random.sample(
            self.buffer,
            batch_size
        )

    def __len__(self):
        return len(self.buffer)
