from steps import WaitFor, Deploy
from component import Component

class Mosquitto(Component):
    def __init__(self, name="mosquitto", host=None, port=1883, timeout=10):
        super().__init__(
            image="eclipse-mosquitto",
            name= name,
            stderr=False,
            stdout=False
        )
        self.host = host or self.name
        self.port = port
        self.timeout = timeout

    def deployment_plan(self, node):
        return [Deploy(self, node), WaitFor(self.port, self.host, self.timeout)]
