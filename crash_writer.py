import itertools
import sys

from kvstore import KVStore

store = KVStore(sys.argv[1])
for i in itertools.count():
    store.set(f"key{i}", f"value{i}")
    print(f"ACK {i}", flush=True)