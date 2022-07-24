import pygame

pygame.font.init()
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 900, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tin tin craft")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
# load spaceship image
red_spaceship_img = pygame.image.load('Assets/spaceship_red.png')
red_spaceship = pygame.transform.rotate(pygame.transform.scale(red_spaceship_img, (60, 60)), 90)
yellow_spaceship_img = pygame.image.load('Assets/spaceship_yellow.png')
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(yellow_spaceship_img, (60, 60)), 270)
space_img = pygame.image.load('Assets/space.png')
space = pygame.transform.scale(space_img, (WIDTH, HEIGHT))
BORDER = pygame.Rect((WIDTH / 2 - 3, 0), (6, 500))
FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')
HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
WIN_SOUND = pygame.mixer.Sound('Assets/JKL83NH-video-game-win.mp3')
BULLET_SIZE = (12, 6)

HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
red_bullets = []
yellow_bullets = []

red_health = 100
yellow_health = 100


def draw(red_rect, yellow_rect):
    global red_health, yellow_health
    window.blit(space, (0, 0))
    pygame.draw.rect(window, RED, BORDER)
    window.blit(red_spaceship, red_rect)
    window.blit(yellow_spaceship, yellow_rect)
    for bullet in red_bullets:
        pygame.draw.rect(window, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(window, YELLOW, bullet)

    if red_health != 0 and yellow_health != 0:
        red_text = HEALTH_FONT.render(f'Health: {red_health}', True, RED)
        yellow_text = HEALTH_FONT.render(f'Health: {yellow_health}', True, YELLOW)
        window.blit(red_text, (10, 10))
        window.blit(yellow_text, (WIDTH - 10 - yellow_text.get_width(), 10))
    else:
        win_text = HEALTH_FONT.render('YOU WIN', True, YELLOW)
        window.blit(win_text, (WIDTH/2 - win_text.get_width()//2, HEIGHT/2 - win_text.get_height()//2))
        WIN_SOUND.play()
    pygame.display.update()


def handle(key, red_rect, yellow_rect):
    # red spaceship control
    if key[pygame.K_w] and red_rect.y - 3 >= 0:
        red_rect.y -= 3
    if key[pygame.K_s] and red_rect.y + red_rect.height + 3 <= 500:
        red_rect.y += 3
    if key[pygame.K_a] and red_rect.x - 3 >= 0:
        red_rect.x -= 3
    if key[pygame.K_d] and red_rect.x + red_rect.width + 3 < BORDER.x:
        red_rect.x += 3
    # yellow spaceship control
    if key[pygame.K_UP] and yellow_rect.y - 3 >= 0:
        yellow_rect.y -= 3
    if key[pygame.K_DOWN] and yellow_rect.y + yellow_rect.height + 3 <= 500:
        yellow_rect.y += 3
    if key[pygame.K_LEFT] and yellow_rect.x - 3 >= BORDER.x + BORDER.width:
        yellow_rect.x -= 3
    if key[pygame.K_RIGHT] and yellow_rect.x + yellow_rect.width + 3 <= WIDTH:
        yellow_rect.x += 3


def handle_bullets(red_rect, yellow_rect):
    global red_health, yellow_health
    global HIT_SOUND
    for bullet in red_bullets:
        bullet.x += 6
        if yellow_rect.colliderect(bullet):
            HIT_SOUND.play()
            red_bullets.remove(bullet)
            if yellow_health - 10 > 0:
                yellow_health -= 10
            else:
                yellow_health = 0
        if bullet.x == 900:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x -= 6
        if red_rect.colliderect(bullet):
            HIT_SOUND.play()
            yellow_bullets.remove(bullet)
            if red_health - 10 > 0:
                red_health -= 10
            else:
                red_health = 0
        if bullet.x + BULLET_SIZE[0] == 0:
            yellow_bullets.remove(bullet)


def main():
    run = True
    clock = pygame.time.Clock()
    red_rect = pygame.Rect((100, 300), (60, 60))
    yellow_rect = pygame.Rect((700, 300), (60, 60))
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    red_bull = pygame.Rect((red_rect.x + red_rect.width, red_rect.y + red_rect.height / 2 - 3),
                                           BULLET_SIZE)
                    red_bullets.append(red_bull)
                    FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL:
                    yellow_bull = pygame.Rect((yellow_rect.x, yellow_rect.y + yellow_rect.height / 2 - 3), BULLET_SIZE)
                    yellow_bullets.append(yellow_bull)
                    FIRE_SOUND.play()
        key = pygame.key.get_pressed()
        handle(key, red_rect, yellow_rect)
        handle_bullets(red_rect, yellow_rect)
        draw(red_rect, yellow_rect)
        if red_health == 0 or yellow_health == 0:
            pygame.time.delay(5000)
            break
    pygame.quit()


if __name__ == '__main__':
    main()
