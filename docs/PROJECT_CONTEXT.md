# Dynamic QoS Cloud-Edge Scheduler
## Project Continuation Context

Last Updated: Day 1
Status: Day 1 COMPLETE

==================================================
1. PROJECT GOAL
==================================================

We are building a Dynamic QoS Cloud-Edge Scheduler for
heterogeneous workloads.

The system will accept workload requirements, convert them
into QoS/resource requirements, and dynamically select the
most suitable Edge or Cloud worker based on available
resources and QoS requirements.

The project is intended to support multiple workload types,
not only GenAI.

Examples:
- GenAI workloads
- Image processing
- Video processing
- ML inference
- Other computational workloads

The LLM is an additional layer that makes it easier for users
to express requirements in natural language. It is NOT the
scheduler itself.

==================================================
2. HIGH-LEVEL SYSTEM IDEA
==================================================

User
  ↓
LLM / Requirement Interpretation
  ↓
QoS Requirements
  ↓
Dynamic QoS Scheduler
  ↓
Available Edge / Cloud Workers
  ↓
Best Worker Selected
  ↓
Task Execution
  ↓
Monitoring + Results

==================================================
3. IMPORTANT PROJECT DECISIONS
==================================================

1. The project should NOT be limited only to GenAI workloads.

2. The project should support heterogeneous workloads such as:
   - GenAI
   - image processing
   - video processing
   - ML inference
   - other computational tasks

3. The LLM is used as a front-end requirement interpretation
   layer.

4. The scheduler remains responsible for resource allocation
   and worker selection.

5. We are NOT initially using physical Edge hardware.

6. Edge resources will initially be represented using
   virtualized/simulated worker nodes.

7. Development progression:
   Python Simulator
       ↓
   Docker Workers
       ↓
   Optional/Recommended Cloud VM validation

8. We will NOT create multiple cloud VMs at the beginning.

9. We are developing incrementally and committing changes
   to GitHub regularly.

10. We will build and understand each component before moving
    to the next component.

==================================================
4. DEVELOPMENT STRATEGY
==================================================

Phase 1:
Python-based Edge/Cloud simulator

Phase 2:
Dynamic resource utilization

Phase 3:
Task/workload model

Phase 4:
QoS requirements and QoS-aware scheduling

Phase 5:
Dynamic scheduler

Phase 6:
Docker-based workers

Phase 7:
LLM requirement interpretation

Phase 8:
Heterogeneous workload execution

Phase 9:
Intelligent/RL-based scheduling improvements
(if retained after evaluation)

Phase 10:
FastAPI/backend and dashboard

Phase 11:
Cloud deployment/validation

Phase 12:
Experiments, comparison, graphs and research evaluation

==================================================
5. CURRENT DEVELOPMENT ENVIRONMENT
==================================================

Operating system:
Windows

Project location:

C:\capstone_project\dynamic-qos-cloud-edge-scheduler

Python:
3.13.5

Git:
2.55.0.windows.3

Python virtual environment:
.venv

Virtual environment is activated successfully.

Python executable currently being used:

C:\capstone_project\dynamic-qos-cloud-edge-scheduler\.venv\Scripts\python.exe

Git branch:
main

GitHub repository:

https://github.com/svkv11/dynamic-qos-cloud-edge-scheduler.git

Git status after Day 1:
clean

==================================================
6. CURRENT PROJECT STRUCTURE
==================================================

dynamic-qos-cloud-edge-scheduler/
│
├── scheduler/
│   ├── compute_node.py
│   └── main.py
│
├── tests/
│
├── README.md
├── .gitignore
└── .venv/   (local only; not committed)

==================================================
7. DAY 1 COMPLETED
==================================================

Day 1 objective:

Create the first simulated Edge/Cloud computing environment.

Completed:

