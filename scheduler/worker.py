class Worker:
    def __init__(self, worker_id, node):
        self.worker_id = worker_id
        self.node = node
        self.status = "IDLE"

    def start(self):
        """
        Mark the worker as ready to execute a task.
        """
        self.status = "READY"

    def stop(self):
        """
        Mark the worker as stopped.
        """
        self.status = "STOPPED"

    def display_info(self):
        print(f"Worker ID: {self.worker_id}")
        print(f"Node ID: {self.node.node_id}")
        print(f"Node Type: {self.node.node_type}")
        print(f"Worker Status: {self.status}")
        print("-" * 40)