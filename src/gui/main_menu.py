import pygame


def draw(screen, events):
    width, height = screen.get_size()

    font = pygame.font.SysFont("Arial", 64, bold=True)
    btn_font = pygame.font.SysFont("Arial", 36)
    # Judul
    title_surf = font.render("MAZE SOLVER", True, (20, 20, 20))
    title_rect = title_surf.get_rect(center=(width//2, height//4))
    screen.blit(title_surf, title_rect)

    # Tombol
    start_btn = pygame.Rect(width//2 - 150, height//2 - 60, 300, 80)
    quit_btn = pygame.Rect(width//2 - 150, height//2 + 40, 300, 80)
    about_btn = pygame.Rect(30, 30, 100, 50)

    pygame.draw.rect(screen, (180, 220, 180), start_btn, border_radius=8)
    pygame.draw.rect(screen, (220, 180, 180), quit_btn, border_radius=8)
    pygame.draw.rect(screen, (180, 180, 250), about_btn, border_radius=8)

    screen.blit(btn_font.render("Mulai", True, (0,0,0)), start_btn.move(95,20))
    screen.blit(btn_font.render("Keluar", True, (0,0,0)), quit_btn.move(85,20))
    screen.blit(btn_font.render("?", True, (0,0,0)), about_btn.move(38,8))

    # Event klik
    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if start_btn.collidepoint(e.pos):
                return "select_maze", None
            elif quit_btn.collidepoint(e.pos):
                return "exit", None
            elif about_btn.collidepoint(e.pos):
                return "about_page", None

    return None, None
