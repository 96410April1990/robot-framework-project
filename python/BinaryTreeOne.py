class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> TreeNode:

        if len(inorder) == 0:
            return None

        if len(preorder) == 1:
            last_node = TreeNode(preorder[0])
            return last_node
        
        ind = inorder.index(preorder.pop(0))
        node = TreeNode(inorder[ind])

        node.left = self.buildTree(preorder, inorder[:ind])
        node.right = self.buildTree(preorder, inorder[ind+1:])

        return node




