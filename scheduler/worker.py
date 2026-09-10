class Worker:
    def __init__(self, worker_id, node):
        self.worker_id = worker_id
        self.node = node
        self.status = "IDLE"

    def start(self):
        """
        Mark the worker as ready to execute tasks.
        """
        self.status = "READY"

    def stop(self):
        """
        Mark the worker as stopped.
        """
        self.status = "STOPPED"

    def execute_task(self, task, executor):
        """
        Execute a task using the TaskExecutor.

        The worker must be READY before execution.

        READY -> BUSY

        Returns the task state created by the executor.
        """
        if self.status != "READY":
            return None

        self.status = "BUSY"

        task_state = executor.start_task(
            task,
            self.node
        )

        return task_state

    def task_finished(self):
        """
        Mark the worker as ready after task execution.
        """
        if self.status == "BUSY":
            self.status = "READY"

    def display_info(self):
        print(f"Worker ID: {self.worker_id}")
        print(f"Node ID: {self.node.node_id}")
        print(f"Node Type: {self.node.node_type}")
        print(f"Worker Status: {self.status}")
        print("-" * 40)