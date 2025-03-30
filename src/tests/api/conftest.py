# tests/conftest.py
import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def base_url():
    return os.getenv("PYTEST_DB_URI")

@pytest.fixture
def http_client(base_url):
    class Client:
        def __init__(self, base_url):
            self.base_url = base_url

        def get(self, path, **kwargs):
            return requests.get(self.base_url + path, **kwargs)

        def post(self, path, **kwargs):
            return requests.post(self.base_url + path, **kwargs)

        def put(self, path, **kwargs):
            return requests.put(self.base_url + path, **kwargs)

        def delete(self, path, **kwargs):
            return requests.delete(self.base_url + path, **kwargs)

    return Client(base_url)
