#!/usr/bin/env python3
"""
LeetCode Local Tester
=====================
A simple framework to test LeetCode solutions locally.

Usage:
    1. Define your Solution class with the required method
    2. Create test cases using TestCase objects
    3. Run the tester

Example:
    class Solution:
        def twoSum(self, nums, target):
            # your solution here
            pass

    tester = LeetCodeTester(Solution)
    tester.add_test([2, 7, 11, 15], 9, expected=[0, 1])
    tester.run()
"""

import time
import traceback
import signal
from typing import Any, List, Optional
from collections import deque
import copy


# ============================================================================
# Timeout Handling
# ============================================================================

class TimeoutException(Exception):
    """Raised when a test exceeds the time limit."""
    pass


def _timeout_handler(signum, frame):
    """Signal handler for timeout."""
    raise TimeoutException("Time Limit Exceeded")


def _run_with_timeout_process(func, args, queue):
    """Helper function to run in separate process."""
    try:
        result = func(*args)
        queue.put(('success', result))
    except Exception as e:
        queue.put(('error', f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"))


# ============================================================================
# Common LeetCode Data Structures
# ============================================================================

class ListNode:
    """Singly-linked list node used in many LeetCode problems."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"

    @staticmethod
    def from_list(arr: List[int]) -> Optional['ListNode']:
        """Create a linked list from a Python list."""
        if not arr:
            return None
        head = ListNode(arr[0])
        current = head
        for val in arr[1:]:
            current.next = ListNode(val)
            current = current.next
        return head

    @staticmethod
    def to_list(head: Optional['ListNode']) -> List[int]:
        """Convert a linked list to a Python list."""
        result = []
        while head:
            result.append(head.val)
            head = head.next
        return result


class TreeNode:
    """Binary tree node used in many LeetCode problems."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"

    @staticmethod
    def from_list(arr: List[Optional[int]]) -> Optional['TreeNode']:
        """Create a binary tree from LeetCode's level-order list format."""
        if not arr or arr[0] is None:
            return None

        root = TreeNode(arr[0])
        queue = deque([root])
        i = 1

        while queue and i < len(arr):
            node = queue.popleft()

            # Left child
            if i < len(arr):
                if arr[i] is not None:
                    node.left = TreeNode(arr[i])
                    queue.append(node.left)
                i += 1

            # Right child
            if i < len(arr):
                if arr[i] is not None:
                    node.right = TreeNode(arr[i])
                    queue.append(node.right)
                i += 1

        return root

    @staticmethod
    def to_list(root: Optional['TreeNode']) -> List[Optional[int]]:
        """Convert a binary tree to LeetCode's level-order list format."""
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            node = queue.popleft()
            if node:
                result.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append(None)

        # Remove trailing Nones
        while result and result[-1] is None:
            result.pop()

        return result


class Node:
    """N-ary tree node / Graph node with neighbors."""
    def __init__(self, val=None, children=None, neighbors=None):
        self.val = val
        self.children = children if children else []
        self.neighbors = neighbors if neighbors else []

    def __repr__(self):
        return f"Node({self.val})"


# ============================================================================
# Test Case and Tester Classes
# ============================================================================

class TestCase:
    """Represents a single test case."""
    def __init__(self, *args, expected=None, description=""):
        self.args = args
        self.expected = expected
        self.description = description


class TestResult:
    """Stores the result of a single test."""
    def __init__(self, test_num: int, passed: bool, expected: Any, actual: Any,
                 time_ms: float, error: str = None, tle: bool = False):
        self.test_num = test_num
        self.passed = passed
        self.expected = expected
        self.actual = actual
        self.time_ms = time_ms
        self.error = error
        self.tle = tle  # Time Limit Exceeded flag


class LeetCodeTester:
    """Main tester class for running LeetCode solutions."""

    def __init__(self, solution_class: type, method_name: str = None):
        """
        Initialize the tester.

        Args:
            solution_class: Your Solution class
            method_name: Name of the method to test. If None, will auto-detect
                        the first non-dunder method.
        """
        self.solution_class = solution_class
        self.method_name = method_name or self._detect_method()
        self.test_cases: List[TestCase] = []
        self.results: List[TestResult] = []

    def _detect_method(self) -> str:
        """Auto-detect the solution method name."""
        for name in dir(self.solution_class):
            if not name.startswith('_'):
                attr = getattr(self.solution_class, name)
                if callable(attr):
                    return name
        raise ValueError("Could not auto-detect solution method")

    def add_test(self, *args, expected=None, description=""):
        """Add a test case."""
        self.test_cases.append(TestCase(*args, expected=expected, description=description))
        return self  # Allow chaining

    def add_tests(self, test_cases: List[tuple]):
        """
        Add multiple test cases at once.
        Each tuple should be (args_tuple, expected) or ((arg1, arg2, ...), expected)
        """
        for tc in test_cases:
            if len(tc) == 2:
                args, expected = tc
                if not isinstance(args, tuple):
                    args = (args,)
                self.add_test(*args, expected=expected)
            else:
                raise ValueError("Each test case should be (args, expected)")
        return self

    def _compare_results(self, expected: Any, actual: Any) -> bool:
        """Compare expected and actual results, handling special cases."""
        # Handle ListNode comparison
        if isinstance(expected, ListNode) or isinstance(actual, ListNode):
            exp_list = ListNode.to_list(expected) if isinstance(expected, ListNode) else expected
            act_list = ListNode.to_list(actual) if isinstance(actual, ListNode) else actual
            return exp_list == act_list

        # Handle TreeNode comparison
        if isinstance(expected, TreeNode) or isinstance(actual, TreeNode):
            exp_list = TreeNode.to_list(expected) if isinstance(expected, TreeNode) else expected
            act_list = TreeNode.to_list(actual) if isinstance(actual, TreeNode) else actual
            return exp_list == act_list

        # Handle list comparison (order might matter or not)
        if isinstance(expected, list) and isinstance(actual, list):
            return expected == actual

        # Handle set comparison
        if isinstance(expected, set) and isinstance(actual, set):
            return expected == actual

        # Handle float comparison with tolerance
        if isinstance(expected, float) and isinstance(actual, float):
            return abs(expected - actual) < 1e-6

        # Default comparison
        return expected == actual

    def _format_value(self, val: Any) -> str:
        """Format a value for display."""
        if isinstance(val, ListNode):
            return f"ListNode{ListNode.to_list(val)}"
        if isinstance(val, TreeNode):
            return f"TreeNode{TreeNode.to_list(val)}"
        if isinstance(val, str):
            return f'"{val}"'
        return str(val)

    def _deep_copy_args(self, args: tuple) -> tuple:
        """Deep copy arguments to prevent mutation."""
        copied = []
        for arg in args:
            if isinstance(arg, ListNode):
                copied.append(ListNode.from_list(ListNode.to_list(arg)))
            elif isinstance(arg, TreeNode):
                copied.append(TreeNode.from_list(TreeNode.to_list(arg)))
            else:
                try:
                    copied.append(copy.deepcopy(arg))
                except Exception:
                    copied.append(arg)
        return tuple(copied)

    def run(self, verbose: bool = True, stop_on_fail: bool = False,
            timeout_ms: float = None) -> bool:
        """
        Run all test cases.

        Args:
            verbose: Print detailed output
            stop_on_fail: Stop running tests after first failure
            timeout_ms: Time limit in milliseconds. If exceeded, test fails with TLE.
                       Common values: 1000 (1s), 2000 (2s), 5000 (5s)
                       Set to None to disable timeout checking.

        Returns:
            True if all tests passed, False otherwise
        """
        self.results = []
        solution = self.solution_class()
        method = getattr(solution, self.method_name)
        timeout_sec = timeout_ms / 1000.0 if timeout_ms else None

        if verbose:
            print(f"\n{'='*60}")
            print(f"Testing: {self.solution_class.__name__}.{self.method_name}()")
            if timeout_ms:
                print(f"Time Limit: {timeout_ms}ms")
            print(f"{'='*60}\n")

        all_passed = True

        for i, tc in enumerate(self.test_cases, 1):
            # Deep copy args to prevent mutation affecting later tests
            args = self._deep_copy_args(tc.args)

            # Run the test
            error = None
            actual = None
            tle = False
            start_time = time.perf_counter()

            try:
                if timeout_sec:
                    # Use signal-based timeout (Unix only, but more accurate)
                    old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
                    signal.setitimer(signal.ITIMER_REAL, timeout_sec)
                    try:
                        actual = method(*args)
                    finally:
                        signal.setitimer(signal.ITIMER_REAL, 0)
                        signal.signal(signal.SIGALRM, old_handler)
                else:
                    actual = method(*args)
            except TimeoutException:
                tle = True
                error = f"⏱ Time Limit Exceeded (>{timeout_ms}ms)"
            except Exception as e:
                error = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"

            elapsed_ms = (time.perf_counter() - start_time) * 1000

            # Check result
            if error or tle:
                passed = False
            elif tc.expected is None:
                passed = True  # No expected value to compare
            else:
                passed = self._compare_results(tc.expected, actual)

            result = TestResult(i, passed, tc.expected, actual, elapsed_ms, error, tle)
            self.results.append(result)

            if not passed:
                all_passed = False

            # Print result
            if verbose:
                if tle:
                    status = "⏱ TLE"
                    status_color = "\033[93m"  # Yellow for TLE
                elif passed:
                    status = "✓ PASS"
                    status_color = "\033[92m"  # Green
                else:
                    status = "✗ FAIL"
                    status_color = "\033[91m"  # Red
                reset_color = "\033[0m"

                time_warning = ""
                if timeout_ms and elapsed_ms > timeout_ms * 0.8 and not tle:
                    time_warning = " ⚠️ close to limit"

                print(f"Test {i}: {status_color}{status}{reset_color} ({elapsed_ms:.3f}ms{time_warning})")

                if tc.description:
                    print(f"  Description: {tc.description}")

                # Show input (truncated for large inputs)
                args_str = ", ".join(self._format_value(a) for a in tc.args)
                if len(args_str) > 200:
                    args_str = args_str[:200] + "..."
                print(f"  Input: {args_str}")

                if not passed:
                    if error:
                        print(f"  Error: {error}")
                    else:
                        print(f"  Expected: {self._format_value(tc.expected)}")
                        print(f"  Actual:   {self._format_value(actual)}")

                print()

            if stop_on_fail and not passed:
                break

        # Print summary
        if verbose:
            passed_count = sum(1 for r in self.results if r.passed)
            tle_count = sum(1 for r in self.results if r.tle)
            total_count = len(self.results)
            total_time = sum(r.time_ms for r in self.results)

            print(f"{'='*60}")
            status_color = "\033[92m" if all_passed else "\033[91m"
            reset_color = "\033[0m"
            result_str = f"{passed_count}/{total_count} passed"
            if tle_count > 0:
                result_str += f" ({tle_count} TLE)"
            print(f"Results: {status_color}{result_str}{reset_color}")
            print(f"Total time: {total_time:.3f}ms")
            print(f"{'='*60}\n")

        return all_passed


# ============================================================================
# Convenience Functions
# ============================================================================

def test_solution(solution_class: type, test_cases: List[tuple],
                  method_name: str = None, **kwargs) -> bool:
    """
    Convenience function to quickly test a solution.

    Args:
        solution_class: Your Solution class
        test_cases: List of (args, expected) tuples
        method_name: Optional method name to test
        **kwargs: Additional arguments passed to run()

    Example:
        test_solution(Solution, [
            (([2, 7, 11, 15], 9), [0, 1]),
            (([3, 2, 4], 6), [1, 2]),
        ])
    """
    tester = LeetCodeTester(solution_class, method_name)
    tester.add_tests(test_cases)
    return tester.run(**kwargs)


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    # Example 1: Two Sum
    print("Example 1: Two Sum")
    print("-" * 40)

    class Solution:
        def twoSum(self, nums: List[int], target: int) -> List[int]:
            seen = {}
            for i, num in enumerate(nums):
                complement = target - num
                if complement in seen:
                    return [seen[complement], i]
                seen[num] = i
            return []

    tester = LeetCodeTester(Solution)
    tester.add_test([2, 7, 11, 15], 9, expected=[0, 1], description="Basic case")
    tester.add_test([3, 2, 4], 6, expected=[1, 2], description="Middle elements")
    tester.add_test([3, 3], 6, expected=[0, 1], description="Same elements")
    tester.run()

    # Example 2: Reverse Linked List
    print("\nExample 2: Reverse Linked List")
    print("-" * 40)

    class Solution2:
        def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
            prev = None
            curr = head
            while curr:
                next_node = curr.next
                curr.next = prev
                prev = curr
                curr = next_node
            return prev

    tester2 = LeetCodeTester(Solution2)
    tester2.add_test(
        ListNode.from_list([1, 2, 3, 4, 5]),
        expected=ListNode.from_list([5, 4, 3, 2, 1])
    )
    tester2.add_test(
        ListNode.from_list([1, 2]),
        expected=ListNode.from_list([2, 1])
    )
    tester2.add_test(None, expected=None, description="Empty list")
    tester2.run()

    # Example 3: Maximum Depth of Binary Tree
    print("\nExample 3: Maximum Depth of Binary Tree")
    print("-" * 40)

    class Solution3:
        def maxDepth(self, root: Optional[TreeNode]) -> int:
            if not root:
                return 0
            return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))

    tester3 = LeetCodeTester(Solution3)
    tester3.add_test(TreeNode.from_list([3, 9, 20, None, None, 15, 7]), expected=3)
    tester3.add_test(TreeNode.from_list([1, None, 2]), expected=2)
    tester3.add_test(None, expected=0)
    tester3.run()

    # Example 4: Quick test with convenience function
    print("\nExample 4: Using convenience function")
    print("-" * 40)

    class Solution4:
        def isPalindrome(self, s: str) -> bool:
            cleaned = ''.join(c.lower() for c in s if c.isalnum())
            return cleaned == cleaned[::-1]

    test_solution(Solution4, [
        (("A man, a plan, a canal: Panama",), True),
        (("race a car",), False),
        ((" ",), True),
    ])

    # Example 5: TLE Detection
    print("\nExample 5: TLE Detection (timeout_ms=100)")
    print("-" * 40)

    class Solution5:
        def slowFunction(self, n: int) -> int:
            """Intentionally slow O(n^2) solution."""
            total = 0
            for i in range(n):
                for j in range(n):
                    total += i * j
            return total

    tester5 = LeetCodeTester(Solution5)
    tester5.add_test(100, expected=None, description="Small input - should pass")
    tester5.add_test(1000, expected=None, description="Medium input - might be slow")
    tester5.add_test(10000, expected=None, description="Large input - likely TLE")
    tester5.run(timeout_ms=100)  # 100ms time limit
