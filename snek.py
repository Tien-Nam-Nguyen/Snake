from operator import ge
from click import password_option
import pygame
from scipy import rand
import Snake as sna
import random
import threading
import time


from pong import BLACK

pygame.font.init()
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1000, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snek")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
FPS = 30
VEL = 1


# load spaceship image
HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
LOSE_SOUND = pygame.mixer.Sound('Assets/JKL83NH-video-game-win.mp3')

x_coor = [x for x in range(0, WIDTH - 20 + 1, 20)]
y_coor = [y for y in range(0, HEIGHT - 20 + 1, 20)]

snakes = []
for i in range(800):
    snakes.append(sna.Snake(x_coor, y_coor))
dead_snakes = []



def draw():
    window.fill(BLACK)
    for snake in snakes:
        for i in range(len(snake.snek_body)):
            pygame.draw.rect(window, GREEN, snake.snek_body[i])
        # Draw food rectangle
        pygame.draw.rect(window, RED, snake.food)
        


    # yellow_text = HEALTH_FONT.render(f'Score: {snake.score}', True, YELLOW)
    # window.blit(yellow_text, (10, 10))

    '''
    if snake.snek_body[0].x + snake.snek_body[0].width > WIDTH or snake.snek_body[0].x < 0 or \
    snake.snek_body[0].y + snake.snek_body[0].height > HEIGHT or snake.snek_body[0].y < 0 or \
    snake.snek_body[0].collidelist(snake.snek_body[1:]) != -1:
        win_text = HEALTH_FONT.render('YOU LOSE', True, YELLOW)
        window.blit(win_text, (WIDTH/2 - win_text.get_width()//2, HEIGHT/2 - win_text.get_height()//2))
        LOSE_SOUND.play()
    '''
    pygame.display.update()



def sort_score(e):
    return e.score




def main():
    run = True
    clock = pygame.time.Clock()
    gen = 1
    record = -1
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            '''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    snakes[0].direction = sna.UP
                if event.key == pygame.K_d:
                    snakes[0].direction = sna.RIGHT
                if event.key == pygame.K_s:
                    snakes[0].direction = sna.DOWN
                if event.key == pygame.K_a:
                    snakes[0].direction = sna.LEFT  '''
        
        
        for snake in snakes:
            
            next_move = snake.predict(snake.get_input())
            if next_move == sna.UP and snake.direction != sna.DOWN:
                snake.direction = sna.UP
            if next_move == sna.DOWN and snake.direction != sna.UP:
                snake.direction = sna.DOWN
            if next_move == sna.LEFT and snake.direction != sna.RIGHT:
                snake.direction = sna.LEFT
            if next_move == sna.RIGHT and snake.direction != sna.LEFT:
                snake.direction = sna.RIGHT
            
            snake.grow()

            
            
            if snake.snek_body[0].colliderect(snake.food):
                snake.score += 3000
                snake.movecountdown = 500
                x, y = snake.food_create()
                snake.food.x = x
                snake.food.y = y
            else:
                snake.snek_body.pop()
            
            snake.movecountdown -= 1
            snake.ttl += 1


        draw()
        for snake in snakes:
            if snake.snek_body[0].x + snake.snek_body[0].width > WIDTH or \
            snake.snek_body[0].x < 0 or snake.snek_body[0].y + snake.snek_body[0].height > HEIGHT or \
            snake.snek_body[0].y < 0 or snake.snek_body[0].collidelist(snake.snek_body[1:]) != -1 or snake.movecountdown <= 0:
                if snake.movecountdown <= 0:
                    snake.score -= snake.ttl * 50
                else:
                    snake.score -= 10000
                    #print('dc cong them ne')
                    snake.score = snake.score + snake.ttl * 10
                dead_snakes.insert(0, snake)
                snakes.remove(snake)
        if len(snakes) == 0 and dead_snakes[0].score < 10000000:
            dead_snakes.sort(key=sort_score, reverse=True)
            print(f'Gen {gen}:      {dead_snakes[0].score} : {dead_snakes[1].score} : {len(dead_snakes[0].snek_body)} : {len(dead_snakes)}')
            gen += 1
            for i in range(200):
                snakes.append(dead_snakes[0].crossover(dead_snakes[1]).mutate(0.05))
            
            for i in range(200):
                snakes.append(dead_snakes[2].crossover(dead_snakes[3]).mutate(0.05))

            for i in range(200):
                snakes.append(dead_snakes[4].crossover(dead_snakes[5]).mutate(0.05))

                
            for snake in dead_snakes[0:200]:
                s = sna.Snake( x_coor, y_coor)
                s.brain = snake.brain
                snakes.append(s)
            dead_snakes.clear()
        elif len(dead_snakes) > 0 and dead_snakes[0].score >= 10000000:
            break

    print(dead_snakes[0].brain.weights)
    pygame.quit()


if __name__ == '__main__':
    main()
