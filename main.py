import pygame
import sys

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Устанавливаем размеры экрана
screen_width = 900
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.mixer.music.load('data/space.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

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
    pygame.mixer.music.set_volume(0.5)
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
    bounce = pygame.mixer.Sound('data/bounce.mp3')
    step = pygame.mixer.Sound('data/step.mp3')
    gameover = pygame.mixer.Sound('data/gameover.mp3')
    victorysound = pygame.mixer.Sound('data/victory.mp3')
    platformsound = pygame.mixer.Sound('data/platform.mp3')
    screamsound = pygame.mixer.Sound('data/uhu.mp3')
    man = pygame.sprite.Sprite()
    man.image = pygame.image.load('data/fall.png')
    man.rect = man.image.get_rect()
    man.rect.x = 500
    man.rect.y = 0
    man_moving = True
    scream = True
    game_over = False
    victory = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if platformlimit > 0:
                    mouse_pos = pygame.mouse.get_pos()
                    new_platform = Platform(mouse_pos)
                    platforms.add(new_platform)  # Добавляем новую платформу в группу
                    platformlimit -= 1
                    platformsound.play()
            elif event.type == pygame.KEYDOWN and not man_moving:
                if event.key == pygame.K_LEFT:
                    man.rect.x -= 10
                    step.play()
                    man.image = pygame.image.load('data/run-left.png')
                elif event.key == pygame.K_RIGHT:
                    man.rect.x += 10
                    step.play()
                    man.image = pygame.image.load('data/run-right.png')
                if not pygame.sprite.spritecollide(man, platforms, False):
                    man.image = pygame.image.load('data/fall.png')
                    man_moving = True
                    scream = True

        if game_over:
            pygame.mixer.music.set_volume(0.0)
            display_game_over('GAME OVER')
            pygame.time.delay(4000)  # Задержка для отображения экрана Game Over
            main()

        if victory:
            pygame.mixer.music.set_volume(0.0)
            display_game_over('CONGRATULATIONS!')
            pygame.time.delay(6000)  # Задержка для отображения экрана Game Over
            main()

        if man_moving:
            vman = 25
            if scream:
                screamsound.play()
                scream = False
        else:
            vman = 0
        if pygame.sprite.spritecollide(man, platforms, False):
            if man_moving:
                bounce.play()
            man_moving = False

        font = pygame.font.Font(None, 50)
        text = font.render(str(platformlimit), True, (100, 255, 100))
        delta_time = clock.tick(25) / 1000
        moon.rect.x += v * delta_time
        rocket.rect.x += v * delta_time * 8
        man.rect.y += vman * delta_time * 2
        if man.rect.y > 700:
            game_over = True
            gameover.play()
        if 625 < man.rect.y < 670 and man.rect.x > 840 and not man_moving:
            victory = True
            victorysound.play()
        screen.blit(bg_image, (0, 0))
        screen.blit(text, (10, 10))
        screen.blit(moon.image, (((moon.rect.x % 950) - 50), moon.rect.y))
        screen.blit(rocket.image, (((rocket.rect.x % 3000), rocket.rect.y)))
        screen.blit(finish.image, ((finish.rect.x, finish.rect.y)))
        screen.blit(man.image, ((man.rect.x, man.rect.y)))
        platforms.draw(screen)  # Рисуем платформы
        pygame.display.flip()


def display_game_over(message):
    # Создаем затемнение
    font = pygame.font.Font(None, 74)
    font2 = pygame.font.Font(None, 50)
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)  # Устанавливаем прозрачность
    screen.blit(overlay, (0, 0))  # Рисуем затемнение на экране

    # Отображаем текст
    text = font.render(message, True,'white')
    text2 = font2.render("INSERT COIN", True, 'green')
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 40))
    text_rect2 = text2.get_rect(center=(screen_width // 2, screen_height // 2 + 10))
    screen.blit(text, text_rect)
    screen.blit(text2, text_rect2)

    pygame.display.flip()  # Обновляем экран




# Запускаем игру
if __name__ == "__main__":
    main()