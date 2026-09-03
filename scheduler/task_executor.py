class TaskExecutor:
    def __init__(self):
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

    def execute_task(self, task, node):
        """
        Simulate task execution and release resources
        after completion.
        """

        execution_time = self.estimate_execution_time(
            task,
            node
        )

        deadline_met = (
            task.deadline_seconds is None
            or execution_time <= task.deadline_seconds
        )

        # Release resources after simulated completion.
        node.release_task(task)

        result = {
            "task_id": task.task_id,
            "node_id": node.node_id,
            "execution_time": execution_time,
            "deadline_seconds": task.deadline_seconds,
            "deadline_met": deadline_met
        }

        self.completed_tasks.append(result)

        return result