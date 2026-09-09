from scheduler.task_queue import TaskQueue

class QoSScheduler:
    def __init__(self, nodes):
        self.nodes = nodes
        self.task_queue = TaskQueue()

    def calculate_priority_score(self, task):
        """
        Convert task priority into a 0-100 score.

        Priority range:
        1 = Low
        5 = Critical
        """

        priority = max(1, min(5, task.priority))

        return (priority / 5) * 100

    def calculate_deadline_score(self, task):
        """
        Convert deadline into a relative urgency score.

        Shorter deadlines receive higher urgency scores.

        This is NOT a deadline guarantee.
        """

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
        """
        Calculate the final task-aware scheduling score.

        80% = infrastructure/resource suitability
        10% = task priority
        10% = deadline urgency
        """

        resource_score = node.calculate_qos_score(task)

        priority_score = self.calculate_priority_score(task)

        deadline_score = self.calculate_deadline_score(task)

        final_score = (
            0.80 * resource_score
            + 0.10 * priority_score
            + 0.10 * deadline_score
        )

        return round(final_score, 2)

    def get_node_rankings(self, task):
        """
        Rank all feasible nodes for a given task.

        Returns a list containing:
        - node
        - resource score
        - priority score
        - deadline score
        - final score

        The highest final score is ranked first.
        """

        rankings = []

        priority_score = self.calculate_priority_score(task)
        deadline_score = self.calculate_deadline_score(task)

        for node in self.nodes:
            if node.can_run_task(task):
                resource_score = node.calculate_qos_score(task)

                final_score = (
                    0.80 * resource_score
                    + 0.10 * priority_score
                    + 0.10 * deadline_score
                )

                rankings.append({
                    "node": node,
                    "resource_score": round(resource_score, 2),
                    "priority_score": round(priority_score, 2),
                    "deadline_score": round(deadline_score, 2),
                    "final_score": round(final_score, 2)
                })

        rankings.sort(
            key=lambda item: item["final_score"],
            reverse=True
        )

        return rankings

    def select_best_node(self, task):
        """
        Select the highest-scoring feasible node.
        """

        rankings = self.get_node_rankings(task)

        if not rankings:
            return None

        return rankings[0]["node"]

    def add_task(self, task):
        """
        Add a pending task to the scheduler queue.
        """

        return self.task_queue.add_task(task)

    def get_next_task(self):
        """
        Retrieve the next pending task from the queue.
        """

        return self.task_queue.get_next_task()

    def has_pending_tasks(self):
        """
        Check whether pending tasks exist in the queue.
        """

        return not self.task_queue.is_empty()

    def pending_task_count(self):
        """
        Return the number of pending tasks.
        """

        return self.task_queue.size()

    def schedule_task(self, task):
        """
        Schedule a task directly onto the best feasible node.

        Queue management is handled separately by add_task()
        and get_next_task().
        """

        best_node = self.select_best_node(task)

        if best_node is None:
            return None

        allocated = best_node.allocate_task(task)

        if not allocated:
            return None

        return best_node

    def schedule_next_task(self):
        """
        Retrieve the next task from the queue and schedule it.

        If no pending task exists, return None.

        If no feasible node exists, the task is returned to the
        pending queue so it is not lost.
        """

        task = self.get_next_task()

        if task is None:
            return None

        best_node = self.select_best_node(task)

        if best_node is None:
            self.task_queue.pending_tasks.insert(0, task)
            return None

        allocated = best_node.allocate_task(task)

        if not allocated:
            self.task_queue.pending_tasks.insert(0, task)
            return None

        return task, best_node