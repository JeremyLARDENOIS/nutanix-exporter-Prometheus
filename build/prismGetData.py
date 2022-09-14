from bcolors import bcolors
from datetime import datetime
from process_request import process_request
import json
import os

def prism_get_entities(api_server, api_server_endpoint, username, secret, secure=False):
    """Retrieves data entities from the Prism Element endpoint chosen
    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        
    Returns:
        All the data in entities
    TODO: Should be merge with process request
    """
    #region prepare the api call
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    api_server_port = int(os.getenv("APP_PORT", "9440"))
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "GET"
    #endregion

    print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Making a {method} API call to {url} with secure set to {secure}{bcolors.RESET}")
    resp = process_request(url, method, username, secret, headers, secure=secure)

    # deal with the result/response
    if resp.ok:
        return json.loads(resp.content)["entities"]
    else:
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] Request failed! Status code: {resp.status_code}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] reason: {resp.reason}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] text: {resp.text}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] raise_for_status: {resp.raise_for_status()}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] elapsed: {resp.elapsed}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] headers: {resp.headers}{bcolors.RESET}")
        if resp.payload is not None: # Maybe resp.payload never exists
            print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] payload: {resp.payload}{bcolors.RESET}")
        print(json.dumps(
            json.loads(resp.content),
            indent=4
        ))
        raise # TODO: Make an exception class
