from math import exp
from leetcode_tester import LeetCodeTester
from typing import List

class Solution:
    def minTimeToVisitAllPoints(self, points: List[List[int]]) -> int:
        dist = 0
        n = len(points)
        for i in range(n-1):
            w = abs(points[i][0] - points[i+1][0])
            h = abs(points[i][1] - points[i+1][1])
            dist += min(h, w) + abs(w - h)
        return dist

tester = LeetCodeTester(Solution)
tester.add_test([[1,1],[3,4],[-1,0]], expected=7)
tester.add_test([[3,2],[-2,2]], expected=5)
tester.run()