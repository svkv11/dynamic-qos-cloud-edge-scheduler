print()
print("=" * 100)
print("RESEARCH EVIDENCE SUMMARY")
print("=" * 100)

print()
print("RQ1 - BASELINE COMPARISON")
print("-" * 100)

print("""
Research Question:
How does the proposed GenAI + Dynamic QoS scheduler perform compared with
traditional Round Robin and Resource Only scheduling under heterogeneous
workload conditions?

Evidence:
- Six workload scenarios were evaluated.
- Five repetitions were performed for each scenario.
- 30 scenario-level observations were obtained for each scheduler.
- The proposed scheduler achieved the lowest mean execution time.
- The proposed scheduler achieved the highest mean QoS score.
- Deadline success was equal to Resource Only and higher than Round Robin.

Results:
- Execution time vs Round Robin: 28.14% reduction
- Execution time vs Resource Only: 20.58% reduction
- QoS vs Round Robin: 15.10% increase
- QoS vs Resource Only: 11.85% increase
- Deadline success vs Round Robin: +3.34 percentage points
- Deadline success vs Resource Only: 0.00 percentage points
""")

print()
print("RQ2 - ABLATION / COMPONENT CONTRIBUTION")
print("-" * 100)

print("""
Research Question:
How do priority awareness and deadline awareness contribute to the scheduling
behavior of the proposed QoS-based scheduler?

Evidence:
- Eight controlled scenarios were evaluated.
- Four scheduler configurations were compared:
  1. Full Dynamic QoS
  2. No Priority
  3. No Deadline
  4. Resource Only

Aggregate ablation results:

Full Dynamic QoS:
- Average QoS: 80.75
- Average execution time: 6.57 s
- Deadline success: 96.88%

No Priority:
- Average QoS: 62.25
- Average execution time: 6.57 s
- Deadline success: 96.88%

No Deadline:
- Average QoS: 63.33
- Average execution time: 7.63 s
- Deadline success: 84.38%

Resource Only:
- Average QoS: 82.17
- Average execution time: 7.63 s
- Deadline success: 84.38%

Interpretation:
- Removing priority reduced the aggregate QoS score substantially.
- Removing deadline awareness increased average execution time.
- Removing deadline awareness reduced deadline success.
- The controlled deadline/resource trade-off demonstrated that deadline-aware
  scoring can change the selected node when resource suitability and deadline
  feasibility conflict.
""")

print()
print("RQ3 - DEADLINE / RESOURCE TRADE-OFF")
print("-" * 100)

print("""
Research Question:
Can node-aware deadline evaluation influence node selection when resource
suitability and deadline feasibility conflict?

Controlled scenario:
- edge-01 resource score: 55.25
- edge-01 deadline score: 75.00
- edge-01 Full Dynamic QoS score: 74.60
- edge-01 execution time: 5.00 s

- cloud-01 resource score: 63.78
- cloud-01 deadline score: 37.04
- cloud-01 Full Dynamic QoS score: 66.62
- cloud-01 execution time: 13.50 s

Deadline:
- 10 seconds

Observed decisions:
- Resource Only selected cloud-01.
- Full Dynamic QoS selected edge-01.
- edge-01 met the deadline.
- cloud-01 missed the deadline.

Interpretation:
The controlled experiment demonstrates that incorporating node-aware
deadline information can alter the scheduling decision when resource
suitability and deadline feasibility conflict.
""")

print()
print("STATISTICAL EVIDENCE")
print("-" * 100)

print("""
Wilcoxon signed-rank analysis was performed using the existing repeated
experiment results.

GenAI + QoS vs Round Robin:
- Execution Time p-value: 0.000002
- QoS Score p-value: 0.000002

GenAI + QoS vs Resource Only:
- Execution Time p-value: 0.000079
- QoS Score p-value: 0.000002

Interpretation:
The paired analysis found statistically significant differences in execution
time and QoS score between the proposed scheduler and both baselines under
the evaluated experimental scenarios.

Important methodological limitation:
The 30 observations consist of six scenarios repeated five times. Therefore,
they should not be interpreted as 30 fully independent real-world workload
samples.
""")

print()
print("REPRODUCIBILITY EVIDENCE")
print("-" * 100)

print("""
Experimental design:
- 6 workload scenarios
- 5 repetitions
- 3 scheduler configurations
- 30 scenario-level observations per scheduler
- Mean and standard deviation reported
- Same workload requirements used across scheduler comparisons
- Existing experiment results reused for statistical analysis
- No scheduler implementation changes were made during final evaluation
""")

print()
print("FINAL RESEARCH POSITION")
print("-" * 100)

print("""
The experimental evidence supports the following research claim:

The proposed GenAI + Dynamic QoS scheduling approach combines natural-language
workload interpretation with resource-, priority-, and deadline-aware node
selection. Across the evaluated heterogeneous workload scenarios, it achieved
lower mean execution time and higher mean QoS scores than the Round Robin and
Resource Only baselines. The ablation and controlled trade-off experiments
further show that deadline-aware scoring can influence node selection when
resource suitability conflicts with deadline feasibility.

The results should be presented as evidence under the evaluated experimental
conditions rather than as a universal guarantee of superiority.
""")

print()
print("=" * 100)
print("END OF RESEARCH EVIDENCE SUMMARY")
print("=" * 100)
print()