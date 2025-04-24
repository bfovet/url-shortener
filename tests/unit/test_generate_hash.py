from url_shortener.shortener import generate_hash_url_with_id


def test_generate_hash():
    assert generate_hash_url_with_id("https://github.com/bfovet", 0) == "ZDc0NGQ"
