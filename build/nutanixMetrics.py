import time
from datetime import datetime
from bcolors import bcolors
from prismGetData import prism_get_entities
from prometheus_client import start_http_server, Gauge, Enum, Info

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
        
        self.main_fetch()
            
    def run_metrics_loop(self):
        """Metrics fetching loop"""
        print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Starting metrics loop {bcolors.RESET}")
        while True:
            self.fetch()
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Waiting for {self.polling_interval_seconds} seconds...{bcolors.RESET}")
            time.sleep(self.polling_interval_seconds)

    def main_fetch(self):
        '''Get the main value, needed to use self.fetch()'''
        if self.cluster_metrics:
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d_%H:%M:%S')} [INFO] Initializing metrics for clusters...{bcolors.RESET}")
            
            api_server_endpoint = "/PrismGateway/services/rest/v2.0/clusters/"
            cluster_details = prism_get_entities(
                api_server=self.prism,
                api_server_endpoint=api_server_endpoint,
                username=self.user,
                secret=self.pwd,
                secure=self.prism_secure)[0]
            
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
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d_%H:%M:%S')} [INFO] Initializing metrics for virtual machines...{bcolors.RESET}")
            # vm_details = prism_get_vm(api_server=self.prism,username=self.user,secret=self.pwd,secure=self.prism_secure)
            api_server_endpoint = "/PrismGateway/services/rest/v1/vms"
            vm_details = prism_get_entities(
                api_server=self.prism,
                api_server_endpoint=api_server_endpoint,
                username=self.user,
                secret=self.pwd,
                secure=self.prism_secure)
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
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d_%H:%M:%S')} [INFO] Initializing metrics for Hosts...{bcolors.RESET}")
            api_server_endpoint = "/PrismGateway/services/rest/v2.0/hosts"
            host_details = prism_get_entities(
                api_server=self.prism,
                api_server_endpoint=api_server_endpoint,
                username=self.user,
                secret=self.pwd,
                secure=self.prism_secure)
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
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d_%H:%M:%S')} [INFO] Initializing metrics for storage containers...{bcolors.RESET}")
            api_server_endpoint = "/PrismGateway/services/rest/v2.0/storage_containers/"
            storage_containers_details = prism_get_entities(
                api_server=self.prism,
                api_server_endpoint=api_server_endpoint,
                username=self.user,
                secret=self.pwd,
                secure=self.prism_secure)
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
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Collecting clusters metrics{bcolors.RESET}")
            api_server_endpoint = "/PrismGateway/services/rest/v2.0/clusters/"
            cluster_details = prism_get_entities(
                api_server=self.prism,
                api_server_endpoint=api_server_endpoint,
                username=self.user,
                secret=self.pwd,
                secure=self.prism_secure)[0]
            # cluster_uuid, cluster_details = prism_get_cluster(api_server=self.prism,username=self.user,secret=self.pwd,secure=self.prism_secure)
        
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
            api_server_endpoint = "/PrismGateway/services/rest/v1/vms"
            vm_details = prism_get_entities(
                api_server=self.prism,
                api_server_endpoint=api_server_endpoint,
                username=self.user,
                secret=self.pwd,
                secure=self.prism_secure)
            # vm_details = prism_get_vm(api_server=self.prism,username=self.user,secret=self.pwd,secure=self.prism_secure)
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Collecting vm metrics for {bcolors.RESET}")
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
            api_server_endpoint = "/PrismGateway/services/rest/v2.0/hosts"
            host_details = prism_get_entities(
                api_server=self.prism,
                api_server_endpoint=api_server_endpoint,
                username=self.user,
                secret=self.pwd,
                secure=self.prism_secure)
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Collecting Host metrics for {bcolors.RESET}")
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
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Collecting storage containers metrics{bcolors.RESET}")
            api_server_endpoint = "/PrismGateway/services/rest/v2.0/storage_containers/"
            storage_containers_details = prism_get_entities(
                api_server=self.prism,
                api_server_endpoint=api_server_endpoint,
                username=self.user,
                secret=self.pwd,
                secure=self.prism_secure)
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