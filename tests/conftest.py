from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from pymongo.database import Database
from pytest import MonkeyPatch

from src.app import app


@pytest.fixture()
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture()
def mongodb(monkeypatch: MonkeyPatch) -> Iterator[Database]:
    monkeypatch.setenv("MONGO_DATABASE_NAME", "hexagonal_architecture_python_testing")

    mongo_client: MongoClient = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5)

    database = mongo_client.get_database("hexagonal_architecture_python_testing")

    yield database

    mongo_client.drop_database("hexagonal_architecture_python_testing")
