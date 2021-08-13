class HashTable:
    def __init__(self):
        # Assuming the max length of the list is 100
        self.MAX = 10
        self.arr = [[] for i in range(self.MAX)]

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

        # Updating an existing value
        found = False
        for idx, ele in enumerate(self.arr[h]):
            # If for this key, we already hae an element
            if len(ele) == 2 and ele[0] == key:
                self.arr[h][idx] = (key, value)
                found = True
                break
        # If key not already in dict
        if not found:
            self.arr[h].append((key, value))

    # def get(self, key):
    def __getitem__(self, key):
        h = self.get_hash(key)
        # Loop through the LL
        for ele in self.arr[h]:
            # If for this key, we already hae an element
            if len(ele) == 2 and ele[0] == key:
                return ele[1]
        # By default, if not found then it will return None

    def __delitem__(self, key):
        h = self.get_hash(key)
        for idx, ele in enumerate(self.arr[h]):
            if ele[0] == key:
                del self.arr[h][idx]

#############################################################################

if __name__ == '__main__':
    ht = HashTable()

    dates = ['Jan 1', 'Jan 2', 'Jan 3', 'Jan 4', 'Jan 5', 'Jan 6', 'Jan 7', 'Jan 8', 'Jan 9', 'Jan 10']
    temps = [27, 31, 23, 34, 37, 38, 29, 30, 35, 30]

    # Set up dictionary
    for idx, ele in enumerate(dates):
        ht[ele] = temps[idx]

    print(ht.arr)
    print(ht['Jan 9'])
    print(ht['Jan 4'])