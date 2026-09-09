class TaskExecutor:
    def __init__(self):
        self.active_tasks = []
        self.completed_tasks = []
        self.failed_tasks = []

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
        Start a task and update its lifecycle state.

        PENDING -> RUNNING
        """

        execution_time = self.estimate_execution_time(
            task,
            node
        )

        # Update task lifecycle
        task.start(node)

        task_state = {
            "task": task,
            "node": node,
            "execution_time": execution_time
        }

        self.active_tasks.append(task_state)

        return task_state

    def complete_task(self, task_state):
        """
        Complete an active task.

        If the estimated execution time exceeds the
        task deadline, the task becomes FAILED.

        Otherwise:

        RUNNING -> COMPLETED

        Deadline exceeded:

        RUNNING -> FAILED
        """

        task = task_state["task"]
        node = task_state["node"]
        execution_time = task_state["execution_time"]

        deadline_met = (
            task.deadline_seconds is None
            or execution_time <= task.deadline_seconds
        )

        # Release allocated resources
        node.release_task(task)

        if deadline_met:

            # Successful completion
            task.complete()

            result = {
                "task_id": task.task_id,
                "node_id": node.node_id,
                "execution_time": execution_time,
                "deadline_seconds": task.deadline_seconds,
                "deadline_met": True,
                "state": task.state,
                "failure_reason": None
            }

            self.completed_tasks.append(result)

        else:

            # Deadline failure
            task.fail("Deadline exceeded")

            result = {
                "task_id": task.task_id,
                "node_id": node.node_id,
                "execution_time": execution_time,
                "deadline_seconds": task.deadline_seconds,
                "deadline_met": False,
                "state": task.state,
                "failure_reason": task.failure_reason
            }

            self.failed_tasks.append(result)

        self.active_tasks.remove(task_state)

        return result