from leetcode_tester import LeetCodeTester

class Solution:
    def hasAllCodes(self, s: str, k: int) -> bool:
        if len(s) - k + 1 < 2 ** k:
            return False

        substring = []
        for i in range(2 ** k):
            b = bin(i)[2:]
            substring.append('0'* (k - len(b)) + b)

        for subs in substring:
            if not subs in s:
                return False
        return True


tester = LeetCodeTester(Solution)
tester.add_test("00110110", 2, expected=True)
tester.add_test("0110", 1, expected=True)
tester.add_test("0110", 2, expected=False)
tester.add_test("0", 1, expected=False)
tester.run()