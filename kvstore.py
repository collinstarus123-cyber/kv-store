import json
import os


class KVStore:
    """A key-value store. Give it a file path and every change is saved to a log."""

    def __init__(self, path=None, fsync=True):
        self._data = {}
        self._path = path
        self._fsync = fsync
        self._log = None
        if path is not None:
            needs_newline = self._replay()
            self._log = open(path, "a", encoding="utf-8", newline="")
            if needs_newline:
                self._log.write("\n")
                self._log.flush()

    def _replay(self):
        """Rebuild memory from the log. Returns True if the file ends mid-line."""
        if not os.path.exists(self._path):
            return False
        with open(self._path, "r", encoding="utf-8", newline="") as f:
            text = f.read()
        for line in text.split("\n"):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue  # a half-written line left by a crash: ignore it
            self._apply(record)
        return bool(text) and not text.endswith("\n")

    def _apply(self, record):
        if not isinstance(record, dict):
            return
        if record.get("op") == "set":
            self._data[record["key"]] = record["value"]
        elif record.get("op") == "del":
            self._data.pop(record["key"], None)

    def _append(self, record):
        if self._log is None:
            return
        self._log.write(json.dumps(record) + "\n")
        self._log.flush()
        if self._fsync:
            os.fsync(self._log.fileno())

    def set(self, key, value):
        self._append({"op": "set", "key": key, "value": value})
        self._data[key] = value

    def get(self, key, default=None):
        return self._data.get(key, default)

    def delete(self, key):
        """Remove a key. Returns True if it existed, False if it did not."""
        if key not in self._data:
            return False
        self._append({"op": "del", "key": key})
        del self._data[key]
        return True

    def keys(self):
        return list(self._data)

    def close(self):
        if self._log is not None:
            self._log.close()
            self._log = None

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()

    def __len__(self):
        return len(self._data)