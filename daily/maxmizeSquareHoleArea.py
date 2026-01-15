"""
2943. Maximize Area of Square Hole in Grid
Medium

Hint
You are given the two integers, n and m and two integer arrays, hBars and vBars. The grid has n + 2 horizontal and m + 2 vertical bars, creating 1 x 1 unit cells. The bars are indexed starting from 1.

You can remove some of the bars in hBars from horizontal bars and some of the bars in vBars from vertical bars. Note that other bars are fixed and cannot be removed.

Return an integer denoting the maximum area of a square-shaped hole in the grid, after removing some bars (possibly none).
"""

from typing import List
from leetcode_tester import LeetCodeTester

class Solution:
    def maximizeSquareHoleArea(self, n: int, m: int, hBars: List[int], vBars: List[int]) -> int:
        hBars.sort()
        vBars.sort()

        def maxConsecutive(Bars):
            max_consec = 0
            consec = 0
            for i in range(len(Bars)-1):
                if Bars[i+1] - Bars[i] == 1:
                    consec += 1
                else:
                    consec = 0
                max_consec = max(consec, max_consec)
            return max_consec

        max_length = min(maxConsecutive(hBars)+2, maxConsecutive(vBars)+2)

        return max_length * max_length


tester = LeetCodeTester(Solution)
tester.add_test(2, 1, [2,3], [2], expected=4)
tester.add_test(1, 1, [2], [2], expected=4)
tester.add_test(2, 3, [2,3], [2,4], expected=4)
tester.add_test(4, 40, [5,3,2,4], [36,41,6,34,33], expected=9)
tester.add_test(4, 4, [5,3,2,4], [2,3,4,5], expected=25)
tester.run()