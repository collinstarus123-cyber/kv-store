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

## Roadmap

- [x] In-memory store with set, get, delete
- [x] Interactive command line
- [ ] Persistence with an append-only write-ahead log
- [ ] Crash recovery
- [ ] Compaction of the log
- [ ] Indexing and range queries
- [ ] Network server