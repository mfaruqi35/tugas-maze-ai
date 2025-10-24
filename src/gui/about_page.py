import pygame

def draw(screen, events):
    font = pygame.font.Font("assets/fonts/Eurostar Regular/Eurostar Regular.ttf", 36)
    btn_font = pygame.font.Font("assets/fonts/Eurostar Black/Eurostar Black.ttf", 36)
    names = ["1. Kamu (Ketua)", "2. Anggota 2", "3. Anggota 3"]
    width, height = screen.get_size()

    title = font.render("Tentang Kelompok", True, (0,0,0))
    screen.blit(title, (width//2 - title.get_width()//2, 100))

    for i, name in enumerate(names):
        text = font.render(name, True, (50, 50, 50))
        screen.blit(text, (width//2 - text.get_width()//2, 200 + i * 50))

    back_btn = pygame.Rect(30, 30, 50, 50)
    pygame.draw.rect(screen, (200, 200, 200), back_btn, border_radius=8)
    text_surf = btn_font.render("<", True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=back_btn.center)
    screen.blit(text_surf, text_rect)

    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if back_btn.collidepoint(e.pos):
                return "main_menu", None

    return None, None
