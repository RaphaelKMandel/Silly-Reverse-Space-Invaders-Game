from Constants import *


def display_main_menu():
    reset_screen()
    limit_fps()
    display_text('Press Space-Bar to Begin', WHITE, x_offset=SCREEN_WIDTH//2-150, y_offset=SCREEN_HEIGHT//2)
    pygame.display.update()


def pause_game():
    display_text('Game Paused...', WHITE, x_offset=SCREEN_WIDTH // 2 - 50, y_offset=SCREEN_HEIGHT // 2)
    display_text('Press ESC to Resume', WHITE, x_offset=SCREEN_WIDTH // 2 - 100, y_offset=SCREEN_HEIGHT // 2 + 30)
    pygame.display.update()
    pygame.time.delay(200)
    paused = True
    while paused:
        paused = get_quit_event()
        limit_fps()
        left, right, down, up, space, shields, dampers, esc, pause = keystrokes()
        if esc or pause:
            pygame.time.delay(200)
            return False


def end_game(mode):
    while True:
        get_quit_event()
        limit_fps()
        if mode == 0:
            display_text('You Won!', WHITE, x_offset=SCREEN_WIDTH // 2 - 50, y_offset=SCREEN_HEIGHT // 2)
        elif mode == 1:
            display_text('You Lost!', WHITE, x_offset=SCREEN_WIDTH // 2 - 50, y_offset=SCREEN_HEIGHT // 2)
        display_text('Press ESC to Quit', WHITE, x_offset=SCREEN_WIDTH // 2 - 100, y_offset=SCREEN_HEIGHT // 2 + 30)
        pygame.display.update()
        left, right, down, up, space, shields, dampers, esc, pause = keystrokes()
        if esc:
            return False


def get_quit_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def limit_fps():
    display_text(f'FPS: {1000//CLOCK.tick(FPS)}', WHITE, x_offset=SCREEN_WIDTH-150, y_offset=30)


def reset_screen():
    game().fill(BLACK)


def display_text(text, color, x_offset=0, y_offset=0, font='comicsans', fontsize=30, bold=True):
    surface = pygame.font.SysFont(font, fontsize, bold)
    render = surface.render(text, True, color)
    game().blit(render, (x_offset, SCREEN_HEIGHT + 100 - y_offset))


def keystrokes():
    keys = pygame.key.get_pressed()
    left = keys[pygame.K_LEFT] or keys[pygame.K_a]
    right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
    down = keys[pygame.K_DOWN] or keys[pygame.K_s]
    up = keys[pygame.K_UP] or keys[pygame.K_w]
    shields = keys[pygame.K_q]
    dampers = keys[pygame.K_e]
    space = keys[pygame.K_SPACE]
    esc = keys[pygame.K_ESCAPE]
    pause = keys[pygame.K_p]
    return left, right, down, up, space, shields, dampers, esc, pause


def display_stats(player, enemy):
    pygame.draw.rect(game(), RED, (0, SCREEN_HEIGHT, SCREEN_WIDTH, 100))
    display_text(f'Player Mass: {round(player.mass, 1)} kg; Enemy Mass: {round(enemy.mass, 1)} kg', 'white',
                 y_offset=60)
    display_text(f'Player Charge: {round(player.charge, 1)}', 'white',
                 y_offset=30)
