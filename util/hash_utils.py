import hashlib


def get_sha256_hash(string: str) -> str:
    string_encoded = string.encode()
    return hashlib.sha256(string_encoded).hexdigest()
