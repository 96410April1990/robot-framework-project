class Solution:
    def reverseList(self, head: ListNode) -> ListNode:

        pre = None
        cur = head
        suc = None

        while cur:
            suc = cur.next
            cur.next = pre
            pre = cur
            cur = suc
        
        head = pre
        return head

