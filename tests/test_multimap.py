import pytest
from pymultimap.multimap import MultiMap # Assuming the class is defined in a file named multimap.py

@pytest.fixture
def md():
    # A fixture that creates and returns a sample MultiMap object
    md = MultiMap()
    md["a"] = 1
    md["a"] = 2
    md["b"] = 3
    return md

def test_getitem(md):
    # A function that tests the __getitem__ method of the MultiMap class
    assert md["a"] == [1, 2] # Check if the key "a" returns the list [1, 2]
    assert md["b"] == [3] # Check if the key "b" returns the list [3]
    with pytest.raises(KeyError): # Check if a non-existent key raises a KeyError
        md["c"]

def test_setitem(md):
    # A function that tests the __setitem__ method of the MultiMap class
    md["c"] = 4 # Add a new key-value pair to the MultiMap object
    assert md["c"] == [4] # Check if the key "c" returns the list [4]
    md["a"] = 5 # Add another value to the existing key "a"
    assert md["a"] == [1, 2, 5] # Check if the key "a" returns the list [1, 2, 5]
