class ListNode:

    def __init__(self, val):
        self.val = val
        self.prev = None 
        self.next = None
    
class MyLinkedList:

    def __init__(self, val):
        #Let's initialize our head, tail and size here.
        self.head = None
        self.tail = None 
        self.size = 0

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1

        cur = self.head

        while index != 0:
            cur = cur.next
            index = index - 1

        return cur.val
            
    def addAtHead(self, val: int) -> None:
        new_node = ListNode()
        
