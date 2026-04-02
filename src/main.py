from cluster import Cluster
from component import Component
from services.mosquitto import Mosquitto

cluster = Cluster()

# Allocate 3 nodes in the cluster
cluster.allocate(3)

# Add 3 robots with 3 ids
for i in range(3):
    cluster.add(Component(image="explorer", name=f"node-{i}", command=f"./explorer process {i}"))

# Add the server
cluster.add(Component(image="explorer", name=f"server", command=f"./explorer serve"))

# Add the services, specify the name to make sure it matches the one we use in the explorer.
cluster.add(Mosquitto(name = "mosquitto", quiet=True))
cluster.add(Streamer(name = "streamer"))

# Execute deployment
cluster.run()

try:
    while True:
        pass
except KeyboardInterrupt:
    cluster.cleanup()
