class QoSScheduler:
    def __init__(self, nodes):
        self.nodes = nodes

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
        Actual deadline satisfaction will be measured later
        when task execution simulation is implemented.
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
        rankings = self.get_node_rankings(task)

        if not rankings:
            return None

        return rankings[0]["node"]

    def schedule_task(self, task):
        best_node = self.select_best_node(task)

        if best_node is None:
            return None

        allocated = best_node.allocate_task(task)

        if not allocated:
            return None

        return best_node