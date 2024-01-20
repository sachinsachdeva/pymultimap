class MultiMap:
    # A class that represents a dictionary with duplicate keys

    def __init__(self):
        # Initialize an empty hashmap to store key-value pairs
        self.items = {}

    def __setitem__(self, key, value):
        # Add a new key-value pair to the hashmap
        # If the key already exists, append the value to the existing list
        # Otherwise, create a new list with the value
        if key in self.items:
            self.items[key].append(value)
        else:
            self.items[key] = [value]

    def __getitem__(self, key):
        # Return a list of values associated with the given key
        # If the key does not exist, raise a KeyError
        if key in self.items:
            return self.items[key]
        else:
            raise KeyError(f"{key} not found")

    def __delitem__(self, key):
        # Delete the key-value pair with the given key
        # If the key does not exist, raise a KeyError
        if key in self.items:
            del self.items[key]
        else:
            raise KeyError(f"{key} not found")

    def __len__(self):
        # Return the number of key-value pairs in the hashmap
        return len(self.items)

    def __str__(self):
        # Return a string representation of the dictionary
        return "{" + ", ".join(f"{k}: {v}" for k, v in self.items.items()) + "}"

    def keys(self):
        # Return a list of keys in the dictionary
        return list(self.items.keys())

    def values(self):
        # Return a list of values in the dictionary
        return list(self.items.values())

    def items(self):
        # Return a list of key-value pairs in the dictionary
        return list(self.items.items())
