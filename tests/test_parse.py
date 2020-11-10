import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


def test_parse80(test_app):
    with open('80.pdf', 'rb') as file:
        response = test_app.post(
            "/decodefile/",
            files={"file": ("filename", file)})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['n'] == 80
    assert data['codes'][-1] == \
           "010460373162109221ikI>HEJLtE:tD\u001d918069\u001d92gBRfERwFH6vF/haAG8ADNMGaTdry3V0j1rfD6OwPJlvK5ftyRbFUnJFdOO7FAZv7FVtwYqkGwLyJ2cwHAjDzRA=="
