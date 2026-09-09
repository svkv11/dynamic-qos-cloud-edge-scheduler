class TaskQueue:
    def __init__(self):
        self.pending_tasks = []

    def add_task(self, task):
        """
        Add a task to the pending queue.
        """

        if task.state != "PENDING":
            return False

        self.pending_tasks.append(task)
        return True

    def get_next_task(self):
        """
        Remove and return the next pending task.

        Returns None if the queue is empty.
        """

        if not self.pending_tasks:
            return None

        return self.pending_tasks.pop(0)

    def peek_next_task(self):
        """
        Return the next pending task without removing it.
        """

        if not self.pending_tasks:
            return None

        return self.pending_tasks[0]

    def is_empty(self):
        """
        Check whether the queue is empty.
        """

        return len(self.pending_tasks) == 0

    def size(self):
        """
        Return the number of pending tasks.
        """

        return len(self.pending_tasks)

    def display_queue(self):
        """
        Display all pending tasks in the queue.
        """

        print("=" * 40)
        print("TASK QUEUE")
        print("=" * 40)

        if self.is_empty():
            print("Queue is empty.")
        else:
            for index, task in enumerate(
                self.pending_tasks,
                start=1
            ):
                print(
                    f"{index}. "
                    f"{task.task_id} | "
                    f"{task.workload_type} | "
                    f"Priority={task.priority} | "
                    f"State={task.state}"
                )

        print("=" * 40)