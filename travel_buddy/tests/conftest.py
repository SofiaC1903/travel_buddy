import pytest

from ..app import create_app
from ..config import TestConfig
from travel_buddy.travel_buddy.db import db
from unittest.mock import MagicMock

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session


@pytest.fixture
def mock_redis(mocker):
    """
    Mock the Redis client to avoid real Redis connections during tests.
    """
    mock = MagicMock()
    # Patch the redis_client in your application
    mocker.patch("travel_buddy.travel_buddy.clients.redis_client.redis_client", mock)
    return mock