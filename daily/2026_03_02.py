# 1536. Minimum Swaps to Arrange a Binary Grid

from typing import List
from leetcode_tester import LeetCodeTester

class Solution:
    def minSwaps(self, grid: List[List[int]]) -> int:
        n = len(grid)
        mostRight = [0] * n
        for i in range(n):
            j = n - 1
            while grid[i][j] != 1 and j > 0:
                j -= 1
            mostRight[i] = j

        sorted_mostRight = sorted(mostRight)
        for row_idx, idx_1 in enumerate(sorted_mostRight):
            if idx_1 > row_idx:
                return -1

        count = 0
        for i in range(n):
            j = i
            while j < n and mostRight[j] > i:
                j += 1
            # count += j - i
            while j > i:
                mostRight[j-1], mostRight[j] = mostRight[j], mostRight[j-1]
                count += 1
                j -= 1


        return count

tester = LeetCodeTester(Solution)
tester.add_test([[1,0,0,0,0,0],[0,1,0,1,0,0],[1,0,0,0,0,0],[1,1,1,0,0,0],[1,1,0,1,0,0],[1,0,0,0,0,0]], expected=2)
tester.add_test([[1,0,0,0,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0],[0,0,0,0,0,1]], expected=4)
tester.add_test([[1,0,0],[1,1,0],[1,1,1]], expected=0)
tester.add_test([[0,0],[0,1]], expected=0)
tester.run(timeout_ms=100)