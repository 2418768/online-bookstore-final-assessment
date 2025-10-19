import pytest

@pytest.fixture
def client():
    """Creat test version of website."""
    from app import app          # import Flask 
    app.config['TESTING'] = True # turn on testing 
    return app.test_client()     # assign web browser

# --- Hypothesis profile for CI (keeps fuzzing fast & stable) ---
try:
    from hypothesis import settings, HealthCheck

    settings.register_profile(
        "ci",
        settings(
            max_examples=25,                # fewer cases in CI
            deadline=500,                   # 500 ms per example
            suppress_health_check=[HealthCheck.too_slow],
        ),
    )
    settings.load_profile("ci")
except Exception:
    pass
