from compute_node import ComputeNode


edge_1 = ComputeNode(
    node_id="edge-01",
    node_type="edge",
    cpu_cores=4,
    memory_gb=8,
    gpu_available=False,
    cpu_utilization=25.0,
    memory_utilization=30.0,
    gpu_utilization=0.0,
    network_latency_ms=10.0
)


edge_2 = ComputeNode(
    node_id="edge-02",
    node_type="edge",
    cpu_cores=8,
    memory_gb=16,
    gpu_available=True,
    cpu_utilization=40.0,
    memory_utilization=45.0,
    gpu_utilization=20.0,
    network_latency_ms=15.0
)


cloud_1 = ComputeNode(
    node_id="cloud-01",
    node_type="cloud",
    cpu_cores=16,
    memory_gb=32,
    gpu_available=True,
    cpu_utilization=55.0,
    memory_utilization=50.0,
    gpu_utilization=35.0,
    network_latency_ms=80.0
)


edge_1.display_info()
edge_2.display_info()
cloud_1.display_info()