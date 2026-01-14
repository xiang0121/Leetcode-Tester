from typing import List
from leetcode_tester import LeetCodeTester

class Solution:
    def separateSquares(self, squares: List[List[int]]) -> float:
        top = -float('inf')
        bottom = float('inf')
        for x, y, l in squares:
            top = max(top, y+l)
            bottom = min(bottom, y)

        # binary search
        line = (top + bottom) / 2


        return ans

tester = LeetCodeTester(Solution)
tester.add_test([[0,0,1],[2,2,1]], expected=1.0000)
tester.add_test([[0,0,2],[1,1,1]], expected=1.16667)
tester.run()