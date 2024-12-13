import os
import sys
import random
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
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


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    for _ in range(20):
        sprite = pygame.sprite.Sprite()
        sprite.image = load_image("bomb.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = random.randint(50, 450)
        sprite.rect.y = random.randint(51, 449)
        all_sprites.add(sprite)
    running = True
    while running:
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i in all_sprites:
                    if i.rect.collidepoint(mouse_pos):
                        i.image = load_image("boom.png")
                        i.rect.x -= 35
                        i.rect.y -= 31

        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()