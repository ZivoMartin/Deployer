from component import Component

class Vider(Component):

    def __init__(self,
                 backend = "no",
                 name="vider",
                 stream_server_ip="vider", 
                 stream_server_port=1808, 
                 web_server_ip="vider", 
                 web_server_port=3333, 
                 broker_host="mosquitto",
                 broker_port=1883
                 ):
        
        command = f"./vider --name {name} --broker-port {broker_port} --broker-host {broker_host} --stream-server-ip {stream_server_ip} --stream-server-port {stream_server_port} --web-server-ip {web_server_ip} --web-server-port {web_server_port} --backend {backend}"


        super().__init__(
            image="vider",
            name = name,
            stderr = False,
            stdout = False,
            ports = { f"{web_server_port}/tcp": web_server_port },
            command = command
        )
    
