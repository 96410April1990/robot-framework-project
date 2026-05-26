#Define a node class

class Node:

    #Creating a constructor that accepts two values - the main value and the .next value.
    #If we want to insert 3, 5, 7 and 9, We will create a node with the main value 3 and the .next value will be null and so on. Follow the same
    #set of steps for the other three elements as well.
    #Next update the .next with the next value and follow the same set of steps for other elements as well.
    def __init__(self, value=None, next=None, prev=None):
        self.value = value
        self.next = next
        self.prev = prev

class LinkedList:
    def __init__(self):
        self.head = None

n1 = Node(3)
n2 = Node(7)
n3 = Node(2)
n4 = Node(9)

ll = LinkedList()

ll.head = n1
n1.next = n2
n2.next = n3
n3.next = n4
n4.next = None
