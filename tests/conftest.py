import copy
import pytest
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Backup and restore the in-memory `activities` dict around each test.

    This ensures tests run with isolated state (Arrange-Act-Assert pattern).
    """
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)
