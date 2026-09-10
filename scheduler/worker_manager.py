class WorkerManager:
    def __init__(self, workers):
        self.workers = workers

    def start_all(self):
        """
        Start all workers.
        """

        for worker in self.workers:
            worker.start()

    def stop_all(self):
        """
        Stop all workers.
        """

        for worker in self.workers:
            worker.stop()

    def get_ready_workers(self):
        """
        Return workers that are currently READY.
        """

        return [
            worker
            for worker in self.workers
            if worker.status == "READY"
        ]

    def get_busy_workers(self):
        """
        Return workers that are currently BUSY.
        """

        return [
            worker
            for worker in self.workers
            if worker.status == "BUSY"
        ]

    def get_available_nodes(self):
        """
        Return nodes whose workers are READY.
        """

        return [
            worker.node
            for worker in self.get_ready_workers()
        ]

    def get_worker_for_node(self, node_id):
        """
        Find the worker assigned to a specific node.
        """

        for worker in self.workers:
            if worker.node.node_id == node_id:
                return worker

        return None

    def get_worker_count(self):
        """
        Return the total number of workers.
        """

        return len(self.workers)

    def get_ready_worker_count(self):
        """
        Return the number of READY workers.
        """

        return len(self.get_ready_workers())

    def get_busy_worker_count(self):
        """
        Return the number of BUSY workers.
        """

        return len(self.get_busy_workers())

    def display_status(self):
        """
        Display the status of all workers.
        """

        print("=" * 60)
        print("WORKER MANAGER STATUS")
        print("=" * 60)

        for worker in self.workers:
            worker.display_info()

        print(
            f"Total Workers: "
            f"{self.get_worker_count()}"
        )

        print(
            f"READY Workers: "
            f"{self.get_ready_worker_count()}"
        )

        print(
            f"BUSY Workers: "
            f"{self.get_busy_worker_count()}"
        )

        print("=" * 60)