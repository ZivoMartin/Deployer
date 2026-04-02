from component import Component
from steps import Deploy
from backends.debug_backend import DebugBackend
from backends.docker_backend import DockerBackend

class Cluster:
    """
    Represents the deployment cluster.

    The Cluster is responsible for:
    - Node allocation
    - Collecting components
    - Building a deployment plan
    - Executing the deployment
    """

    def __init__(self, backend=DockerBackend(), clean_after=False):
        """Initialize an empty cluster."""
        self.backend = backend
        self.node_count = 0
        self.components = []
        self.clean_after = clean_after

    def allocate(self, n):
        """
        Allocate nodes in the cluster.
        """
        self.node_count += n

    def add(self, comp):
        """
        Add a Component to the cluster.
        """
        self.components.append(comp)

    def _allocate_nodes(self):
        """
        Generate node identifiers.
        """
        return self.backend.allocate_nodes(self.node_count)

    def get_priority_sorted_components(self):
        return sorted(
            self.components,
            key=lambda x: (x.priority is None, x.priority if x.priority is not None else 0)
        )
    
    def _build_plan(self):
        """
        Build a deployment plan.
        The plan assigns each component replica to a node
        using a simple round-robin strategy.
        """
        nodes = self._allocate_nodes()
        n = len(nodes)

        if n == 0:
            raise ValueError("No nodes allocated")

        plan = []
        i = 0

        components = self.get_priority_sorted_components()

        for comp in components:
            for _ in range(comp.replicas):
                node = nodes[i % n]

                plan.extend(comp.before())
                plan.append(Deploy(comp, node))
                plan.extend(comp.after())

                i += 1

        return plan

    def _execute(self, plan):
        """
        Execute the deployment plan.
        """
        for step in plan:
            step.process(self.backend)

    def run(self):
        """
        Run the deployment process.
        This includes:
        1. Building the deployment plan
        2. Executing it
        """
        plan = self._build_plan()
        self._execute(plan)
        if self.clean_after:
            self.backend.cleanup()

    def cleanup(self):
        self.backend.cleanup()
