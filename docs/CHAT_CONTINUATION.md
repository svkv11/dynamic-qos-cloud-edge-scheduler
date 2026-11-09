# CHAT CONTINUATION — Dynamic-Aware Task Scheduling in Cloud-Edge Environments

**Last updated:** 9 November 2026
**Project status:** Main implementation and experiments completed; statistical analysis completed; DQN investigation and IEEE research-paper finalization pending.

## 1. Project identity

- **Official project title:** Dynamic-Aware Task Scheduling in Cloud-Edge Environments
- **Repository:** Dynamic QoS Cloud-Edge Scheduler
- **GitHub:** https://github.com/svkv11/dynamic-qos-cloud-edge-scheduler
- **Local path:** `C:\capstone_project\dynamic-qos-cloud-edge-scheduler`
- **Branch:** `main`
- **Environment:** Windows CMD, Python virtual environment `.venv`, Git/GitHub.
- **Project type:** Software-based cloud-edge scheduling simulator.

Do not change the official project title unless explicitly requested.

## 2. Current verified progress

### Implementation
- Implemented a software-based cloud-edge task scheduling simulator.
- Configured three simulated nodes: `edge-01`, `edge-02`, and `cloud-01`.
- Implemented heterogeneous CPU-intensive, memory-intensive, GPU-intensive, latency-sensitive, and general workloads.
- Implemented Round Robin, Resource Only, Dynamic QoS, and DQN scheduling policies.
- Implemented workload requirement interpretation using Ollama and Gemini API.
- Implemented Dynamic QoS scoring using resource suitability, priority, and node-aware deadline considerations.
- Implemented experimental scenarios and result-generation scripts.

The configured nodes are simulator representations, not actual deployed cloud or edge machines. Execution-time results are simulated estimates, not real-world wall-clock measurements.

### Main four-policy comparison
The latest main comparison uses:
- 30 matched seeds: 100–129.
- 20 tasks per episode.
- 600 tasks per policy.
- Completed episodes for all policies.
- DQN exploration disabled during evaluation.
- Zero invalid DQN actions.

| Policy | Mean simulated execution time | Deadline success | Mean QoS |
|---|---:|---:|---:|
| Round Robin | 8.710504 | 95.6667% | 72.607067 |
| Resource Only | 8.374264 | 96.5000% | 75.022783 |
| Dynamic QoS | 8.307071 | 96.6667% | 74.955000 |
| DQN | 8.975170 | 96.8333% | 69.531383 |

Interpretation:
- Dynamic QoS achieved the lowest mean simulated execution time.
- Resource Only achieved the highest mean QoS.
- DQN achieved the highest observed deadline-success rate, but its mean execution time was highest and its mean QoS was lowest.
- Deadline-success differences were not statistically significant in the paired analysis.

### Statistical analysis
- Paired Wilcoxon signed-rank tests were performed against Dynamic QoS.
- Holm correction was applied.
- Sign-test sensitivity analysis was also completed.
- The statistical analysis scripts include `ml/analyze_policy_comparison.py` and `verify_wilcoxon.py`.
- Statistical findings and sign-test results were recorded in the project context.

### DQN investigation
- DQN evaluation and diagnostic scripts have been created.
- Diagnostic outputs already exist under `experiments/results/dqn_diagnostics/`.
- A potential implementation concern has been identified: action selection masks infeasible actions, but the target-network maximum in the Bellman target is not masked.
- This is an investigation point, not a proven cause of DQN performance.
- The user explicitly requires evidence and approval before modifying DQN implementation, reward design, action masks, architecture, workload generation, or formulas.
- The original checkpoint `experiments/results/dqn/dqn_model.pt` must never be overwritten.

## 3. IEEE research-paper status

The research paper uses the official title:

**Dynamic-Aware Task Scheduling in Cloud-Edge Environments**

Previously established paper structure:
1. Title
2. Abstract
3. Index Terms / Keywords
4. I. Introduction
5. II. Related Work
6. III. System Model and Problem Formulation
7. IV. Proposed Scheduling Framework and Methodology
8. V. Experimental Setup and Results
9. VI. Conclusion and Future Work
10. References

Previously established research questions:
- RQ1: How does the proposed Dynamic QoS scheduling approach compare with baseline scheduling policies?
- RQ2: What is the contribution of priority and deadline awareness?
- RQ3: What trade-offs arise between resource suitability and deadline/latency requirements?

