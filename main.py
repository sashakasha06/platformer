import pygame
import sys

pygame.init()
pygame.mixer.init()
screen_width = 900
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.mixer.music.load('data/space.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)
bg_image = pygame.image.load('data/bg.png')

class Ledder(pygame.sprite.Sprite):
    def __init__(self, mouse_pos):
        super().__init__()
        self.image = pygame.image.load("data/ledder.png")
        self.rect = self.image.get_rect(topleft=mouse_pos)

class LedderGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

class Platform(pygame.sprite.Sprite):
    def __init__(self, mouse_pos):
        super().__init__()
        self.image = pygame.image.load("data/platform.png")
        self.rect = self.image.get_rect(topleft=mouse_pos)

class PlatformGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

class Invisplatform(pygame.sprite.Sprite):
    def __init__(self, *pos):
        super().__init__()
        self.image = pygame.image.load("data/1x1.png")
        self.rect = pos

class InvisplatformGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()


def main():
    pygame.mixer.music.set_volume(0.5)
    platformlimit = 5
    ledderlimit = 5
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
    ledders = LedderGroup()
    invisibles = InvisplatformGroup()
    bounce = pygame.mixer.Sound('data/bounce.mp3')
    step = pygame.mixer.Sound('data/step.mp3')
    gameover = pygame.mixer.Sound('data/gameover.mp3')
    victorysound = pygame.mixer.Sound('data/victory.mp3')
    platformsound = pygame.mixer.Sound('data/platform.mp3')
    leddersound = pygame.mixer.Sound('data/ledder.mp3')
    screamsound = pygame.mixer.Sound('data/uhu.mp3')
    man = pygame.sprite.Sprite()
    man.image = pygame.image.load('data/fall.png')
    man.rect = man.image.get_rect()
    man.rect.x = 500
    man.rect.y = 0
    man_moving = True
    man_ledder = False
    scream = True
    game_over = False
    victory = False
    running = True
    invisspis = [(532, 354, 190, 20), (569, 510, 199, 20), (645, 623, 128, 20)]
    for i in invisspis:
        invisibles.add(Invisplatform(i))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if platformlimit > 0:
                        mouse_pos = pygame.mouse.get_pos()
                        new_platform = Platform(mouse_pos)
                        platforms.add(new_platform)  # Добавляем новую платформу в группу
                        platformlimit -= 1
                        platformsound.play()
                elif event.button == 3:
                    if ledderlimit > 0:
                        mouse_pos = pygame.mouse.get_pos()
                        new_ledder = Ledder(mouse_pos)
                        ledders.add(new_ledder)  # Добавляем новую платформу в группу
                        ledderlimit -= 1
                        leddersound.play()
                print(mouse_pos)
            elif event.type == pygame.KEYDOWN and not man_moving:
                if event.key == pygame.K_LEFT:
                    man.rect.x -= 10
                    step.play()
                    man.image = pygame.image.load('data/run-left.png')
                elif event.key == pygame.K_RIGHT:
                    man.rect.x += 10
                    step.play()
                    man.image = pygame.image.load('data/run-right.png')
                elif event.key == pygame.K_UP and man_ledder:
                    man.rect.y -= 10
                    leddersound.play()
                    man.image = pygame.image.load('data/fall.png')
                elif event.key == pygame.K_DOWN and man_ledder:
                    man.rect.y += 10
                    leddersound.play()
                    man.image = pygame.image.load('data/fall.png')







                fl1 = True
                if pygame.sprite.spritecollide(man, platforms, False):
                    fl1 = False
                fl2 = True
                if pygame.sprite.spritecollide(man, invisibles, False):
                    fl2 = False
                fl3 = True
                if pygame.sprite.spritecollide(man, ledders, False):
                    fl3 = False
                fl4 = True
                for platform in platforms:
                    if manlower.colliderect(platform.rect):
                        fl4 = False
                fl5 = True
                for ledder in ledders:
                    if manlower.colliderect(ledder.rect):
                        fl5 = False
                fl6 = True
                for invisplatf in invisibles:
                    if manlower.colliderect(invisplatf.rect):
                        fl6 = False
                if fl4 and fl5 and fl6:
                    man.image = pygame.image.load('data/fall.png')
                    man_moving = True
                    scream = True

        manlower = pygame.Rect(man.rect.x, man.rect.y + 50, 36, 5)
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
            for platform in platforms:
                if manlower.colliderect(platform.rect):
                    if man_moving:
                        bounce.play()
                    man_moving = False
        if pygame.sprite.spritecollide(man, ledders, False):
            if man_moving:
                bounce.play()
            man_moving = False
            man_ledder = True
        if pygame.sprite.spritecollide(man, invisibles, False):
            if man_moving:
                bounce.play()
            man_moving = False

        font = pygame.font.Font(None, 50)
        text = font.render(str(platformlimit), True, (100, 255, 100))
        text2 = font.render(str(ledderlimit), True, (255, 100, 100))
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
        screen.blit(text2, (40, 10))
        screen.blit(moon.image, (((moon.rect.x % 950) - 50), moon.rect.y))
        screen.blit(rocket.image, (((rocket.rect.x % 3000), rocket.rect.y)))
        screen.blit(finish.image, ((finish.rect.x, finish.rect.y)))
        platforms.draw(screen)  # Рисуем платформы
        ledders.draw(screen)
        invisibles.draw(screen)
        screen.blit(man.image, ((man.rect.x, man.rect.y)))
        pygame.display.flip()

def display_game_over(message):
    # Создаем затемнение
    font = pygame.font.Font(None, 74)
    font2 = pygame.font.Font(None, 50)
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)  # Устанавливаем прозрачность
    screen.blit(overlay, (0, 0))  # Рисуем затемнение на экране
    text = font.render(message, True,'white')
    text2 = font2.render("INSERT COIN", True, 'green')
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 40))
    text_rect2 = text2.get_rect(center=(screen_width // 2, screen_height // 2 + 10))
    screen.blit(text, text_rect)
    screen.blit(text2, text_rect2)
    pygame.display.flip()

if __name__ == "__main__":
    main()