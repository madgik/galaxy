# Galaxy Docker Image with Reverse Proxy

The following instructions are used to create a docker image of galaxy with a reverse proxy in from of it.

## Requirements

  - Docker Engine

## Building the docker image:

1. (Optional) Edit galaxy.conf :
	- On line 15 and 30 change ```nativeGalaxy``` to the desired location.

2. Create the docker image by running the command :
	```docker build -t hbpmip/galaxy:v1.2.2 . ```

3. (Optional) Pre-run the galaxy installer:
	- Run and access the image internally with ```docker run -i -t hbpmip/galaxy:v1.2.2 bash```
	- Run the galaxy installer ```./run.sh ```
	- After it is done installing and the service has started stop it with Ctrl+C and exit the image with ```exit```
	- Get the container id with ```docker ps -a```
	- Save the changes to the docker image with ```docker commit aaa527d9d22f hbpmip/galaxy:v1.2.2```
	- Upload the image ```docker push hbpmip/galaxy:v1.2.2```

## Deploy:

1. EXAREME_IP has to be the IP of the exareme.
2. EXAREME_PORT has to be the port of the exareme.
3. In the cmd "htpasswd -bc /etc/apache2/htpasswd admin password", you can change the password. Username (admin) cannot be changed on runtime.
4. You can also change the galaxy image that is going to be deployed, by changing the tag of the image (hbpmip/galaxy:v1.2.2).

Use the following command after changing the appropriate variables:
```
docker run -d -e EXAREME_IP=88.197.53.100 -e EXAREME_PORT=9090 -p 8090:80 hbpmip/galaxy:v1.2.2 /bin/bash -c "htpasswd -bc /etc/apache2/htpasswd admin password && ./createExaremeVariables.sh && /etc/init.d/apache2 restart && ./run.sh"
```

Galaxy will take some time until it is up and running.

You can check the logs by running the command ```docker ps```  and then ```docker logs CONTAINER_ID``` with the specific galaxy container id.

# Galaxy Integration with MIP Front-End

In order for this instance of Galaxy to be included in the MIP front end, it has to be in the same reverse proxy as the front end portal.

In order to do that an additional apache proxy has to be installed.

## Installing the Apache

You can install apache yourself or follow these commands for Ubuntu instances:

```
sudo apt-get install apache2
sudo apt-get install apache2 libapache2-mod-proxy-uwsgi
sudo a2enmod headers deflate expires rewrite proxy proxy_uwsgi
sudo a2enmod proxy_http
```

After it is installed go to the folder ```/etc/apache2/sites-enabled/``` and modify ```000-default.conf``` to the following:

```
<VirtualHost *:80>
	# The ServerName directive sets the request scheme, hostname and port that
	# the server uses to identify itself. This is used when creating
	# redirection URLs. In the context of virtual hosts, the ServerName
	# specifies what hostname must appear in the request's Host: header to
	# match this virtual host. For the default virtual host (this file) this
	# value is not decisive as it is used as a last resort host regardless.
	# However, you must set it for any further virtual host explicitly.
	#ServerName www.example.com

	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html

	# Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
	# error, crit, alert, emerg.
	# It is also possible to configure the loglevel for particular
	# modules, e.g.
	#LogLevel info ssl:warn

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	# For most configuration files from conf-available/, which are
	# enabled or disabled at a global level, it is possible to
	# include a line for only one particular virtual host. For example the
	# following line enables the CGI configuration for this host only
	# after it has been globally disabled with "a2disconf".
	#Include conf-available/serve-cgi-bin.conf


	ProxyPass /nativeGalaxy http://{Galaxy Installation Ip}:{Galaxy Installation Port}/nativeGalaxy
	ProxyPassReverse /nativeGalaxy http://{Galaxy Installation Ip}:{Galaxy Installation Port}/nativeGalaxy

	ProxyPass / http://http://{Front End Installation Ip}:{Front End Installation Port}/
	ProxyPassReverse / http://http://{Front End Installation Ip}:{Front End Installation Port}/
</VirtualHost>
```
```{Galaxy Installation Ip}``` and ```{Front End Installation Ip}``` should be modified accordingly.


Then you can restart apache: ```sudo systemctl restart apache2```

Galaxy should appear on the front end at the ```/galaxy``` location.
