from typing import List

class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        number = 0
        n = len(digits)
        for i in range(n):
            number += (10 ** i) * digits[n-i-1]
        number += 1
        return list(map(int, str(number)))