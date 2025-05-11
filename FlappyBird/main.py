import pygame
import sys
import time
from gesture_detector import GestureDetector
from game import Game

def main():
    pygame.init()
    pygame.mixer.init()

    WIDTH, HEIGHT = 800, 800
    FPS = 60

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    game = Game(WIDTH, HEIGHT)
    gesture_detector = GestureDetector()

    while not gesture_detector.gesture_peace_detected:
        pygame.event.pump()
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 50)
        text = font.render("Show Peace Sign to Start", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()
        time.sleep(0.05)

    COUNTDOWN_DURATION = 3
    countdown_start_time = pygame.time.get_ticks() / 1000
    game_started = False
    countdown_active = True

    gesture_allowed = True
    running = True
    while running:
        current_time = pygame.time.get_ticks() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

            game.handle_input(event)

        if gesture_detector.gesture_peace_detected and gesture_allowed and not countdown_active:
            countdown_start_time = current_time
            countdown_active = True
            game_started = False
            game.restart()
            gesture_allowed = False
            gesture_detector.gesture_peace_detected = False

        if countdown_active:
            elapsed = current_time - countdown_start_time
            if elapsed < COUNTDOWN_DURATION:
                screen.fill((0, 0, 0))
                countdown_value = COUNTDOWN_DURATION - int(elapsed)
                font = pygame.font.SysFont(None, 120)
                text = font.render(str(countdown_value), True, (255, 255, 255))
                info_font = pygame.font.SysFont(None, 50)
                info_text = info_font.render("Get Ready!", True, (180, 180, 255))
                screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, HEIGHT // 2 - 100))
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
                pygame.display.update()
                continue
            else:
                countdown_active = False
                game_started = True

        if gesture_detector.gesture_fist_detected and not game.game_over and game_started:
            game.bird.jump()

        game.update()

        if game.game_over:
            gesture_allowed = True

        game.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

    gesture_detector.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
