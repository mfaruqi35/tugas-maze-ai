import pygame
import os
from core.solver import bfs_solve, dfs_solve


# ----------------------------------------------------------
# Fungsi membaca maze
# ----------------------------------------------------------
def load_maze(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    rows, cols = map(int, lines[0].split())
    grid = [list(map(int, line.split())) for line in lines[1:1 + rows]]
    start_r, start_c = map(int, lines[1 + rows].split())
    start = (start_r - 1, start_c - 1)

    # cari cell yang merupakan exit (0 di pinggir)
    exits = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0 and (r == 0 or c == 0 or r == rows - 1 or c == cols - 1):
                exits.append((r, c))
    return grid, rows, cols, start, exits


# ----------------------------------------------------------
# Tombol dasar
# ----------------------------------------------------------
class Button:
    def __init__(self, x, y, w, h, text,
                 bg_color=(240,240,240), hover_color=(200,200,200),
                 active_color=(160,160,160),
                 text_color=(0,0,0), border_color=(0,0,0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.active_color = active_color
        self.text_color = text_color
        self.border_color = border_color
        self.active = False

    def draw(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        if self.active:
            color = self.active_color
        else:
            color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, self.border_color, self.rect, width=2, border_radius=8)
        text_surf = font.render(self.text, True, self.text_color)
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos))


# ----------------------------------------------------------
# Fungsi menggambar maze
# ----------------------------------------------------------
def draw_maze(surface, maze_rect, grid, start, exits, visited=None, path=None):
    rows, cols = len(grid), len(grid[0])
    cell_w, cell_h = maze_rect.width // cols, maze_rect.height // rows
    cell_size = min(cell_w, cell_h)
    offset_x = maze_rect.x + (maze_rect.width - cols * cell_size) // 2
    offset_y = maze_rect.y + (maze_rect.height - rows * cell_size) // 2

    for r in range(rows):
        for c in range(cols):
            val = grid[r][c]
            color = (40, 40, 40) if val == -1 else (230, 230, 230)
            rect = pygame.Rect(offset_x + c * cell_size, offset_y + r * cell_size, cell_size, cell_size)
            pygame.draw.rect(surface, color, rect)

            # sel visited
            if visited and (r, c) in visited:
                pygame.draw.rect(surface, (200, 200, 100), rect)
            # path hasil
            if path and (r, c) in path:
                pygame.draw.rect(surface, (255, 180, 50), rect)

            pygame.draw.rect(surface, (180, 180, 180), rect, 1)

    # start
    sx, sy = start[1], start[0]
    srect = pygame.Rect(offset_x + sx * cell_size, offset_y + sy * cell_size, cell_size, cell_size)
    pygame.draw.rect(surface, (50, 100, 255), srect)

    # exits
    for (er, ec) in exits:
        erect = pygame.Rect(offset_x + ec * cell_size, offset_y + er * cell_size, cell_size, cell_size)
        pygame.draw.rect(surface, (0, 200, 0), erect)


# ----------------------------------------------------------
# Fungsi BFS/DFS yang bisa memberi urutan visited
# ----------------------------------------------------------
def bfs_search_steps(grid, start):
    from collections import deque

    n, m = len(grid), len(grid[0])
    sr, sc = start
    visited = [[False]*m for _ in range(n)]
    parent = [[None]*m for _ in range(n)]
    q = deque([(sr, sc)])
    visited[sr][sc] = True
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    steps = []

    while q:
        r, c = q.popleft()
        steps.append((r, c))

        # kalau sampai di pinggir dan cell 0 -> goal ditemukan
        if (r == 0 or c == 0 or r == n-1 or c == m-1) and grid[r][c] == 0:
            # bangun path aman
            path = []
            cur = (r, c)
            while cur is not None:
                path.append(cur)
                pr = parent[cur[0]][cur[1]]
                if pr is None:
                    break
                cur = pr
            path.reverse()
            return steps, path

        # lanjut eksplorasi tetangga
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 0 and not visited[nr][nc]:
                visited[nr][nc] = True
                parent[nr][nc] = (r, c)
                q.append((nr, nc))

    # kalau tidak ada jalan keluar
    return steps, []

# ----------------------------------------------------------
# Fungsi DFS yang memberi urutan visited (untuk animasi)
# ----------------------------------------------------------
def dfs_search_steps(grid, start):
    n, m = len(grid), len(grid[0])
    sr, sc = start
    visited = [[False]*m for _ in range(n)]
    parent = [[None]*m for _ in range(n)]
    steps = []
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    path = []
    found = [False]  # list agar bisa diubah di dalam nested function

    def dfs(r, c):
        if not (0 <= r < n and 0 <= c < m):
            return
        if grid[r][c] == -1 or visited[r][c] or found[0]:
            return

        visited[r][c] = True
        steps.append((r, c))

        # cek goal (0 di pinggir)
        if (r == 0 or c == 0 or r == n-1 or c == m-1) and grid[r][c] == 0:
            found[0] = True
            # bangun path
            cur = (r, c)
            while cur is not None:
                path.append(cur)
                cur = parent[cur[0]][cur[1]]
            path.reverse()
            return

        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and not visited[nr][nc] and grid[nr][nc] == 0:
                parent[nr][nc] = (r, c)
                dfs(nr, nc)

    dfs(sr, sc)
    return steps, path


# ----------------------------------------------------------
# Fungsi utama: draw()
# ----------------------------------------------------------
def draw(screen, events, data):
    pygame.font.init()
    font = pygame.font.SysFont("Arial", int(screen.get_height() * 0.02) + 20, bold=True)
    WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
    MARGIN, PANEL_GAP, INNER_PADDING = int(WINDOW_WIDTH * 0.03), int(WINDOW_WIDTH * 0.015), int(WINDOW_WIDTH * 0.005)

    # layout
    frame_rect = pygame.Rect(MARGIN, MARGIN, WINDOW_WIDTH - 2*MARGIN, WINDOW_HEIGHT - 2*MARGIN)
    left_width = int(frame_rect.width * 0.3)
    right_width = frame_rect.width - left_width - PANEL_GAP
    left_panel = pygame.Rect(frame_rect.x, frame_rect.y, left_width, frame_rect.height)
    right_panel = pygame.Rect(left_panel.right + PANEL_GAP, frame_rect.y, right_width, frame_rect.height)

    # panel background
    pygame.draw.rect(screen, (100, 100, 100), left_panel)
    pygame.draw.rect(screen, (0, 0, 0), right_panel)

    # tombol
    btn_size = int(WINDOW_WIDTH * 0.05)
    back_button = Button(left_panel.x + INNER_PADDING, left_panel.y + INNER_PADDING, btn_size, btn_size, "<")
    algo_w = left_panel.width - 2*INNER_PADDING
    algo_h = int(WINDOW_HEIGHT * 0.08)
    bfs_button = Button(left_panel.x + INNER_PADDING, back_button.rect.bottom + 40, algo_w, algo_h, "BFS")
    dfs_button = Button(left_panel.x + INNER_PADDING, bfs_button.rect.bottom + 20, algo_w, algo_h, "DFS")

    algo_mode = data.get("algo", "BFS")
    bfs_button.active = (algo_mode == "BFS")
    dfs_button.active = (algo_mode == "DFS")

    maze_container = pygame.Rect(
        right_panel.x + INNER_PADDING,
        right_panel.y + INNER_PADDING,
        right_panel.width - 2 * INNER_PADDING,
        int(right_panel.height * 0.85)
    )
    button_container = pygame.Rect(
        right_panel.x + INNER_PADDING,
        maze_container.bottom + INNER_PADDING,
        right_panel.width - 2 * INNER_PADDING,
        right_panel.bottom - maze_container.bottom - INNER_PADDING
    )

    btn_w = int(button_container.width * 0.15)
    btn_h = int(button_container.height * 0.6)
    btn_margin = int(button_container.width * 0.02)
    x_start = button_container.x + btn_margin
    y_center = button_container.centery - btn_h // 2
    auto_btn = Button(x_start, y_center, btn_w, btn_h, "AUTO")

    # gambar tombol
    for btn in [back_button, bfs_button, dfs_button, auto_btn]:
        btn.draw(screen, font)

    # muat maze
    maze_file = data.get("maze_file", "./mazes/maze_2.txt")
    grid, rows, cols, start, exits = load_maze(maze_file)

    # ambil state
    animating = data.get("animating", False)
    visited = data.get("visited", [])
    path = data.get("path", [])

    draw_maze(screen, maze_container, grid, start, exits, visited, path)

    # handle event
    for e in events:
        if back_button.is_clicked(e):
            return "select_maze", None
        if bfs_button.is_clicked(e):
            data["algo"] = "BFS"
        if dfs_button.is_clicked(e):
            data["algo"] = "DFS"
        if auto_btn.is_clicked(e) and not animating:
            data["animating"] = True
            return None, data

    # animasi BFS step-by-step
    if data.get("animating", False):
        algo = data.get("algo", "BFS")
        if algo == "BFS":
            steps, path = bfs_search_steps(grid, start)
        else:
            steps, path = dfs_search_steps(grid, start)  # dfs bisa dibuat versi serupa

        visited = []
        for pos in steps:
            visited.append(pos)
            draw_maze(screen, maze_container, grid, start, exits, visited)
            pygame.display.flip()
            pygame.time.wait(80)
        # setelah goal ketemu
        for i in range(1, len(path) + 1):
            draw_maze(screen, maze_container, grid, start, exits, visited, path[:i])
            pygame.display.flip()
            pygame.time.wait(100)

        data["animating"] = False
        data["visited"] = visited
        data["path"] = path

    return None, data
