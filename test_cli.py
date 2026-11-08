from cli import run_command
from kvstore import KVStore


def test_cli_set_and_get():
    store = KVStore()
    assert run_command(store, "SET city Paris") == "OK"
    assert run_command(store, "GET city") == "Paris"


def test_cli_value_can_contain_spaces():
    store = KVStore()
    run_command(store, "SET name Ada Lovelace")
    assert run_command(store, "GET name") == "Ada Lovelace"


def test_cli_commands_are_case_insensitive():
    store = KVStore()
    run_command(store, "set a 1")
    assert run_command(store, "get a") == "1"


def test_cli_get_missing_and_unknown_command():
    store = KVStore()
    assert run_command(store, "GET nothing") == "(nil)"
    assert run_command(store, "FLY away").startswith("ERR")


def test_cli_del_and_keys():
    store = KVStore()
    run_command(store, "SET a 1")
    run_command(store, "SET b 2")
    assert run_command(store, "KEYS") == "a\nb"
    assert run_command(store, "DEL a") == "1"
    assert run_command(store, "DEL a") == "0"
    assert run_command(store, "KEYS") == "b"


def test_cli_exit_returns_none():
    assert run_command(KVStore(), "EXIT") is None