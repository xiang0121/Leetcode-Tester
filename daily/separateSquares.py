from leetcode_tester import LeetCodeTester
from typing import List

class Solution:
    def separateSquares(self, squares: List[List[int]]) -> float:
        top = -float('inf')
        bottom = float('inf')
        total_area = 0
        for x, y, l in squares:
            top = max(top, y+l)
            bottom = min(bottom, y)
            total_area += l * l
        line = (top + bottom) / 2

        # binary search
        for _ in range(50):
            half_area = 0
            for x, y, l in squares:
                if y < line:
                    half_area += l * min(float(l), line-y)

            if half_area >= (total_area / 2):
                top = line
            else:
                bottom = line
  
            line = (top + bottom) / 2

        return line

tester = LeetCodeTester(Solution)
tester.add_test([[0,0,1],[2,2,1]], expected=1.0)
tester.add_test([[0,0,2],[1,1,1]], expected=1.1667)
tester.add_test([[0,0,3],[1,1,1],[2,2,1]], expected=1.625)
tester.add_test([[0,0,4],[1,1,1],[2,2,1],[3,3,1]], expected=2.1)
tester.add_test([[0,0,5],[1,1,1],[2,2,1],[3,3,1],[4,4,1]], expected=2.5833)
tester.run(timeout_ms=1000)