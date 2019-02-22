import requests

#BASE_URL = "http://wimpsite.ahines.net/WIMPSite/api"
BASE_URL = "http://localhost:8000/WIMPSite/api"


def post_chemical_test(json):
    url = BASE_URL + "/test/add_test/"
    request = requests.post(url, json=json)

    print(request.text)


def post_test_strip(name):
    url = BASE_URL + "/test/add_strip/"

    request = requests.post(url, json={"strip_name": name})

    return  request.json()["id"]


def get_test_strips():
    url = BASE_URL + "/test/test_strip/"

    request = requests.get(url)

    return request.json()


def get_test_strip(id):
    url = BASE_URL + "/test/test_strip/"

    request = requests.get(url, json={"id": id})

    return request.json()
