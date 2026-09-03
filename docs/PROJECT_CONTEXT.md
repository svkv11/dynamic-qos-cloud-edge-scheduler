# Dynamic QoS Cloud-Edge Scheduler

## Project Overview

Dynamic QoS Cloud-Edge Scheduler is a software-based cloud-edge scheduling system that dynamically selects the most suitable compute node for heterogeneous workloads.

The scheduler considers:

- CPU requirements
- Memory requirements
- GPU requirements
- Current CPU utilization
- Current memory utilization
- Current GPU utilization
- Network latency
- Task priority
- Task deadline
- QoS score

The long-term architecture is:

User/Application
        ↓
LLM Requirement Interpretation
        ↓
Task/Workload Model
        ↓
Dynamic QoS Scheduler
        ↓
Cloud/Edge Workers
        ↓
Task Execution
        ↓
Resource Updates
        ↓
Scheduler Feedback


## Completed Milestones

### Day 1 — Project Setup

Completed:

- GitHub repository created
- Python virtual environment configured
- Project structure created
- Scheduler package created
- Git configuration completed
- README created
- `.gitignore` created
- `docs/PROJECT_CONTEXT.md` created


### Day 2 — Compute Node Model

Implemented `scheduler/compute_node.py`.

The `ComputeNode` model supports:

#### Fixed Resources

- Node ID
- Node type
- CPU cores
- Memory capacity
- GPU availability

#### Dynamic Resource State

- CPU utilization
- Memory utilization
- GPU utilization
- Network latency

#### Node Operations

- Display node state
- Check task feasibility
- Allocate task resources
- Release task resources
- Calculate QoS score


### Day 2 — Task / Workload Model

Implemented `scheduler/task.py`.

The `Task` model supports:

- Task ID
- Workload type
- CPU requirement
- Memory requirement
- GPU requirement
- Deadline
- Priority

Example workload categories:

- CPU-intensive
- Memory-intensive
- GPU-intensive
- Latency-sensitive


### Day 2 — Basic QoS Scheduler

Implemented `scheduler/scheduler.py`.

The `QoSScheduler` supports:

- Feasible-node filtering
- QoS-based node selection
- Task allocation
- Node ranking


### Day 3 — Task-Aware QoS Scoring

The scheduler was extended to include task-specific scheduling factors.

Current scoring model:

- 80% infrastructure/resource suitability
- 10% task priority
- 10% deadline urgency

Priority mapping:

- Priority 1 → 20
- Priority 2 → 40
- Priority 3 → 60
- Priority 4 → 80
- Priority 5 → 100

Deadline urgency:

- No deadline → 50
- Non-positive deadline → 100
- Shorter deadlines receive higher urgency
- Score is bounded between 0 and 100

The deadline score currently represents urgency rather than a guaranteed deadline constraint.


### Day 3 — Heterogeneous Workload Testing

The scheduler was tested using four workload types:

1. CPU-intensive
2. Memory-intensive
3. GPU-intensive
4. Latency-sensitive

The tests confirmed that workload requirements affect:

- Node feasibility
- QoS score
- Node ranking
- Final node selection


### Day 3 — Task Execution Simulation

Implemented:

`scheduler/task_executor.py`

The `TaskExecutor` currently simulates task execution.

Execution time is estimated using:

- CPU requirement
- Memory requirement
- GPU requirement
- Node type
- Network latency

GPU workloads receive simulated acceleration when executed on GPU-capable nodes.

The executor also:

- Calculates estimated execution time
- Checks whether the deadline is met
- Releases allocated resources after simulated completion
- Records completed task information


## Current Execution Pipeline

The scheduler currently performs the following complete workflow:

Task
 ↓
Feasibility Check
 ↓
Resource QoS Calculation
 ↓
Priority Score
 ↓
Deadline Urgency Score
 ↓
Final Task-Aware Score
 ↓
Node Ranking
 ↓
Best Node Selection
 ↓
Resource Allocation
 ↓
Execution Time Estimation
 ↓
Deadline Evaluation
 ↓
Resource Release


## Verified Execution Results

The execution simulation has been successfully tested using four heterogeneous workloads.

### CPU-intensive

- Selected node: `edge-02`
- Execution time: 7.8 seconds
- Deadline: 60 seconds
- Deadline met: Yes


### Memory-intensive

- Selected node: `edge-02`
- Execution time: 7.8 seconds
- Deadline: 60 seconds
- Deadline met: Yes


### GPU-intensive

- Selected node: `edge-02`
- Execution time: 6.9 seconds
- Deadline: 30 seconds
- Deadline met: Yes


### Latency-sensitive

- Selected node: `edge-01`
- Execution time: 3.25 seconds
- Deadline: 5 seconds
- Deadline met: Yes


## Important Simulation Limitation

The current task execution model is a synthetic simulation.

It does not execute real workloads or wait for the estimated execution duration.

The execution-time formula is currently used to model and evaluate scheduler behavior.

Later stages may replace or extend this simulation with more realistic worker/task execution.


## Current Project Files

```text
dynamic-qos-cloud-edge-scheduler/
│
├── scheduler/
│   ├── __init__.py
│   ├── compute_node.py
│   ├── task.py
│   ├── scheduler.py
│   ├── task_executor.py
│   └── main.py
│
├── docs/
│   └── PROJECT_CONTEXT.md
│
├── README.md
└── .gitignore