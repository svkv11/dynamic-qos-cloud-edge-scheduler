import os
import sys


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from scheduler.compute_node import ComputeNode
from scheduler.task import Task
from scheduler.scheduler import QoSScheduler
from scheduler.baseline_scheduler import BaselineScheduler
from scheduler.task_executor import TaskExecutor

from services.scheduling_pipeline import SchedulingPipeline
from services.workload_profiler import WorkloadProfiler
from services.llm_requirement_interpreter import (
    LLMRequirementInterpreter
)


def create_nodes():
    """
    Create a fresh set of nodes for every experiment.
    """

    return [
        ComputeNode(
            node_id="edge-01",
            node_type="edge",
            cpu_cores=4,
            memory_gb=8,
            gpu_available=False,
            cpu_utilization=25,
            memory_utilization=30,
            gpu_utilization=0,
            network_latency_ms=10
        ),

        ComputeNode(
            node_id="edge-02",
            node_type="edge",
            cpu_cores=8,
            memory_gb=16,
            gpu_available=True,
            cpu_utilization=40,
            memory_utilization=45,
            gpu_utilization=20,
            network_latency_ms=15
        ),

        ComputeNode(
            node_id="cloud-01",
            node_type="cloud",
            cpu_cores=16,
            memory_gb=32,
            gpu_available=True,
            cpu_utilization=55,
            memory_utilization=50,
            gpu_utilization=35,
            network_latency_ms=80
        )
    ]


def create_tasks_from_requests(requests):
    """
    Convert the natural-language requests into Tasks
    using the same LLM interpretation and workload
    profiling used by the GenAI scheduler.

    This gives the traditional baselines the same
    underlying task requirements for a fair comparison.
    """

    tasks = []

    for index, request in enumerate(requests, start=1):

        interpreted = LLMRequirementInterpreter.interpret(
            request
        )

        requirements = WorkloadProfiler.build_requirements(
            interpreted
        )

        task = Task(
            task_id=f"baseline-task-{index}",
            workload_type=requirements["workload_type"],
            cpu_required=requirements["cpu_required"],
            memory_required_gb=requirements[
                "memory_required_gb"
            ],
            gpu_required=requirements[
                "gpu_required"
            ],
            deadline_seconds=requirements[
                "deadline_seconds"
            ],
            priority=requirements[
                "priority"
            ]
        )

        tasks.append({
            "request": request,
            "interpreted": interpreted,
            "requirements": requirements,
            "task": task
        })

    return tasks


def execute_assignments(assignments, scheduler=None):
    """
    Execute baseline assignments and calculate
    execution metrics.
    """

    executor = TaskExecutor()

    results = []

    for assignment in assignments:

        task = assignment["task"]
        node = assignment["node"]

        if node is None:

            results.append({
                "task_id": task.task_id,
                "node_id": None,
                "execution_time": None,
                "deadline_met": False,
                "qos_score": 0.0,
                "state": "FAILED"
            })

            continue

        execution_time = executor.estimate_execution_time(
            task,
            node
        )

        deadline_met = (
            task.deadline_seconds is None
            or execution_time <= task.deadline_seconds
        )

        qos_score = None

        if scheduler is not None:
            qos_score = scheduler.calculate_task_score(
                node,
                task
            )
        else:
            qos_score = node.calculate_qos_score(
                task
            )

        results.append({
            "task_id": task.task_id,
            "node_id": node.node_id,
            "execution_time": execution_time,
            "deadline_met": deadline_met,
            "qos_score": round(qos_score, 2),
            "state": (
                "COMPLETED"
                if deadline_met
                else "FAILED"
            )
        })

    return results


def calculate_summary(results):
    """
    Calculate summary statistics for one scheduler.
    """

    total_tasks = len(results)

    completed_tasks = sum(
        1
        for result in results
        if result["state"] == "COMPLETED"
    )

    failed_tasks = sum(
        1
        for result in results
        if result["state"] == "FAILED"
    )

    deadline_successes = sum(
        1
        for result in results
        if result["deadline_met"]
    )

    execution_times = [
        result["execution_time"]
        for result in results
        if result["execution_time"] is not None
    ]

    qos_scores = [
        result["qos_score"]
        for result in results
        if result["qos_score"] is not None
    ]

    average_execution_time = (
        round(
            sum(execution_times)
            / len(execution_times),
            2
        )
        if execution_times
        else 0.0
    )

    average_qos = (
        round(
            sum(qos_scores)
            / len(qos_scores),
            2
        )
        if qos_scores
        else 0.0
    )

    deadline_success_rate = (
        round(
            (deadline_successes / total_tasks) * 100,
            2
        )
        if total_tasks
        else 0.0
    )

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "failed_tasks": failed_tasks,
        "deadline_success_rate": deadline_success_rate,
        "average_execution_time": average_execution_time,
        "average_qos": average_qos
    }


def run_round_robin(tasks):
    """
    Run the Round Robin baseline.
    """

    nodes = create_nodes()

    baseline = BaselineScheduler(nodes)

    task_objects = [
        item["task"]
        for item in tasks
    ]

    assignments = baseline.round_robin(
        task_objects
    )

    return execute_assignments(
        assignments
    )


def run_resource_only(tasks):
    """
    Run the resource-only baseline.
    """

    nodes = create_nodes()

    baseline = BaselineScheduler(nodes)

    task_objects = [
        item["task"]
        for item in tasks
    ]

    assignments = baseline.resource_only(
        task_objects
    )

    scheduler = QoSScheduler(nodes)

    return execute_assignments(
        assignments,
        scheduler
    )


