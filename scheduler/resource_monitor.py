class ResourceMonitor:
    def __init__(self, nodes):
        self.nodes = nodes

    def update_node_state(
        self,
        node_id,
        cpu_utilization=None,
        memory_utilization=None,
        gpu_utilization=None,
        network_latency_ms=None
    ):
        """
        Update the dynamic state of a specific node.

        Only the values provided by the caller are updated.
        """

        node = self.get_node(node_id)

        if node is None:
            return False

        if cpu_utilization is not None:
            node.cpu_utilization = cpu_utilization

        if memory_utilization is not None:
            node.memory_utilization = memory_utilization

        if gpu_utilization is not None:
            node.gpu_utilization = gpu_utilization

        if network_latency_ms is not None:
            node.network_latency_ms = network_latency_ms

        return True

    def get_node(self, node_id):
        """
        Find a node using its node ID.
        """

        for node in self.nodes:
            if node.node_id == node_id:
                return node

        return None

    def get_node_state(self, node_id):
        """
        Return the current dynamic state of a node.
        """

        node = self.get_node(node_id)

        if node is None:
            return None

        return {
            "node_id": node.node_id,
            "cpu_utilization": node.cpu_utilization,
            "memory_utilization": node.memory_utilization,
            "gpu_utilization": node.gpu_utilization,
            "network_latency_ms": node.network_latency_ms
        }

    def get_all_node_states(self):
        """
        Return the current state of all nodes.
        """

        return [
            self.get_node_state(node.node_id)
            for node in self.nodes
        ]

    def display_status(self):
        """
        Display the current resource state of all nodes.
        """

        print("=" * 60)
        print("RESOURCE MONITOR STATUS")
        print("=" * 60)

        for node in self.nodes:
            print(
                f"{node.node_id} | "
                f"CPU={node.cpu_utilization}% | "
                f"Memory={node.memory_utilization}% | "
                f"GPU={node.gpu_utilization}% | "
                f"Latency={node.network_latency_ms} ms"
            )

        print("=" * 60)