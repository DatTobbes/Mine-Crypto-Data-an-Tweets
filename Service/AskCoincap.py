import numpy as np
import requests
from requests.auth import HTTPDigestAuth
import json


url = "http://coincap.io/front"

myResponse = requests.get(url)
# For successful API call, response code will be 200 (OK)
if(myResponse.ok):
    print("\n")
    test= myResponse.content
    json_data = json.loads(myResponse.text)

else:
    myResponse.raise_for_status()

