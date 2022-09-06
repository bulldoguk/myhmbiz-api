from routers import bundles
import pytest
from fastapi.testclient import TestClient
from .server_mock.backend import MockBackendServer


server = MockBackendServer()
client = TestClient(server)


@pytest.fixture
def credit():
    return bundles.Credit(credits=1, default="default selection")


@pytest.fixture
def bundle():
    return bundles.Bundle(shoppe_guid='test_shoppe', type='mum', size='single', description='some descriptive text', price=70, credits=[])


def test_constructor(credit, bundle):
    assert isinstance(credit, bundles.Credit)
    assert isinstance(bundle, bundles.Bundle)


def test_get():
    """Should give a list of bundles"""
    response = client.get("/list")
    detail_response = response.json()
    assert response.status_code == 200
    assert detail_response['data']['output'] == 'mock'


