import pygame

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
        return


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.alive = True

        self.image = load_image("FlappyBird/Assets/bird.png", (40, 30))
        self.angle = 0

        self.GRAVITY = 0.25
        self.JUMP_VELOCITY = -5

        try:
            self.jump_sound = pygame.mixer.Sound("jump.wav")
        except:
            self.jump_sound = None

    def draw(self, screen):

        self.angle = max(-30, min(self.velocity * 3, 80))

        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))

        screen.blit(rotated_image, new_rect.topleft)

    def update(self, screen_height):

        self.velocity += self.GRAVITY
        self.y += self.velocity

        if self.y < 0:
            self.y = 0
            self.velocity = 0
        elif self.y > screen_height:
            self.y = screen_height
            self.velocity = 0
            self.alive = False

    def jump(self):
        self.velocity = self.JUMP_VELOCITY
        if self.jump_sound:
            self.jump_sound.play()

    def get_rect(self):

        return pygame.Rect(self.x - 15, self.y - 15, 30, 30)