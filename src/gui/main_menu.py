import pygame

def draw(screen, events):
    width, height = screen.get_size()
    font = pygame.font.Font("assets/fonts/Eurostar Black/Eurostar Black.ttf", 64)
    btn_font = pygame.font.Font("assets/fonts/Eurostar Black/Eurostar Black.ttf", 36)

    # Warna dasar
    start_color = (12, 236, 13)
    quit_color = (233, 12, 9)
    about_color = (241,220,9)   
    border_color = (50, 50, 50)
    border_thickness = 4

    # Warna hover (sedikit lebih terang)
    hover_start = (0, 255, 1)
    hover_quit = (250, 11, 7)
    hover_about = (255, 232, 0)
    hover_border = (80, 80, 80)

    # Judul
    title_surf = font.render("MAZE SOLVER", True, (20, 20, 20))
    title_rect = title_surf.get_rect(center=(width // 2, height // 4))
    screen.blit(title_surf, title_rect)

    # Tombol
    start_btn = pygame.Rect(width // 2 - 150, height // 2 - 60, 300, 80)
    quit_btn = pygame.Rect(width // 2 - 150, height // 2 + 40, 300, 80)
    about_btn = pygame.Rect(30, 30, 50, 50)

    mouse_pos = pygame.mouse.get_pos()  # posisi mouse saat ini

    # Fungsi bantu untuk menggambar tombol dengan hover
    def draw_button(rect, base_color, hover_color, text, border_color, hover_border_color):
        if rect.collidepoint(mouse_pos):  # jika mouse di atas tombol
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

    # Gambar ketiga tombol
    draw_button(start_btn, start_color, hover_start, "Mulai", border_color, hover_border)
    draw_button(quit_btn, quit_color, hover_quit, "Keluar", border_color, hover_border)
    draw_button(about_btn, about_color, hover_about, "?", border_color, hover_border)

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
