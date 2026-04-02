from steps import WaitFor
from component import Component

class Mosquitto(Component):
    def __init__(self, name=None, host="localhost", port=1883, timeout=10, quiet=False):
        super().__init__(
            image="eclipse-mosquitto",
            priority=1,
            replicas=1,
            name="mosquitto" if name is None else name,
            quiet=quiet
        )
        self.host = self.name
        self.port = port
        self.timeout = timeout

        
    def after(self):
        return [WaitFor(self.name, self.port, self.host, self.timeout)]