1. Verified Python installation.
2. Verified Git installation.
3. Connected local project to GitHub.
4. Created Python virtual environment.
5. Activated .venv.
6. Verified Python is running from .venv.
7. Created ComputeNode class.
8. Created three simulated computing nodes.
9. Successfully executed the simulator.
10. Added the project files to Git.
11. Committed the changes.
12. Pushed the changes to GitHub.
13. Verified Git working tree is clean.

==================================================
8. CURRENT SIMULATED NODES
==================================================

Edge-01:

Node ID:
edge-01

Node type:
edge

CPU:
4 cores

Memory:
8 GB

GPU:
No


Edge-02:

Node ID:
edge-02

Node type:
edge

CPU:
8 cores

Memory:
16 GB

GPU:
Yes


Cloud-01:

Node ID:
cloud-01

Node type:
cloud

CPU:
16 cores

Memory:
32 GB

GPU:
Yes

==================================================
9. CURRENT CODE CONCEPT
==================================================

compute_node.py currently contains a ComputeNode class.

The class currently stores:

- node_id
- node_type
- cpu_cores
- memory_gb
- gpu_available

It also has a display_info() method.

main.py creates:

- edge_1
- edge_2
- cloud_1

and displays their information.

==================================================
10. CURRENT LIMITATION
==================================================

The current nodes are STATIC.

Example:

Edge-01:
CPU = 4 cores

At the moment the simulator does not track:

- current CPU utilization
- current RAM utilization
- current GPU utilization
- network latency
- workload status
- task execution
- resource availability
- dynamic changes over time

The scheduler has NOT been implemented yet.

The LLM has NOT been implemented yet.

Docker has NOT been implemented yet.

Cloud deployment has NOT been implemented yet.

==================================================
11. DAY 2 OBJECTIVE
==================================================

Next objective:

Make the simulated computing nodes dynamic.

We need to add concepts such as:

- CPU utilization
- RAM utilization
- GPU utilization
- network latency
- availability
- current workload
- resource capacity
- available resources

The simulation should eventually behave approximately like:

Edge-01
CPU capacity: 4 cores
Current CPU utilization: 72%

Edge-02
CPU capacity: 8 cores
Current CPU utilization: 25%

Cloud-01
CPU capacity: 16 cores
Current CPU utilization: 61%

Resource values should eventually change when tasks
start and finish.

==================================================
12. GIT WORKFLOW
==================================================

After completing each meaningful feature:

1. Run the program.
2. Test the feature.
3. Check:

   git status

4. Add changes:

   git add .

5. Commit with a meaningful message.

Example:

   git commit -m "Add dynamic resource utilization"

6. Push:

   git push origin main

7. Verify:

   git status

Expected:

   nothing to commit, working tree clean

Do NOT commit the .venv directory.

==================================================
13. DAILY DEVELOPMENT RULE
==================================================

For every development session:

1. Explain what we are building.
2. Explain why it is needed.
3. Create/change only the necessary files.
4. Give exact commands/code.
5. Run and test the code.
6. Explain the output.
7. Commit to GitHub.
8. Update this project context.
9. Provide a Chat Continuation Summary.

==================================================
14. IMPORTANT INSTRUCTION FOR CONTINUATION
==================================================

If this project is continued in a NEW ChatGPT conversation,
use this file/context as the source of the current project
state.

Do NOT restart the project from the beginning.

Current progress:

DAY 1 COMPLETE

Next:

DAY 2 — Dynamic Resource Utilization

==================================================
15. LAST KNOWN STATE
==================================================

The simulator successfully runs using:

python scheduler\main.py

Successful output includes:

Node ID: edge-01
Node Type: edge
CPU Cores: 4
Memory: 8 GB
GPU Available: False

Node ID: edge-02
Node Type: edge
CPU Cores: 8
Memory: 16 GB
GPU Available: True

Node ID: cloud-01
Node Type: cloud
CPU Cores: 16
Memory: 32 GB
GPU Available: True

Git status:
clean

==================================================
END OF CONTEXT
==================================================