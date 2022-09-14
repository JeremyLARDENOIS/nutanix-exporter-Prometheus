# nutanix-exporter-Prometheus

This is a containerised exporter written in python to collect metrics for Cluster, Hosts, VMs and Storage Containers.

## Building the container

Available environment variables are listed in the `.env.example` file in the **build** directory.

You can copy this file in .env in the **build** directory:

`cp .env.example .env`

Please, edit variables `PRISM`, `PRISM_USERNAME` and `PRISM_SECRET`.

From the **build** directory, run:

`docker build -t nutanix-prometheus-exporter .`

## Running the container

Example of docker command line:

`docker run --name nutanix-exporter-1 -p 8000:8000 nutanix-prometheus-exporter`

You can then open your browser to [http://localhost:8000](http://localhost:8000) to verify metrics are being published correctly.

To access the metrcis server from another machine over IP, allow the port on firewall in the metrics server VM

`firewall-cmd --zone=public --add-port=8000/tcp --permanent`

`systemctl restart firewalld`

 You can use `docker logs nutanix-exporter-1` to troubleshoot issues in the container.
