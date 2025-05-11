import pygame
import sys
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

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            game.handle_input(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        if gesture_detector.gesture_fist_detected and not game.game_over:
            game.bird.jump()

        game.update()

        game.draw(screen)

        pygame.display.update()

        clock.tick(FPS)

    gesture_detector.stop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()