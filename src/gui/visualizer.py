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
                 bg_color=(255, 235, 34), hover_color=(193, 179, 36),
                 active_color=(193, 179, 36),
                 text_color=(0,0,0), border_color=(70,70,70)):
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
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, self.border_color, self.rect, width=3, border_radius=10)
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

    wall_texture = pygame.image.load("assets/images/walls.png").convert()
    wall_texture = pygame.transform.smoothscale(wall_texture, (cell_size, cell_size))

    for r in range(rows):
        for c in range(cols):
            val = grid[r][c]
            rect = pygame.Rect(offset_x + c * cell_size, offset_y + r * cell_size, cell_size, cell_size)

            if val == -1:
                surface.blit(wall_texture, rect)
            else:
                pygame.draw.rect(surface, (250, 250, 250), rect)
                pygame.draw.rect(surface, (200, 200, 200), rect, 1)

            # warna sel frontier
            if frontier and (r, c) in frontier:
                pygame.draw.rect(surface, (255, 178, 0), rect)
                pygame.draw.rect(surface, (200, 200, 200), rect, 1)
            # warna sel visited
            if visited and (r, c) in visited:
                pygame.draw.rect(surface, (64, 161, 255), rect)
                pygame.draw.rect(surface, (200, 200, 200), rect, 1)
            # warna path akhir
            if path and (r, c) in path:
                pygame.draw.rect(surface, (255, 235, 34), rect)
                pygame.draw.rect(surface, (200, 200, 200), rect, 1)


    # start
    sx, sy = start[1], start[0]
    srect = pygame.Rect(offset_x + sx * cell_size, offset_y + sy * cell_size, cell_size, cell_size)
    pygame.draw.rect(surface, (0, 255, 1), srect)

    # exits
    for (er, ec) in exits:
        erect = pygame.Rect(offset_x + ec * cell_size, offset_y + er * cell_size, cell_size, cell_size)
        pygame.draw.rect(surface, (233, 12, 9), erect)


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

def draw_info_box(screen, font, text, x, y, w, h,
                  bg_color=(255, 235, 34), border_color=(70, 70, 70), text_color=(0,0,0)):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, bg_color, rect, border_radius=10)
    pygame.draw.rect(screen, border_color, rect, width=3, border_radius=10)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    return rect

