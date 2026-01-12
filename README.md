# Leetcode-Tester
A simple framework to test LeetCode solutions locally.

## Usage
  1. Define your Solution class with the required method
  2. Create test cases using TestCase objects
  3. Run the tester

## Example
```python
from leetcode_tester import LeetCodeTester

class Solution:
    def twoSum(self, nums, target):
        # your solution here
        pass

tester = LeetCodeTester(Solution)
tester.add_test([2, 7, 11, 15], 9, expected=[0, 1])
tester.run()
```
