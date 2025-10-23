import pygame

def draw(screen, events):
    font = pygame.font.SysFont("Arial", 48, bold=True)
    btn_font = pygame.font.SysFont("Arial", 36)
    width, height = screen.get_size()
    title = font.render("Pilih Maze", True, (0,0,0))
    screen.blit(title, (width//2 - title.get_width()//2, 100))

    # Dua tombol maze
    maze1_btn = pygame.Rect(width//2 - 300, height//2 - 60, 250, 80)
    maze2_btn = pygame.Rect(width//2 + 50, height//2 - 60, 250, 80)
    back_btn  = pygame.Rect(30, 30, 150, 50)

    pygame.draw.rect(screen, (180, 220, 180), maze1_btn, border_radius=8)
    pygame.draw.rect(screen, (180, 180, 250), maze2_btn, border_radius=8)
    pygame.draw.rect(screen, (200, 200, 200), back_btn, border_radius=8)

    screen.blit(btn_font.render("Maze 1", True, (0,0,0)), maze1_btn.move(70,20))
    screen.blit(btn_font.render("Maze 2", True, (0,0,0)), maze2_btn.move(70,20))
    screen.blit(btn_font.render("Kembali", True, (0,0,0)), back_btn.move(20,5))

    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if maze1_btn.collidepoint(e.pos):
                return "visualizer", {"maze_file": "./mazes/maze_1.txt"}
            elif maze2_btn.collidepoint(e.pos):
                return "visualizer", {"maze_file": "./mazes/maze_2.txt"}
            elif back_btn.collidepoint(e.pos):
                return "main_menu", None

    return None, None
