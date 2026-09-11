class NodeSelectionAnalyzer:
    """
    Analyze how task-to-node selections change
    across different resource scenarios.
    """

    def get_selected_node(self, task_rankings):
        """
        Return the highest-ranked node for a task.
        """

        if not task_rankings:
            return None

        return task_rankings[0]["node_id"]

    def build_selection_matrix(self, results):
        """
        Build a matrix showing the selected node for
        every task under every experiment scenario.
        """

        selection_matrix = {}

        for scenario_name, result in results.items():

            for task_id, rankings in result[
                "initial_rankings"
            ].items():

                if task_id not in selection_matrix:
                    selection_matrix[task_id] = {}

                selected_node = self.get_selected_node(
                    rankings
                )

                selection_matrix[task_id][
                    scenario_name
                ] = selected_node

        return selection_matrix

    def get_changed_tasks(self, selection_matrix):
        """
        Identify tasks whose selected node changes
        between experiment scenarios.
        """

        changed_tasks = {}

        for task_id, scenario_selections in (
            selection_matrix.items()
        ):

            selected_nodes = set(
                node
                for node in scenario_selections.values()
                if node is not None
            )

            if len(selected_nodes) > 1:
                changed_tasks[task_id] = (
                    scenario_selections
                )

        return changed_tasks

    def get_selection_change_count(
        self,
        selection_matrix
    ):
        """
        Count how many tasks changed their selected node.
        """

        return len(
            self.get_changed_tasks(
                selection_matrix
            )
        )

    def get_selection_adaptation_rate(
        self,
        selection_matrix
    ):
        """
        Calculate the percentage of tasks whose selected
        node changed across the experiment scenarios.
        """

        total_tasks = len(selection_matrix)

        if total_tasks == 0:
            return 0.0

        changed_tasks = self.get_selection_change_count(
            selection_matrix
        )

        adaptation_rate = (
            changed_tasks / total_tasks
        ) * 100

        return round(adaptation_rate, 2)

    def display_selection_matrix(
        self,
        selection_matrix
    ):
        """
        Display task-to-node selections across scenarios.
        """

        print("=" * 80)
        print("NODE SELECTION ADAPTATION ANALYSIS")
        print("=" * 80)

        for task_id, scenario_selections in (
            selection_matrix.items()
        ):

            print()
            print(f"Task: {task_id}")

            for scenario_name, node_id in (
                scenario_selections.items()
            ):

                print(
                    f"  {scenario_name:<15} -> "
                    f"{node_id}"
                )

        print("=" * 80)

    def display_changed_tasks(
        self,
        changed_tasks
    ):
        """
        Display tasks whose selected node changed.
        """

        print("=" * 80)
        print("TASKS WITH CHANGED NODE SELECTION")
        print("=" * 80)

        if not changed_tasks:
            print("No task selection changes detected.")
        else:

            for task_id, selections in (
                changed_tasks.items()
            ):

                print()
                print(f"Task: {task_id}")

                for scenario_name, node_id in (
                    selections.items()
                ):

                    print(
                        f"  {scenario_name:<15} -> "
                        f"{node_id}"
                    )

        print("=" * 80)

    def display_adaptation_rate(
        self,
        selection_matrix
    ):
        """
        Display the overall node selection adaptation rate.
        """

        adaptation_rate = (
            self.get_selection_adaptation_rate(
                selection_matrix
            )
        )

        print("=" * 80)
        print("NODE SELECTION ADAPTATION RATE")
        print("=" * 80)

        print(
            f"Adaptation Rate: "
            f"{adaptation_rate}%"
        )

        print("=" * 80)