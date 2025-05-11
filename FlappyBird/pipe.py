import pygame
import random


def load_image(name, scale=None, convert_alpha=True):
    try:
        if convert_alpha:
            image = pygame.image.load(name).convert_alpha()
        else:
            image = pygame.image.load(name).convert()

        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        print(f"Could not load image {name}: {e}")
        placeholder = pygame.Surface((50, 300))
        if name.endswith("pipe.png") or "pipe" in name:
            placeholder.fill((0, 128, 0))

        if scale:
            placeholder = pygame.transform.scale(placeholder, scale)
        return placeholder


class Pipe:
    def __init__(self, screen_width, screen_height, pipe_gap=300, speed=2):
        self.gap_y = random.randint(300, screen_height - 300)
        self.x = screen_width
        self.passed = False
        self.pipe_top = load_image("FlappyBird//Assets/pipe_top.png", (70, 500))
        self.pipe_bottom = load_image("FlappyBird//Assets/pipe_bottom.png", (70, 500))
        self.width = self.pipe_top.get_width()

        self.PIPE_GAP = pipe_gap
        self.PIPE_SPEED = speed
        self.SCREEN_HEIGHT = screen_height

    def draw(self, screen):
        pipe_top_pos = (self.x, self.gap_y - self.PIPE_GAP // 2 - self.pipe_top.get_height())
        pipe_bottom_pos = (self.x, self.gap_y + self.PIPE_GAP // 2)

        screen.blit(self.pipe_top, pipe_top_pos)
        screen.blit(self.pipe_bottom, pipe_bottom_pos)

    def update(self):
        self.x -= self.PIPE_SPEED

    def off_screen(self):
        return self.x < -self.width

    def get_rects(self):
        top_pipe = pygame.Rect(self.x, 0, self.width, self.gap_y - self.PIPE_GAP // 2)
        bottom_pipe = pygame.Rect(self.x, self.gap_y + self.PIPE_GAP // 2,
                                  self.width, self.SCREEN_HEIGHT - (self.gap_y + self.PIPE_GAP // 2))
        return top_pipe, bottom_pipe