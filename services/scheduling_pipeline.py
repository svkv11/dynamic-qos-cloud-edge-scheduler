import os
import sys


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from services.llm_requirement_interpreter import (
    LLMRequirementInterpreter
)

from services.workload_profiler import (
    WorkloadProfiler
)

from scheduler.task import Task

from scheduler.scheduler import (
    QoSScheduler
)

from scheduler.task_executor import (
    TaskExecutor
)

from scheduler.worker import (
    Worker
)

from scheduler.metrics import (
    MetricsCollector
)


class SchedulingPipeline:
    """
    Complete end-to-end pipeline for the
    Dynamic QoS Cloud-Edge Scheduler.

    Pipeline:

        Natural-language request
                    ↓
        LLM Requirement Interpreter
                    ↓
        Workload Profiler
                    ↓
        Task
                    ↓
        QoS Scheduler
                    ↓
        Best Node
                    ↓
        Worker
                    ↓
        Task Executor
                    ↓
        Execution Result
                    ↓
        Metrics Collector
    """

    def __init__(self, nodes):
        self.nodes = nodes
        self.scheduler = QoSScheduler(nodes)
        self.executor = TaskExecutor()
        self.metrics_collector = MetricsCollector()

    def process_request(
        self,
        user_request,
        task_id="llm-task-001"
    ):
        interpreted_requirements = (
            LLMRequirementInterpreter.interpret(
                user_request
            )
        )

        final_requirements = (
            WorkloadProfiler.build_requirements(
                interpreted_requirements
            )
        )

        task = Task(
            task_id=task_id,
            workload_type=final_requirements[
                "workload_type"
            ],
            cpu_required=final_requirements[
                "cpu_required"
            ],
            memory_required_gb=final_requirements[
                "memory_required_gb"
            ],
            gpu_required=final_requirements[
                "gpu_required"
            ],
            deadline_seconds=final_requirements[
                "deadline_seconds"
            ],
            priority=final_requirements[
                "priority"
            ]
        )

        rankings = self.scheduler.get_node_rankings(
            task
        )

        best_node = self.scheduler.select_best_node(
            task
        )

        if best_node is None:
            raise RuntimeError(
                "No feasible node is available "
                "for the requested task."
            )

        worker = Worker(
            worker_id=f"worker-{best_node.node_id}",
            node=best_node
        )

        worker.start()

        task_state = worker.execute_task(
            task,
            self.executor
        )

        if task_state is None:
            raise RuntimeError(
                "The selected worker was not ready "
                "to execute the task."
            )

        execution_result = (
            self.executor.complete_task(
                task_state
            )
        )

        worker.task_finished()

        qos_score = (
            self.scheduler.calculate_task_score(
                best_node,
                task
            )
        )

        self.metrics_collector.record_task(
            task=task,
            node=best_node,
            execution_time=execution_result[
                "execution_time"
            ],
            deadline_met=execution_result[
                "deadline_met"
            ],
            qos_score=qos_score
        )

        return {
            "user_request": user_request,
            "interpreted_requirements":
                interpreted_requirements,
            "final_requirements":
                final_requirements,
            "task": task,
            "rankings": rankings,
            "selected_node": best_node,
            "execution_result": execution_result,
            "qos_score": qos_score,
            "metrics_collector":
                self.metrics_collector
        }

    def get_metrics(self):
        return self.metrics_collector