from routers import bundles
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI


class MockBackendServer(FastAPI):

    def __init__(self):
        super().__init__(title='mock', version='0.0.1')

        @self.get('/{fn}', response_model=BackendResponse)
        def mock_backend(request: Request, fn: str) -> BackendResponse:
            return BackendResponse(data={'output': 'mock', 'function': fn})


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
    response = client.get("/bundles/list")
    assert response.status_code == 200
