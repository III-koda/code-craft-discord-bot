import logging
import re

import requests

_LOGGER = logging.getLogger(__name__)


def api_handler(method, url):
    lowMethod = method.lower()
    pattern = r"^https:\/\/[0-9A-z.]+.[0-9A-z.]+.[a-z]"
    result = re.match(pattern, url)

    if not result:
        return "The URL is invalided"

    if lowMethod == "get":
        r = requests.get(url)
        if r.status_code != 200:
            _LOGGER.error(f"Execute code request returned error:\n{r.content}")
            return r.content.decode("utf-8")
        j = r.json()
        return j
    elif lowMethod == "post":
        r = requests.post(url)
        if r.status_code != 200:
            _LOGGER.error(f"Execute code request returned error:\n{r.content}")
            return r.content.decode("utf-8")
        j = r.json()
        return j

    else:
        return "Methods should be: GET, POST"
