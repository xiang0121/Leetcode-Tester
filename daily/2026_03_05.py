"""
    1758. Minimum Changes To Make Alternating Binary String
    Easy

    You are given a string s consisting only of the characters '0' and '1'. In one operation, you can change any '0' to '1' or vice versa.

    The string is called alternating if no two adjacent characters are equal. For example, the string "010" is alternating, while the string "0100" is not.

    Return the minimum number of operations needed to make s alternating.
"""


from leetcode_tester import LeetCodeTester

class Solution:
    def minOperations(self, s: str) -> int:
        n = len(s)
        if n % 2 == 0:
            case_10 = "10" * (n // 2)
        else:
            case_10 = "10" * (n // 2) + "1"

        case_10_count = 0
        for i , c in enumerate(s):
            if c != case_10[i]:
                case_10_count += 1

        return min(case_10_count, n - case_10_count)



tester = LeetCodeTester(Solution)
tester.add_test("0010", expected=1)
tester.add_test("10", expected=0)
tester.run()