def run_genai_scheduler(requests):
    """
    Run the complete GenAI-assisted scheduler.
    """

    nodes = create_nodes()

    pipeline = SchedulingPipeline(nodes)

    results = []

    for index, request in enumerate(
        requests,
        start=1
    ):

        result = pipeline.process_request(
            user_request=request,
            task_id=f"genai-task-{index}"
        )

        execution = result[
            "execution_result"
        ]

        results.append({
            "task_id": f"genai-task-{index}",
            "node_id": result[
                "selected_node"
            ].node_id,
            "execution_time": execution[
                "execution_time"
            ],
            "deadline_met": execution[
                "deadline_met"
            ],
            "qos_score": round(
                result["qos_score"],
                2
            ),
            "state": execution[
                "state"
            ]
        })

    return results


def display_results(
    name,
    results
):
    """
    Display task-level results.
    """

    print()
    print("=" * 70)
    print(f"{name} RESULTS")
    print("=" * 70)

    for result in results:

        print(
            f"Task: {result['task_id']}"
        )

        print(
            f"Node: {result['node_id']}"
        )

        print(
            f"Execution Time: "
            f"{result['execution_time']} seconds"
        )

        print(
            f"Deadline Met: "
            f"{result['deadline_met']}"
        )

        print(
            f"QoS Score: "
            f"{result['qos_score']}"
        )

        print(
            f"State: "
            f"{result['state']}"
        )

        print("-" * 70)


def display_comparison(
    round_robin_summary,
    resource_only_summary,
    genai_summary
):
    """
    Display the final comparison.
    """

    print()
    print("=" * 90)
    print("GENAI vs TRADITIONAL SCHEDULER COMPARISON")
    print("=" * 90)

    print(
        f"{'Metric':<30}"
        f"{'Round Robin':<20}"
        f"{'Resource Only':<20}"
        f"{'GenAI + QoS':<20}"
    )

    print("-" * 90)

    print(
        f"{'Total Tasks':<30}"
        f"{round_robin_summary['total_tasks']:<20}"
        f"{resource_only_summary['total_tasks']:<20}"
        f"{genai_summary['total_tasks']:<20}"
    )

    print(
        f"{'Completed Tasks':<30}"
        f"{round_robin_summary['completed_tasks']:<20}"
        f"{resource_only_summary['completed_tasks']:<20}"
        f"{genai_summary['completed_tasks']:<20}"
    )

    print(
        f"{'Failed Tasks':<30}"
        f"{round_robin_summary['failed_tasks']:<20}"
        f"{resource_only_summary['failed_tasks']:<20}"
        f"{genai_summary['failed_tasks']:<20}"
    )

    print(
        f"{'Deadline Success (%)':<30}"
        f"{round_robin_summary['deadline_success_rate']:<20}"
        f"{resource_only_summary['deadline_success_rate']:<20}"
        f"{genai_summary['deadline_success_rate']:<20}"
    )

    print(
        f"{'Average Execution Time':<30}"
        f"{round_robin_summary['average_execution_time']:<20}"
        f"{resource_only_summary['average_execution_time']:<20}"
        f"{genai_summary['average_execution_time']:<20}"
    )

    print(
        f"{'Average QoS Score':<30}"
        f"{round_robin_summary['average_qos']:<20}"
        f"{resource_only_summary['average_qos']:<20}"
        f"{genai_summary['average_qos']:<20}"
    )

    print("=" * 90)


def main():

    print()
    print("=" * 70)
    print("STEP 14 - GENAI vs TRADITIONAL SCHEDULER")
    print("=" * 70)

    requests = [
        "Create an AI image quickly.",

        "Analyze a very large dataset that requires "
        "a lot of RAM.",

        "Process this CPU-heavy workload using 6 CPU cores.",

        "Run the deep learning model using GPU "
        "within 15 seconds.",

        "Run this task as urgently as possible."
    ]

    print()
    print("Natural-Language Workloads:")
    print()

    for index, request in enumerate(
        requests,
        start=1
    ):
        print(
            f"{index}. {request}"
        )

    print()
    print(
        "Interpreting workloads using Qwen..."
    )

    tasks = create_tasks_from_requests(
        requests
    )

    print()
    print(
        "LLM-derived task requirements:"
    )

    for item in tasks:

        print()
        print(
            f"Request: {item['request']}"
        )

        print(
            f"Workload Type: "
            f"{item['requirements']['workload_type']}"
        )

        print(
            f"CPU: "
            f"{item['requirements']['cpu_required']}"
        )

        print(
            f"Memory: "
            f"{item['requirements']['memory_required_gb']} GB"
        )

        print(
            f"GPU: "
            f"{item['requirements']['gpu_required']}"
        )

        print(
            f"Priority: "
            f"{item['requirements']['priority']}"
        )

        print(
            f"Deadline: "
            f"{item['requirements']['deadline_seconds']}"
        )

    print()
    print(
        "Running Round Robin baseline..."
    )

    round_robin_results = run_round_robin(
        tasks
    )

    print(
        "Running Resource Only baseline..."
    )

    resource_only_results = run_resource_only(
        tasks
    )

    print(
        "Running GenAI + Dynamic QoS scheduler..."
    )

    genai_results = run_genai_scheduler(
        requests
    )

    display_results(
        "ROUND ROBIN",
        round_robin_results
    )

    display_results(
        "RESOURCE ONLY",
        resource_only_results
    )

    display_results(
        "GENAI + DYNAMIC QOS",
        genai_results
    )

    round_robin_summary = calculate_summary(
        round_robin_results
    )

    resource_only_summary = calculate_summary(
        resource_only_results
    )

    genai_summary = calculate_summary(
        genai_results
    )

    display_comparison(
        round_robin_summary,
        resource_only_summary,
        genai_summary
    )

    print()
    print("=" * 70)
    print(
        "STEP 14 BASELINE COMPARISON COMPLETED"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()