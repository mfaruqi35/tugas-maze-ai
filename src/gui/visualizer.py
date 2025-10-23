import pygame
import os
from collections import deque
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
        color = (
            self.active_color if self.active else
            self.hover_color if self.rect.collidepoint(mouse_pos) else
            self.bg_color
        )
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, self.border_color, self.rect, width=2, border_radius=8)
        text_surf = font.render(self.text, True, self.text_color)
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos))


# ----------------------------------------------------------
# Fungsi menggambar maze
# ----------------------------------------------------------
def draw_maze(surface, maze_rect, grid, start, exits, visited=None, path=None, frontier=None):
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

            # warna sel frontier
            if frontier and (r, c) in frontier:
                pygame.draw.rect(surface, (100, 200, 255), rect)
            # warna sel visited
            if visited and (r, c) in visited:
                pygame.draw.rect(surface, (200, 200, 100), rect)
            # warna path akhir
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
# BFS dan DFS yang juga melacak frontier (queue/stack)
# ----------------------------------------------------------
def bfs_search_steps(grid, start):
    n, m = len(grid), len(grid[0])
    sr, sc = start
    visited = [[False]*m for _ in range(n)]
    parent = [[None]*m for _ in range(n)]
    q = deque([(sr, sc)])
    visited[sr][sc] = True
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    steps, queue_history = [], []

    while q:
        queue_history.append(list(q))
        r, c = q.popleft()
        steps.append((r, c))
        # goal
        if (r == 0 or c == 0 or r == n-1 or c == m-1) and grid[r][c] == 0:
            path = []
            cur = (r, c)
            while cur is not None:
                path.append(cur)
                cur = parent[cur[0]][cur[1]]
            path.reverse()
            return steps, path, queue_history
        # explore
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 0 and not visited[nr][nc]:
                visited[nr][nc] = True
                parent[nr][nc] = (r, c)
                q.append((nr, nc))
    return steps, [], queue_history


def dfs_search_steps(grid, start):
    n, m = len(grid), len(grid[0])
    sr, sc = start
    visited = [[False]*m for _ in range(n)]
    parent = [[None]*m for _ in range(n)]
    stack = [(sr, sc)]
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    steps, path, stack_history = [], [], []

    while stack:
        stack_history.append(list(stack))
        r, c = stack.pop()
        if visited[r][c]:
            continue
        visited[r][c] = True
        steps.append((r, c))
        if (r == 0 or c == 0 or r == n-1 or c == m-1) and grid[r][c] == 0:
            cur = (r, c)
            while cur is not None:
                path.append(cur)
                cur = parent[cur[0]][cur[1]]
            path.reverse()
            return steps, path, stack_history
        for dr, dc in reversed(dirs):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 0 and not visited[nr][nc]:
                parent[nr][nc] = (r, c)
                stack.append((nr, nc))
    return steps, path, stack_history


