import argparse

from kvstore import KVStore

HELP = """Commands:
  SET key value   store a value
  GET key         read a value
  DEL key         delete a key
  KEYS            list all keys
  HELP            show this message
  EXIT            quit"""


def run_command(store, line):
    """Run one command line. Returns the text to print, or None to quit."""
    parts = line.strip().split(maxsplit=2)
    if not parts:
        return ""
    command = parts[0].upper()

    if command == "SET" and len(parts) == 3:
        store.set(parts[1], parts[2])
        return "OK"
    if command == "GET" and len(parts) == 2:
        value = store.get(parts[1])
        return "(nil)" if value is None else value
    if command == "DEL" and len(parts) == 2:
        return "1" if store.delete(parts[1]) else "0"
    if command == "KEYS" and len(parts) == 1:
        return "\n".join(sorted(store.keys())) or "(empty)"
    if command == "HELP":
        return HELP
    if command in ("EXIT", "QUIT"):
        return None
    return "ERR unknown command or wrong arguments (type HELP)"


def main():
    parser = argparse.ArgumentParser(description="A small key-value database.")
    parser.add_argument(
        "--file", default="kv.log", help="log file that keeps your data (default: kv.log)"
    )
    args = parser.parse_args()

    store = KVStore(args.file)
    print(f"kv-store ready ({len(store)} keys loaded from {args.file}). Type HELP for commands.")
    try:
        while True:
            try:
                line = input("> ")
            except (EOFError, KeyboardInterrupt):
                print()
                break
            result = run_command(store, line)
            if result is None:
                break
            if result:
                print(result)
    finally:
        store.close()


if __name__ == "__main__":
    main()