from typing import Generator

import pytest
from db.session import SessionLocal
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
