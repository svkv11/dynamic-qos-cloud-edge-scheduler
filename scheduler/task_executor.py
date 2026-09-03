class TaskExecutor:
    def __init__(self):
        self.active_tasks = []
        self.completed_tasks = []

    def estimate_execution_time(self, task, node):
        """
        Estimate task execution time based on:
        - CPU requirement
        - Memory requirement
        - GPU requirement
        - Node type
        - Current network latency

        This is a simulation model, not real execution time.
        """

        base_time = (
            task.cpu_required * 2
            + task.memory_required_gb * 0.5
        )

        # GPU acceleration
        if task.gpu_required and node.gpu_available:
            base_time *= 0.5

        # Edge nodes are assumed to have faster local execution.
        if node.node_type == "edge":
            base_time *= 0.9
        else:
            base_time *= 1.1

        # Network latency contribution
        network_delay = node.network_latency_ms / 10

        execution_time = base_time + network_delay

        return round(execution_time, 2)

    def start_task(self, task, node):
        """
        Start a task without immediately releasing its resources.

        The task remains active until complete_task() is called.
        """

        execution_time = self.estimate_execution_time(
            task,
            node
        )

        task_state = {
            "task": task,
            "node": node,
            "execution_time": execution_time
        }

        self.active_tasks.append(task_state)

        return task_state

    def complete_task(self, task_state):
        """
        Complete an active task and release its resources.
        """

        task = task_state["task"]
        node = task_state["node"]
        execution_time = task_state["execution_time"]

        deadline_met = (
            task.deadline_seconds is None
            or execution_time <= task.deadline_seconds
        )

        node.release_task(task)

        result = {
            "task_id": task.task_id,
            "node_id": node.node_id,
            "execution_time": execution_time,
            "deadline_seconds": task.deadline_seconds,
            "deadline_met": deadline_met
        }

        self.active_tasks.remove(task_state)
        self.completed_tasks.append(result)

        return result