from scheduler.task_queue import TaskQueue
from scheduler.task_executor import TaskExecutor


class QoSScheduler:
    """
    Dynamic QoS Scheduler.

    The scheduler selects a feasible compute node for a task using:

    1. Resource suitability
    2. Task priority
    3. Node-aware deadline performance

    The deadline component is node-aware because estimated execution
    time can differ between candidate nodes.

    Modes:
        full
            Resource + Priority + Node-aware Deadline

        no_priority
            Resource + Node-aware Deadline

        no_deadline
            Resource + Priority

    The default mode is "full".
    """

    VALID_MODES = {
        "full",
        "no_priority",
        "no_deadline"
    }

    def __init__(self, nodes, mode="full"):
        if mode not in self.VALID_MODES:
            raise ValueError(
                f"Unknown QoS scheduler mode: {mode}. "
                f"Available modes: {sorted(self.VALID_MODES)}"
            )

        self.nodes = nodes
        self.mode = mode
        self.task_queue = TaskQueue()

        # Used only for execution-time estimation.
        # It does not execute tasks.
        self.task_executor = TaskExecutor()

    def calculate_priority_score(self, task):
        """
        Convert task priority from 1-5 into a 0-100 score.
        """

        priority = max(
            1,
            min(5, task.priority)
        )

        return (priority / 5) * 100

    def calculate_deadline_score(
        self,
        task,
        node
    ):
        """
        Calculate node-aware deadline performance.

        The score depends on the estimated execution time of the
        task on the specific candidate node.

        If the task meets the deadline:

            score = 50 + 50 * (deadline - execution_time) / deadline

        If the task misses the deadline:

            score = 50 * deadline / execution_time

        The result is bounded to the range 0-100.

        A score of:
            > 50 -> task finishes before the deadline
            = 50 -> task finishes exactly at the deadline
            < 50 -> task misses the deadline
        """

        if task.deadline_seconds is None:
            return 50.0

        deadline = task.deadline_seconds

        if deadline <= 0:
            return 0.0

        execution_time = (
            self.task_executor.estimate_execution_time(
                task,
                node
            )
        )

        if execution_time <= deadline:
            score = (
                50
                + 50 * (
                    (deadline - execution_time)
                    / deadline
                )
            )
        else:
            score = (
                50
                * deadline
                / execution_time
            )

        return round(
            max(0.0, min(100.0, score)),
            2
        )

    def calculate_adaptive_weights(self, task):
        """
        Calculate scheduling weights based on task priority.

        Higher-priority tasks give more importance to priority and
        deadline performance, while lower-priority tasks remain more
        resource-oriented.

        Priority 1:
            Resource = 80%
            Priority = 10%
            Deadline = 10%

        Priority 2:
            Resource = 70%
            Priority = 15%
            Deadline = 15%

        Priority 3:
            Resource = 60%
            Priority = 20%
            Deadline = 20%

        Priority 4:
            Resource = 50%
            Priority = 25%
            Deadline = 25%

        Priority 5:
            Resource = 40%
            Priority = 30%
            Deadline = 30%
        """

        priority = max(
            1,
            min(5, task.priority)
        )

        non_resource_weight = (
            0.10
            + 0.05 * (priority - 1)
        )

        resource_weight = (
            1.0
            - 2 * non_resource_weight
        )

        return (
            round(resource_weight, 2),
            round(non_resource_weight, 2),
            round(non_resource_weight, 2)
        )

    def calculate_task_score(
        self,
        node,
        task
    ):
        """
        Calculate the final task-node scheduling score.
        """

        resource_score = node.calculate_qos_score(
            task
        )

        priority_score = self.calculate_priority_score(
            task
        )

        deadline_score = self.calculate_deadline_score(
            task,
            node
        )

        (
            resource_weight,
            priority_weight,
            deadline_weight
        ) = self.calculate_adaptive_weights(
            task
        )

        if self.mode == "full":

            final_score = (
                resource_weight * resource_score
                + priority_weight * priority_score
                + deadline_weight * deadline_score
            )

        elif self.mode == "no_priority":

            # Preserve the adaptive resource/deadline relationship
            # while removing the priority contribution.

            final_score = (
                resource_weight * resource_score
                + deadline_weight * deadline_score
            )

        elif self.mode == "no_deadline":

            # Preserve the adaptive resource/priority relationship
            # while removing the deadline contribution.

            final_score = (
                resource_weight * resource_score
                + priority_weight * priority_score
            )

        else:
            raise ValueError(
                f"Unsupported scheduler mode: {self.mode}"
            )

        return round(
            final_score,
            2
        )

    def get_node_rankings(
        self,
        task,
        available_nodes=None
    ):
        """
        Rank feasible nodes for a task.
        """

        if available_nodes is None:
            candidate_nodes = self.nodes
        else:
            candidate_nodes = available_nodes

        rankings = []

        priority_score = self.calculate_priority_score(
            task
        )

        (
            resource_weight,
            priority_weight,
            deadline_weight
        ) = self.calculate_adaptive_weights(
            task
        )

        for node in candidate_nodes:

            if not node.can_run_task(task):
                continue

            resource_score = node.calculate_qos_score(
                task
            )

            deadline_score = self.calculate_deadline_score(
                task,
                node
            )

            final_score = self.calculate_task_score(
                node,
                task
            )

            rankings.append({
                "node": node,
                "resource_score": round(
                    resource_score,
                    2
                ),
                "priority_score": round(
                    priority_score,
                    2
                ),
                "deadline_score": round(
                    deadline_score,
                    2
                ),
                "resource_weight": resource_weight,
                "priority_weight": priority_weight,
                "deadline_weight": deadline_weight,
                "final_score": final_score
            })

        rankings.sort(
            key=lambda item: item["final_score"],
            reverse=True
        )

        return rankings

    def select_best_node(
        self,
        task,
        available_nodes=None
    ):
        """
        Select the highest-scoring feasible node.
        """

        rankings = self.get_node_rankings(
            task,
            available_nodes
        )

        if not rankings:
            return None

        return rankings[0]["node"]

    def add_task(self, task):
        return self.task_queue.add_task(
            task
        )

    def requeue_task(self, task):
        if task.state != "PENDING":
            return False

        return self.task_queue.add_task(
            task
        )

    def get_next_task(self):
        return self.task_queue.get_next_task()

    def has_pending_tasks(self):
        return not self.task_queue.is_empty()

    def pending_task_count(self):
        return self.task_queue.size()

    def schedule_task(
        self,
        task,
        available_nodes=None
    ):
        """
        Schedule a specific task.
        """

        best_node = self.select_best_node(
            task,
            available_nodes
        )

        if best_node is None:
            return None

        task.scheduling_qos_score = (
            self.calculate_task_score(
                best_node,
                task
            )
        )

        allocated = best_node.allocate_task(
            task
        )

        if not allocated:
            task.scheduling_qos_score = None
            return None

        return best_node

    def schedule_next_task(
        self,
        available_nodes=None
    ):
        """
        Retrieve and schedule the next queued task.
        """

        task = self.get_next_task()

        if task is None:
            return None

        best_node = self.select_best_node(
            task,
            available_nodes
        )

        if best_node is None:
            self.task_queue.add_task(
                task
            )
            return None

        task.scheduling_qos_score = (
            self.calculate_task_score(
                best_node,
                task
            )
        )

        allocated = best_node.allocate_task(
            task
        )

        if not allocated:
            task.scheduling_qos_score = None
            self.task_queue.add_task(
                task
            )
            return None

        return task, best_node

    def retry_pending_tasks(
        self,
        available_nodes=None
    ):
        """
        Retry scheduling pending tasks.
        """

        scheduled_tasks = []

        pending_count = (
            self.pending_task_count()
        )

        for _ in range(pending_count):

            result = self.schedule_next_task(
                available_nodes
            )

            if result is None:
                break

            scheduled_tasks.append(
                result
            )

        return scheduled_tasks