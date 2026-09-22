import time

from execution.execution_result import ExecutionResult


class WorkloadRunner:
    """
    Execute real workloads for the Live Execution Layer.

    This component is separate from TaskExecutor.
    TaskExecutor continues to provide the estimated execution
    time used by the research scheduler.

    WorkloadRunner measures actual wall-clock execution time.
    """

    def run(self, task, node):
        """
        Execute the workload associated with the task.

        Parameters:
        - task: existing scheduler Task object
        - node: selected ComputeNode

        Returns:
        - ExecutionResult
        """

        start_time = time.perf_counter()

        try:
            output = self._execute_workload(task)

            end_time = time.perf_counter()

            actual_execution_time = round(
                end_time - start_time,
                4
            )

            deadline_met = self._check_deadline(
                task.deadline_seconds,
                actual_execution_time
            )

            return ExecutionResult(
                task_id=task.task_id,
                node_id=node.node_id,
                workload_type=task.workload_type,
                output=output,
                actual_execution_time=actual_execution_time,
                deadline_seconds=task.deadline_seconds,
                deadline_met=deadline_met,
                success=True,
                error=None
            )

        except Exception as error:

            end_time = time.perf_counter()

            actual_execution_time = round(
                end_time - start_time,
                4
            )

            return ExecutionResult(
                task_id=task.task_id,
                node_id=node.node_id,
                workload_type=task.workload_type,
                output=None,
                actual_execution_time=actual_execution_time,
                deadline_seconds=task.deadline_seconds,
                deadline_met=False,
                success=False,
                error=str(error)
            )

    def _execute_workload(self, task):
        """
        Execute a real workload based on workload type.
        """

        if task.workload_type == "general":
            return self._run_general_workload(task)

        if task.workload_type == "cpu_intensive":
            return self._run_cpu_workload(task)

        if task.workload_type == "memory_intensive":
            return self._run_memory_workload(task)

        raise ValueError(
            "Live execution is not yet supported for workload type: "
            + task.workload_type
        )

    def _run_general_workload(self, task):
        """
        Perform a real computational workload.
        """

        iterations = max(
            100_000,
            task.cpu_required * 100_000
        )

        total = 0

        for number in range(1, iterations + 1):
            total += number * number

        return {
            "message": "General workload executed successfully.",
            "iterations": iterations,
            "computed_value": total
        }

    def _run_cpu_workload(self, task):
        """
        Perform a CPU-intensive computational workload.
        """

        iterations = max(
            500_000,
            task.cpu_required * 500_000
        )

        total = 0

        for number in range(1, iterations + 1):
            total += number * number

        return {
            "message": "CPU-intensive workload executed successfully.",
            "iterations": iterations,
            "computed_value": total
        }

    def _run_memory_workload(self, task):
        """
        Perform a real memory-intensive workload.

        The amount of memory is bounded so that the live demo
        does not attempt to consume excessive system memory.
        """

        requested_memory_mb = max(
            16,
            int(task.memory_required_gb * 64)
        )

        memory_mb = min(
            requested_memory_mb,
            512
        )

        block_size = 1024 * 1024

        data = bytearray(
            memory_mb * block_size
        )

        for index in range(0, len(data), block_size):
            data[index] = 1

        checksum = sum(
            data[index]
            for index in range(
                0,
                len(data),
                block_size
            )
        )

        return {
            "message": "Memory-intensive workload executed successfully.",
            "allocated_memory_mb": memory_mb,
            "processed_blocks": memory_mb,
            "checksum": checksum
        }

    @staticmethod
    def _check_deadline(
        deadline_seconds,
        actual_execution_time
    ):
        """
        Determine whether the real execution met the deadline.
        """

        if deadline_seconds is None:
            return None

        return actual_execution_time <= deadline_seconds