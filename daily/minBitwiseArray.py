"""
3314. Construct the Minimum Bitwise Array I

You are given an array nums consisting of n prime integers.

You need to construct an array ans of length n, such that, for each index i, the bitwise OR of ans[i] and ans[i] + 1 is equal to nums[i], i.e. ans[i] OR (ans[i] + 1) == nums[i].

Additionally, you must minimize each value of ans[i] in the resulting array.

If it is not possible to find such a value for ans[i] that satisfies the condition, then set ans[i] = -1.
"""

from typing import List
from leetcode_tester import LeetCodeTester

class Solution:
    def minBitwiseArray(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [-1] * n
        for i in range(n):
            tmp = 0
            while tmp < nums[i]:
                if (tmp | tmp + 1) == nums[i]:
                    ans[i] = tmp
                    break
                tmp += 1
        return ans

# Optimized solution
class Solution:
    def minBitwiseArray(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [-1] * n
        for i in range(n):
            if nums[i] == 2:
                ans[i] = -1
            else:
                tmp = 1
                num = nums[i]
                while num | 1 == num:
                    tmp <<= 1
                    num >>= 1
                tmp >>= 1
                ans[i] = nums[i] & ~tmp
        return ans


tester = LeetCodeTester(Solution)
tester.add_test([2,3,5,7], expected=[-1,1,4,3])
tester.add_test([11,13,31], expected=[9,12,15])
tester.run()