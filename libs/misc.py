import hashlib


def hexdigest(s: str):
    h = hashlib.sha256()
    h.update(s.encode('utf-8'))
    return h.hexdigest()
