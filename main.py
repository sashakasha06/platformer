import os
import sys
import random
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # Если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class BombSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("bomb.png")
        self.rect = self.image.get_rect(topleft=(x, y))

    def explode(self):
        self.image = load_image("boom.png")
        self.rect.x -= 35
        self.rect.y -= 31


class BombGroup(pygame.sprite.Group):
    def __init__(self, num_bombs):
        super().__init__()
        self.used_positions = []
        self.create_bombs(num_bombs)

    def create_bombs(self, num_bombs):
        while num_bombs > 0:
            x = random.randint(60, 440)
            y = random.randint(61, 439)
            if not self.is_position_used(x, y):
                bomb = BombSprite(x, y)
                self.add(bomb)
                self.used_positions.append((x, y))
                num_bombs -= 1

    def is_position_used(self, x, y):
        for value in self.used_positions:
            if abs(x - value[0]) < 65 and abs(y - value[1]) < 65:
                return True
        return False


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)

    bomb_group = BombGroup(num_bombs=20)

    running = True
    while running:
        for event in pygame.event.get():
            # При закрытии окна
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for bomb in bomb_group:
                    if bomb.rect.collidepoint(mouse_pos):
                        bomb.explode()

        screen.fill((255, 255, 255))
        bomb_group.draw(screen)
        pygame.display.flip()

    pygame.quit()