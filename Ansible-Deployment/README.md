The Galaxy-Ansible-Scripts builds the Galaxy workflow execution backend for a single host. This script facilitates the local installation and execution of the workflow infrastructure stack and on a user's own infrastructure.

This script installs two separate Galaxy deployments (editor and executor) on two separate postgresql databases. It also exports the data and tools directories of the Executor deployment with NFS (the tools directory of the editor is also internally linked to the Executor tools directory). The Galaxy deployments can be accessible through an automatically setup apache2 proxy, although this option is switched off by default.

## Requirements

* python 2.7
* python-virtualenv
* ansible 2.7 or later

If you have trouble setting up ansible on your system, try virtualenv and run the installation script from there.

## Setup ansible

```code=bash
$ git clone https://github.com/madgik/Galaxy-Ansible-Scripts.git
$ cd Galaxy-Ansible-Scripts
```
If you target the local host, there is no need to edit the `hosts` file. If you target a different host for the installation, update `hosts` file to target the IP of this host.

Please edit the `group_vars/all` file, to set up secure credentials and edit various options of your system. If you don't edit this file, the system will be deployed with default options.

## Configure NFS exports

NFS is used to give access to the `data` and `tools` directories of Galaxy Executor (Executor and Editor share the `tools` directory). You must provide the IPs of the hosts which will have access to these directories, by adding them to your `hosts` file, under the groups `data_nfs_clients` and `tools_nfs_clients` respectively.

### Changes in `group_vars/all`

By default, the system will pull docker images from docker hub. If you have a private docker registry, you must uncommend the following lines. The username and password are http passwords and are optional.
```code=yaml
# registry_url: https://registry.example.com
# registry_username: omtduser
# registry_password: omtdpass
```

By default, the system will setup a postgres database for each galaxy, with DB username and password. You can change the credentials here
```code=yaml,name=group_vars/all
executor_db_name: executor
executor_db_user: executor
executor_db_password: executor
editor_db_name: editor
editor_db_user: editor
editor_db_password: editor
```

For access to the editor, set the API secret
```code=yaml,name=group_vars/all
editor_remote_user_secret: your-secret-here
```

If you want to enable apache2, set this with caution (make sure you don't already have an apache2 on your machine, because it might mess it up)
```code=yaml,name=group_vars/all
apache2_as_reverse_proxy: True
```

## Change ports for Galaxy deployments
If the ports 8080 and/or 8081 are in use, you can change them in `group_vars/all` by setting the variables `executor_port` and `editor_port` to different values.

## Make your Galaxy accessible
Galaxy will be reachable through localhost:8080 (executor) and localhost:8081 (editor) but it is common practice to run it behind a reverse proxy. You can optionally instruct ansible to install apache2 as a reverse proxy for your executor and editor, by setting a flag in `group_vars/all`:

```code=yaml,name=group_vars/all
apache2_as_reverse_proxy: True
```

## Run the script
It is assumed that the scripts run with superuser priviledges. If this is not the case, set add a line in `group_vars/all`:

```code=yaml
executor_directory: /my/locally/accessible/location/executor
editor_directory: /my/locally/accessible/location/editor
``` 

So, we are ready to fire:
```code=bash
$ ansible-galaxy install -r requirements.yaml
$ ansible-playbook -i hosts -u username --ask-pass --ask-become-pass site.yaml
```

If the script completes without errors, you must have a galaxy installation on `/srv/galaxy`. Check `service galaxy status` to see if galaxy runs. You can even run it explicitely with `/srv/galaxy/run.sh`.
