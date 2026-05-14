from steps import Deploy

class Component:
    """
    Represents a deployable unit in the cluster.

    A Component corresponds to a container image and its deployment
    configuration (replicas, etc.).
    """

    def __init__(self, image, replicas=1, name=None, command=None, stdout=False, stderr=True, ports=None):
        """
        Initialize a Component.
        """
        self.stdout = stdout
        self.stderr = stderr
        self.command = command
        self.name = image if name is None else name
        self.image = image
        self.replicas = replicas
        self.ports = ports or {}
        self.mounting = {}
        self.dependencies = []

    def depends_on(self, dependency):
        self.dependencies.append(dependency)

    def expose_port(self, from_p, to_p):
        self.ports[from_p] = to_p

    def get_dependencies(self):
        return self.dependencies

    def mount(self, src, target):
        self.mounting[src] = target

    def set_priority(self, priority):
        self.priority = priority

    def set_logs(self, stderr=None, stdout=None):
        if not stderr is None:
            self.stderr = stderr
        if not stdout is None:
            self.stdout = stdout

    def deployment_plan(self, node):
        return [Deploy(self, node)]

    def get_name(self):
        return self.name
