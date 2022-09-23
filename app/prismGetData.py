import message
from process_request import process_request
import json
import os

def prism_get(api_server, api_server_endpoint, username, secret, secure=False):
    """Retrieves data from the Prism Element endpoint chosen
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

    message.ok(f"Making a {method} API call to {url} with secure set to {secure}")
    resp = process_request(url, method, username, secret, headers, secure=secure)

    # deal with the result/response
    if resp.ok:
        return json.loads(resp.content)
    else:
        message.error(f"Request failed! Status code: {resp.status_code}")
        message.error(f"reason: {resp.reason}")
        message.error(f"text: {resp.text}")
        message.error(f"raise_for_status: {resp.raise_for_status()}")
        message.error(f"elapsed: {resp.elapsed}")
        message.error(f"headers: {resp.headers}")
        if resp.payload is not None: # Maybe resp.payload never exists
            message.error(f"payload: {resp.payload}")
        print(json.dumps(
            json.loads(resp.content),
            indent=4
        ))
        raise # TODO: Make an exception class
