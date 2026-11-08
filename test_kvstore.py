from kvstore import KVStore


def test_set_then_get():
    store = KVStore()
    store.set("name", "Ada")
    assert store.get("name") == "Ada"


def test_get_missing_key_returns_none():
    assert KVStore().get("nope") is None


def test_set_overwrites_old_value():
    store = KVStore()
    store.set("k", "1")
    store.set("k", "2")
    assert store.get("k") == "2"


def test_delete_removes_key():
    store = KVStore()
    store.set("k", "v")
    assert store.delete("k") is True
    assert store.get("k") is None


def test_delete_missing_key_returns_false():
    assert KVStore().delete("nope") is False


def test_keys_and_length():
    store = KVStore()
    store.set("a", "1")
    store.set("b", "2")
    assert sorted(store.keys()) == ["a", "b"]
    assert len(store) == 2