from backends.backend import Backend
import docker
from docker.errors import NotFound, ImageNotFound, APIError

class DockerBackend(Backend):

    def __init__(self, network_name = "docker_testbed"):
        self.network_name = network_name
        self.client = docker.from_env()
        self.image_count = {}


    def setup(self):
        try:
            return self.client.networks.get(self.network_name)
        except NotFound:
            return self.client.networks.create(
                self.network_name,
                check_duplicate=True
            )

    def allocate_nodes(self, nodes_count: int):
        """Allocate a number of nodes and return them."""
        self.setup()
        return [f"node{i}" for i in range(nodes_count)]

    def _remove_one_container(self, container_id):
        container = self.client.containers.get(container_id)
        print(f"Removing container {container.name}")
        container.remove(force=True)

    
    def cleanup(self):
        try:
            net = self.client.networks.get(self.network_name)
            
            for container_info in net.attrs["Containers"].values():
                container_id = container_info["Name"]
                self._remove_one_container(container_id)

            net.remove()
            print(f"Network '{self.network_name}' removed")

        except NotFound:
            print(f"[ERROR] Failed to clean the network {self.network_name}, not found.")

    def wait_for(self, name, host, port, timeout):
        import time

        deadline = time.time() + timeout
        container = self.client.containers.get(host)

        while time.time() < deadline:
            exit_code, _ = container.exec_run(f"nc -z localhost {port}")
            if exit_code == 0:
                return
            time.sleep(0.2)


    def deploy(self, component, node):
        """Deploy an image to a given node."""
        name = component.name
        image = component.image
        command = component.command

        if name is None:
            base_name = f"{image}-{node}"
            count = self.image_count.get(base_name, 0)
            name = base_name if count == 0 else f"{base_name}_{count}"
            self.image_count[base_name] = count + 1
        
        try:
            container = self.client.containers.run(
                image,
                detach=True,
                network=self.network_name,
                labels={"node": node},
                name=name,
                command=command
            )

            if not component.quiet:
                import threading
                def stream_logs(container):
                    for line in container.logs(stream=True, stderr=True, stdout=False):
                        print(line.decode(), end="")

                threading.Thread(target=stream_logs, args=(container,)).start()

        except ImageNotFound:
            print(f"[ERROR] Image '{image}' not found.")
            return None
        except APIError as e:
            print(f"[ERROR] Docker API error while deploying '{name}': {e.explanation}")
            return None
