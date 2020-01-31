# Galaxy Docker Image with Reverse Proxy

The following instructions are used to create a docker image of galaxy with a reverse proxy in from of it.

## Requirements

  - Docker Engine

## Deploy:

1. EXAREME_IP has to be the IP of the exareme.
2. EXAREME_PORT has to be the port of the exareme.
3. In the cmd "htpasswd -bc /etc/apache2/htpasswd admin password", you can change the password. Username (admin) cannot be changed on runtime.
4. You can also change the galaxy image that is going to be deployed, by changing the tag of the image (hbpmip/galaxy:v1.3).

Use the following command after changing the appropriate variables:
```
docker run -d -e EXAREME_IP=88.197.53.100 -e EXAREME_PORT=9090 -p 8090:80 hbpmip/galaxy:v1.3 /bin/bash -c "htpasswd -bc /etc/apache2/htpasswd admin password && ./createExaremeVariables.sh && /etc/init.d/apache2 restart && ./run.sh"
```

Galaxy will take some time until it is up and running.

You can check the logs by running the command ```docker ps```  and then ```docker logs CONTAINER_ID``` with the specific galaxy container id.

Galaxy will be visible on the  ```localhost:8090/nativeGalaxy``` location.


## Building the docker image:

If you want to create a new image of Galaxy you can follow these instructions:

1. (Optional) Edit galaxy.conf :
	- On line 15 and 30 change ```nativeGalaxy``` to the desired location.

2. Create the docker image by running the command :
	```docker build -t hbpmip/galaxy:v1.3 . ```

3. (Optional) Pre-run the galaxy installer:
	- Run and access the image internally with ```docker run -i -t hbpmip/galaxy:v1.3 bash```
	- Run the galaxy installer ```./run.sh ```
	- After it is done, open galaxy from the browser `localhost:8090/nativeGalaxy` and create all the workflows that you want to be pre-installed.
	- Afterwards stop the running service with Ctrl+C and exit the image with ```exit```
	- Get the container id with ```docker ps -a```
	- Save the changes to the docker image with ```docker commit aaa527d9d22f hbpmip/galaxy:v1.3```
	- Upload the image ```docker push hbpmip/galaxy:v1.3```

