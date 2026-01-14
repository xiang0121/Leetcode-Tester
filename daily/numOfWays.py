"""
# 1411. Number of Ways to Paint N × 3 Grid

Hard

You have a grid of size n x 3 and you want to paint each cell of the grid with exactly one of the three colors: Red, Yellow, or Green while making sure that no two adjacent cells have the same color (i.e., no two cells that share vertical or horizontal sides have the same color).

Given n the number of rows of the grid, return the number of ways you can paint this grid. As the answer may grow large, the answer must be computed modulo 109 + 7.
"""

class Solution:
    def numOfWays(self, n: int) -> int:
        dp = [0] * n
        if n == 1:
            dp[0] = 12
        elif n == 2:
            dp[0] = 12
            dp[1] = 54
        else:
            dp[0] = 12
            dp[1] = 54
            for i in range(2, n):
                dp[i] = dp[i-1] * 5 - dp[i-2] * 2
        return dp[-1] % (10 ** 9 + 7)