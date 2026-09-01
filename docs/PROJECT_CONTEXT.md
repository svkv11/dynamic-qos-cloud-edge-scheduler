# Dynamic QoS Cloud-Edge Scheduler - Project Context

## Project Status

The project is a software-based Dynamic QoS Cloud-Edge Scheduler.

GitHub repository:
dynamic-qos-cloud-edge-scheduler

Current branch:
main

Current Git status:
Clean

---

## Project Goal

Build a dynamic scheduler that receives heterogeneous workloads/tasks and selects the most suitable cloud or edge compute node based on:

- CPU requirements
- Memory requirements
- GPU requirements
- Current CPU utilization
- Current memory utilization
- Current GPU utilization
- Network latency
- QoS score
- Task priority
- Task deadline

The long-term goal is to add an LLM-based requirement interpretation layer and support heterogeneous workloads beyond a single workload category.

---

# Completed Work

## Day 1 - Project Setup

Completed:

- GitHub repository created
- Python virtual environment created
- Project folder structure created
- Initial scheduler structure created
- Git configured
- README.md created
- .gitignore created
- docs/PROJECT_CONTEXT.md created

---

# Day 2 - Core Scheduler

## 1. ComputeNode Model

File:

scheduler/compute_node.py

ComputeNode contains:

### Fixed resources

- node_id
- node_type
- cpu_cores
- memory_gb
- gpu_available

### Dynamic state

- cpu_utilization
- memory_utilization
- gpu_utilization
- network_latency_ms

The node can:

- display its current state
- determine whether it can run a task
- allocate task resources
- release task resources
- calculate a QoS score

---

## 2. Task / Workload Model

File:

scheduler/task.py

Task contains:

- task_id
- workload_type
- cpu_required
- memory_required_gb
- gpu_required
- deadline_seconds
- priority

Example workloads currently tested:

- image_processing
- video_processing

---

## 3. Feasibility Checking

The scheduler checks whether a node has sufficient resources for a task.

Example:

Task-002 requires GPU.

Edge-01:

GPU Available = False

Therefore:

Task-002 on Edge-01 = False

Edge-02 and Cloud-01 are feasible.

---

## 4. Resource Allocation

When a task is allocated:

- CPU utilization increases
- memory utilization increases
- GPU utilization increases when applicable

Example:

Edge-01 before Task-001:

CPU = 25%
Memory = 30%

After Task-001:

CPU = 75%
Memory = 55%

---

## 5. Resource Release

Allocated resources can be released.

Example:

Edge-01 after Task-001 allocation:

CPU = 75%
Memory = 55%

After release:

CPU = 25%
Memory = 30%

---

## 6. QoS Scoring

The system currently calculates a QoS score using:

- CPU utilization
- memory utilization
- GPU utilization
- network latency

Current test results:

Edge-01 = 82.5
Edge-02 = 69.0
Cloud-01 = 44.0

This is currently a basic QoS scoring mechanism.

It is NOT yet the final research-level task-aware QoS mechanism.

---

## 7. Best-Node Selection

File:

scheduler/scheduler.py

Class:

QoSScheduler

Method:

select_best_node(task)

The scheduler:

1. Checks all nodes
2. Removes infeasible nodes
3. Calculates QoS scores
4. Selects the node with the highest QoS score

Test result:

Task-001 → edge-01

Task-002 → edge-02

---

## 8. Dynamic Multi-Task Scheduling

The scheduler can now:

1. Receive Task-001
2. Select a suitable node
3. Allocate resources
4. Update node state
5. Receive Task-002
6. Re-evaluate nodes using their updated state
7. Select another suitable node
8. Allocate resources

Verified output:

Task-001 assigned to edge-01

Task-002 assigned to edge-02

Final state:

edge-01:
CPU = 75%
Memory = 55%

edge-02:
CPU = 90%
Memory = 95%
GPU = 45%

cloud-01:
CPU = 55%
Memory = 50%
GPU = 35%

---

# Current Project Files

scheduler/
├── compute_node.py
├── task.py
├── scheduler.py
└── main.py

tests/

docs/
└── PROJECT_CONTEXT.md

README.md
.gitignore

---

# Important Development Rule

The developer will provide complete replacement code for files that need modification.

Do not manually insert small code fragments unless explicitly instructed.

For every implementation step:

1. Replace the specified file completely.
2. Save it.
3. Run the provided test command.
4. Send the complete terminal output.
5. Verify the result.
6. Commit only after successful verification.

---

# Current Checkpoint

Day 2 core scheduler implementation is complete.

Git status:

nothing to commit, working tree clean

The latest successfully tested functionality is dynamic multi-task scheduling.

---

# Next Development Stage

Do NOT immediately add Docker, AWS EC2, or the LLM.

The next stage is to improve the scheduler's decision-making mechanism.

Planned progression:

1. Improve task-aware QoS scoring
2. Add better scheduling decision information
3. Add more heterogeneous workload types
4. Test scheduling under increasing load
5. Add task execution simulation
6. Add Docker-based worker simulation
7. Integrate cloud/edge worker environment
8. Add LLM requirement interpretation
9. Connect LLM output to the Task model
10. Perform experiments and evaluation

---

# Long-Term Architecture

User / Application
        |
        v
LLM Requirement Interpretation
        |
        v
Task / Workload Model
        |
        v
Dynamic QoS Scheduler
        |
        +-------------------+
        |                   |
        v                   v
   Edge Workers        Cloud Workers
        |                   |
        +---------+---------+
                  |
                  v
          Task Execution
                  |
                  v
          Resource Updates
                  |
                  v
          Scheduler Feedback

The LLM should interpret workload requirements.

The scheduler should remain responsible for infrastructure-aware scheduling decisions.

The LLM should NOT directly replace the scheduler.