from typing import List

class Solution:
    def minimumPairRemoval(self, nums: List[int]) -> int:
        ans = 0
        def isSorted(nums):
            return all(nums[i] <= nums[i+1] for i in range(len(nums) - 1))

        while not isSorted(nums):
            sums = [nums[i] + nums[i+1] for i in range(len(nums) - 1)]
            min_sum = min(sums)
            min_idx = sums.index(min_sum)
            nums[min_idx] = sums[min_idx]
            del nums[min_idx + 1]
            ans += 1
        return ans