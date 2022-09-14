from bcolors import bcolors
from datetime import datetime
import json
from process_request import process_request
import os

def prism_get_cluster(api_server,username,secret,secure=False):
    """Retrieves data from the Prism Element v2 REST API endpoint /clusters.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        
    Returns:
        Cluster uuid as cluster_uuid. Cluster details as cluster_details
    """
    
    #region prepare the api call
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    api_server_port = int(os.getenv("APP_PORT", "9440"))
    api_server_endpoint = "/PrismGateway/services/rest/v2.0/clusters/"
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "GET"
    #endregion

    print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Making a {method} API call to {url} with secure set to {secure}{bcolors.RESET}")
    resp = process_request(url,method,username,secret,headers,secure=secure)

    # deal with the result/response
    if resp.ok:
        json_resp = json.loads(resp.content)
        cluster_uuid = json_resp['entities'][0]['uuid']
        cluster_details = json_resp['entities'][0]
        return cluster_uuid, cluster_details
    else:
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] Request failed! Status code: {resp.status_code}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] reason: {resp.reason}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] text: {resp.text}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] raise_for_status: {resp.raise_for_status()}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] elapsed: {resp.elapsed}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] headers: {resp.headers}{bcolors.RESET}")
        if payload:
            print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] payload: {payload}{bcolors.RESET}")
        print(json.dumps(
            json.loads(response.content),
            indent=4
        ))
        raise "Error"

def prism_get_vm(api_server,username,secret,secure=False):
    """Retrieves data from the Prism Element v1 REST API endpoint /vms .

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        
    Returns:
        List of VMs and their details as vm_details
    """
    
    #region prepare the api call
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    api_server_port = int(os.getenv("APP_PORT", "9440"))
    api_server_endpoint = f"/PrismGateway/services/rest/v1/vms"
    # api_server_endpoint = f"/PrismGateway/services/rest/v2.0/vms"
    # api_server_endpoint = f'/api/nutanix/v2.0/vms'
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "GET"
    #endregion
    
    print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Making a {method} API call to {url} with secure set to {secure}{bcolors.RESET}")
    resp = process_request(url,method,username,secret,headers,secure=secure)

    # deal with the result/response
    if resp.ok:
        json_resp = json.loads(resp.content)
        vm_details = json_resp['entities']
        return vm_details
    else:
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] Request failed! Status code: {resp.status_code}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] reason: {resp.reason}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] text: {resp.text}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] raise_for_status: {resp.raise_for_status()}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] elapsed: {resp.elapsed}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] headers: {resp.headers}{bcolors.RESET}")
        if payload is not None:
            print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] payload: {payload}{bcolors.RESET}")
        print(json.dumps(
            json.loads(response.content),
            indent=4
        ))
        raise

def prism_get_host(api_server,username,secret,secure=False):
    """Retrieves data from the Prism Element v2 REST API endpoint /hosts .

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        
    Returns:
        List of hosts and their details as host_details
    """
    
    #region prepare the api call
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    api_server_port = int(os.getenv("APP_PORT", "9440"))
    api_server_endpoint = f"/PrismGateway/services/rest/v2.0/hosts"
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "GET"
    #endregion
    
    print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Making a {method} API call to {url} with secure set to {secure}{bcolors.RESET}")
    resp = process_request(url,method,username,secret,headers,secure=secure)

    # deal with the result/response
    if resp.ok:
        json_resp = json.loads(resp.content)
        host_details = json_resp['entities']
        return host_details
    else:
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] Request failed! Status code: {resp.status_code}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] reason: {resp.reason}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] text: {resp.text}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] raise_for_status: {resp.raise_for_status()}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] elapsed: {resp.elapsed}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] headers: {resp.headers}{bcolors.RESET}")
        if payload is not None:
            print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] payload: {payload}{bcolors.RESET}")
        print(json.dumps(
            json.loads(response.content),
            indent=4
        ))
        raise

def prism_get_storage_containers(api_server,username,secret,secure=False):
    """Retrieves data from the Prism Element v2 REST API endpoint /storage_containers.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        
    Returns:
        Storage containers details as storage_containers_details
    """
    
    #region prepare the api call
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    api_server_port = int(os.getenv("APP_PORT", "9440"))
    api_server_endpoint = f"/PrismGateway/services/rest/v2.0/storage_containers/"
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "GET"
    #endregion
    
    print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Making a {method} API call to {url} with secure set to {secure}{bcolors.RESET}")
    resp = process_request(url,method,username,secret,headers,secure=secure)

    # deal with the result/response
    if resp.ok:
        json_resp = json.loads(resp.content)
        storage_containers_details = json_resp['entities']
        return storage_containers_details
    else:
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] Request failed! Status code: {resp.status_code}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] reason: {resp.reason}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] text: {resp.text}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] raise_for_status: {resp.raise_for_status()}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] elapsed: {resp.elapsed}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] headers: {resp.headers}{bcolors.RESET}")
        if payload is not None:
            print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] payload: {payload}{bcolors.RESET}")
        print(json.dumps(
            json.loads(response.content),
            indent=4
        ))
        raise