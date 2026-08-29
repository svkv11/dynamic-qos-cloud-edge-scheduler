from compute_node import ComputeNode


edge_1 = ComputeNode(
    node_id="edge-01",
    node_type="edge",
    cpu_cores=4,
    memory_gb=8,
    gpu_available=False
)

edge_2 = ComputeNode(
    node_id="edge-02",
    node_type="edge",
    cpu_cores=8,
    memory_gb=16,
    gpu_available=True
)

cloud_1 = ComputeNode(
    node_id="cloud-01",
    node_type="cloud",
    cpu_cores=16,
    memory_gb=32,
    gpu_available=True
)


edge_1.display_info()
edge_2.display_info()
cloud_1.display_info()