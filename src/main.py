import pygame
from gui import main_menu, about_page, select_maze, visualizer

pygame.init()
screen = pygame.display.set_mode((2500, 1500))
pygame.display.set_caption("Maze Solver")
clock = pygame.time.Clock()

current_page = "main_menu"
page_data = {}
running = True

while running:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            running = False

    screen.fill((240, 240, 240))

    # Render page berdasarkan state
    if current_page == "main_menu":
        next_page, data = main_menu.draw(screen, events)
    elif current_page == "about_page":
        next_page, data = about_page.draw(screen, events)
    elif current_page == "select_maze":
        next_page, data = select_maze.draw(screen, events)
        if next_page:
            current_page = next_page
            page_data = data or {}
    elif current_page == "visualizer":
        next_page, data = visualizer.draw(screen, events, page_data)
        if next_page:
            current_page = next_page
            page_data = data or {}
    else:
        next_page, data = None, None

    # Pindah halaman
    if next_page:
        if next_page == "exit":
            running = False
        else:
            current_page = next_page
            page_data = data or {}

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
