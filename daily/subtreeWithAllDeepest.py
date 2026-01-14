from leetcode_tester import LeetCodeTester, TreeNode
from typing import Optional

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def subtreeWithAllDeepest(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def maxDepth(root):
            if not root:
                return 0
            return 1 + max(maxDepth(root.left), maxDepth(root.right))

        def dfs(root, current_length, max_depth):
            if root:
                left = dfs(root.left, current_length + 1, max_depth)
                right = dfs(root.right, current_length + 1, max_depth)
                if current_length == max_depth - 1:
                    return root

                if left and right:
                    return root
                return left or right

        max_depth = maxDepth(root)

        return dfs(root, 0, max_depth)

tester = LeetCodeTester(Solution)
tester.add_test(TreeNode.from_list([3,5,1,6,2,0,8,None,None,7,4]), expected=TreeNode.from_list([2,7,4]))
tester.add_test(TreeNode.from_list([1]), expected=TreeNode.from_list([1]))
tester.add_test(TreeNode.from_list([0,1,3,None,2]), expected=TreeNode.from_list([2]))
tester.add_test(TreeNode.from_list([0,1,3,None,2,None,4]), expected=TreeNode.from_list([0,1,3,None,2,None,4]))
tester.run()