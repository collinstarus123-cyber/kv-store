# kv-store

![CI](https://github.com/collinstarus123-cyber/kv-store/actions/workflows/ci.yml/badge.svg)

A key-value database built from scratch in Python, growing step by step toward a durable storage engine.

## Try it

```
python cli.py
```

```
> SET city Paris
OK
> GET city
Paris
> DEL city
1
```

Commands: `SET key value`, `GET key`, `DEL key`, `KEYS`, `HELP`, `EXIT`.

## Run the tests

```
python -m pip install pytest
python -m pytest -v
```
## How durability works

Every change is first appended to a **write-ahead log** (`kv.log`), one JSON record per line, and only then applied in memory:

```
{"op": "set", "key": "city", "value": "Paris"}
{"op": "del", "key": "city"}
```

On startup the log is replayed from the top to rebuild the state.

- Each append is flushed and `fsync`ed, so an acknowledged write survives a crash or power cut.
- A write cut off mid-line by a crash is detected and ignored, and the log stays usable.
- `test_persistence.py` includes a test that hard-kills a writer process and checks that every acknowledged write is still there.
- Trade-off: `fsync` on every write is slow, because the log grows forever and each write waits for the disk. Compaction is next on the roadmap.

## Roadmap

- [x] In-memory store with set, get, delete
- [x] Interactive command line
- [x] Persistence with an append-only write-ahead log
- [x] Crash recovery
- [ ] Compaction of the log
- [ ] Indexing and range queries
- [ ] Network server