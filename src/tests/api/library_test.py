import pytest
import datetime
import json
from typing import List
from api.schemas import IndexTypes, ResponseLibrary
from api.schemas.metadata import LibraryMetadata

LIBRARY_NAME = "test"

def test_get_libraries(http_client):
    """
    Tests that the library endpoint returns an empty list when there are no libraries.
    """
    response = http_client.get("/library")
    assert response.status_code == 200
    assert len(response.json()) == 0
    
def test_add_library(http_client):
    """
    Tests that a library can be added with a POST to the /library endpoint.
    """
    payload = {
        "name": LIBRARY_NAME,
        "metadata": LibraryMetadata(**{}).dict()
    }
    index_type = IndexTypes.FlatL2
    response = http_client.post(
        "/library",
        params={"index_type": index_type},
        json=payload
    )
    assert response.status_code == 201
    
def test_get_library_after_adding(http_client):
    """
    Tests that a library can be retrieved after adding it via the /library endpoint,
    and validate the response is as expected.
    """
    response = http_client.get("/library")
    assert response.status_code == 200
    response = response.json()
    assert len(response) == 1
    assert response == [ResponseLibrary(**response[0]).dict()]
    
def test_add_library_duplicate(http_client):
    """
    Tests that adding a library with a duplicate name fails.
    """
    payload = {
        "name": LIBRARY_NAME,
        "metadata": LibraryMetadata(**{}).dict()
    }
    index_type = IndexTypes.FlatL2
    response = http_client.post(
        "/library",
        params={"index_type": index_type},
        json=payload
    )
    assert response.status_code == 409
    
def test_get_library_by_name(http_client):
    """
    Tests that a library can be retrieved by name via the /library/{name} endpoint,
    and validate the response is as expected.
    """
    response = http_client.get(f"/library/{LIBRARY_NAME}")
    assert response.status_code == 200
    response = response.json()
    assert response == ResponseLibrary(**response).dict()