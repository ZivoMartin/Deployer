from component import Component

class Streamer(Component):
    def __init__(self, name=None):
        super().__init__(
            image = "streamer",
            replicas = 1,
            name = "streamer" if name is None else name
        )
