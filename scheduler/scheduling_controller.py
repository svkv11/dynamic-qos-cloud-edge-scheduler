class SchedulingController:
    def __init__(
        self,
        scheduler,
        executor,
        worker_manager
    ):
        self.scheduler = scheduler
        self.executor = executor
        self.worker_manager = worker_manager

        self.active_tasks = []
        self.completed_tasks = []
        self.failed_tasks = []

    def start_workers(self):
        """
        Start all workers managed by WorkerManager.
        """

        self.worker_manager.start_all()

    def schedule_pending_tasks(self):
        """
        Schedule as many pending tasks as possible
        using currently READY workers.
        """

        scheduled_count = 0

        while self.scheduler.has_pending_tasks():

            available_nodes = (
                self.worker_manager.get_available_nodes()
            )

            result = self.scheduler.schedule_next_task(
                available_nodes
            )

            if result is None:
                break

            task, node = result

            worker = (
                self.worker_manager.get_worker_for_node(
                    node.node_id
                )
            )

            if worker is None:
                break

            task_state = worker.execute_task(
                task,
                self.executor
            )

            if task_state is None:
                break

            self.active_tasks.append(
                {
                    "task_state": task_state,
                    "worker": worker
                }
            )

            scheduled_count += 1

        return scheduled_count

    def complete_active_tasks(self):
        """
        Complete all currently active tasks.

        Workers become READY after their tasks finish.
        """

        completed_count = 0

        while self.active_tasks:

            active_task = self.active_tasks.pop(0)

            task_state = active_task["task_state"]
            worker = active_task["worker"]

            result = self.executor.complete_task(
                task_state
            )

            worker.task_finished()

            if result["state"] == "COMPLETED":
                self.completed_tasks.append(result)
                completed_count += 1
            else:
                self.failed_tasks.append(result)

        return completed_count

    def run_cycle(self):
        """
        Execute one complete scheduling cycle.

        1. Schedule pending tasks
        2. Complete active tasks
        3. Retry any remaining pending tasks
        4. Repeat until no pending or active tasks remain
        """

        total_completed = 0

        while (
            self.scheduler.has_pending_tasks()
            or self.active_tasks
        ):

            scheduled = self.schedule_pending_tasks()

            if self.active_tasks:
                completed = self.complete_active_tasks()
                total_completed += completed
            else:
                completed = 0

            if (
                self.scheduler.has_pending_tasks()
                and scheduled == 0
                and completed == 0
            ):
                break

        return total_completed

    def get_active_task_count(self):
        """
        Return the number of currently active tasks.
        """

        return len(self.active_tasks)

    def get_completed_task_count(self):
        """
        Return the number of completed tasks.
        """

        return len(self.completed_tasks)

    def get_failed_task_count(self):
        """
        Return the number of failed tasks.
        """

        return len(self.failed_tasks)

    def display_status(self):
        """
        Display the current scheduling controller status.
        """

        print("=" * 60)
        print("SCHEDULING CONTROLLER STATUS")
        print("=" * 60)

        print(
            f"Pending Tasks: "
            f"{self.scheduler.pending_task_count()}"
        )

        print(
            f"Active Tasks: "
            f"{self.get_active_task_count()}"
        )

        print(
            f"Completed Tasks: "
            f"{self.get_completed_task_count()}"
        )

        print(
            f"Failed Tasks: "
            f"{self.get_failed_task_count()}"
        )

        print("=" * 60)