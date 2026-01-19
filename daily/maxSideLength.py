class Solution:
    def maxSideLength(self, mat: List[List[int]], threshold: int) -> int:
        n, m = len(mat), len(mat[0])
        length = min(n, m)
        ans = 0
        prefix = [[0] * (m+1) for _ in range(n+1)]
        for i in range(1, n+1):
            for j in range(1, m+1):
                prefix[i][j] = mat[i-1][j-1] + prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1]
        # print(prefix)
        for i in range(1, n+1):
            for j in range(1, m+1):
                max_len = ans + 1
                if i >= max_len and j >= max_len:
                    grid_sum = prefix[i][j] - prefix[i - max_len][j] - prefix[i][j - max_len] + prefix[i - max_len][j - max_len]
                    if grid_sum <= threshold:
                        ans += 1

        return ans