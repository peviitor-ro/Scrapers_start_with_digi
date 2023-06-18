#
#
#
# This file is for logo update
#
import requests
import json


def update_logo(id: str, logo_url: str):
    """
    Update Logo
    """
    headers = {
        "Content-Type": "application/json"
    }
    url = "https://api.peviitor.ro/v1/logo/add/"
    data = json.dumps([{"id": id, "logo": logo_url}])

    response = requests.post(url, headers=headers, data=data)

    return response
