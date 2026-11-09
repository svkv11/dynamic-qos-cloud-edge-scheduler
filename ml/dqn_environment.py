
import random

import numpy as np

from scheduler.compute_node import ComputeNode
from scheduler.task import Task


class DQNCloudEdgeEnvironment:
    """
    Controlled cloud-edge simulation environment for DQN training.

    State: 5 task features + 5 workload features + 21 node features = 31.
    Actions: 0=edge-01, 1=edge-02, 2=cloud-01.

    Tasks execute sequentially in simulation. Allocated resources are
    released after each simulated execution. Background utilization and
    latency fluctuate around each node's configured baseline.
    """

    ACTION_TO_NODE = {
        0: "edge-01",
        1: "edge-02",
        2: "cloud-01",
    }

    WORKLOAD_TYPES = [
        "cpu_intensive",
        "memory_intensive",
        "gpu_intensive",
        "latency_sensitive",
        "general",
    ]

    NODE_CONFIGS = [
        {
            "node_id": "edge-01",
            "node_type": "edge",
            "cpu_cores": 4,
            "memory_gb": 8,
            "gpu_available": False,
            "cpu_utilization": 25.0,
            "memory_utilization": 30.0,
            "gpu_utilization": 0.0,
            "network_latency_ms": 10.0,
        },
        {
            "node_id": "edge-02",
            "node_type": "edge",
            "cpu_cores": 8,
            "memory_gb": 16,
            "gpu_available": True,
            "cpu_utilization": 40.0,
            "memory_utilization": 45.0,
            "gpu_utilization": 20.0,
            "network_latency_ms": 15.0,
        },
        {
            "node_id": "cloud-01",
            "node_type": "cloud",
            "cpu_cores": 16,
            "memory_gb": 32,
            "gpu_available": True,
            "cpu_utilization": 55.0,
            "memory_utilization": 50.0,
            "gpu_utilization": 35.0,
            "network_latency_ms": 80.0,
        },
    ]

    MAX_CPU = 16.0
    MAX_MEMORY = 32.0
    MAX_LATENCY = 100.0
    MAX_DEADLINE = 60.0
    MAX_EXECUTION_TIME = 60.0

    def __init__(self, tasks_per_episode=20, seed=42, training=True):
        if tasks_per_episode < 1:
            raise ValueError("tasks_per_episode must be at least 1.")

        self.tasks_per_episode = tasks_per_episode
        self.seed = seed
        self.training = training
        self.rng = random.Random(seed)
        self.np_rng = np.random.default_rng(seed)

        self.nodes = []
        self.tasks = []
        self.current_task_index = 0
        self.last_execution_time = 0.0
        self.last_deadline_met = False
        self.last_reward = 0.0
        self.last_action = None

        self.reset()

    def reset(self, seed=None):
        """Start a fresh episode; reseed only when explicitly requested."""
        if seed is not None:
            self.seed = seed
            self.rng.seed(seed)
            self.np_rng = np.random.default_rng(seed)

        self.nodes = self._create_nodes()
        self.tasks = self._generate_episode_tasks()
        self.current_task_index = 0
        self.last_execution_time = 0.0
        self.last_deadline_met = False
        self.last_reward = 0.0
        self.last_action = None

        return self._get_state()

    def _create_nodes(self):
        return [ComputeNode(**config) for config in self.NODE_CONFIGS]

    def _generate_episode_tasks(self):
        """
        Generate diverse tasks that remain feasible on the cloud node
        within its configured background-load variation range.
        """
        tasks = []

        for index in range(self.tasks_per_episode):
            workload_type = self.rng.choice(self.WORKLOAD_TYPES)

            if workload_type == "cpu_intensive":
                cpu_required = self.rng.randint(2, 6)
                memory_required = self.rng.choice([2, 4, 6, 8])
                gpu_required = False
                deadline = self.rng.choice([15, 30, 45, 60])

            elif workload_type == "memory_intensive":
                cpu_required = self.rng.randint(1, 6)
                memory_required = self.rng.choice([4, 8, 12])
                gpu_required = False
                deadline = self.rng.choice([20, 30, 45, 60])

            elif workload_type == "gpu_intensive":
                cpu_required = self.rng.randint(4, 6)
                memory_required = self.rng.choice([4, 8, 12])
                gpu_required = True
                deadline = self.rng.choice([15, 30, 45])

            elif workload_type == "latency_sensitive":
                cpu_required = self.rng.randint(1, 6)
                memory_required = self.rng.choice([2, 4, 8])
                gpu_required = False
                deadline = self.rng.choice([5, 8, 12, 15])

            else:
                cpu_required = self.rng.randint(1, 6)
                memory_required = self.rng.choice([2, 4, 8])
                gpu_required = self.rng.random() < 0.15
                deadline = self.rng.choice([15, 30, 45, 60])

            tasks.append(
                Task(
                    task_id=f"dqn-task-{index + 1}",
                    workload_type=workload_type,
                    cpu_required=cpu_required,
                    memory_required_gb=memory_required,
                    gpu_required=gpu_required,
                    deadline_seconds=deadline,
                    priority=self.rng.randint(1, 5),
                )
            )

        return tasks

    def _encode_workload_type(self, workload_type):
        return [
            1.0 if workload_type == current_type else 0.0
            for current_type in self.WORKLOAD_TYPES
        ]

    def _get_state(self):
        task = self.tasks[self.current_task_index]

        state = [
            min(task.cpu_required / self.MAX_CPU, 1.0),
            min(task.memory_required_gb / self.MAX_MEMORY, 1.0),
            1.0 if task.gpu_required else 0.0,
            task.priority / 5.0,
            min(
                (task.deadline_seconds or self.MAX_DEADLINE)
                / self.MAX_DEADLINE,
                1.0,
            ),
        ]

        state.extend(self._encode_workload_type(task.workload_type))

        for node in self.nodes:
            state.extend(
                [
                    min(node.cpu_cores / self.MAX_CPU, 1.0),
                    min(node.memory_gb / self.MAX_MEMORY, 1.0),
                    1.0 if node.gpu_available else 0.0,
                    min(node.cpu_utilization / 100.0, 1.0),
                    min(node.memory_utilization / 100.0, 1.0),
                    min(node.gpu_utilization / 100.0, 1.0),
                    min(node.network_latency_ms / self.MAX_LATENCY, 1.0),
                ]
            )

        return np.asarray(state, dtype=np.float32)

    def get_action_mask(self):
        """True means the node can currently accommodate the task."""
        task = self.tasks[self.current_task_index]
        return np.asarray(
            [bool(node.can_run_task(task)) for node in self.nodes],
            dtype=bool,
        )

    def _get_selected_node(self, action):
        if action not in self.ACTION_TO_NODE:
            raise ValueError(f"Invalid action: {action}")

        node_id = self.ACTION_TO_NODE[action]
        for node in self.nodes:
            if node.node_id == node_id:
                return node

        raise RuntimeError(f"Node {node_id} not found.")

    def _calculate_simulated_execution_time(self, task, node):
        """Estimate simulated execution time, not measured wall-clock time."""
        workload_factor = {
            "cpu_intensive": 1.25,
            "memory_intensive": 1.15,
            "gpu_intensive": 1.10,
            "latency_sensitive": 0.80,
            "general": 1.00,
        }[task.workload_type]

        cpu_pressure = task.cpu_required / max(node.cpu_cores, 1)
        memory_pressure = (
            task.memory_required_gb / max(node.memory_gb, 1)
        )

        current_pressure = (
            0.45 * node.cpu_utilization / 100.0
            + 0.35 * node.memory_utilization / 100.0
            + 0.20 * node.gpu_utilization / 100.0
        )

        processing_capacity = (
            1.0
            + 0.70 * cpu_pressure
            + 0.50 * memory_pressure
            + 0.80 * current_pressure
        )

        node_factor = 0.90 if node.node_type == "edge" else 1.05
        latency_factor = 1.0 + node.network_latency_ms / 100.0

        resource_component = (
            2.0 + 3.0 * cpu_pressure + 2.0 * memory_pressure
        )

        execution_time = (
            resource_component
            * workload_factor
            * processing_capacity
            * node_factor
            * latency_factor
        )

        if task.gpu_required and node.gpu_available:
            execution_time *= 0.65

        if (
            task.workload_type == "latency_sensitive"
            and node.network_latency_ms <= 20
        ):
            execution_time *= 0.80

        if self.training:
            execution_time *= self.rng.uniform(0.95, 1.05)

        return max(0.5, round(execution_time, 4))

    def _calculate_resource_efficiency(self, task, node):
        cpu_after = (
            node.cpu_utilization
            + task.cpu_required / max(node.cpu_cores, 1) * 100.0
        )
        memory_after = (
            node.memory_utilization
            + task.memory_required_gb / max(node.memory_gb, 1) * 100.0
        )

        cpu_util = min(cpu_after / 100.0, 1.0)
        memory_util = min(memory_after / 100.0, 1.0)

        efficiencies = [
            max(0.0, 1.0 - abs(0.70 - cpu_util)),
            max(0.0, 1.0 - abs(0.70 - memory_util)),
        ]

        if task.gpu_required:
            gpu_after = node.gpu_utilization + 25.0
            gpu_util = min(gpu_after / 100.0, 1.0)
            efficiencies.append(
                max(0.0, 1.0 - abs(0.70 - gpu_util))
            )

        return float(sum(efficiencies) / len(efficiencies))

    def _calculate_reward(
        self,
        task,
        node,
        execution_time,
        deadline_met,
        invalid_action=False,
    ):
        if invalid_action:
            return -20.0

        deadline_reward = 10.0 if deadline_met else -10.0
        execution_penalty = -5.0 * min(
            execution_time / self.MAX_EXECUTION_TIME, 1.0
        )
        latency_penalty = -2.0 * min(
            node.network_latency_ms / self.MAX_LATENCY, 1.0
        )
        resource_efficiency = self._calculate_resource_efficiency(
            task, node
        )

        return float(
            round(
                deadline_reward
                + execution_penalty
                + latency_penalty
                + 2.0 * resource_efficiency,
                4,
            )
        )

    def _apply_dynamic_variation(self):
        """
        Sample background conditions around configured baselines.
        This avoids unbounded random-walk drift across sequential tasks.
        """
        for node in self.nodes:
            config = next(
                item
                for item in self.NODE_CONFIGS
                if item["node_id"] == node.node_id
            )

            node.cpu_utilization = min(
                95.0,
                max(
                    5.0,
                    config["cpu_utilization"]
                    + self.rng.uniform(-3.0, 3.0),
                ),
            )
            node.memory_utilization = min(
                95.0,
                max(
                    5.0,
                    config["memory_utilization"]
                    + self.rng.uniform(-3.0, 3.0),
                ),
            )
            node.network_latency_ms = min(
                100.0,
                max(
                    5.0,
                    config["network_latency_ms"]
                    + self.rng.uniform(-2.0, 2.0),
                ),
            )

    def step(self, action):
        """Run one simulated scheduling decision."""
        if self.current_task_index >= len(self.tasks):
            raise RuntimeError(
                "Episode has already completed. Call reset()."
            )

        task = self.tasks[self.current_task_index]
        action = int(action)
        action_mask = self.get_action_mask()

        if (
            action < 0
            or action >= len(self.nodes)
            or not action_mask[action]
        ):
            reward = -20.0
            self.last_execution_time = 0.0
            self.last_deadline_met = False
            self.last_reward = reward
            self.last_action = action

            self.current_task_index += 1
            done = self.current_task_index >= len(self.tasks)
            next_state = None if done else self._get_state()

            return (
                next_state,
                reward,
                done,
                {
                    "task_id": task.task_id,
                    "selected_node": None,
                    "execution_time": None,
                    "deadline_met": False,
                    "invalid_action": True,
                    "action_mask": action_mask.copy(),
                },
            )

        node = self._get_selected_node(action)
        execution_time = self._calculate_simulated_execution_time(
            task, node
        )
        deadline_met = (
            task.deadline_seconds is None
            or execution_time <= task.deadline_seconds
        )
        reward = self._calculate_reward(
            task, node, execution_time, deadline_met
        )

        if not node.allocate_task(task):
            raise RuntimeError(
                "A node marked feasible failed task allocation."
            )

        # The simulated task has finished: release its temporary allocation.
        node.release_task(task)

        self.last_execution_time = execution_time
        self.last_deadline_met = deadline_met
        self.last_reward = reward
        self.last_action = action

        self.current_task_index += 1

        if self.current_task_index < len(self.tasks):
            self._apply_dynamic_variation()

        done = self.current_task_index >= len(self.tasks)
        next_state = None if done else self._get_state()

        return (
            next_state,
            reward,
            done,
            {
                "task_id": task.task_id,
                "selected_node": node.node_id,
                "execution_time": execution_time,
                "deadline_met": deadline_met,
                "invalid_action": False,
                "action_mask": action_mask.copy(),
            },
        )

    @property
    def state_size(self):
        return len(self._get_state())

    @property
    def action_size(self):
        return len(self.ACTION_TO_NODE)