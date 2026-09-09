class TaskQueue:
    def __init__(self):
        self.pending_tasks = []

    def add_task(self, task):
        """
        Add a pending task to the queue.

        Tasks are maintained in QoS-aware order:
        1. Higher priority first
        2. Shorter deadline first
        3. Earlier arrival first when values are equal
        """

        if task.state != "PENDING":
            return False

        self.pending_tasks.append(task)

        self._sort_queue()

        return True

    def _deadline_value(self, task):
        """
        Convert deadline into a sortable value.

        Tasks without a deadline are placed after
        tasks that have deadlines.
        """

        if task.deadline_seconds is None:
            return float("inf")

        return task.deadline_seconds

    def _sort_queue(self):
        """
        Sort pending tasks according to QoS requirements.

        Higher priority comes first.
        For equal priority, shorter deadlines come first.
        Python's stable sorting preserves arrival order
        when both values are equal.
        """

        self.pending_tasks.sort(
            key=lambda task: (
                -task.priority,
                self._deadline_value(task)
            )
        )

    def get_next_task(self):
        """
        Remove and return the highest-priority pending task.

        Returns None if the queue is empty.
        """

        if not self.pending_tasks:
            return None

        return self.pending_tasks.pop(0)

    def peek_next_task(self):
        """
        Return the next task without removing it.
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
        Display all pending tasks in QoS order.
        """

        print("=" * 40)
        print("QOS-AWARE TASK QUEUE")
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
                    f"Deadline={task.deadline_seconds}s | "
                    f"State={task.state}"
                )

        print("=" * 40)