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

    def refresh_node_state(
        self,
        node_id,
        cpu_utilization,
        memory_utilization,
        gpu_utilization,
        network_latency_ms
    ):
        """
        Simulate a fresh resource measurement for a node.

        This method represents a monitoring system receiving
        a new resource snapshot from a node.
        """

        return self.update_node_state(
            node_id=node_id,
            cpu_utilization=cpu_utilization,
            memory_utilization=memory_utilization,
            gpu_utilization=gpu_utilization,
            network_latency_ms=network_latency_ms
        )

    def refresh_all_nodes(self, resource_data):
        """
        Refresh the resource state of multiple nodes.

        resource_data must be a dictionary in the form:

        {
            "edge-01": {
                "cpu_utilization": 30.0,
                "memory_utilization": 35.0,
                "gpu_utilization": 0.0,
                "network_latency_ms": 12.0
            }
        }

        Returns the number of successfully refreshed nodes.
        """

        refreshed_count = 0

        for node_id, state in resource_data.items():

            updated = self.refresh_node_state(
                node_id=node_id,
                cpu_utilization=state.get(
                    "cpu_utilization"
                ),
                memory_utilization=state.get(
                    "memory_utilization"
                ),
                gpu_utilization=state.get(
                    "gpu_utilization"
                ),
                network_latency_ms=state.get(
                    "network_latency_ms"
                )
            )

            if updated:
                refreshed_count += 1

        return refreshed_count

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