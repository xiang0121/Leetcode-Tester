import heapq
class Solution:
    def minCost(self, n: int, edges: List[List[int]]) -> int:
        e = len(edges)
        ans = 0
        adj = [[] for _ in range(n)] 
        dist = [0] + [float('inf')] * (n-1)

        for i in range(e):
            u, v, w  = edges[i]
            edges.append([v, u, w * 2])
        
        for u, v, w in edges:
            adj[u].append((v, w))

        q = [(0, 0)]
        while q != []:
            d, u = heapq.heappop(q)
            if d > dist[u]:
                continue
            for v, w in adj[u]:
                if dist[v] > dist[u] + w:
                    dist[v] = dist[u] + w
                    heapq.heappush(q, (dist[v], v))
        return -1 if dist[-1] == float('inf') else dist[-1]