from backends.backend import Backend

class DebugBackend(Backend):

    def allocate_nodes(self, nodes_count: int):
        """Allocate a number of nodes and return them."""
        return [f"node{i}" for i in range(nodes_count)]

    def deploy(self, node, component):
        """Deploy an image to a given node."""
        print(f"[DEPLOY] {image} -> {node}")

    def cleanup(self):
        print("Cleaning the network.")
