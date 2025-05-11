import pygame
from bird import Bird
from pipe import Pipe, load_image


class Game:
    def __init__(self, width=400, height=600):
        self.WIDTH = width
        self.HEIGHT = height

        self.PIPE_GAP = 500
        self.PIPE_FREQUENCY = 2000
        self.PIPE_SPEED = 2

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)

        self.bird = Bird(100, self.HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.last_pipe = pygame.time.get_ticks()

        self.font = pygame.font.SysFont(None, 50)

        self.background = load_image("FlappyBird/Assets/background.png", (self.WIDTH, self.HEIGHT), convert_alpha=False)
        self.ground = load_image("FlappyBird/Assets/ground.png", (self.WIDTH, 100))
        self.ground_scroll = 0
        self.ground_scroll_speed = self.PIPE_SPEED


    def draw_background(self, screen):
        screen.blit(self.background, (0, 0))

        screen.blit(self.ground, (self.ground_scroll, self.HEIGHT - 100))
        screen.blit(self.ground, (self.ground_scroll + self.WIDTH, self.HEIGHT - 100))

        if not self.game_over:
            self.ground_scroll -= self.ground_scroll_speed
            if abs(self.ground_scroll) > self.WIDTH:
                self.ground_scroll = 0

    def draw(self, screen):
        self.draw_background(screen)

        for pipe in self.pipes:
            pipe.draw(screen)

        self.bird.draw(screen)

        score_text = self.font.render(f"Score: {self.score}", True, self.BLACK)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))

            game_over_text = self.font.render("Game Over!", True, self.RED)
            restart_text = pygame.font.SysFont(None, 30).render("Press R to Restart", True, self.WHITE)
            screen.blit(game_over_text, (self.WIDTH // 2 - game_over_text.get_width() // 2,
                                         self.HEIGHT // 2 - game_over_text.get_height() // 2))
            screen.blit(restart_text, (self.WIDTH // 2 - restart_text.get_width() // 2,
                                       self.HEIGHT // 2 + game_over_text.get_height()))

    def update(self):
        if not self.game_over:
            self.bird.update(self.HEIGHT)

            now = pygame.time.get_ticks()
            if now - self.last_pipe > self.PIPE_FREQUENCY:
                self.pipes.append(Pipe(self.WIDTH, self.HEIGHT, self.PIPE_GAP, self.PIPE_SPEED))
                self.last_pipe = now

            for pipe in self.pipes:
                pipe.update()

                if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                    pipe.passed = True
                    self.score += 1

            self.pipes = [pipe for pipe in self.pipes if not pipe.off_screen()]

            self.check_collisions()

            if not self.bird.alive:
                self.game_over = True

    def check_collisions(self):
        bird_rect = self.bird.get_rect()

        for pipe in self.pipes:
            top_pipe, bottom_pipe = pipe.get_rects()
            if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
                self.bird.alive = False
                break

        if bird_rect.bottom >= self.HEIGHT - 100:
            self.bird.alive = False

    def restart(self):
        self.__init__(self.WIDTH, self.HEIGHT)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.game_over:
                self.bird.jump()
            if event.key == pygame.K_r and self.game_over:
                self.restart()