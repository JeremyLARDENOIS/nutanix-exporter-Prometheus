import time
import message
import json
import requests

def process_request(url, method, user, password, headers, payload=None, secure=False):
    """
    Processes a web request and handles result appropriately with retries.
    Returns the content of the web request if successfull.
    """
    if payload is not None:
        payload = json.dumps(payload)

    #configuring web request behavior
    timeout=10
    retries = 5
    sleep_between_retries = 5

    while retries > 0:
        try:
            if method == 'GET':
                #print("secure is {}".format(secure))
                response = requests.get(
                    url,
                    headers=headers,
                    auth=(user, password),
                    verify=secure,
                    timeout=timeout
                )
            elif method == 'POST':
                response = requests.post(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password),
                    verify=secure,
                    timeout=timeout
                )
            elif method == 'PUT':
                response = requests.put(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password),
                    verify=secure,
                    timeout=timeout
                )
            elif method == 'PATCH':
                response = requests.patch(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password),
                    verify=secure,
                    timeout=timeout
                )
            elif method == 'DELETE':
                response = requests.delete(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password),
                    verify=secure,
                    timeout=timeout
                )
            else:
                raise Exception("Method not handled")

        except requests.exceptions.HTTPError as error_code:
            message.error(f"Http Error! Status code: {response.status_code}")
            message.error(f"reason: {response.reason}")
            message.error(f"[ERROR] text: {response.text}")
            message.error(f"ERROR] elapsed: {response.elapsed}")
            message.error(f"headers: {response.headers}")
            if payload is not None:
                message.error(f"payload: {payload}")
            print(json.dumps(
                json.loads(response.content),
                indent=4
            ))
            exit(response.status_code)
        except requests.exceptions.ConnectionError as error_code:
            if retries == 1:
                message.error(f"{type(error_code).__name__} {str(error_code)} ")
                exit(1)
            else:
                message.warning(f"{type(error_code).__name__} {str(error_code)} ")
                time.sleep(sleep_between_retries)
                retries -= 1
                message.warning(f"Retries left: {retries}")
                continue
        except requests.exceptions.Timeout as error_code:
            if retries == 1:
                message.error(f"{type(error_code).__name__} {str(error_code)} ")
                exit(1)
            else:
                message.warning(f"{type(error_code).__name__} {str(error_code)} ")
                time.sleep(sleep_between_retries)
                retries -= 1
                message.warning(f"Retries left: {retries}")
                continue
        except requests.exceptions.RequestException as error_code:
            message.error(f"{response.status_code} ")
            exit(response.status_code)
        break

    if response.ok:
        return response
    if response.status_code == 401:
        message.error(f"{response.status_code} {response.reason} ")
        exit(response.status_code)
    elif response.status_code == 500:
        message.error(f"{response.status_code} {response.reason} {response.text} ")
        exit(response.status_code)
    else:
        message.error(f"Request failed! Status code: {response.status_code}")
        message.error(f"reason: {response.reason}")
        message.error(f"text: {response.text}")
        message.error(f"raise_for_status: {response.raise_for_status()}")
        message.error(f"elapsed: {response.elapsed}")
        message.error(f"headers: {response.headers}")
        if payload is not None:
            message.error(f"payload: {payload}")
        print(json.dumps(
            json.loads(response.content),
            indent=4
        ))
        exit(response.status_code)