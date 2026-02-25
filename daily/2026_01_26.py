from typing import List
from leetcode_tester import LeetCodeTester

class Solution:
    def minRemoval(self, nums: List[int], k: int) -> int:
        nums.sort()  # O(n log n)
        n = len(nums)
        max_len = 1
        j = 0

        for i in range(n):
            j = max(j, i)
            while j < n and nums[j] <= k * nums[i]:
                j += 1

            max_len = max(max_len, j - i)

        return n - max_len

tester = LeetCodeTester(Solution)
tester.add_test([2,1,5], 2, expected=1)
tester.add_test([1,6,2,9], 3, expected=2)
tester.add_test([4,6], 2, expected=0)
tester.add_test([1,12], 2, expected=1)
tester.add_test([8], 1, expected=0)
tester.add_test([33,6,19], 1, expected=2)
tester.run()