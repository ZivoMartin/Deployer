from component import Component

class Kairos(Component):
    def __init__(self, name=None):
        super().__init__(
            image = "kairos",
            name = name or "kairos",
            stderr = False,
            stdout = False
        )
