class HashTable:
    def __init__(self):
        # Assuming the max length of the list is 100
        self.MAX = 10
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
        first_loop = 1
        while self.arr[h] is not None:
            h += 1
            if h >= (self.MAX-1):
                if first_loop:
                    first_loop = 0
                    h = 0
                else:
                    print("Hash map is full.  Please delete an entry.")
                    return
        self.arr[h] = (key, value)

    # def get(self, key):
    def __getitem__(self, key):
        h = self.get_hash(key)
        while self.arr[h] is None:
            h += 1
            first_loop = 1
            while self.arr[h] is not None:
                h += 1
                if h >= (self.MAX-1):
                    if first_loop:
                        first_loop = 0
                        h = 0
                    else:
                        print("Hash map is full.  Please delete an entry.")
                        return
        return self.arr[h][1]

    # Introducing this function, to get rid of the for loop that I was previously using
    def get_prob_range(self, index):
        return [*range(index, len(self.arr))] + [*range(0,index)]

    def __delitem__(self, key):
        h = self.get_hash(key)
        prob_range = self.get_prob_range(h)
        for prob_index in prob_range:
            if self.arr[prob_index] is None:
                # item not found so return. You can also throw exception
                print("Not found")
                return
            if self.arr[prob_index][0] == key:
                print("Successful deletion")
                self.arr[prob_index] = None
        print(self.arr)


#############################################################################

if __name__ == '__main__':
    ht = HashTable()

    # Set up 1
    # Note: all have the same hashes
    # 'March 6', 'March 17', 'March 26'

    ht['January 1'] = 15
    print(ht.get_hash('January 1'))
    print(ht.arr)
    ht['January 27'] = 27
    print(ht.get_hash('January 27'))
    print(ht.arr)
    print("------------------------------")
    ht['March 6'] = 130
    print(ht.get_hash('March 6'))
    print(ht.arr)
    ht['March 17'] = 34
    print(ht.get_hash('March 17'))
    print(ht.arr)
    ht['March 21'] = 111
    print(ht.get_hash('March 21'))
    print(ht.arr)
    ht['March 26'] = 255
    print(ht.get_hash('March 26'))
    print(ht.arr)
    print("------------------------------")
    ht['October 1'] = 1
    print(ht.get_hash('October 1'))
    print(ht.arr)
    ht['October 9'] = 2
    print(ht.get_hash('October 9'))
    print(ht.arr)
    ht['October 31'] = 3
    print(ht.get_hash('October 31'))
    print(ht.arr)
    print("------------------------------")
    ht['December 3'] = 8
    print(ht.get_hash('December 3'))
    print(ht.arr)
    ht['December 4'] = 67
    print(ht.get_hash('December 4'))
    print(ht.arr)
    ht['December 21'] = 12
    print(ht.get_hash('December 21'))
    print(ht.arr)
    ht['December 23'] = 88
    print(ht.get_hash('December 23'))
    print(ht.arr)
    print("------------------------------")
    print("DELETING KEYS NOW")
    del ht['December 23']
    print(ht.arr)
    del ht['March 17']
    print(ht.arr)
    del ht['January 1']
    print(ht.arr)
