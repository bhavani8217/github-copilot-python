import pytest

from app import app, CURRENT


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        CURRENT['puzzle'] = None
        CURRENT['solution'] = None
        yield test_client
