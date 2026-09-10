from scheduler.task_queue import TaskQueue


class QoSScheduler:
    def __init__(self, nodes):
        self.nodes = nodes
        self.task_queue = TaskQueue()

    def calculate_priority_score(self, task):
        priority = max(1, min(5, task.priority))
        return (priority / 5) * 100

    def calculate_deadline_score(self, task):
        if task.deadline_seconds is None:
            return 50.0

        if task.deadline_seconds <= 0:
            return 100.0

        deadline_score = 100 - (
            task.deadline_seconds / 60
        ) * 100

        return round(
            max(0.0, min(100.0, deadline_score)),
            2
        )

    def calculate_task_score(self, node, task):
        resource_score = node.calculate_qos_score(task)
        priority_score = self.calculate_priority_score(task)
        deadline_score = self.calculate_deadline_score(task)

        final_score = (
            0.80 * resource_score
            + 0.10 * priority_score
            + 0.10 * deadline_score
        )

        return round(final_score, 2)

    def get_node_rankings(self, task, available_nodes=None):
        """
        Rank feasible nodes for a task.

        If available_nodes is provided, only those nodes
        are considered for scheduling.
        """

        if available_nodes is None:
            candidate_nodes = self.nodes
        else:
            candidate_nodes = available_nodes

        rankings = []

        priority_score = self.calculate_priority_score(task)
        deadline_score = self.calculate_deadline_score(task)

        for node in candidate_nodes:

            if node.can_run_task(task):

                resource_score = node.calculate_qos_score(task)

                final_score = (
                    0.80 * resource_score
                    + 0.10 * priority_score
                    + 0.10 * deadline_score
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
                    "final_score": round(
                        final_score,
                        2
                    )
                })

        rankings.sort(
            key=lambda item: item["final_score"],
            reverse=True
        )

        return rankings

    def select_best_node(self, task, available_nodes=None):
        rankings = self.get_node_rankings(
            task,
            available_nodes
        )

        if not rankings:
            return None

        return rankings[0]["node"]

    def add_task(self, task):
        return self.task_queue.add_task(task)

    def requeue_task(self, task):
        """
        Re-add a retryable task to the scheduler queue.

        The task must be in PENDING state.
        """

        if task.state != "PENDING":
            return False

        return self.task_queue.add_task(task)

    def get_next_task(self):
        return self.task_queue.get_next_task()

    def has_pending_tasks(self):
        return not self.task_queue.is_empty()

    def pending_task_count(self):
        return self.task_queue.size()

    def schedule_task(self, task, available_nodes=None):
        """
        Schedule a task on the best available node.

        available_nodes can be used to restrict scheduling
        to nodes whose workers are currently available.
        """

        best_node = self.select_best_node(
            task,
            available_nodes
        )

        if best_node is None:
            return None

        allocated = best_node.allocate_task(task)

        if not allocated:
            return None

        return best_node

    def schedule_next_task(self, available_nodes=None):
        """
        Get the next task from the queue and schedule it.

        Only nodes in available_nodes are considered when
        available_nodes is provided.
        """

        task = self.get_next_task()

        if task is None:
            return None

        best_node = self.select_best_node(
            task,
            available_nodes
        )

        if best_node is None:
            self.task_queue.add_task(task)
            return None

        allocated = best_node.allocate_task(task)

        if not allocated:
            self.task_queue.add_task(task)
            return None

        return task, best_node

    def retry_pending_tasks(self, available_nodes=None):
        """
        Try to schedule pending tasks using only available nodes.
        """

        scheduled_tasks = []

        pending_count = self.pending_task_count()

        for _ in range(pending_count):

            result = self.schedule_next_task(
                available_nodes
            )

            if result is None:
                break

            scheduled_tasks.append(result)

        return scheduled_tasks