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


print("=" * 60)
print("LLM + PROFILER + TASK INTEGRATION TEST")
print("=" * 60)


user_request = "Create an AI image quickly."


print("\nUser Request:")
print(user_request)


try:

    # --------------------------------------------------
    # Step 1: Interpret natural-language request
    # --------------------------------------------------

    interpreted_requirements = (
        LLMRequirementInterpreter.interpret(
            user_request
        )
    )

    print("\nLLM Interpretation:")
    print(interpreted_requirements)

    # --------------------------------------------------
    # Step 2: Build final technical requirements
    # --------------------------------------------------

    final_requirements = (
        WorkloadProfiler.build_requirements(
            interpreted_requirements
        )
    )

    print("\nFinal Profiled Requirements:")
    print(final_requirements)

    # --------------------------------------------------
    # Step 3: Create Task object
    # --------------------------------------------------

    task = Task(
        task_id="llm-task-001",
        workload_type=final_requirements["workload_type"],
        cpu_required=final_requirements["cpu_required"],
        memory_required_gb=final_requirements["memory_required_gb"],
        gpu_required=final_requirements["gpu_required"],
        deadline_seconds=final_requirements["deadline_seconds"],
        priority=final_requirements["priority"]
    )

    print("\nCreated Task:")
    print(task)

    # --------------------------------------------------
    # Step 4: Display Task information
    # --------------------------------------------------

    print("\nTask Information:")

    if hasattr(task, "display_info"):
        task.display_info()
    else:
        print("Task object created successfully.")

    print("\n" + "=" * 60)
    print("TASK INTEGRATION TEST PASSED")
    print("=" * 60)


except Exception as error:

    print("\nERROR:")
    print(error)