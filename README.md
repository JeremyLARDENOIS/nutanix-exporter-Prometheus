# nutanix-exporter-Prometheus

This is a containerised exporter written in python to collect metrics for Cluster, Hosts, VMs and Storage Containers.

## TLDR

Execute this command line

```sh
. bin/activate ; ./bin/python3 app/main.py > /dev/null &
```

## With Python Venv

In the root of the repository, activate the virtual env:

```sh
. bin/activate
```

To launch the app, do:

```sh
./bin/python3 app/main.py
```

You can launch the app in background doing:

```sh
./bin/python3 app/main.py > /dev/null &
```

You can have some help about the argumets that you can pass with the command

```sh
./bin/python3 app/main.py --help
```

If you want exit the virtual env, you can type `deactivate` in the shell.

## With docker

### TLDR, but with docker

Go in the **app** directory and run this:

```sh
docker rm nutanix-exporter-1; docker build -t nutanix-prometheus-exporter . &&  docker run --name nutanix-exporter-1 -p 8000:8000 nutanix-prometheus-exporter
```

Add `-d` option if you want to launch it in background at the docker run command

It can take some minutes to have some logs.

### Building the container

From the **app** directory, run:

`docker build -t nutanix-prometheus-exporter .`

### Running the container

Example of docker command line:

`docker run --name nutanix-exporter-1 -p 8000:8000 nutanix-prometheus-exporter`

You can then open your browser to [http://localhost:8000](http://localhost:8000) to verify metrics are being published correctly.

To access the metrcis server from another machine over IP, allow the port on firewall in the metrics server VM

`firewall-cmd --zone=public --add-port=8000/tcp --permanent`

`systemctl restart firewalld`

You can use `docker logs nutanix-exporter-1` to troubleshoot issues in the container.
