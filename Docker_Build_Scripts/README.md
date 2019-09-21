# Galaxy Docker Image with Reverse Proxy

The following instructions are used to create a docker image of galaxy with a reverse proxy in from of it.

## Requirements

  - Docker Engine

## Building the docker image:

1. Edit the Dockerfile :
	- On line 32 change the ```username``` and ```password```.

2. Edit exareme_env.py :
	- ```Exareme Ip``` and ```Port``` should be changed and point to the exareme instance.

3. (Optional) Edit galaxy.conf :
	- On line 15 and 37 change ```nativeGalaxy``` to the desired location.

4. Create the docker image by running the command :
	```docker build -t hbpmip/galaxy```

## Deploy:

Use the following command after changing the appropriate variables:

```
docker run -d -p 8090:80 hbpmip/galaxy /bin/bash -c "/etc/init.d/apache2 restart && ./run.sh"
```

Galaxy will take some time until it is up and running.

You can check the logs by running the command ```docker ps```  and then ```docker logs CONTAINER_ID``` with the specific galaxy container id.

