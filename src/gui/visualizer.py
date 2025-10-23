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

    # Cari semua cell yang merupakan exit (0 di pinggir grid)
    exits = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0 and (r == 0 or c == 0 or r == rows - 1 or c == cols - 1):
                exits.append((r, c))

    return grid, rows, cols, start, exits


# ----------------------------------------------------------
# Fungsi menggambar maze di dalam container
# ----------------------------------------------------------
def draw_maze(surface, maze_rect, grid, start, exits):
    rows = len(grid)
    cols = len(grid[0])
    cell_w = maze_rect.width // cols
    cell_h = maze_rect.height // rows
    cell_size = min(cell_w, cell_h)

    offset_x = maze_rect.x + (maze_rect.width - cols * cell_size) // 2
    offset_y = maze_rect.y + (maze_rect.height - rows * cell_size) // 2

    for r in range(rows):
        for c in range(cols):
            val = grid[r][c]
            color = (40, 40, 40) if val == -1 else (230, 230, 230)
            rect = pygame.Rect(
                offset_x + c * cell_size,
                offset_y + r * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (180, 180, 180), rect, 1)

    # Start (biru)
    sx, sy = start[1], start[0]
    rect = pygame.Rect(
        offset_x + sx * cell_size,
        offset_y + sy * cell_size,
        cell_size, cell_size
    )
    pygame.draw.rect(surface, (50, 100, 255), rect)

    # Exit (hijau)
    for (er, ec) in exits:
        rect = pygame.Rect(
            offset_x + ec * cell_size,
            offset_y + er * cell_size,
            cell_size, cell_size
        )
        pygame.draw.rect(surface, (0, 200, 0), rect)


# ----------------------------------------------------------
# Tombol dasar
# ----------------------------------------------------------
class Button:
    def __init__(self, x, y, w, h, text,
                 bg_color=(240,240,240), hover_color=(200,200,200),
                 text_color=(0,0,0), border_color=(0,0,0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color

    def draw(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        pygame.draw.rect(surface, self.border_color, self.rect, width=2, border_radius=6)

        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.rect.collidepoint(event.pos))


# ----------------------------------------------------------
# Fungsi utama: draw()
# ----------------------------------------------------------
def draw(screen, events, data):
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 32, bold=True)

    WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
    MARGIN, PANEL_GAP, INNER_PADDING = 75, 40, 10

    # Layout
    frame_rect = pygame.Rect(MARGIN, MARGIN, WINDOW_WIDTH - 2*MARGIN, WINDOW_HEIGHT - 2*MARGIN)
    left_width = 847
    left_panel = pygame.Rect(frame_rect.x, frame_rect.y, left_width, frame_rect.height)
    right_panel = pygame.Rect(left_panel.right + PANEL_GAP, frame_rect.y,
                              frame_rect.width - left_width - PANEL_GAP, frame_rect.height)

    # Panel dasar
    pygame.draw.rect(screen, (100, 100, 100), left_panel)
    pygame.draw.rect(screen, (0, 0, 0), right_panel)

    left_inner = pygame.Rect(
        left_panel.x + INNER_PADDING, left_panel.y + INNER_PADDING,
        left_panel.width - 2*INNER_PADDING, left_panel.height - 2*INNER_PADDING
    )
    pygame.draw.rect(screen, (200, 200, 200), left_inner)

    # Tombol kembali
    back_button = Button(
        left_panel.x + INNER_PADDING,
        left_panel.y + INNER_PADDING,
        120, 120, "<"
    )
    back_button.draw(screen, font)

    # Area maze
    maze_container = pygame.Rect(
        right_panel.x + INNER_PADDING,
        right_panel.y + INNER_PADDING,
        right_panel.width - 2 * INNER_PADDING,
        right_panel.height - 20 * INNER_PADDING
    )
    pygame.draw.rect(screen, (250, 250, 250), maze_container)

    # Area tombol bawah
    button_container = pygame.Rect(
        right_panel.x + INNER_PADDING,
        maze_container.bottom + INNER_PADDING,
        right_panel.width - 2 * INNER_PADDING,
        right_panel.height - maze_container.height - 3 * INNER_PADDING
    )
    pygame.draw.rect(screen, (220, 220, 220), button_container)

    # Tombol bawah
    btn_margin, btn_w, btn_h = 30, 220, 90
    x_start = button_container.x + btn_margin
    y_center = button_container.centery - btn_h // 2

    restart_btn = Button(x_start, y_center, btn_w, btn_h, "RESTART")
    auto_btn    = Button(x_start + btn_w + btn_margin, y_center, btn_w, btn_h, "AUTO")
    prev_btn    = Button(button_container.right - (btn_w * 2 + btn_margin * 2), y_center, btn_w, btn_h, "< PREV")
    next_btn    = Button(button_container.right - (btn_w + btn_margin), y_center, btn_w, btn_h, "NEXT >")

    for btn in [restart_btn, auto_btn, prev_btn, next_btn]:
        btn.draw(screen, font)

    # Tampilkan maze dari file pilihan user
    maze_file = data.get("maze_file", "./mazes/maze_2.txt")
    grid, rows, cols, start, exits = load_maze(maze_file)
    draw_maze(screen, maze_container, grid, start, exits)

    # Event handling
    for e in events:
        if back_button.is_clicked(e):
            return "select_maze", None  # balik ke halaman pilih maze
    
        if auto_btn.is_clicked(e):
            path, steps = bfs_solve(grid, start)  # atau dfs_solve
            print(f"Langkah: {steps}")


    # Kalau tidak berpindah halaman
    return None, None
