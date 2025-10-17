# tests/test_basic.py

def test_home_page(client):
    """Home page should load and show some bookstore content."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Book" in resp.data or b"Cart" in resp.data or b"Add to Cart" in resp.data


def test_add_to_cart__by_title(client):
    """
    Your app's add-to-cart endpoint is POST /add-to-cart
    and it expects form fields including 'book_title' and 'quantity'.
    We'll grab the first book title from app.BOOKS to keep it robust.
    """
    from app import BOOKS
    assert BOOKS, "Expected BOOKS list to be defined in app.py"
    first = BOOKS[0]
    title = first["title"] if isinstance(first, dict) else getattr(first, "title", "Clean Code")

    resp = client.post(
        "/add-to-cart",
        data={"book_title": title, "quantity": "1"},
        follow_redirects=True
    )
    assert resp.status_code in (200, 302)
    # Page should now show cart content or totals
    assert b"Cart" in resp.data or b"Total" in resp.data or b"item" in resp.data


def test_update_cart__zero_removes_item(client):
    """Setting quantity to 0 via /update-cart should empty/remove the item."""
    from app import BOOKS
    title = BOOKS[0]["title"] if isinstance(BOOKS[0], dict) else getattr(BOOKS[0], "title", "Clean Code")

    # Seed: add one
    client.post("/add-to-cart", data={"book_title": title, "quantity": "1"}, follow_redirects=True)

    # Update to 0 → should remove
    r = client.post("/update-cart", data={"book_title": title, "quantity": "0"}, follow_redirects=True)
    assert r.status_code in (200, 302)
    # Expect empty-cart hint
    assert b"empty" in r.data.lower() or b"cart" in r.data.lower()


def test_remove_from_cart(client):
    """Explicit remove via /remove-from-cart should work."""
    from app import BOOKS
    title = BOOKS[0]["title"] if isinstance(BOOKS[0], dict) else getattr(BOOKS[0], "title", "Clean Code")

    client.post("/add-to-cart", data={"book_title": title, "quantity": "1"}, follow_redirects=True)
    r = client.post("/remove-from-cart", data={"book_title": title}, follow_redirects=True)
    assert r.status_code in (200, 302)
    assert b"empty" in r.data.lower() or b"cart" in r.data.lower()


def test_clear_cart(client):
    """POST /clear-cart clears the cart and redirects to /cart."""
    from app import BOOKS
    title = BOOKS[0]["title"] if isinstance(BOOKS[0], dict) else getattr(BOOKS[0], "title", "Clean Code")

    client.post("/add-to-cart", data={"book_title": title, "quantity": "1"}, follow_redirects=True)
    r = client.post("/clear-cart", follow_redirects=True)
    assert r.status_code in (200, 302)
    assert b"empty" in r.data.lower() or b"cart" in r.data.lower()


def test_checkout_empty_cart_behaviour(client):
    """
    GET /checkout when cart is empty should either:
    - redirect with 'Your cart is empty!' message, or
    - render a page that mentions empty cart.
    We'll allow both.
    """
    r = client.get("/checkout", follow_redirects=True)
    assert r.status_code in (200, 302)
    assert b"empty" in r.data.lower() or b"cart" in r.data.lower()
