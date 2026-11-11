import subprocess
import sys
from pathlib import Path

from kvstore import KVStore

WRITER = Path(__file__).parent / "crash_writer.py"


def test_values_survive_reopen(tmp_path):
    path = tmp_path / "data.log"
    store = KVStore(path)
    store.set("city", "Paris")
    store.set("name", "Ada")
    store.close()

    reopened = KVStore(path)
    assert reopened.get("city") == "Paris"
    assert reopened.get("name") == "Ada"
    reopened.close()


def test_delete_survives_reopen(tmp_path):
    path = tmp_path / "data.log"
    store = KVStore(path)
    store.set("a", "1")
    store.delete("a")
    store.close()

    reopened = KVStore(path)
    assert reopened.get("a") is None
    reopened.close()


def test_last_write_wins(tmp_path):
    path = tmp_path / "data.log"
    store = KVStore(path)
    store.set("k", "old")
    store.set("k", "new")
    store.close()

    reopened = KVStore(path)
    assert reopened.get("k") == "new"
    reopened.close()


def test_awkward_values_round_trip(tmp_path):
    path = tmp_path / "data.log"
    awkward = {
        "spaces": "a b  c",
        "newline": "line1\nline2",
        "quote": 'say "hi"',
        "unicode": "café ☕",
    }
    store = KVStore(path)
    for key, value in awkward.items():
        store.set(key, value)
    store.close()

    reopened = KVStore(path)
    for key, value in awkward.items():
        assert reopened.get(key) == value
    reopened.close()


def test_torn_last_line_is_ignored_and_log_stays_usable(tmp_path):
    path = tmp_path / "data.log"
    store = KVStore(path)
    store.set("good", "1")
    store.close()

    with open(path, "a", encoding="utf-8", newline="") as f:
        f.write('{"op": "set", "key": "bad", "val')  # a write cut off by a crash

    store = KVStore(path)
    assert store.get("good") == "1"
    assert store.get("bad") is None
    store.set("after", "2")
    store.close()

    final = KVStore(path)
    assert final.get("good") == "1"
    assert final.get("after") == "2"
    final.close()


def test_acknowledged_writes_survive_a_hard_kill(tmp_path):
    path = tmp_path / "data.log"
    proc = subprocess.Popen(
        [sys.executable, str(WRITER), str(path)],
        stdout=subprocess.PIPE,
        text=True,
    )
    lines = []
    try:
        while len(lines) < 50:
            line = proc.stdout.readline()
            assert line, "writer exited before 50 writes"
            lines.append(line)
    finally:
        proc.kill()  # no cleanup, no goodbye: like pulling the plug
    lines += proc.stdout.read().splitlines(keepends=True)
    proc.wait()
    proc.stdout.close()

    acked = [line.split()[1] for line in lines if line.endswith("\n")]
    assert len(acked) >= 50

    store = KVStore(path)
    for i in acked:
        assert store.get(f"key{i}") == f"value{i}"
    store.close()