from url_shortener.shortener import generate_hash_url


def test_create_short_link():
    hash_key = generate_hash_url("https://github.com/bfovet", 42)
    assert hash_key == "Yzg0MjV"