Research contribution:
- Natural-language workload requirement interpretation using a GenAI component.
- Conversion of interpreted requirements into structured workload characteristics.
- Deterministic, interpretable Dynamic QoS scheduling using resource suitability, latency, priority, and node-aware deadlines.
- Comparison against Round Robin, Resource Only, and DQN scheduling.

Paper preparation progress previously recorded:
- Abstract finalized in an earlier paper-preparation session.
- All eight paper figures were generated.
- Numerical consistency, figure mapping, Fig. 1 reference, EAT base-paper explanation, research gap, and college requirements were reviewed.
- Standard IEEE-style formatting was planned because a college-specific template was not available.
- Complete manuscript assembly remained pending.

**Important:** Do not assume that the earlier paper abstract and its numerical claims automatically reflect the latest 600-task experiment. Reconcile the paper's tables, abstract, figures, and discussion with the latest verified experiment before finalizing the manuscript.

The EAT paper was identified as the primary base paper:
Z. Xu et al., “EAT: QoS-Aware Edge-Collaborative AIGC Task Scheduling via Attention-Guided Diffusion Reinforcement Learning,” IEEE Transactions on Mobile Computing, 2026, DOI: 10.1109/TMC.2026.3656318.

The project is inspired by the QoS-aware scheduling problem, but uses its own GenAI requirement extraction and interpretable resource/latency/priority/deadline scoring approach. Do not claim to reproduce the EAT method.

## 4. Current Git repository status

Latest command executed:

`git status --short --branch`

Output:

```text
## main...origin/main
 M docs/CHAT_CONTINUATION.md
 D docs/PROJECT_CONTEXT.md
 M genai/gemini_interpreter.py
?? docs/PROJECT_CONTEXT_before_ieee_update.md
?? experiments/results/dqn/
?? experiments/results/dqn_comparison/
?? experiments/results/dqn_diagnostics/
?? ml/
?? verify_wilcoxon.py
```

Latest commit:

`097a2b1 Improve Ollama requirement handling`

The local `main` and the locally recorded `origin/main` both point to this commit. A fresh fetch has not yet been performed, so GitHub synchronization has not been conclusively verified.

Do not restore, delete, stage, commit, or push files without the user's explicit approval.

## 5. Immediate pending tasks

Follow this order:

1. Continue the Git audit. The next command to run is:

   `git remote -v`

2. Verify the configured GitHub remote.
3. Fetch remote information and compare the local branch with the actual GitHub branch. Explain before running each command.
4. Inspect the missing `docs/PROJECT_CONTEXT.md` history and the current `docs/CHAT_CONTINUATION.md`.
5. Preserve all modified and untracked files.
6. Review the current experiment outputs and ML scripts before deciding which files belong in GitHub.
7. Replace/update the project context and continuation documents only after their contents are reviewed.
8. Check the IEEE paper's existing abstract, eight figures, tables, references, and numerical claims. Reconcile them with the latest main experiment.
9. Continue the DQN investigation by inspecting the existing diagnostic CSV and JSON files. Do not rerun scripts that refuse to overwrite existing diagnostic outputs.
10. Prepare a repository update plan. Ask for explicit approval before staging, committing, or pushing.

## 6. Required working rules

- Work with one CMD command at a time.
- Explain what each command does and wait for the user's output before proceeding.
- Use Windows CMD commands and the existing `.venv` environment.
- Inspect files before editing them.
- Before editing, explain the reason and preserve a backup where appropriate.
- Provide complete replacement file contents when a replacement is required.
- Give the exact validation/test command after an edit.
- Never overwrite or delete existing experiment results, model checkpoints, or source files without approval.
- Never overwrite the original DQN checkpoint.
- Do not tune reward functions, masks, architectures, workload generation, or formulas just to improve results.
- Do not invent experimental results, references, or paper claims.
- Distinguish verified facts, experimental observations, statistical findings, hypotheses, and proposed improvements.
- Keep the project software-simulation-only. Do not describe simulator nodes as actual deployed machines.
- Describe execution time as simulated execution time.
- Preserve the official project title.
- Update this continuation document and `docs/PROJECT_CONTEXT.md` after meaningful verified progress.

## 7. Source of truth

Use these sources in this order:
1. Current repository files and actual command outputs for implementation and Git status.
2. `docs/PROJECT_CONTEXT.md` for detailed technical and research history.
3. This document for the latest continuation instructions and immediate pending tasks.
4. The IEEE manuscript and its figures/tables for paper-specific content.

If sources conflict, identify the conflict and investigate it. Do not silently choose a value or combine results from different experiments.

**Start the next session by continuing the Git audit with `git remote -v`.**