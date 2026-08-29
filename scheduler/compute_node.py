class ComputeNode:
    def __init__(self, node_id, node_type, cpu_cores, memory_gb, gpu_available):
        self.node_id = node_id
        self.node_type = node_type
        self.cpu_cores = cpu_cores
        self.memory_gb = memory_gb
        self.gpu_available = gpu_available

    def display_info(self):
        print(f"Node ID: {self.node_id}")
        print(f"Node Type: {self.node_type}")
        print(f"CPU Cores: {self.cpu_cores}")
        print(f"Memory: {self.memory_gb} GB")
        print(f"GPU Available: {self.gpu_available}")
        print("-" * 40)