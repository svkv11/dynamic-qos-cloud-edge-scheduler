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

        # Prevent utilization from becoming negative
        self.cpu_utilization = max(0.0, self.cpu_utilization)
        self.memory_utilization = max(0.0, self.memory_utilization)
        self.gpu_utilization = max(0.0, self.gpu_utilization)