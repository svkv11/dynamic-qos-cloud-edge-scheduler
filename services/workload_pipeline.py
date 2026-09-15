import os
import sys


# Add the project root directory to Python's import path.
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from llm_requirement_interpreter import (
    LLMRequirementInterpreter
)

from workload_profiler import (
    WorkloadProfiler
)

from scheduler.task import Task

from scheduler.scheduler import (
    QoSScheduler
)


class WorkloadPipeline:
    """
    Complete natural-language workload processing pipeline.

    Flow:

    User Request
        ↓
    LLM Requirement Interpreter
        ↓
    Workload Profiler
        ↓
    Task
        ↓
    QoS Scheduler
    """

    def __init__(self, nodes):
        """
        Initialize the pipeline with available compute nodes.
        """

        self.scheduler = QoSScheduler(nodes)

    def process_request(self, user_request, task_id="llm-task-001"):
        """
        Process a natural-language workload request.

        Returns:

        {
            "user_request": ...,
            "interpreted_requirements": ...,
            "final_requirements": ...,
            "task": ...,
            "selected_node": ...,
            "rankings": ...
        }
        """

        # --------------------------------------------------
        # Step 1: Interpret natural-language request
        # --------------------------------------------------

        interpreted_requirements = (
            LLMRequirementInterpreter.interpret(
                user_request
            )
        )

        # --------------------------------------------------
        # Step 2: Convert interpretation into
        #         technical requirements
        # --------------------------------------------------

        final_requirements = (
            WorkloadProfiler.build_requirements(
                interpreted_requirements
            )
        )

        # --------------------------------------------------
        # Step 3: Create Task
        # --------------------------------------------------

        task = Task(
            task_id=task_id,
            workload_type=final_requirements["workload_type"],
            cpu_required=final_requirements["cpu_required"],
            memory_required_gb=final_requirements["memory_required_gb"],
            gpu_required=final_requirements["gpu_required"],
            deadline_seconds=final_requirements["deadline_seconds"],
            priority=final_requirements["priority"]
        )

        # --------------------------------------------------
        # Step 4: Rank available nodes
        # --------------------------------------------------

        rankings = self.scheduler.get_node_rankings(
            task
        )

        # --------------------------------------------------
        # Step 5: Select best node
        # --------------------------------------------------

        selected_node = self.scheduler.select_best_node(
            task
        )

        # --------------------------------------------------
        # Return complete pipeline result
        # --------------------------------------------------

        return {
            "user_request": user_request,
            "interpreted_requirements": interpreted_requirements,
            "final_requirements": final_requirements,
            "task": task,
            "selected_node": selected_node,
            "rankings": rankings
        }