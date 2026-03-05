from typing import List
from leetcode_tester import LeetCodeTester

class Solution:
    def numSpecial(self, mat: List[List[int]]) -> int:
        m = len(mat)
        n = len(mat[0])
        ans = 0
        row_sum = [sum(row) for row in mat]
        col_sum = [0] * n
        for j in range(n):
            for i in range(m):
                col_sum[j] += mat[i][j]

        for i in range(m):
            for j in range(n):
                if mat[i][j] == 1 and row_sum[i] == 1 and col_sum[j] == 1:
                    ans += 1
        return ans

tester = LeetCodeTester(Solution)
tester.add_test([[1,0,0],[0,0,1],[1,0,0]], expected=1)
tester.add_test([[1,0,0],[0,1,0],[0,0,1]], expected=3)
tester.add_test([[0,0,0,0,0,1,0,0],[0,0,0,0,1,0,0,1],[0,0,0,0,1,0,0,0],[1,0,0,0,1,0,0,0],[0,0,1,1,0,0,0,0]], expected=1)
tester.run()