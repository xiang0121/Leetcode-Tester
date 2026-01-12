from leetcode_tester import LeetCodeTester
from typing import List

class Solution:

    def maxDotProduct(self, nums1: List[int], nums2: List[int]) -> int:
        n = len(nums1)
        m = len(nums2)
        dp = [[-float('inf')] * (m+1) for _ in range(n+1)]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                product = nums1[i-1] * nums2[j-1]
                dp[i][j] = max(
                    dp[i-1][j],
                    dp[i][j-1],
                    max(dp[i-1][j-1], 0) + product
            )

        return dp[n][m]



tester = LeetCodeTester(Solution)
tester.add_test([2, 1, -2, 5], [3, 0, -6], expected=18)
tester.add_test([3, -2], [2, -6, 7], expected=21)
tester.add_test([-1, -1], [1, 1], expected=-1)
tester.add_test([5, -4, -3], [-4, -3, 0, -4, 2], expected=28)
tester.add_test([13,-7,12,-15,-7,8,3,-7,-5,13,-15,-8,5,7,-1,3,-11,-12,2,-12], [-1,13,-4,-2,-13,2,-4,6,-9,13,-8,-3,-9], expected=972)
tester.run(timeout_ms=1000)