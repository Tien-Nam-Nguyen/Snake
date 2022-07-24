import pygame

WIDTH, HEIGHT = 1000, 600
PADDLE_SIZE = (20, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
R = 10
PADDLE_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))


def draw(left_rect, right_rect):
    window.fill(WHITE)
    pygame.draw.rect(window, BLACK, left_rect)
    pygame.draw.rect(window, BLACK, right_rect)
    # pygame.draw.circle(window, BLACK, (left_rect.x + left_rect.width + R, HEIGHT / 2), R, 0)
    pygame.display.update()


def key_handle(key, left_rect, right_rect):
    if key == pygame.K_w and left_rect.y - PADDLE_VEL >= 0:
        left_rect.y -= PADDLE_VEL
    if key == pygame.K_s and left_rect.y + left_rect.height + PADDLE_VEL <= HEIGHT:
        left_rect.y += PADDLE_VEL

    if key == pygame.K_UP and right_rect.y - PADDLE_VEL >= 0:
        right_rect.y -= PADDLE_VEL
    if key == pygame.K_DOWN and right_rect.y + right_rect.height + PADDLE_VEL <= HEIGHT:
        right_rect.y += PADDLE_VEL


def main():
    run = True
    clock = pygame.time.Clock()
    left_rect = pygame.Rect((0, HEIGHT / 2 - PADDLE_SIZE[1] / 2), PADDLE_SIZE)
    right_rect = pygame.Rect((WIDTH - PADDLE_SIZE[0], HEIGHT / 2 - PADDLE_SIZE[1] / 2), PADDLE_SIZE)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        key = pygame.key.get_pressed()
        key_handle(key, left_rect, right_rect)
        draw(left_rect, right_rect)
    pygame.quit()


if __name__ == '__main__':
    main()
