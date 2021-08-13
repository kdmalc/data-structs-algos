class HashTable:
    def __init__(self):
        # Assuming the max length of the list is 100
        self.MAX = 100
        self.arr = [None for i in range(self.MAX)]

    # This is the implementation of a dictionary
    def get_hash(self, key):
        # Hash
        h = 0
        # This creates the hash by summing the ASCII values of the key's characters
        for char in key:
            h += ord(char)
        # Now map the hash for the given size of the hash map
        return h % self.MAX

    # Note that if we use the built in __setitem__, then we can access via [] instead of ()
    # def add(self, key, value):
    def __setitem__(self, key, value):
        h = self.get_hash(key)
        self.arr[h] = value

    # def get(self, key):
    def __getitem__(self, key):
        h = self.get_hash(key)
        return self.arr[h]

    def __delitem__(self, key):
        h = self.get_hash(key)
        self.arr[h] = None

#############################################################################

if __name__ == '__main__':
    ht = HashTable()

    # Set up 1
    ht['March 6'] = 130
    ht['March 21'] = 34
    ht['December'] = 88

    print(ht.arr)
