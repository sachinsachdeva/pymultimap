import threading

import pytest

from pymultimap import MultiMap


@pytest.fixture
def basic_multimap():
    multimap = MultiMap()
    multimap["a"] = 1
    multimap["a"] = 2
    multimap["b"] = 3
    return multimap


@pytest.fixture(params=[False, True], ids=["sorted", "sorted-reverse"])
def sorted_multimap(request):
    multimap = MultiMap(sorted=True, reverse=request.param)
    multimap[1] = "a"
    multimap[3] = "c"
    multimap[2] = "b"
    return multimap


def test_getitem_returns_all_values_for_a_key(basic_multimap):
    assert basic_multimap["a"] == [1, 2]
    assert basic_multimap["b"] == [3]


def test_getitem_raises_for_missing_key(basic_multimap):
    with pytest.raises(KeyError, match="'c' not found"):
        basic_multimap["c"]


def test_setitem_appends_to_existing_key(basic_multimap):
    basic_multimap["a"] = 5
    basic_multimap["c"] = 4

    assert basic_multimap["a"] == [1, 2, 5]
    assert basic_multimap["c"] == [4]


def test_delitem_removes_key(basic_multimap):
    del basic_multimap["a"]

    assert "a" not in basic_multimap
    assert len(basic_multimap) == 1


def test_delitem_raises_for_missing_key(basic_multimap):
    with pytest.raises(KeyError, match="'c' not found"):
        del basic_multimap["c"]


def test_len_counts_distinct_keys(basic_multimap):
    assert len(basic_multimap) == 2


def test_clear_removes_all_keys(basic_multimap):
    basic_multimap.clear()

    assert len(basic_multimap) == 0
    assert list(basic_multimap.items()) == []


def test_repr_matches_string_form(basic_multimap):
    assert repr(basic_multimap) == "{a: [1, 2], b: [3]}"
    assert str(basic_multimap) == "{a: [1, 2], b: [3]}"


def test_iter_yields_keys_in_insertion_order(basic_multimap):
    assert list(iter(basic_multimap)) == ["a", "b"]


def test_get_returns_default_for_missing_key(basic_multimap):
    assert basic_multimap.get("c") is None
    assert basic_multimap.get("c", []) == []


def test_reverse_requires_sorted():
    with pytest.raises(ValueError, match="reverse=True requires sorted=True"):
        MultiMap(reverse=True)


def test_sorted_multimap_orders_keys_and_values(sorted_multimap):
    expected_keys = [3, 2, 1] if sorted_multimap._reverse else [1, 2, 3]
    expected_values = (
        [["c"], ["b"], ["a"]] if sorted_multimap._reverse else [["a"], ["b"], ["c"]]
    )

    assert list(sorted_multimap.keys()) == expected_keys
    assert list(sorted_multimap.values()) == expected_values
    assert list(sorted_multimap.items()) == list(zip(expected_keys, expected_values))


def test_sorted_multimap_appends_and_retains_order(sorted_multimap):
    sorted_multimap[5] = "e"
    sorted_multimap[4] = "d"
    sorted_multimap[1] = "aa"

    assert sorted_multimap[1] == ["a", "aa"]
    assert list(sorted_multimap.keys()) == (
        [5, 4, 3, 2, 1] if sorted_multimap._reverse else [1, 2, 3, 4, 5]
    )


def test_delete_and_reinsert_key_resets_value_bucket(basic_multimap):
    del basic_multimap["a"]
    basic_multimap["a"] = 7

    assert basic_multimap["a"] == [7]


def test_setitem_preserves_both_values_when_threads_write_same_new_key():
    class CoordinatedStore(dict):
        def __init__(self):
            super().__init__()
            self.barrier = threading.Barrier(2)

        def __contains__(self, key):
            result = super().__contains__(key)
            try:
                self.barrier.wait(timeout=0.2)
            except threading.BrokenBarrierError:
                pass
            return result

    multimap = MultiMap()
    store = CoordinatedStore()
    multimap._store = store

    def worker(value):
        multimap["shared"] = value

    threads = [
        threading.Thread(target=worker, args=(1,)),
        threading.Thread(target=worker, args=(2,)),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    assert sorted(multimap["shared"]) == [1, 2]
