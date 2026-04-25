from __future__ import annotations

import threading
from collections.abc import MutableMapping
from typing import Dict, Generic, Iterator, List, Tuple, TypeVar, Union

from sortedcontainers import SortedDict

K = TypeVar("K")
V = TypeVar("V")


class MultiMap(MutableMapping[K, List[V]], Generic[K, V]):
    """Dictionary-like container that stores multiple values per key."""

    def __init__(self, sorted: bool = False, reverse: bool = False):
        if reverse and not sorted:
            raise ValueError("reverse=True requires sorted=True")

        self._store: Union[Dict[K, List[V]], SortedDict[K, List[V]]] = SortedDict() if sorted else {}
        self._sorted = sorted
        self._reverse = reverse
        self._lock = threading.RLock()

    def __setitem__(self, key: K, value: V) -> None:
        with self._lock:
            if key in self._store:
                self._store[key].append(value)
            else:
                self._store[key] = [value]

    def __getitem__(self, key: K) -> List[V]:
        with self._lock:
            if key in self._store:
                return self._store[key]
            raise KeyError(f"{key!r} not found")

    def __delitem__(self, key: K) -> None:
        with self._lock:
            if key in self._store:
                del self._store[key]
                return
            raise KeyError(f"{key!r} not found")

    def __iter__(self) -> Iterator[K]:
        with self._lock:
            return iter(self.keys())

    def __len__(self) -> int:
        with self._lock:
            return len(self._store)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        with self._lock:
            return "{" + ", ".join(f"{k}: {v}" for k, v in self.items()) + "}"

    def keys(self) -> List[K]:
        with self._lock:
            if self._sorted and self._reverse:
                return list(reversed(self._store.keys()))
            return list(self._store.keys())

    def values(self) -> List[List[V]]:
        with self._lock:
            if self._sorted and self._reverse:
                return list(reversed(self._store.values()))
            return list(self._store.values())

    def items(self) -> List[Tuple[K, List[V]]]:
        with self._lock:
            if self._sorted and self._reverse:
                return list(reversed(self._store.items()))
            return list(self._store.items())
