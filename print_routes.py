# print_routes.py
import sys

def get_app():
    """
    Try both common patterns:
      1) from app import create_app  -> create_app({"TESTING": True})
      2) from app import app         -> existing Flask instance
    """
    try:
        from app import create_app  # type: ignore
        try:
            return create_app({"TESTING": True})
        except TypeError:
            # Some factories accept no args
            return create_app()
    except Exception as e1:
        print(f"[info] create_app() path failed: {e1}", file=sys.stderr)

    try:
        from app import app as _app  # type: ignore
        return _app
    except Exception as e2:
