import requests

BASE_URL = "http://127.0.0.1:8090/api"

def handle_request_exception(e):
    print(f"An error occurred: {e}")
    raise Exception(f"API request failed: {e}")

def make_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        handle_request_exception(e)

# CRUD

def create():
    pass