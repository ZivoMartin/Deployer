import os
from cluster import Cluster
from component import Component
from services.mosquitto import Mosquitto
from services.kairos import Kairos

cluster = Cluster()
nodes = cluster.allocate(3)

robot_count = 6

docker_video_path = "/data/crowd_run_1080p50.y4m"
host_video_path = os.path.abspath("./crowd_run_1080p50.y4m")

# Add 3 robots with 3 ids
for i in range(robot_count):
    component = Component(
        image="explorer",
        name=f"node-{i}",
        command=f"./explorer process {i} {docker_video_path}",
        stdout=True
    )
    component.mount(host_video_path, docker_video_path)
    cluster.add(component)

# Add the server
cluster.add(Component(
    image="explorer",
    name=f"server",
    command=f"./explorer serve {robot_count}",
    stdout=True,
    ports={"3333/tcp": 3333}
))

# Add the cloud
cluster.add(Component(
    image="explorer",
    name=f"cloud",
    command=f"./explorer cloud",
    stdout=True,
    priority=1
))

# Add the services, specify the name to make sure it matches the one we use in the explorer.
mosquitto = Mosquitto(name = "mosquitto")
mosquitto.set_priority(2)
cluster.add(mosquitto)

kairos = Kairos(name="kairos")
kairos.set_logs(stderr=True, stdout=True)
kairos.set_priority(1)
cluster.add(kairos)

# Execute deployment
cluster.run()

try:
    while True:
        pass
except KeyboardInterrupt:
    pass
