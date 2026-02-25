from leetcode_tester import LeetCodeTester, TreeNode
from typing import Optional
null = None
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:

    def sumRootToLeaf(self, root: Optional[TreeNode]) -> int:
        def dfs(root: Optional[TreeNode], path: str):
            if root is None:
                return []
            p  = path + str(root.val)
            if root.left is None and root.right is None:
                return [p]
            return dfs(root.left, p) + dfs(root.right, p)
        leafs = dfs(root, "")

        ans = 0
        for leaf in leafs:
            ans += int(leaf, 2)

        return ans




tester = LeetCodeTester(Solution, method_name="sumRootToLeaf")
tester.add_test(TreeNode.from_list([1,0,1,0,1,0,1]), expected=22)
tester.add_test(TreeNode.from_list([0]), expected=0)
tester.add_test(TreeNode.from_list([1,1]), expected=3)
tester.add_test(TreeNode.from_list([1,1,1,1,null,null,null]), expected=10)
[1,1,1,1,null,null,null]
tester.add_test(TreeNode.from_list([1,0,1,0,1,1,0,1,0,0,0,1,0,0,0,0,1,1,0,null,1,0,null,1,1,1,1,null,0,null,null,null,null,null,null,1,null,0,null,null,null,null,null,0,1,1,0,0,0,0,null,null,null,0,null,null,null,0,null,0,null,null,null,null,1,null,null,0,0,0,null,null,null,1,null,null,null,0,0,null,null,null,null,null,0,null,null,null,null,1,null,null,null,0,1,null,0]), expected=4433)
tester.run()