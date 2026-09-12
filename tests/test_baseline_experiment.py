from experiments.baseline_experiment import BaselineExperiment


def test_normal_scenario():
    experiment = BaselineExperiment()

    results = experiment.run_scenario("normal")

    assert "round_robin" in results
    assert "resource_only" in results
    assert "dynamic_qos" in results

    for strategy, result in results.items():
        assert result["scenario"] == "normal"
        assert result["completed_tasks"] == 4
        assert result["failed_tasks"] == 0
        assert result["deadline_success_rate"] == 100.0
        assert result["average_execution_time"] > 0
        assert len(result["task_results"]) == 4

    print("Normal Scenario Test: PASSED")


def test_round_robin():
    experiment = BaselineExperiment()

    result = experiment.run_round_robin("normal")

    assignments = {
        item["task_id"]: item["node_id"]
        for item in result["task_results"]
    }

    assert assignments["task-01"] == "edge-01"
    assert assignments["task-02"] == "edge-02"
    assert assignments["task-03"] == "cloud-01"
    assert assignments["task-04"] == "edge-01"

    print("Round Robin Test: PASSED")


def test_resource_only():
    experiment = BaselineExperiment()

    result = experiment.run_resource_only("normal")

    assignments = {
        item["task_id"]: item["node_id"]
        for item in result["task_results"]
    }

    assert assignments["task-01"] == "edge-01"
    assert assignments["task-02"] == "edge-02"
    assert assignments["task-03"] == "edge-02"
    assert assignments["task-04"] == "edge-01"

    for item in result["task_results"]:
        assert item["selection_qos_score"] is not None

    print("Resource-Only Test: PASSED")


def test_dynamic_qos():
    experiment = BaselineExperiment()

    result = experiment.run_dynamic_qos("normal")

    assignments = {
        item["task_id"]: item["node_id"]
        for item in result["task_results"]
    }

    assert assignments["task-01"] == "edge-01"
    assert assignments["task-02"] == "edge-02"
    assert assignments["task-03"] == "edge-02"
    assert assignments["task-04"] == "edge-01"

    for item in result["task_results"]:
        assert item["selection_qos_score"] is not None

    print("Dynamic QoS Test: PASSED")


def test_strategy_comparison():
    experiment = BaselineExperiment()

    results = experiment.run_scenario("normal")

    round_robin_time = results[
        "round_robin"
    ]["average_execution_time"]

    resource_only_time = results[
        "resource_only"
    ]["average_execution_time"]

    dynamic_qos_time = results[
        "dynamic_qos"
    ]["average_execution_time"]

    assert round_robin_time == 7.67
    assert resource_only_time == 5.75
    assert dynamic_qos_time == 5.75

    assert resource_only_time < round_robin_time
    assert dynamic_qos_time < round_robin_time

    print("Strategy Comparison Test: PASSED")


if __name__ == "__main__":
    print("=" * 60)
    print("BASELINE EXPERIMENT TEST")
    print("=" * 60)

    test_normal_scenario()
    test_round_robin()
    test_resource_only()
    test_dynamic_qos()
    test_strategy_comparison()

    print("=" * 60)
    print("Baseline Experiment Tests: ALL PASSED")
    print("=" * 60)