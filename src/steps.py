from dataclasses import dataclass
from abc import ABC, abstractmethod

class Step(ABC):
    def process(self, backend):
        pass

@dataclass
class Deploy(Step):
    comp: str
    node: str

    def process(self, backend):
        backend.deploy(self.comp, self.node)


@dataclass
class WaitFor(Step):
    port: int
    host: str
    timeout: float

    def process(self, backend):
        backend.wait_for(self.host, self.port, self.timeout)
