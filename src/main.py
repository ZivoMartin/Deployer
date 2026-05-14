import os
import time
from cluster import Cluster
from component import Component
from services.mosquitto import Mosquitto
from services.kairos import Kairos
from services.vider import Vider
from services.resolver import Resolver

cluster = Cluster(max_concurency=5)

nodes = cluster.allocate(3)

# Add the services

def add_service(service, log_it, dependency=None):
    global cluster
    if log_it:
        service.set_logs(stdout=True, stderr=True)

    if dependency is not None:
        service.depends_on(dependency)
    cluster.add(service)

mosquitto = Mosquitto()
add_service(mosquitto, False)

resolver = Resolver()
add_service(Resolver(), False, mosquitto)

vider = Vider(backend="no")
add_service(vider, False, resolver)

add_service(Kairos(), False, mosquitto)

# Add the app nodes

robot_count = 5

docker_video_path = "/data/crowd_run_1080p50.y4m"
host_video_path = os.path.abspath("./crowd_run_1080p50.y4m")

for i in range(robot_count):
    component = Component(
        image="explorer",
        name=f"node-{i}",
        command=f"./explorer process {i} {docker_video_path} --n {robot_count} --framing detached",
        stdout=False
    )
    component.mount(host_video_path, docker_video_path)
    component.depends_on(vider)
    cluster.add(component)

cloud = Component(
    image="explorer",
    name=f"cloud",
    command=f"./explorer cloud",
    stdout=False,
)
cloud.depends_on(mosquitto)

cluster.add(cloud)



# Execute deployment
cluster.run()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
