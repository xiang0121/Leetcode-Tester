"""
You are given a 2D integer array squares. Each squares[i] = [xi, yi, li] represents the coordinates of the bottom-left point and the side length of a square parallel to the x-axis.

Find the minimum y-coordinate value of a horizontal line such that the total area covered by squares above the line equals the total area covered by squares below the line.

Answers within 1e-5 of the actual answer will be accepted.

Note: Squares may overlap. Overlapping areas should be counted only once in this version.
"""


from leetcode_tester import LeetCodeTester
from typing import List

class Solution:
    def separateSquares(self, squares: list[list[int]]) -> float:
        # Step 1: X-coordinate Discretization
        # Since X coordinates can be large, we map them to discrete indices [0, 1, 2...]
        x_coords = set()
        for x, y, l in squares:
            x_coords.add(x)
            x_coords.add(x + l)
        sorted_x = sorted(list(x_coords))
        x_map = {val: i for i, val in enumerate(sorted_x)}
        num_x = len(sorted_x)
        
        # Step 2: Create Scanline Events
        # An event consists of (y_coordinate, type, x_start, x_end)
        # type 1: bottom edge (entering), type -1: top edge (leaving)
        events = []
        for x, y, l in squares:
            events.append((y, 1, x, x + l))
            events.append((y + l, -1, x, x + l))
        # Sort events by Y-coordinate to process from bottom to top
        events.sort()

        # Step 3: Segment Tree Implementation
        # tree_len: stores the total union length covered in this node's range
        # tree_cnt: tracks how many squares fully cover this node's range
        tree_len = [0] * (4 * num_x)
        tree_cnt = [0] * (4 * num_x)

        def update(v, tl, tr, l, r, add):
            """
            v: current node index
            tl, tr: boundaries of the current node in discrete X-indices
            l, r: target range to update
            add: 1 for adding a square, -1 for removing
            """
            if l <= tl and tr <= r:
                tree_cnt[v] += add
            else:
                tm = (tl + tr) // 2
                if l < tm:
                    update(2 * v, tl, tm, l, r, add)
                if r > tm:
                    update(2 * v + 1, tm, tr, l, r, add)
            
            # Post-order logic to calculate tree_len[v]
            if tree_cnt[v] > 0:
                # If fully covered, the length is the actual X-distance of this range
                tree_len[v] = sorted_x[tr] - sorted_x[tl]
            else:
                # Otherwise, it's the sum of covered lengths of its children
                if tr - tl > 1:
                    tree_len[v] = tree_len[2 * v] + tree_len[2 * v + 1]
                else:
                    # Leaf node with no coverage
                    tree_len[v] = 0

        # Step 4: First Pass - Calculate Total Union Area
        total_area = 0
        prev_y = events[0][0]
        for i in range(len(events)):
            curr_y, etype, x1, x2 = events[i]
            # Area = current_width * height_difference
            # tree_len[1] represents the total union width on the X-axis
            total_area += tree_len[1] * (curr_y - prev_y)
            update(1, 0, num_x - 1, x_map[x1], x_map[x2], etype)
            prev_y = curr_y

        # Step 5: Second Pass - Locate the Median Line
        # Reset Segment Tree for the second pass
        tree_len = [0] * (4 * num_x)
        tree_cnt = [0] * (4 * num_x)
        target = total_area / 2
        current_area = 0
        prev_y = events[0][0]
        
        for i in range(len(events)):
            curr_y, etype, x1, x2 = events[i]
            area_step = tree_len[1] * (curr_y - prev_y)
            
            # Check if the target area falls within the current vertical strip
            if current_area + area_step >= target:
                needed_area = target - current_area
                # If width is 0, we avoid division (though theoretically area_step would be 0)
                if tree_len[1] > 0:
                    return prev_y + (needed_area / tree_len[1])
            
            current_area += area_step
            update(1, 0, num_x - 1, x_map[x1], x_map[x2], etype)
            prev_y = curr_y
            
        return float(events[-1][0]) # Fallback return

tester = LeetCodeTester(Solution)
tester.add_test([[0,0,1],[2,2,1]], expected=1.0)
tester.add_test([[0,0,2],[1,1,1]], expected=1.1667)
tester.add_test([[0,0,3],[1,1,1],[2,2,1]], expected=1.625)
tester.add_test([[0,0,4],[1,1,1],[2,2,1],[3,3,1]], expected=2.1)
tester.add_test([[0,0,5],[1,1,1],[2,2,1],[3,3,1],[4,4,1]], expected=2.5833)
tester.run(timeout_ms=1000)