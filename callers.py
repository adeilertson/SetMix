import requests
from requests.exceptions import ConnectionError
import json
import logging

import file_handeling

module_logger = logging.getLogger("primary.callers")


def setlist_call(url):
    """Setlist.fm API call

    Args:
        url (str): URL for API call

    Returns:
        dict: JSON response data converted to dict for returned data
    """
    # Load config to get API key
    cfg = file_handeling.get_config()
    # Set headers with API key and return format
    headers = {
    'x-api-key': cfg['setlist_fm_api_key'],
    'accept': 'application/json'
    }
    # Make API call
    try:
        res = requests.get(url, headers=headers)
    except ConnectionError:
        module_logger.error(f"Connection error while attempting to make call to {url}")
        print(f"\nConnection error while attempting to make call to {url}")
        cont = input('\nPress enter to return to menu.\n')
        return None
    # Convert response to json
    data = json.loads(res.content)

    # Bad result check
    # 'status' only returned with errors
    if 'status' in data.keys():
        module_logger.error(f"Status {data['code']} {data['status']} returned for {url}")
        print(f"\nError - Status {data['code']} {data['status']} returned for {url}")
        cont = input('\nPress enter to return to menu.\n')
        return None

    module_logger.info(f"Succesful call to {url}")
    return data