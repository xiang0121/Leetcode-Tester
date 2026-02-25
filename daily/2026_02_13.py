from leetcode_tester import LeetCodeTester

class Solution:
    def longestBalanced(self, s: str) -> int:
        n = len(s)
        def single(s):
            ans = 1
            count = 1
            for i in range(1, n):
                if s[i] == s[i-1]:
                    count += 1
                else:
                    count = 1
                ans = max(ans, count)
            return ans

        def double(s: str, char_a: str, char_b: str):
            third = next(c for c in 'abc' if c not in (char_a, char_b))
            ans = 0
            for segment in s.split(third):
                if not segment:
                    continue
                m = len(segment)
                prefix_a = [0] * m
                prefix_b = [0] * m
                if segment[0] == char_a:
                    prefix_a[0] = 1
                elif segment[0] == char_b:
                    prefix_b[0] = 1
                for i in range(1, m):
                    if segment[i] == char_a:
                        prefix_a[i] = prefix_a[i-1] + 1
                        prefix_b[i] = prefix_b[i-1]
                    else:
                        prefix_a[i] = prefix_a[i-1]
                        prefix_b[i] = prefix_b[i-1] + 1
                hmap = {0: -1}
                for j in range(m):
                    diff = prefix_a[j] - prefix_b[j]
                    if diff in hmap:
                        ans = max(ans, j - hmap[diff])
                    else:
                        hmap[diff] = j
            return ans

        def triple(s):
            ans = 0
            hmap = {(0, 0): -1}  # diff (0,0) at position -1 for substring starting at 0
            prefix_a = [0] * n
            prefix_b = [0] * n
            prefix_c = [0] * n
            if s[0] == 'a':
                prefix_a[0] = 1
            elif s[0] == 'b':
                prefix_b[0] = 1
            else:
                prefix_c[0] = 1
            for i in range(1, n):
                if s[i] == 'a':
                    prefix_a[i] = prefix_a[i-1] + 1
                    prefix_b[i] = prefix_b[i-1]
                    prefix_c[i] = prefix_c[i-1]
                elif s[i] == 'b':
                    prefix_a[i] = prefix_a[i-1]
                    prefix_b[i] = prefix_b[i-1] + 1
                    prefix_c[i] = prefix_c[i-1]
                else:
                    prefix_a[i] = prefix_a[i-1]
                    prefix_b[i] = prefix_b[i-1]
                    prefix_c[i] = prefix_c[i-1] + 1
            for j in range(n):
                diff = (prefix_a[j] - prefix_b[j], prefix_b[j] - prefix_c[j])
                if diff in hmap:
                    ans = max(ans, j - hmap[diff])
                else:
                    hmap[diff] = j
            return ans
        ans = max(
            single(s),
            double(s, 'a', 'b'),
            double(s, 'b', 'c'),
            double(s, 'a', 'c'),
            triple(s),
        )
        return ans

tester = LeetCodeTester(Solution)
tester.add_test("abbac", expected=4)
tester.add_test("aabcc", expected=3)
tester.add_test("aba", expected=2)
tester.add_test("aaabbaaa", expected=4)
tester.add_test("aaaaaa", expected=6)
tester.add_test("ab", expected=2)
tester.add_test("aa", expected=2)
tester.add_test("abc", expected=3)
tester.run()