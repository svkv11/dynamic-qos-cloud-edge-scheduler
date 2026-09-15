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


def create_nodes(
    include_memory_edge_node=False
):
    """
    Create a fresh node environment for each experiment.

    The optional memory-capable edge node is used for
    memory-pressure evaluation so that the scheduler has
    multiple feasible placement choices.
    """

    nodes = [
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

    if include_memory_edge_node:
        nodes.append(
            ComputeNode(
                node_id="edge-03",
                node_type="edge",
                cpu_cores=12,
                memory_gb=24,
                gpu_available=False,
                cpu_utilization=35,
                memory_utilization=35,
                gpu_utilization=0,
                network_latency_ms=20
            )
        )

    return nodes


def interpret_requests(requests):
    """
    Convert natural-language requests into structured
    scheduling requirements.

    This is done once so all schedulers receive the
    same workload requirements.
    """

    tasks = []

    for index, request in enumerate(
        requests,
        start=1
    ):

        interpreted = (
            LLMRequirementInterpreter.interpret(
                request
            )
        )

        requirements = (
            WorkloadProfiler.build_requirements(
                interpreted
            )
        )

        tasks.append({
            "request": request,
            "interpreted": interpreted,
            "requirements": requirements,
            "task_id": f"stress-task-{index}"
        })

    return tasks


def build_tasks(task_information):
    """
    Build Task objects from previously interpreted
    requirements.
    """

    tasks = []

    for item in task_information:

        requirements = item["requirements"]

        task = Task(
            task_id=item["task_id"],
            workload_type=requirements[
                "workload_type"
            ],
            cpu_required=requirements[
                "cpu_required"
            ],
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

        tasks.append(task)

    return tasks


def execute_assignments(
    assignments,
    scheduler
):
    """
    Evaluate baseline assignments.
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

        execution_time = (
            executor.estimate_execution_time(
                task,
                node
            )
        )

        deadline_met = (
            task.deadline_seconds is None
            or execution_time <= task.deadline_seconds
        )

        qos_score = scheduler.calculate_task_score(
            node,
            task
        )

        results.append({
            "task_id": task.task_id,
            "node_id": node.node_id,
            "execution_time": execution_time,
            "deadline_met": deadline_met,
            "qos_score": round(
                qos_score,
                2
            ),
            "state": (
                "COMPLETED"
                if deadline_met
                else "FAILED"
            )
        })

    return results


def run_round_robin(
    task_information,
    include_memory_edge_node=False
):
    """
    Run Round Robin baseline.
    """

    nodes = create_nodes(
        include_memory_edge_node
    )

    baseline = BaselineScheduler(nodes)

    tasks = build_tasks(
        task_information
    )

    assignments = baseline.round_robin(
        tasks
    )

    scheduler = QoSScheduler(nodes)

    return execute_assignments(
        assignments,
        scheduler
    )


def run_resource_only(
    task_information,
    include_memory_edge_node=False
):
    """
    Run resource-only baseline.
    """

    nodes = create_nodes(
        include_memory_edge_node
    )

    baseline = BaselineScheduler(nodes)

    tasks = build_tasks(
        task_information
    )

    assignments = baseline.resource_only(
        tasks
    )

    scheduler = QoSScheduler(nodes)

    return execute_assignments(
        assignments,
        scheduler
    )


def run_genai(
    requests,
    include_memory_edge_node=False
):
    """
    Run the complete GenAI + Dynamic QoS pipeline.
    """

    nodes = create_nodes(
        include_memory_edge_node
    )

    pipeline = SchedulingPipeline(nodes)

    results = []

    for index, request in enumerate(
        requests,
        start=1
    ):

        result = pipeline.process_request(
            user_request=request,
            task_id=f"genai-stress-{index}"
        )

        execution = result[
            "execution_result"
        ]

        results.append({
            "task_id": f"genai-stress-{index}",
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


def calculate_summary(results):
    """
    Calculate evaluation metrics.
    """

    total = len(results)

    completed = sum(
        1
        for result in results
        if result["state"] == "COMPLETED"
    )

    failed = sum(
        1
        for result in results
        if result["state"] == "FAILED"
    )

    deadline_success = sum(
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

    deadline_rate = (
        round(
            deadline_success
            / total
            * 100,
            2
        )
        if total
        else 0.0
    )

    return {
        "total": total,
        "completed": completed,
        "failed": failed,
        "deadline_rate": deadline_rate,
        "average_execution_time":
            average_execution_time,
        "average_qos":
            average_qos
    }


def print_summary(
    scenario_name,
    summaries
):
    """
    Print scenario comparison.
    """

    print()
    print("=" * 95)

    print(
        f"SCENARIO: {scenario_name}"
    )

    print("=" * 95)

    print(
        f"{'Metric':<30}"
        f"{'Round Robin':<20}"
        f"{'Resource Only':<20}"
        f"{'GenAI + QoS':<20}"
    )

    print("-" * 95)

    print(
        f"{'Tasks':<30}"
        f"{summaries['Round Robin']['total']:<20}"
        f"{summaries['Resource Only']['total']:<20}"
        f"{summaries['GenAI + QoS']['total']:<20}"
    )

    print(
        f"{'Completed':<30}"
        f"{summaries['Round Robin']['completed']:<20}"
        f"{summaries['Resource Only']['completed']:<20}"
        f"{summaries['GenAI + QoS']['completed']:<20}"
    )

    print(
        f"{'Failed':<30}"
        f"{summaries['Round Robin']['failed']:<20}"
        f"{summaries['GenAI + QoS']['failed']:<20}"
        f"{summaries['GenAI + QoS']['failed']:<20}"
    )

    print(
        f"{'Deadline Success (%)':<30}"
        f"{summaries['Round Robin']['deadline_rate']:<20}"
        f"{summaries['Resource Only']['deadline_rate']:<20}"
        f"{summaries['GenAI + QoS']['deadline_rate']:<20}"
    )

    print(
        f"{'Avg Execution Time':<30}"
        f"{summaries['Round Robin']['average_execution_time']:<20}"
        f"{summaries['Resource Only']['average_execution_time']:<20}"
        f"{summaries['GenAI + QoS']['average_execution_time']:<20}"
    )

    print(
        f"{'Avg QoS':<30}"
        f"{summaries['Round Robin']['average_qos']:<20}"
        f"{summaries['Resource Only']['average_qos']:<20}"
        f"{summaries['GenAI + QoS']['average_qos']:<20}"
    )

    print("=" * 95)


def run_scenario(
    scenario_name,
    requests
):
    """
    Execute one complete stress scenario.
    """

    print()
    print("=" * 95)

    print(
        f"STARTING SCENARIO: {scenario_name}"
    )

    print("=" * 95)

    print(
        f"Number of workloads: "
        f"{len(requests)}"
    )

    include_memory_edge_node = (
        scenario_name == "High Memory Pressure"
    )

    if include_memory_edge_node:
        print()
        print(
            "Memory-capable edge node enabled:"
        )
        print(
            "edge-03 | 12 CPU cores | "
            "24 GB RAM | 20 ms latency"
        )

    print()
    print(
        "Interpreting natural-language workloads..."
    )

    task_information = interpret_requests(
        requests
    )

    print(
        "Running Round Robin..."
    )

    round_robin_results = run_round_robin(
        task_information,
        include_memory_edge_node
    )

    print(
        "Running Resource Only..."
    )

    resource_only_results = run_resource_only(
        task_information,
        include_memory_edge_node
    )

    print(
        "Running GenAI + Dynamic QoS..."
    )

    genai_results = run_genai(
        requests,
        include_memory_edge_node
    )

    summaries = {
        "Round Robin": calculate_summary(
            round_robin_results
        ),
        "Resource Only": calculate_summary(
            resource_only_results
        ),
        "GenAI + QoS": calculate_summary(
            genai_results
        )
    }

    print_summary(
        scenario_name,
        summaries
    )

    return summaries


def main():

    print()
    print("=" * 95)

    print(
        "STEP 17 - MEMORY-AWARE STRESS EVALUATION"
    )

    print("=" * 95)

    scenarios = {

        "Normal Mixed Workload": [
            "Create an AI image quickly.",
            "Analyze a large dataset.",
            "Process a CPU-heavy workload.",
            "Run a deep learning model using GPU.",
            "Run a normal data processing task.",
            "Analyze a large memory-intensive dataset.",
            "Run an urgent AI workload.",
            "Process a CPU-intensive computation.",
            "Generate an AI image using GPU.",
            "Run a normal workload."
        ],

        "High CPU Pressure": [
            "Process a CPU-heavy workload using 6 CPU cores.",
            "Run a CPU-intensive computation.",
            "Perform heavy CPU processing.",
            "Execute a CPU-heavy data analysis task.",
            "Run a CPU-intensive workload.",
            "Process a workload requiring high CPU.",
            "Perform intensive CPU computation.",
            "Run another CPU-heavy task.",
            "Execute heavy CPU processing.",
            "Process a high CPU workload."
        ],

        "High Memory Pressure": [
            "Analyze a very large dataset that requires a lot of RAM.",
            "Process a memory-intensive dataset.",
            "Run a large RAM-intensive analysis.",
            "Analyze a very large memory workload.",
            "Process a workload requiring high memory.",
            "Run a memory-intensive computation.",
            "Analyze a large dataset with high RAM usage.",
            "Process a large memory workload.",
            "Run another RAM-intensive task.",
            "Analyze a high-memory dataset."
        ],

        "GPU Heavy": [
            "Create an AI image quickly.",
            "Run a deep learning model using GPU.",
            "Perform GPU-accelerated machine learning.",
            "Generate an AI image using GPU.",
            "Run a neural network training workload using GPU.",
            "Perform GPU-intensive deep learning.",
            "Run an AI inference workload using GPU.",
            "Generate an image with GPU acceleration.",
            "Run a GPU-intensive model.",
            "Perform deep learning using GPU."
        ],

        "Tight Deadlines": [
            "Run the deep learning model using GPU within 8 seconds.",
            "Process the CPU workload within 10 seconds.",
            "Analyze the dataset within 12 seconds.",
            "Create the AI image within 8 seconds.",
            "Run the urgent GPU workload within 10 seconds.",
            "Process the task within 12 seconds.",
            "Run the deep learning task within 9 seconds.",
            "Complete the CPU-heavy task within 10 seconds.",
            "Analyze the memory-intensive workload within 12 seconds.",
            "Finish the AI workload within 8 seconds."
        ],

        "Priority Conflict": [
            "Run this task urgently using CPU.",
            "Run the GPU workload urgently.",
            "Analyze the large dataset with high priority.",
            "Process this CPU-heavy workload normally.",
            "Run the deep learning workload as soon as possible.",
            "Perform the memory-intensive task urgently.",
            "Run this normal workload with low priority.",
            "Process the CPU task urgently.",
            "Run the GPU task with critical priority.",
            "Analyze this dataset normally."
        ]
    }

    all_results = {}

    for scenario_name, requests in scenarios.items():

        summaries = run_scenario(
            scenario_name,
            requests
        )

        all_results[
            scenario_name
        ] = summaries

    print()
    print("=" * 110)

    print(
        "OVERALL STRESS EVALUATION"
    )

    print("=" * 110)

    print(
        f"{'Scenario':<25}"
        f"{'RR Time':<12}"
        f"{'Resource Time':<15}"
        f"{'GenAI Time':<12}"
        f"{'RR QoS':<12}"
        f"{'Resource QoS':<15}"
        f"{'GenAI QoS':<12}"
    )

    print("-" * 110)

    for scenario_name, summaries in all_results.items():

        rr = summaries["Round Robin"]
        resource = summaries["Resource Only"]
        genai = summaries["GenAI + QoS"]

        print(
            f"{scenario_name:<25}"
            f"{rr['average_execution_time']:<12}"
            f"{resource['average_execution_time']:<15}"
            f"{genai['average_execution_time']:<12}"
            f"{rr['average_qos']:<12}"
            f"{resource['average_qos']:<15}"
            f"{genai['average_qos']:<12}"
        )

    print("=" * 110)

    print()
    print(
        "STEP 17 MEMORY-AWARE EVALUATION COMPLETED"
    )


if __name__ == "__main__":
    main()