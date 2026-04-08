from steps import WaitFor
from component import Component

class Mosquitto(Component):
    def __init__(self, name=None, host=None, port=1883, timeout=10):
        super().__init__(
            image="eclipse-mosquitto",
            priority=1,
            name= name or "mosquitto",
            stderr=False,
            stdout=False
        )
        self.host = host or self.name
        self.port = port
        self.timeout = timeout

        
    def after(self):
        return [WaitFor(self.port, self.host, self.timeout)]