# ----------------------------------------------------------
# Fungsi utama: draw()
# ----------------------------------------------------------
def draw(screen, events, data):
    pygame.font.init()
    font = pygame.font.SysFont("Arial", int(screen.get_height() * 0.02) + 20, bold=True)
    small_font = pygame.font.SysFont("Arial", 24)
    WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
    MARGIN, PANEL_GAP, INNER_PADDING = int(WINDOW_WIDTH * 0.03), int(WINDOW_WIDTH * 0.015), int(WINDOW_WIDTH * 0.005)

    frame_rect = pygame.Rect(MARGIN, MARGIN, WINDOW_WIDTH - 2*MARGIN, WINDOW_HEIGHT - 2*MARGIN)
    left_width = int(frame_rect.width * 0.3)
    right_width = frame_rect.width - left_width - PANEL_GAP
    left_panel = pygame.Rect(frame_rect.x, frame_rect.y, left_width, frame_rect.height)
    right_panel = pygame.Rect(left_panel.right + PANEL_GAP, frame_rect.y, right_width, frame_rect.height)

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

    # bagian kanan
    maze_container = pygame.Rect(right_panel.x + INNER_PADDING, right_panel.y + INNER_PADDING,
                                 right_panel.width - 2 * INNER_PADDING, int(right_panel.height * 0.85))
    button_container = pygame.Rect(right_panel.x + INNER_PADDING, maze_container.bottom + INNER_PADDING,
                                   right_panel.width - 2 * INNER_PADDING, right_panel.bottom - maze_container.bottom - INNER_PADDING)

    btn_w = int(button_container.width * 0.15)
    btn_h = int(button_container.height * 0.6)
    btn_margin = int(button_container.width * 0.02)
    x_start = button_container.x + btn_margin
    y_center = button_container.centery - btn_h // 2

    auto_btn = Button(x_start, y_center, btn_w, btn_h, "AUTO")
    restart_btn = Button(x_start + btn_w + btn_margin, y_center, btn_w, btn_h, "RESTART")
    prev_btn = Button(button_container.right - (btn_w * 2 + btn_margin * 2), y_center, btn_w, btn_h, "< PREV")
    next_btn = Button(button_container.right - (btn_w + btn_margin), y_center, btn_w, btn_h, "NEXT >")

    for btn in [back_button, bfs_button, dfs_button, auto_btn, restart_btn, prev_btn, next_btn]:
        btn.draw(screen, font)

    maze_file = data.get("maze_file", "./mazes/maze_2.txt")
    grid, rows, cols, start, exits = load_maze(maze_file)

    # inisialisasi state
    data.setdefault("visited", [])
    data.setdefault("path", [])
    data.setdefault("steps", [])
    data.setdefault("path_final", [])
    data.setdefault("frontiers", [])
    data.setdefault("step_index", 0)
    data.setdefault("status", "Idle")

    visited, path = data["visited"], data["path"]
    frontier = []
    if data["frontiers"] and data["step_index"] < len(data["frontiers"]):
        frontier = data["frontiers"][data["step_index"]]

    # tampilkan info status
    step_goal = len(data.get("path_final", []))
    step_total = len(data.get("steps", []))
    screen.blit(small_font.render(f"Status: {data['status']}", True, (255,255,255)),
                (left_panel.x + INNER_PADDING, dfs_button.rect.bottom + 80))
    screen.blit(small_font.render(f"Langkah ke goal: {step_goal}", True, (255,255,255)),
                (left_panel.x + INNER_PADDING, dfs_button.rect.bottom + 120))
    screen.blit(small_font.render(f"Total dikunjungi: {step_total}", True, (255,255,255)),
                (left_panel.x + INNER_PADDING, dfs_button.rect.bottom + 160))

    # gambar maze
    draw_maze(screen, maze_container, grid, start, exits, visited, path, frontier)

    # tombol handling
    for e in events:
        if back_button.is_clicked(e):
            return "select_maze", None
        if bfs_button.is_clicked(e):
            data["algo"] = "BFS"
        if dfs_button.is_clicked(e):
            data["algo"] = "DFS"
        if restart_btn.is_clicked(e):
            data.update({"visited": [], "path": [], "steps": [], "path_final": [], "frontiers": [], "step_index": 0, "status": "Idle"})
        if auto_btn.is_clicked(e):
            data["animating"] = True
            data["status"] = "Running"
            return None, data
        if next_btn.is_clicked(e):
            algo = data.get("algo", "BFS")
            if not data["steps"]:
                if algo == "BFS":
                    steps, path_final, fronts = bfs_search_steps(grid, start)
                else:
                    steps, path_final, fronts = dfs_search_steps(grid, start)
                data["steps"], data["path_final"], data["frontiers"] = steps, path_final, fronts
            if data["step_index"] < len(data["steps"]):
                data["step_index"] += 1
                data["visited"] = data["steps"][:data["step_index"]]
                if data["visited"][-1] == data["path_final"][-1]:
                    data["path"] = data["path_final"]
                    data["status"] = "Finished"
                else:
                    data["status"] = "Running"
        if prev_btn.is_clicked(e):
            if data["step_index"] > 0:
                data["step_index"] -= 1
                data["visited"] = data["steps"][:data["step_index"]]
                data["path"] = []
                data["status"] = "Running" if data["step_index"] > 0 else "Idle"

    # auto animasi
    if data.get("animating", False):
        algo = data.get("algo", "BFS")
        if algo == "BFS":
            steps, path, fronts = bfs_search_steps(grid, start)
        else:
            steps, path, fronts = dfs_search_steps(grid, start)
        for i in range(len(steps)):
            draw_maze(screen, maze_container, grid, start, exits, steps[:i+1], None, fronts[i])
            pygame.display.flip()
            pygame.time.wait(80)
        for i in range(1, len(path)+1):
            draw_maze(screen, maze_container, grid, start, exits, steps, path[:i])
            pygame.display.flip()
            pygame.time.wait(100)
        data.update({"animating": False, "visited": steps, "path": path,
                     "steps": steps, "path_final": path, "frontiers": fronts,
                     "status": "Finished"})

    return None, data
