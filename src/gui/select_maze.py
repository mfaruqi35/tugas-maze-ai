import pygame

def draw(screen, events):
    font = pygame.font.Font("assets/fonts/Eurostar Black/Eurostar Black.ttf", 42)
    btn_font = pygame.font.Font("assets/fonts/Eurostar Black/Eurostar Black.ttf", 36)
    width, height = screen.get_size()
    # title = font.render("Pilih Maze", True, (0,0,0))
    # screen.blit(title, (width//2 - title.get_width()//2, 100))

    # Warna dasar
    maze1_color = (255, 235, 34)
    maze2_color = (255, 235, 34)
    back_color = (233, 12, 9)
    border_color = (70, 70, 70)
    border_thickness = 3

    # Warna hover (sedikit lebih terang)
    hover_maze1 = (193, 179, 36)
    hover_maze2 = (193, 179, 36)
    hover_back = (212, 10, 7)
    hover_border = (70, 70, 70)

    title_surf = font.render("PILIH MAZE", True, (20, 20, 20))
    title_rect = title_surf.get_rect(center=(width // 2, height // 6))
    screen.blit(title_surf, title_rect)

    # Dua tombol maze
    maze1_btn = pygame.Rect(width//2 - 300, height//2 - 60, 250, 80)
    maze2_btn = pygame.Rect(width//2 + 50, height//2 - 60, 250, 80)
    back_btn  = pygame.Rect(30, 30, 50, 50)

    mouse_pos = pygame.mouse.get_pos()

    def draw_button(rect, base_color, hover_color, text, border_color, hover_border_color):
        if rect.collidepoint(mouse_pos):
            fill = hover_color
            border = hover_border_color
        else:
            fill = base_color
            border = border_color
        
        pygame.draw.rect(screen, fill, rect, border_radius=10)
        pygame.draw.rect(screen, border, rect, border_radius=10, width=border_thickness)

        # render teks dan letakkan di tengah tombol
        text_surf = btn_font.render(text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    draw_button(maze1_btn, maze1_color, hover_maze1, "Maze 1", border_color, hover_border)
    draw_button(maze2_btn, maze2_color, hover_maze2, "Maze 2", border_color, hover_border)
    draw_button(back_btn, back_color, hover_back, "<", border_color, hover_border)

    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if maze1_btn.collidepoint(e.pos):
                return "visualizer", {"maze_file": "./mazes/maze_1.txt"}
            elif maze2_btn.collidepoint(e.pos):
                return "visualizer", {"maze_file": "./mazes/maze_2.txt"}
            elif back_btn.collidepoint(e.pos):
                return "main_menu", None

    return None, None
