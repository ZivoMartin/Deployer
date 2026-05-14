from component import Component

class Resolver(Component):

    def __init__(self, name="resolver", broker="mosquitto", broker_port=1883, channel_cap=10):
        command = f"./resolver --name {name} --broker-port {broker_port} --channel-cap {channel_cap} --broker {broker}"

        super().__init__(
            image="resolver",
            name = name,
            stderr = False,
            stdout = False,
            command = command
        )
