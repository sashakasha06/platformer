import pygame
import sys

# Инициализация Pygame
pygame.init()

# Устанавливаем размеры экрана
screen_width = 900
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

# Загружаем фоновое изображение
bg_image = pygame.image.load('data/bg.png')

class Platform(pygame.sprite.Sprite):
    def __init__(self, mouse_pos):
        super().__init__()
        self.image = pygame.image.load("data/platform.png")
        self.rect = self.image.get_rect(topleft=mouse_pos)

class PlatformGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

# Основной игровой цикл
def main():
    platformlimit = 5
    moon = pygame.sprite.Sprite()
    moon.image = pygame.image.load('data/moon.png')
    moon.rect = moon.image.get_rect()
    moon.rect.x = 0
    moon.rect.y = 50
    rocket = pygame.sprite.Sprite()
    rocket.image = pygame.image.load('data/rocket.png')
    rocket.rect = moon.image.get_rect()
    rocket.rect.x = 100
    rocket.rect.y = 80
    finish = pygame.sprite.Sprite()
    finish.image = pygame.image.load('data/finish.png')
    finish.rect = finish.image.get_rect()
    finish.rect.x = 510
    finish.rect.y = 315
    v = 25
    clock = pygame.time.Clock()
    platforms = PlatformGroup()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if platformlimit > 0:
                    mouse_pos = pygame.mouse.get_pos()
                    new_platform = Platform(mouse_pos)
                    platforms.add(new_platform)  # Добавляем новую платформу в группу
                    platformlimit -= 1

        # Отображаем фоновое изображение
        font = pygame.font.Font(None, 50)
        text = font.render(str(platformlimit), True, (100, 255, 100))
        delta_time = clock.tick(25) / 1000
        moon.rect.x += v * delta_time
        rocket.rect.x += v * delta_time * 8
        screen.blit(bg_image, (0, 0))
        screen.blit(text, (10, 10))
        screen.blit(moon.image, (((moon.rect.x % 950) - 50), moon.rect.y))
        screen.blit(rocket.image, (((rocket.rect.x % 3000), rocket.rect.y)))
        screen.blit(finish.image, ((finish.rect.x, finish.rect.y)))
        platforms.draw(screen)  # Рисуем платформы
        pygame.display.flip()

# Запускаем игру
if __name__ == "__main__":
    main()