# ----------------------------------------------------------
# Fungsi utama: draw()
# ----------------------------------------------------------
def draw(screen, events, data):
    pygame.font.init()
    font = pygame.font.Font("assets/fonts/Eurostar Black/Eurostar Black.ttf", int(screen.get_height() * 0.02) + 10)
    small_font = pygame.font.Font("assets/fonts/Eurostar Regular/Eurostar Regular.ttf", 20)
    WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
    MARGIN, INNER_PADDING = int(WINDOW_WIDTH * 0.03), int(WINDOW_WIDTH * 0.005)

    frame_rect = pygame.Rect(MARGIN + 2, MARGIN, WINDOW_WIDTH - 2*MARGIN, WINDOW_HEIGHT - 2*MARGIN)
    left_width = int(frame_rect.width * 0.3)
    right_width = frame_rect.width - left_width - 10
    left_panel = pygame.Rect(frame_rect.x + 3, frame_rect.y + 3, left_width, frame_rect.height - 7)
    right_panel = pygame.Rect(left_panel.right + 3, frame_rect.y + 3, right_width, frame_rect.height - 7)

    # Frame border
    pygame.draw.rect(screen, (50, 50, 50), frame_rect, width=4)

    # Panels
    pygame.draw.rect(screen, (220, 220, 220), left_panel)
    pygame.draw.rect(screen, (250, 250, 250), right_panel)

    # Panel Separator
    pygame.draw.line(screen, (50, 50, 50), (left_panel.right, frame_rect.y), (left_panel.right, frame_rect.bottom - 2), 4)


    # tombol
    btn_size = 50
    back_button = Button(left_panel.x + INNER_PADDING, left_panel.y + INNER_PADDING, btn_size, btn_size, "<", bg_color=(250, 11, 7), hover_color=(212, 10, 7), active_color=(212, 10, 7))
    
    # Tulisan ALGORITMA
    text_algo = font.render("ALGORITMA", True, (0, 0, 0))
    text_algo_rect = text_algo.get_rect(midtop=(left_panel.centerx, back_button.rect.bottom + 20))
    screen.blit(text_algo, text_algo_rect)

    algo_w = left_panel.width // 2.2
    algo_h = int(WINDOW_HEIGHT * 0.08)
    bfs_button = Button(left_panel.x + INNER_PADDING + 5, back_button.rect.bottom + 60, algo_w, algo_h, "BFS")
    dfs_button = Button(left_panel.x * 4.95 + INNER_PADDING, back_button.rect.bottom + 60, algo_w, algo_h, "DFS")

    algo_mode = data.get("algo", "BFS")
    bfs_button.active = (algo_mode == "BFS")
    dfs_button.active = (algo_mode == "DFS")

    # bagian kanan
    maze_container = pygame.Rect(right_panel.x + INNER_PADDING, right_panel.y + INNER_PADDING,
                                 right_panel.width - 2 * INNER_PADDING, int(right_panel.height * 0.85))
    button_container = pygame.Rect(right_panel.x + INNER_PADDING, maze_container.bottom + INNER_PADDING,
                                   right_panel.width - 2 * INNER_PADDING, right_panel.bottom - maze_container.bottom - INNER_PADDING)

    btn_w = int(button_container.width * 0.18)
    btn_h = int(button_container.height * 0.75)
    btn_margin = int(button_container.width * 0.02)
    x_start = button_container.x + btn_margin
    y_center = button_container.centery - btn_h // 2

    auto_btn = Button(x_start, y_center, btn_w, btn_h, "AUTO")
    restart_btn = Button(x_start + btn_w + btn_margin, y_center, btn_w + 20, btn_h, "RESTART")
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

    # Tulisan INFO
    text_info = font.render("INFO", True, (0, 0, 0))
    text_info_rect = text_info.get_rect(midtop=(left_panel.centerx, dfs_button.rect.bottom + 50))
    screen.blit(text_info, text_info_rect)

    # Tampilkan info status
    current_step = data.get("step_index", 0)
    goal_reached = False
    if data.get("path_final"):
        # kalau posisi terakhir sudah sampai ke goal (elemen terakhir path_final)
        if current_step > 0 and data["visited"] and data["visited"][-1] == data["path_final"][-1]:
            goal_reached = True

    step_goal = len(data["path_final"]) if goal_reached else 0
    step_total = current_step
    # --- Kotak besar untuk info ---
    info_box_w = left_panel.width - 40
    info_box_h = 120
    info_x = left_panel.x + 20
    info_y = dfs_button.rect.bottom + 90
    info_rect = pygame.Rect(info_x, info_y, info_box_w, info_box_h)

    # Gaya seperti tombol (tapi non-interaktif)
    pygame.draw.rect(screen, (255, 235, 34), info_rect, border_radius=10)
    pygame.draw.rect(screen, (70, 70, 70), info_rect, width=3, border_radius=10)

    # --- Teks di dalam kotak ---
    padding = 15
    text_start_y = info_y + padding
    line_spacing = 30

    screen.blit(small_font.render(f"Status: {data['status']}", True, (0,0,0)),
                (info_x + padding, text_start_y))
    screen.blit(small_font.render(f"Langkah ke goal: {step_goal}", True, (0,0,0)),
                (info_x + padding, text_start_y + line_spacing))
    screen.blit(small_font.render(f"Total dikunjungi: {step_total}", True, (0,0,0)),
                (info_x + padding, text_start_y + 2*line_spacing))



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

        # Jalankan pencarian penuh dulu (biar kita tahu hasil akhirnya)
        if algo == "BFS":
            steps, path, fronts = bfs_search_steps(grid, start)
        else:
            steps, path, fronts = dfs_search_steps(grid, start)

        # Langsung tampilkan hasil langkah di panel kiri (tanpa nunggu animasi)
        data.update({
            "steps": steps,
            "path_final": path,
            "frontiers": fronts,
            "visited": steps,   # biar jumlah total langkah muncul langsung
            "path": path,       # biar langkah ke goal muncul
            "step_index": len(steps),
            "status": "Running"
        })

        # Tetap jalankan animasi visualnya
        for i in range(len(steps)):
            draw_maze(screen, maze_container, grid, start, exits, steps[:i+1], None, fronts[i])
            pygame.display.flip()
            pygame.time.wait(80)

        for i in range(1, len(path)+1):
            draw_maze(screen, maze_container, grid, start, exits, steps, path[:i])
            pygame.display.flip()
            pygame.time.wait(100)

        # Setelah animasi selesai
        data.update({
            "animating": False,
            "status": "Finished"
        })


    return None, data
