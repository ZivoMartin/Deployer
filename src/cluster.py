from component import Component
from backends.debug_backend import DebugBackend
from backends.docker_backend import DockerBackend
from steps import ParallelGroup, Step

class Cluster:
    """
    Represents the deployment cluster.

    The Cluster is responsible for:
    - Node allocation
    - Collecting components
    - Building a deployment workflow
    - Executing the deployment
    """

    def __init__(self, backend=DockerBackend(clean_before=True), setup_logging=True, max_concurency=None):
        """Initialize an empty cluster."""
        self.backend = backend
        self.node_count = 0
        self.components = []
        self.max_concurency = max_concurency
        
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


    def get_parallel_sorted_components(self):
        result = {}
        state = {}
        comp_map = {}

        def visit(comp):
            name = comp.get_name()
            s = state.get(name, 0)
            
            if s == 1:
                raise RuntimeError(f"Dependency cycle detected involving {name}")

            if s == 2:
                return comp_map[name]

            state[name] = 1

            my_index = 0
            for parent in comp.get_dependencies():
                candidate = visit(parent) + 1
                if candidate > my_index:
                    my_index = candidate

            if my_index not in result:
                result[my_index] = []

            comp_map[name] = my_index
            result[my_index].append(comp)
            state[name] = 2            
        
        for comp in self.components:
            visit(comp)

        return [result[k] for k in sorted(result)]
    
    def _build_plan(self):
        """
        Build a deployment plan.
        The plan assigns each component replica to a node.
        """
        nodes = self._allocate_nodes()
        n = len(nodes)

        if n == 0:
            raise ValueError("No nodes allocated")

        def build_components_workflow(components, i=0):
            workflows = []
            for comp in components:
                for _ in range(comp.replicas):
                    node = nodes[i % n]
                    workflows.append(comp.deployment_workflow(node))
                    i += 1
            return (workflows, i)

        if self.max_concurency is not None:
            launching_rounds = self.get_parallel_sorted_components()
            i = 0
            plan = []
            for components in launching_rounds:
                (workflows, i) = build_components_workflow(components)
                plan_round = workflows[0] if len(workflows) == 1 else ParallelGroup(workflows, self.max_concurency)
                plan.append(plan_round)

            return plan
        else:
            components = self.get_sorted_components()
            (plan, _) = build_components_workflow(components)

            return plan

        
    def _execute(self, plan):
        """
        Execute the deployment plan.
        """
        for plan_step in plan:
            plan_step.process(self.backend)

    def run(self):
        """
        Run the deployment process.
        This includes:
        1. Building the deployment workflow
        2. Executing it
        """
        plan = self._build_plan()
        self._execute(plan)
