from scheduler.task import Task
from genai.task_requirements import TaskRequirements


class TaskConverter:
    """
    Convert structured GenAI task requirements
    into the existing scheduler Task model.
    """

    @staticmethod
    def requirements_to_task(
        requirements,
        task_id,
        max_retries=3
    ):
        """
        Convert TaskRequirements into a Task object.
        """

        if not isinstance(
            requirements,
            TaskRequirements
        ):
            raise TypeError(
                "requirements must be a "
                "TaskRequirements object"
            )

        return Task(
            task_id=task_id,
            workload_type=requirements.workload_type,
            cpu_required=requirements.cpu_required,
            memory_required_gb=(
                requirements.memory_required_gb
            ),
            gpu_required=requirements.gpu_required,
            deadline_seconds=(
                requirements.deadline_seconds
            ),
            priority=requirements.priority,
            max_retries=max_retries
        )