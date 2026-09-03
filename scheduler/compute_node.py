class ComputeNode:
    def __init__(
        self,
        node_id,
        node_type,
        cpu_cores,
        memory_gb,
        gpu_available,
        cpu_utilization=0.0,
        memory_utilization=0.0,
        gpu_utilization=0.0,
        network_latency_ms=0.0
    ):
        self.node_id = node_id
        self.node_type = node_type

        # Fixed resources
        self.cpu_cores = cpu_cores
        self.memory_gb = memory_gb
        self.gpu_available = gpu_available

        # Dynamic resource state
        self.cpu_utilization = cpu_utilization
        self.memory_utilization = memory_utilization
        self.gpu_utilization = gpu_utilization
        self.network_latency_ms = network_latency_ms

    def display_info(self):
        print(f"Node ID: {self.node_id}")
        print(f"Node Type: {self.node_type}")

        print(f"CPU Cores: {self.cpu_cores}")
        print(f"CPU Utilization: {self.cpu_utilization}%")

        print(f"Memory: {self.memory_gb} GB")
        print(f"Memory Utilization: {self.memory_utilization}%")

        print(f"GPU Available: {self.gpu_available}")
        print(f"GPU Utilization: {self.gpu_utilization}%")

        print(f"Network Latency: {self.network_latency_ms} ms")

        print("-" * 40)

    def can_run_task(self, task):
        available_cpu = self.cpu_cores * (
            1 - self.cpu_utilization / 100
        )

        available_memory = self.memory_gb * (
            1 - self.memory_utilization / 100
        )

        if task.cpu_required > available_cpu:
            return False

        if task.memory_required_gb > available_memory:
            return False

        if task.gpu_required and not self.gpu_available:
            return False

        return True

    def allocate_task(self, task):
        if not self.can_run_task(task):
            return False

        cpu_increase = (
            task.cpu_required / self.cpu_cores
        ) * 100

        memory_increase = (
            task.memory_required_gb / self.memory_gb
        ) * 100

        self.cpu_utilization += cpu_increase
        self.memory_utilization += memory_increase

        if task.gpu_required:
            self.gpu_utilization += 25.0

        return True

    def release_task(self, task):
        cpu_decrease = (
            task.cpu_required / self.cpu_cores
        ) * 100

        memory_decrease = (
            task.memory_required_gb / self.memory_gb
        ) * 100

        self.cpu_utilization -= cpu_decrease
        self.memory_utilization -= memory_decrease

        if task.gpu_required:
            self.gpu_utilization -= 25.0

        self.cpu_utilization = max(
            0.0,
            self.cpu_utilization
        )

        self.memory_utilization = max(
            0.0,
            self.memory_utilization
        )

        self.gpu_utilization = max(
            0.0,
            self.gpu_utilization
        )

    def calculate_qos_score(self, task):
        """
        Calculate a task-aware QoS score.

        The score considers:
        - CPU efficiency
        - Memory efficiency
        - GPU suitability
        - Network latency

        Feasibility is checked separately by can_run_task().
        """

        available_cpu = self.cpu_cores * (
            1 - self.cpu_utilization / 100
        )

        available_memory = self.memory_gb * (
            1 - self.memory_utilization / 100
        )

        # -----------------------------
        # CPU Efficiency
        # -----------------------------

        if task.cpu_required == 0:
            cpu_score = 100.0
        else:
            cpu_usage_ratio = (
                task.cpu_required / available_cpu
            )

            cpu_score = max(
                0.0,
                100.0 - (
                    abs(0.5 - cpu_usage_ratio) * 100
                )
            )

            cpu_score = min(100.0, cpu_score)

        # -----------------------------
        # Memory Efficiency
        # -----------------------------

        if task.memory_required_gb == 0:
            memory_score = 100.0
        else:
            memory_usage_ratio = (
                task.memory_required_gb
                / available_memory
            )

            memory_score = max(
                0.0,
                100.0 - (
                    abs(0.5 - memory_usage_ratio) * 100
                )
            )

            memory_score = min(
                100.0,
                memory_score
            )

        # -----------------------------
        # GPU Suitability
        # -----------------------------

        if task.gpu_required:
            if not self.gpu_available:
                gpu_score = 0.0
            else:
                gpu_score = max(
                    0.0,
                    100.0 - self.gpu_utilization
                )
        else:
            gpu_score = 100.0

        # -----------------------------
        # Network Latency
        # -----------------------------

        latency_score = max(
            0.0,
            100.0 - self.network_latency_ms
        )

        # -----------------------------
        # Final QoS Score
        # -----------------------------

        qos_score = (
            0.30 * cpu_score
            + 0.25 * memory_score
            + 0.20 * gpu_score
            + 0.25 * latency_score
        )

        return round(qos_score, 2)