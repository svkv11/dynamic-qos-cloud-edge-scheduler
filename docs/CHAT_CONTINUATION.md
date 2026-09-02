# Chat Continuation Guide

## Project

Project Name:
Dynamic QoS Cloud-Edge Scheduler

GitHub Repository:
https://github.com/svkv11/dynamic-qos-cloud-edge-scheduler.git

---

# Purpose of This File

This file contains the standard prompt to use when continuing this
project in a new ChatGPT conversation.

The project may be continued from:
- a completed milestone
- the middle of a development day
- an unverified implementation
- a testing stage

The new chat must determine the actual current state instead of
assuming that the previous day was completed.

---

# Master Continuation Prompt

Copy the following prompt into a new chat:

---

Continue my Dynamic QoS Cloud-Edge Scheduler project.

GitHub repository:

https://github.com/svkv11/dynamic-qos-cloud-edge-scheduler.git

Do NOT restart the project from the beginning.

Use:

docs/PROJECT_CONTEXT.md

as the primary project handover document.

Also consider the actual project files and Git status as the source
of truth for the current implementation state.

IMPORTANT DEVELOPMENT RULES:

1. Do not restart completed work.
2. Do not replace the existing architecture without first explaining
   why a change is necessary.
3. Read PROJECT_CONTEXT.md before deciding what to implement next.
4. Determine whether the current work is:
   - completed and verified
   - implemented but not verified
   - currently being tested
   - not yet implemented
5. Never assume an implementation works just because code exists.
6. If the previous chat ended during testing, continue from the testing
   stage rather than starting another feature.
7. Do not jump ahead to future features.

---

# Coding Workflow

For every new implementation:

1. Explain what we are building.
2. Explain why it is needed.
3. Explain where it fits in the architecture.
4. Give the complete replacement code for every file that needs to change.
5. Do not ask me to manually insert individual lines into existing files.
6. I will replace the specified file completely.
7. Give me the exact command to run.
8. I will send the complete terminal output.
9. Verify the output before considering the feature complete.
10. Only after successful verification should we create a Git checkpoint.
11. Update PROJECT_CONTEXT.md at meaningful milestones.

I am still learning Python, Docker, cloud computing, and scheduling,
so explanations should be simple and step-by-step.

---

# Complete Replacement Code Rule

When modifying a file, use this style:

"Replace scheduler/main.py completely with the following code."

Then provide the entire file.

Do NOT normally say:

- Add these lines after line 20.
- Insert this method inside the class.
- Change these three lines.
- Copy this code into the existing function.

The goal is to minimize manual editing mistakes.

---

# Testing Rule

After providing code:

1. Tell me exactly what command to execute.
2. Wait for my terminal output.
3. Check whether the output is correct.
4. If it fails, diagnose the failure before changing anything.
5. Do not make multiple unrelated changes at once.

---

# Git Workflow

Git is used to protect the actual project code.

Normal workflow:

Code change
    ↓
Run test
    ↓
Successful result
    ↓
Verify result
    ↓
Git add
    ↓
Git commit
    ↓
Git push
    ↓
git status
    ↓
Clean checkpoint

Expected clean state:

nothing to commit, working tree clean

Do not tell me to commit code that has not been successfully tested.

---

# Project Context Workflow

PROJECT_CONTEXT.md records the project state.

Update it at meaningful milestones.

It should record:

- completed features
- current feature
- unverified work
- last successful test
- current files
- important architecture decisions
- next implementation step
- research direction
- development constraints

Do not wait until the end of a calendar day if an important milestone
has already been completed.

---

# Mid-Task Chat Limit Rule

If the previous chat ended in the middle of a task:

Do NOT assume the task was completed.

Use PROJECT_CONTEXT.md and the actual Git/project state to determine:

- what was already completed
- what code was changed
- whether it was tested
- whether the test passed
- whether it was committed
- what exact step comes next

If the latest implementation was not verified, continue with verification.

If code was successfully tested and committed, continue from the next
feature.

If the state is ambiguous, explain the ambiguity before changing code.

---

# Important Project Architecture Decision

The project will eventually contain:

User/Application
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

The LLM interprets natural-language workload requirements.

The scheduler remains responsible for infrastructure-aware scheduling.

The LLM should NOT directly replace the scheduler.

---

# Project Development Direction

Current development order:

1. Core scheduler
2. Task-aware QoS scheduling
3. Improved scheduling decisions
4. Heterogeneous workload support
5. Increasing-load experiments
6. Task execution simulation
7. Docker worker simulation
8. Cloud/edge worker environment
9. LLM requirement interpretation
10. Integration
11. Experiments and evaluation

Do not jump directly to Docker, AWS EC2, or LLM integration unless
PROJECT_CONTEXT.md says the current stage is ready.

---

# Current User Preference

The user wants a safe, incremental development process.

They prefer:

Complete file replacement
        ↓
Run
        ↓
Send output
        ↓
Verification
        ↓
Commit

They do not want to guess where code should be inserted.

---

# First Action in a New Chat

After reading this file and PROJECT_CONTEXT.md:

Do NOT immediately write code.

First tell me:

1. Current project status
2. Completed features
3. Current implementation/testing status
4. Last verified milestone
5. Exact next development step

Then wait for confirmation before starting implementation.