class KVStore:
    """A tiny in-memory key-value store."""

    def __init__(self):
        self._data = {}

    def set(self, key, value):
        self._data[key] = value

    def get(self, key, default=None):
        return self._data.get(key, default)

    def delete(self, key):
        """Remove a key. Returns True if it existed, False if it did not."""
        if key in self._data:
            del self._data[key]
            return True
        return False

    def keys(self):
        return list(self._data)

    def __len__(self):
        return len(self._data)