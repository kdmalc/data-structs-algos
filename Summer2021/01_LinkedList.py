class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        node = Node(data, self.head)
        self.head = node

    def print(self):
        if self.head is None:
            print("Linked list is empty")
            return

        itr = self.head
        llstr = ''
        while itr:
            llstr += str(itr.data) + '-->'
            itr = itr.next
        print(llstr)

    def insert_at_end(self, data):
        if self.head is None:
            self.head = Node(data, None)
            return

        # Must iterate through all the elements first (traverse full LL)
        itr = self.head
        while itr.next: #E.g. while there is another node after this one
            itr = itr.next
        # Once you finish the above, you are at the last element
        # Ergo, the next node is the one we insert
        itr.next = Node(data, None)

    def insert_values(self, data_list):
        self.head = None
        for data in data_list:
            self.insert_at_end(data)

    def get_length(self):
        itr = self.head
        length = 0
        while itr:
            length += 1
            itr = itr.next
        return length

    def remove_at(self,index):
        if index<0 or index>=self.get_length():
            raise Exception("Out of bounds of Linked List")
        elif index==0:
            self.head = self.head.next

        # Iterate until you reach the node BEFORE the desired index
        itr = self.head
        count = 0
        while itr:
            if count == index - 1:
                # Then just point past the next node, directly to the node thereafter
                itr.next = itr.next.next
                break
            count += 1
            itr = itr.next

    def insert_at(self, index, data):
        if index<0 or index>=self.get_length():
            raise Exception("Out of bounds of Linked List")
        elif index==0:
            self.insert_at_beginning(data)

        count = 0
        itr = self.head
        while itr:
            if count == index - 1:
                itr.next = Node(data, itr.next)
                break
            count += 1
            itr = itr.next

    def replace_at(self, index, data):
        if index<0 or index>=self.get_length():
            raise Exception("Out of bounds of Linked List")
        elif index==0:
            self.insert_at_beginning(data)

        count = 0
        itr = self.head
        while itr:
            if count == index - 1:
                itr.next = Node(data, itr.next.next)
                break
            count += 1
            itr = itr.next

    ############################
    ## Exercise ##
    ############################

    # Helper function:
    def find_index_by_value(self, value):
        itr = self.head
        index = 0
        while itr:
            if value == itr.data:
                return index
            itr = itr.next
            index += 1

    # Actual exercises:
    def insert_after_value(self, data_after, data_to_insert):
        if self.get_length()==0:
            raise Exception("No Linked List exists (0 length)")
        elif self.get_length()==1 and (self.head.data == data_after):
            self.insert_at_end(data_to_insert)
            return

        index = self.find_index_by_value(data_after)
        self.insert_at(index+1, data_to_insert)

    def remove_by_value(self, data):
        if self.get_length()==0:
            raise Exception("No Linked List exists (0 length)")
        elif self.get_length()==1 and self.head.data==data:
            self.head = None
            return

        index = self.find_index_by_value(data)
        self.remove_at(index)


if __name__ == '__main__':
    ll = LinkedList()
    # Set up 1
    '''
    ll.insert_at_beginning(5)
    ll.insert_at_beginning(59)
    ll.insert_at_end(79)
    ll.insert_at_end(80)
    ll.insert_at_end(81)
    '''

    # Additions 2
    ll.insert_values(["banana","mango","grape","pear"])
    ll.print()
    print(ll.get_length())
    ll.remove_at(3)
    ll.print()
    ll.insert_at(2, "Jackfruit")
    ll.print()

    # Exercises
    ll.insert_values([1,2,3,4,5,6,7,8,9])
    ll.print()
    ll.insert_after_value(3,3.5)
    ll.print()
    ll.remove_by_value(3.5)
    ll.print()