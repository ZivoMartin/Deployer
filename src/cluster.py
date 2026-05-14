from component import Component
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

    def __init__(self, backend=DockerBackend(clean_before=True), setup_logging=True):
        """Initialize an empty cluster."""
        self.backend = backend
        self.node_count = 0
        self.components = []
        
        if setup_logging:
            self.setup_logging()

    def setup_logging(self):
        import logging
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(
                level=logging.INFO,
                format="[%(name)s] %(message)s"
            )

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


    def get_sorted_components(self):
        """
        Return a topological sort of the components based on the dependency graph.
        Fail if detects a cycle.
        """

        result = []
        state = {}

        def visit(comp):
            name = comp.get_name()
            s = state.get(name, 0)

            if s == 1:
                raise RuntimeError(f"Dependency cycle detected involving {name}")

            if s == 2:
                return

            state[name] = 1

            for dep in comp.get_dependencies():
                visit(dep)

            state[name] = 2
            result.append(comp)

        for comp in self.components:
            visit(comp)

        return result
    
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

        components = self.get_sorted_components()
        print(list(map(lambda c: c.get_name(),components)))

        for comp in components:
            for _ in range(comp.replicas):
                node = nodes[i % n]
                plan.extend(comp.deployment_plan(node))
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
