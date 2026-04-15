# Deployer

The first implementation will focus on a deployer for the testbed. The goal is to follow a design similar to FogROS2 by providing a generic Python API.

This API will allow users to write simple scripts to deploy Docker containers onto the testbed. At a high level, users will specify:

* the number of nodes to allocate,
* the Docker images to deploy,
* and any additional services required by the distributed system.

These services will themselves run as containers on allocated nodes and will provide additional optional functionalities.

In summary, the API will likely expose three main functionalities:

* **Node allocation**
* **Container deployment**
* **Service specification**, allowing users to define which auxiliary services should run as part of the system

The primary goal of this project is to deliver an initial working prototype. Once this is achieved, we will focus on extending the tool by enabling more precise deployment customization through a variety of parameters and contextual constraints. For example, certain nodes may need to run in more resource-rich environments, or require additional specifications for their allocation.

