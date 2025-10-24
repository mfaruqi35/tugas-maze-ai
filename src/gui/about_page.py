import pygame

def draw(screen, events):
    title_font = pygame.font.Font("assets/fonts/Eurostar Black/Eurostar Black.ttf", 42)
    font = pygame.font.Font("assets/fonts/Eurostar Regular/Eurostar Regular.ttf", 36)
    btn_font = pygame.font.Font("assets/fonts/Eurostar Black/Eurostar Black.ttf", 36)

    names = ["1. Muhammad Faruqi", "2. Khalisha Adzraini Arif", "3. Nurul Izzati"]
    width, height = screen.get_size()

    back_color = (233, 12, 9)
    border_color = (70, 70, 70)
    border_thickness = 3

    hover_back = (212, 10, 7)
    hover_border = (70, 70, 70)

    # title = title_font.render("Tentang Kelompok", True, (0,0,0))
    # screen.blit(title, (width//2 - title.get_width()//2, 100))
    title_surf = title_font.render("ANGGOTA KELOMPOK", True, (20, 20, 20))
    title_rect = title_surf.get_rect(center=(width // 2, height // 6))
    screen.blit(title_surf, title_rect)

    for i, name in enumerate(names):
        text = font.render(name, True, (50, 50, 50))
        screen.blit(text, (width//2 - text.get_width()//2, 200 + i * 50))

    back_btn = pygame.Rect(30, 30, 50, 50)
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
    # pygame.draw.rect(screen, (200, 200, 200), back_btn, border_radius=8)
    # text_surf = btn_font.render("<", True, (0, 0, 0))
    # text_rect = text_surf.get_rect(center=back_btn.center)
    # screen.blit(text_surf, text_rect)
    draw_button(back_btn, back_color, hover_back, "<", border_color, hover_border)

    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if back_btn.collidepoint(e.pos):
                return "main_menu", None

    return None, None
