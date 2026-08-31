class QoSScheduler:
    def __init__(self, nodes):
        self.nodes = nodes

    def select_best_node(self, task):
        feasible_nodes = []

        for node in self.nodes:
            if node.can_run_task(task):
                feasible_nodes.append(node)

        if not feasible_nodes:
            return None

        best_node = max(
            feasible_nodes,
            key=lambda node: node.calculate_qos_score()
        )

        return best_node