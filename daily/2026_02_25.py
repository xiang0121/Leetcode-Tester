# 1356. Sort Integers by The Number of 1 Bits

from typing import List

class Solution:
    def sortByBits(self, arr: List[int]) -> List[int]:
        arr.sort()
        bits_map = list()
        ans = []
        for num in arr:
            bits_map.append((num, bin(num).count('1')))
        bits_map = sorted(bits_map, key=lambda x : x[1])
        for k, v in bits_map:
            ans.append(k)

        # Times: O(nlogn)
        return ans