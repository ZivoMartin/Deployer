from abc import ABC, abstractmethod

class Backend(ABC):

    @abstractmethod
    def allocate_nodes(self, nodes_count: int):
        """Allocate a number of nodes and return them."""
        pass

    @abstractmethod
    def deploy(self, node, component):
        """Deploy an image to a given node."""
        pass
