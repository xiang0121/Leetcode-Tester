from typing import List

class Solution:
    def sumFourDivisors(self, nums: List[int]) -> int:
        ans = 0
        for num in nums:
            div = set()
            for j in range(1, int(num ** 0.5)+1):
                if num % j == 0:
                    div.add(j)
                    div.add(num // j)
            if len(div) == 4:
                ans = ans + sum(div)
        return ans