# nutanix-exporter-Prometheus

This is a containerised exporter written in python to collect metrics for Cluster, Hosts, VMs and Storage Containers.

## TLDR

```sh
cp app/.env.example app/.env
```

Edit **app/.env**

```sh
. bin/activate ; python3 app/main.py > /dev/null &
```

## With Python Venv

In the root of the repository, activate the virtual env:

```sh
. bin/activate
```

Go in the **app** directory, copy `.env.example` in `.env`, change variables `PRISM`, `PRISM_USERNAME` and `PRISM_SECRET`

To launch the app, do:

```sh
python3 app/main.py
```

You can launch the app in backgroud doing:

```sh
python3 app/main.py > /dev/null &
```

If you want exit the virtual env, you can type `deactivate` in the shell.

## With docker

### TLDR, but with docker

Go in the **app** directory, copy `.env.example` in `.env`, change variables `PRISM`, `PRISM_USERNAME` and `PRISM_SECRET`, and run this:

```sh
docker rm nutanix-exporter-1; docker build -t nutanix-prometheus-exporter . &&  docker run --name nutanix-exporter-1 -p 8000:8000 nutanix-prometheus-exporter
```

Add `-d` option if you want to launch it in background at the docker run command

It can take some minutes to have some logs.

### Building the container

Available environment variables are listed in the `.env.example` file in the **app** directory.

You can copy this file in .env in the **app** directory:

`cp .env.example .env`

Please, edit variables `PRISM`, `PRISM_USERNAME` and `PRISM_SECRET`.

From the **build** directory, run:

`docker build -t nutanix-prometheus-exporter .`

### Running the container

Example of docker command line:

`docker run --name nutanix-exporter-1 -p 8000:8000 nutanix-prometheus-exporter`

You can then open your browser to [http://localhost:8000](http://localhost:8000) to verify metrics are being published correctly.

To access the metrcis server from another machine over IP, allow the port on firewall in the metrics server VM

`firewall-cmd --zone=public --add-port=8000/tcp --permanent`

`systemctl restart firewalld`

You can use `docker logs nutanix-exporter-1` to troubleshoot issues in the container.
