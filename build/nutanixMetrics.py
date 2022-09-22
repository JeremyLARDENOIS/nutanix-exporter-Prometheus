import json
import time
import message
from prismGetData import prism_get
from prometheus_client import Gauge, Info
from process_request import process_request

class NutanixMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """
    def __init__(self, app_port=9440, polling_interval_seconds=5, prism='127.0.0.1', user='admin', pwd='Nutanix/4u', prism_secure=False, vm_metrics=True, host_metrics=True, cluster_metrics=True, storage_containers_metrics=True):
        self.app_port = app_port
        self.polling_interval_seconds = polling_interval_seconds
        self.prism = prism
        self.user = user
        self.pwd = pwd
        self.prism_secure = prism_secure
        self.vm_metrics = vm_metrics
        self.host_metrics = host_metrics
        self.cluster_metrics = cluster_metrics
        self.storage_containers_metrics = storage_containers_metrics
        self.headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        self.hosts = []

        self._init_fetch()
            
    def run_metrics_loop(self):
        """Metrics fetching loop"""
        message.ok("Starting metrics loop")
        while True:
            self.fetch()
            message.ok(f"Waiting for {self.polling_interval_seconds} seconds...")
            time.sleep(self.polling_interval_seconds)

    def _init_fetch(self):
        '''Get the main value, needed to use before self.fetch()'''

        message.ok("Initializing metrics for clusters...")
        
        api_server_endpoint = "/PrismGateway/services/rest/v2.0/clusters/"
        cluster_details = prism_get(
            api_server=self.prism,
            api_server_endpoint=api_server_endpoint,
            username=self.user,
            secret=self.pwd,
            secure=self.prism_secure)["entities"][0]
        
        for key,value in cluster_details['stats'].items():
            #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
            key_string = f"NutanixClusters_stats_{key}"
            key_string = key_string.replace(".","_")
            key_string = key_string.replace("-","_")
            setattr(self, key_string, Gauge(key_string, key_string, ['cluster']))
        for key,value in cluster_details['usage_stats'].items():
            #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
            key_string = f"NutanixClusters_usage_stats_{key}"
            key_string = key_string.replace(".","_")
            key_string = key_string.replace("-","_")
            setattr(self, key_string, Gauge(key_string, key_string, ['cluster']))
        
        #self.lts = Enum("is_lts", "AOS Long Term Support", ['cluster'], states=['True', 'False'])
        setattr(self, 'NutanixClusters_info', Info('is_lts', 'Long Term Support AOS true/false', ['cluster']))

        if self.vm_metrics:
            message.ok("Initializing metrics for virtual machines...")

            # Prepare for GET Vms counts 
            key_string = "NutanixVms_count"
            self.NutanixVms_count = Gauge(key_string, key_string)     

            api_server_endpoint = "/PrismGateway/services/rest/v1/vms"
            vm_details = prism_get(
                api_server=self.prism,
                api_server_endpoint=api_server_endpoint,
                username=self.user,
                secret=self.pwd,
                secure=self.prism_secure)["entities"]
            for key,value in vm_details[0]['stats'].items():
                #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                key_string = f"NutanixVms_stats_{key}"
                key_string = key_string.replace(".","_")
                key_string = key_string.replace("-","_")
                setattr(self, key_string, Gauge(key_string, key_string, ['vm']))
            for key,value in vm_details[0]['usageStats'].items():
                #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                key_string = f"NutanixVms_usage_stats_{key}"
                key_string = key_string.replace(".","_")
                key_string = key_string.replace("-","_")
                setattr(self, key_string, Gauge(key_string, key_string, ['vm']))

        if self.host_metrics:
            message.ok("Initializing metrics for Hosts...")

            # Get hostnames on api v3
            key_string="NutanixHosts_count_vms"
            self.NutanixHost_vms_count = Gauge(key_string, key_string, ['host'])

            api_server_endpoint = "/PrismGateway/services/rest/v2.0/hosts"
            host_details = prism_get(
                api_server=self.prism,
                api_server_endpoint=api_server_endpoint,
                username=self.user,
                secret=self.pwd,
                secure=self.prism_secure)["entities"]
            for key,value in host_details[0]['stats'].items():
                #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                key_string = f"NutanixHosts_stats_{key}"
                key_string = key_string.replace(".","_")
                key_string = key_string.replace("-","_")
                setattr(self, key_string, Gauge(key_string, key_string, ['host']))
            for key,value in host_details[0]['usage_stats'].items():
                #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                key_string = f"NutanixHosts_usage_stats_{key}"
                key_string = key_string.replace(".","_")
                key_string = key_string.replace("-","_")
                setattr(self, key_string, Gauge(key_string, key_string, ['host']))

        if self.storage_containers_metrics:
            message.ok("Initializing metrics for storage containers...")
            api_server_endpoint = "/PrismGateway/services/rest/v2.0/storage_containers/"
            storage_containers_details = prism_get(
                api_server=self.prism,
                api_server_endpoint=api_server_endpoint,
                username=self.user,
                secret=self.pwd,
                secure=self.prism_secure)["entities"]
            for key,value in storage_containers_details[0]['stats'].items():
                #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                key_string = f"NutanixStorageContainers_stats_{key}"
                key_string = key_string.replace(".","_")
                key_string = key_string.replace("-","_")
                setattr(self, key_string, Gauge(key_string, key_string, ['storage_container']))
            for key,value in storage_containers_details[0]['usage_stats'].items():
                #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                key_string = f"NutanixStorageContainers_usage_stats_{key}"
                key_string = key_string.replace(".","_")
                key_string = key_string.replace("-","_")
                setattr(self, key_string, Gauge(key_string, key_string, ['storage_container']))

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics with
        new values.
        """

        if self.cluster_metrics:
            message.ok("Collecting clusters metrics")
            api_server_endpoint = "/PrismGateway/services/rest/v2.0/clusters/"
            cluster_details = prism_get(
                api_server=self.prism,
                api_server_endpoint=api_server_endpoint,
                username=self.user,
                secret=self.pwd,
                secure=self.prism_secure)["entities"][0]
        
            for key, value in cluster_details['stats'].items():
                #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                key_string = f"NutanixClusters_stats_{key}"
                key_string = key_string.replace(".","_")
                key_string = key_string.replace("-","_")
                self.__dict__[key_string].labels(cluster=cluster_details['name']).set(value)
            for key, value in cluster_details['usage_stats'].items():
                #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                key_string = f"NutanixClusters_usage_stats_{key}"
                key_string = key_string.replace(".","_")
                key_string = key_string.replace("-","_")
                self.__dict__[key_string].labels(cluster=cluster_details['name']).set(value)
            
            #self.lts.labels(cluster=cluster_details['name']).state(str(cluster_details['is_lts']))
            self.NutanixClusters_info.labels(cluster=cluster_details['name']).info({'is_lts': str(cluster_details['is_lts'])})
        
        if self.vm_metrics:
            # TODO: Refactor this
            # Get the number of VM
            url = f"https://{self.prism}:{self.app_port}/api/nutanix/v3/vms/list"
            resp = process_request(url=url, method="POST", user=self.user, password=self.pwd, payload={"kind":"vm"}, headers=self.headers, secure=self.prism_secure)
            if resp.ok:
                resp_json = json.loads(resp.content)
            else:
                raise
            total_vm = resp_json["metadata"]["total_matches"]
            self.NutanixVms_count.set(total_vm)

            api_server_endpoint = "/PrismGateway/services/rest/v1/vms"
            vm_details = prism_get(
                api_server=self.prism,
                api_server_endpoint=api_server_endpoint,
                username=self.user,
                secret=self.pwd,
                secure=self.prism_secure)["entities"]
            # vm_details = prism_get_vm(api_server=self.prism,username=self.user,secret=self.pwd,secure=self.prism_secure)
            message.ok("Collecting vm metrics for")
            for entity in vm_details:
                for key, value in entity['stats'].items():
                    #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                    key_string = f"NutanixVms_stats_{key}"
                    key_string = key_string.replace(".","_")
                    key_string = key_string.replace("-","_")
                    self.__dict__[key_string].labels(vm=entity['vmName']).set(value)
                for key, value in entity['usageStats'].items():
                    #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                    key_string = f"NutanixVms_usage_stats_{key}"
                    key_string = key_string.replace(".","_")
                    key_string = key_string.replace("-","_")
                    self.__dict__[key_string].labels(vm=entity['vmName']).set(value)
                    
        if self.host_metrics:
            message.ok("Collecting Host metrics for")

            # GET on API V3
            url = f"https://{self.prism}:{self.app_port}/api/nutanix/v3/hosts/list"
            resp = process_request(url=url, method="POST", user=self.user, password=self.pwd, payload={}, headers=self.headers, secure=self.prism_secure)
            if resp.ok:
                resp_json = json.loads(resp.content)
                for host in resp_json["entities"]:
                    name = host["status"].get("name", None)
                    if name:
                        # Look for the number of Vms per host
                        value = host["status"]["resources"]["hypervisor"]["num_vms"]
                        self.NutanixHost_vms_count.labels(host=name).set(value)
            else:
                raise

            api_server_endpoint = "/PrismGateway/services/rest/v2.0/hosts"
            host_details = prism_get(
                api_server=self.prism,
                api_server_endpoint=api_server_endpoint,
                username=self.user,
                secret=self.pwd,
                secure=self.prism_secure)["entities"]
            
            for entity in host_details:
                for key, value in entity['stats'].items():
                    #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                    key_string = f"NutanixHosts_stats_{key}"
                    key_string = key_string.replace(".","_")
                    key_string = key_string.replace("-","_")
                    self.__dict__[key_string].labels(host=entity['name']).set(value)
                for key, value in entity['usage_stats'].items():
                    #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                    key_string = f"NutanixHosts_usage_stats_{key}"
                    key_string = key_string.replace(".","_")
                    key_string = key_string.replace("-","_")
                    self.__dict__[key_string].labels(host=entity['name']).set(value)

        if self.storage_containers_metrics:
            message.ok("Collecting storage containers metrics")
            api_server_endpoint = "/PrismGateway/services/rest/v2.0/storage_containers/"
            storage_containers_details = prism_get(
                api_server=self.prism,
                api_server_endpoint=api_server_endpoint,
                username=self.user,
                secret=self.pwd,
                secure=self.prism_secure)["entities"]
            for container in storage_containers_details:
                for key, value in container['stats'].items():
                    #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                    key_string = f"NutanixStorageContainers_stats_{key}"
                    key_string = key_string.replace(".","_")
                    key_string = key_string.replace("-","_")
                    self.__dict__[key_string].labels(storage_container=container['name']).set(value)
                for key, value in container['usage_stats'].items():
                    #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                    key_string = f"NutanixStorageContainers_usage_stats_{key}"
                    key_string = key_string.replace(".","_")
                    key_string = key_string.replace("-","_")
                    self.__dict__[key_string].labels(storage_container=container['name']).set(value)
