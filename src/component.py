class Component:
    """
    Represents a deployable unit in the cluster.

    A Component corresponds to a container image and its deployment
    configuration (replicas, etc.).
    """

    def __init__(self, image, replicas=1, name=None, priority=None, command=None, stdout=False, stderr=True, ports=None):
        """
        Initialize a Component.
        """
        self.stdout = stdout
        self.stderr = stderr
        self.command = command
        self.priority = priority or 0
        self.name = image if name is None else name
        self.image = image
        self.replicas = replicas
        self.ports = ports or {}
        self.mounting = {}


    def mount(self, src, target):
        self.mounting[src] = target

    def set_priority(self, priority):
        self.priority = priority

    def after(self):
        return []

    def before(self):
        return []

    def set_logs(self, stderr=None, stdout=None):
        if not stderr is None:
            self.stderr = stderr
        if not stdout is None:
            self.stdout = stdout

    @staticmethod
    def parse_compose(content: str):
        pass

    @staticmethod
    def from_compose(compose_file_path: str):
        try:
            with open(compose_file_path, "r") as f:
                content = f.read()
                return parse_compose(content)
        except FileNotFoundError:
            print(f"[ERROR] Failed to open docker-compose file {compose_file_path}.")
        except IOError as e:
            print(f"[ERROR] IO error when opening docker-compose file {compose_file_path}: {e.explanation}")
