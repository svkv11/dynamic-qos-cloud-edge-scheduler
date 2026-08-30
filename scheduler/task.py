class Task:
    def __init__(
        self,
        task_id,
        workload_type,
        cpu_required,
        memory_required_gb,
        gpu_required=False,
        deadline_seconds=None,
        priority=1
    ):
        self.task_id = task_id
        self.workload_type = workload_type

        # Resource requirements
        self.cpu_required = cpu_required
        self.memory_required_gb = memory_required_gb
        self.gpu_required = gpu_required

        # QoS requirements
        self.deadline_seconds = deadline_seconds
        self.priority = priority

    def display_info(self):
        print(f"Task ID: {self.task_id}")
        print(f"Workload Type: {self.workload_type}")

        print(f"CPU Required: {self.cpu_required} cores")
        print(f"Memory Required: {self.memory_required_gb} GB")
        print(f"GPU Required: {self.gpu_required}")

        print(f"Deadline: {self.deadline_seconds} seconds")
        print(f"Priority: {self.priority}")

        print("-" * 40)