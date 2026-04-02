class Component:
    """
    Represents a deployable unit in the cluster.

    A Component corresponds to a container image and its deployment
    configuration (replicas, etc.).
    """

    def __init__(self, image, replicas=1, name=None, priority=None, command=None, quiet=False):
        """
        Initialize a Component.
        """
        self.command = command
        self.priority = priority
        self.name = image if name is None else name
        self.image = image
        self.replicas = replicas
        self.quiet = quiet


    def after(self):
        return []

    def before(self):
        return []

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
