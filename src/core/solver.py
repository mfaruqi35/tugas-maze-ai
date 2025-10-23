from collections import deque

# --------------------------------------------------
# Fungsi BFS
# --------------------------------------------------
def bfs_solve(grid, start):
    """
    Menyelesaikan maze menggunakan BFS (jalur terpendek).
    Mengembalikan (path, langkah)
    """
    n, m = len(grid), len(grid[0])
    sr, sc = start
    visited = [[False]*m for _ in range(n)]
    parent = [[None]*m for _ in range(n)]
    q = deque([(sr, sc)])
    visited[sr][sc] = True

    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    while q:
        r, c = q.popleft()
        if (r == 0 or c == 0 or r == n-1 or c == m-1) and grid[r][c] == 0:
            path = reconstruct_path(parent, start, (r, c))
            return path, len(path)

        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 0 and not visited[nr][nc]:
                visited[nr][nc] = True
                parent[nr][nc] = (r, c)
                q.append((nr, nc))

    return [], 0


# --------------------------------------------------
# Fungsi DFS
# --------------------------------------------------
def dfs_solve(grid, start):
    """
    Menyelesaikan maze menggunakan DFS (rekursif).
    Mengembalikan (path, langkah)
    """
    n, m = len(grid), len(grid[0])
    sr, sc = start
    visited = [[False]*m for _ in range(n)]
    best_path = []

    def dfs(r, c, path):
        nonlocal best_path
        if not (0 <= r < n and 0 <= c < m) or grid[r][c] == -1 or visited[r][c]:
            return
        visited[r][c] = True
        path.append((r, c))

        if (r == 0 or c == 0 or r == n-1 or c == m-1) and grid[r][c] == 0:
            if not best_path or len(path) < len(best_path):
                best_path = path.copy()
        else:
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                dfs(r+dr, c+dc, path)

        path.pop()
        visited[r][c] = False

    dfs(sr, sc, [])
    return best_path, len(best_path)


# --------------------------------------------------
# Rekonstruksi jalur (untuk BFS)
# --------------------------------------------------
def reconstruct_path(parent, start, end):
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = parent[cur[0]][cur[1]]
    path.reverse()
    return path
