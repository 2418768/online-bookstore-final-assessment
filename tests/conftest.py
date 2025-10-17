import pytest

@pytest.fixture
def client():
    """Creat test version of website."""
    from app import app          # import Flask 
    app.config['TESTING'] = True # turn on testing 
    return app.test_client()     # assign web browser
