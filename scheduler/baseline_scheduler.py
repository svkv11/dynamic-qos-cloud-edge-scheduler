class BaselineScheduler:
    """
    Simple baseline scheduling strategies used
    for comparison with the Dynamic QoS Scheduler.
    """

    def __init__(self, nodes):
        self.nodes = nodes

    def round_robin(self, tasks):
        """
        Assign tasks to feasible nodes in round-robin order.

        This baseline does not consider QoS, priority,
        deadline urgency, or node ranking.
        """

        assignments = []

        node_index = 0

        for task in tasks:

            assigned_node = None

            for _ in range(len(self.nodes)):

                node = self.nodes[
                    node_index % len(self.nodes)
                ]

                node_index += 1

                if node.can_run_task(task):
                    assigned_node = node
                    break

            assignments.append({
                "task": task,
                "node": assigned_node
            })

        return assignments

    def resource_only(self, tasks):
        """
        Select the feasible node with the highest
        resource-based QoS score.

        This intentionally ignores task priority
        and deadline scoring.

        It provides a stronger baseline than
        simple round-robin scheduling.
        """

        assignments = []

        for task in tasks:

            best_node = None
            best_score = -1

            for node in self.nodes:

                if not node.can_run_task(task):
                    continue

                score = node.calculate_qos_score(task)

                if score > best_score:
                    best_score = score
                    best_node = node

            assignments.append({
                "task": task,
                "node": best_node,
                "resource_score": (
                    round(best_score, 2)
                    if best_node is not None
                    else None
                )
            })

        return assignments