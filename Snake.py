from turtle import right
import pygame
import numpy as np
import random

pygame.init()
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SNAKE_SIZE = (20, 20)  # 15 X 15
SPACE = 1

# Directions
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

SIN45 = np.sqrt(2) / 2

class Brain:        # 25 x 10 x 4
    
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.weights = [np.random.randn(y, x) / np.sqrt(x) for x, y in zip(self.sizes[:-2], self.sizes[1:-1])]
        self.biases = [np.random.randn(x, 1) for x in self.sizes[1:-1]]

        self.output_weight = np.random.randn(self.sizes[-1], self.sizes[-2]) / np.sqrt(self.sizes[-2])
        self.output_bias = np.random.randn(4, 1)




    def feedforward(self, a):
        for w, b in zip(self.weights, self.biases):
            a = self.sigmoid(np.dot(w, a) + b)
        a = self.softmax(np.dot(self.output_weight, a) + self.output_bias)
        return a

    
    def sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-z))


    def softmax(self, z):
        m = np.exp(z)
        return m / m.sum()



class Snake:

    def __init__(self, head_pos, x_coor, y_coor):
        self.snek_body = []
        self.x_coor = x_coor
        self.y_coor = y_coor
        self.snek_body.append(pygame.Rect(self.food_create(), SNAKE_SIZE))
        self.direction = random.randint(0, 3)
        self.score = 0  
        first_food_pos = self.food_create()
        self.food = pygame.Rect(first_food_pos, SNAKE_SIZE)
        self.movecountdown = 200

        self.brain = Brain([25, 10, 10, 4])


    def grow(self):
        new_square = None
        if self.direction == LEFT:
            new_square = pygame.Rect((self.snek_body[0].x - SNAKE_SIZE[0], self.snek_body[0].y), SNAKE_SIZE)
        if self.direction == RIGHT:
            new_square = pygame.Rect((self.snek_body[0].x + SNAKE_SIZE[0], self.snek_body[0].y), SNAKE_SIZE)
        if self.direction == UP:
            new_square = pygame.Rect((self.snek_body[0].x, self.snek_body[0].y - SNAKE_SIZE[0]), SNAKE_SIZE)
        if self.direction == DOWN:
            new_square = pygame.Rect((self.snek_body[0].x, self.snek_body[0].y + SNAKE_SIZE[0]), SNAKE_SIZE)
        self.snek_body.insert(0, new_square)

    def food_create(self):
        excep = [(z.x, z.y) for z in self.snek_body]
        while True:
            x = random.randint(0, len(self.x_coor) - 1)
            y = random.randint(0, len(self.y_coor) - 1)
            if (self.x_coor[x], self.y_coor[y]) not in excep:
                x = self.x_coor[x]
                y = self.y_coor[y]
                break
        return x, y
        
    def crossover(self, partner):
        child = Snake((500, 300), self.x_coor, self.y_coor)
        for w, child_w, partner_w in zip(self.brain.weights, child.brain.weights, partner.brain.weights):
            size = w.shape
            r = np.random.randint(0, size[0])
            c = np.random.randint(0, size[1])
            for i in range(size[0]):
                for j in range(size[1]):
                    if i < r or (i <= r and j <= c):
                        child_w[i][j] = w[i][j]
                    else:
                        child_w[i][j] = partner_w[i][j]
        
        for b, child_b, partner_b in zip(self.brain.biases, child.brain.biases, partner.brain.biases):
            r = np.random.randint(0, b.shape[0])
            for i in range(b.shape[0]):
                if i <= r:
                    child_b[i][0] = b[i][0]
                else:
                    child_b[i][0] = partner_b[i][0]

        # Output weight crossover
        sizeo = self.brain.output_weight.shape
        r = np.random.randint(0, sizeo[0])
        c = np.random.randint(0, sizeo[1])
        for i in range(sizeo[0]):
            for j in range(sizeo[1]):
                if i < r or (i <= r and j <= c):
                    child.brain.output_weight[i][j] = self.brain.output_weight[i][j]
                else:
                    child.brain.output_weight[i][j] = partner.brain.output_weight[i][j]
        
        # Output bias crossover
        r = np.random.randint(0, self.brain.output_bias.shape[0])
        for i in range(self.brain.output_bias.shape[0]):
            if i <= r:
                child.brain.output_bias[i][0] = self.brain.output_bias[i][0]
            else:
                child.brain.output_bias[i][0] = partner.brain.output_bias[i][0]
        
        return child





    def mutate(self, rate):
        for w in self.brain.weights:
            #size = w.shape
            for i in range(w.shape[0]):
                for j in range(w.shape[1]):
                    if np.random.rand() < rate:
                        w[i][j] += random.uniform(-1, 1)
                        if w[i][j] > 1:
                            w[i][j] = 1
                        elif w[i][j] < -1:
                            w[i][j] = -1
        
        for b in self.brain.biases:
            for i in range(b.shape[0]):
                if np.random.rand() < rate:
                    b[i][0] += random.uniform(-1, 1)
                if b[i][0] > 1:
                    b[i][0] = 1
                elif b[i][0] < -1:
                    b[i][0] = -1
        
        # Mutate output weight
        for i in range(self.brain.output_weight.shape[0]):
            for j in range(self.brain.output_weight.shape[1]):
                if np.random.rand() < rate:
                    self.brain.output_weight[i][j] += random.uniform(-1, 1)
                if self.brain.output_weight[i][j] > 1:
                    self.brain.output_weight[i][j] = 1
                elif self.brain.output_weight[i][j] < -1:
                    self.brain.output_weight[i][j] = -1

        # Mutate output bias
        for i in range(self.brain.output_bias.shape[0]):
            if np.random.rand() < rate:
                self.brain.output_bias[i][0] += random.uniform(-1, 1)
            if self.brain.output_bias[i][0] > 1:
                self.brain.output_bias[i][0] = 1
            elif self.brain.output_bias[i][0] < -1:
                self.brain.output_bias[i][0] = -1
        return self


                        
    def get_input(self):
        res = []
        eyes = self.snek_body[0]
        # Distances to the wall
        # D-T-N-B
        res.append(1000 - eyes.x)
        res.append(eyes.x)
        res.append(600 - eyes.y)
        res.append(eyes.y)

        # Distances to the body
        if eyes.y <= 1000 - eyes.x:
            right_up = eyes.y / SIN45
        else:
            right_up = (1000 - eyes.x) / SIN45
        res.append(right_up)

        if 1000 - eyes.x <= 600 - eyes.y:
            right_down = (1000 - eyes.x) / SIN45
        else:
            right_down = (600 - eyes.y) / SIN45
        res.append(right_down)

        if 600 - eyes.y <= eyes.x:
            left_down = (600 - eyes.y) / SIN45
        else:
            left_down = eyes.x / SIN45
        res.append(left_down)

        if eyes.x <= eyes.y:
            left_up = eyes.x / SIN45
        else:
            left_up = eyes.y / SIN45
        res.append(left_up)


        # Food distances
        if eyes.y == self.food.y and self.food.x >= eyes.x:
            res.append(self.food.x - eyes.x)
        else:
            res.append(-1)
        
        if eyes.y == self.food.y and self.food.x <= eyes.x:
            res.append(eyes.x - self.food.x)
        else:
            res.append(-1)

        if eyes.x == self.food.x and self.food.y >= eyes.y:
            res.append(self.food.y - eyes.y)
        else:
            res.append(-1)
        
        if eyes.x == self.food.x and self.food.y <= eyes.y:
            res.append(eyes.y - self.food.y)
        else:
            res.append(-1)

        # Right up
        x, y = eyes.x, eyes.y
        res.append(self.vision(x, y, self.food.x, self.food.y, 20, -20))
        
        # Right down
        x, y = eyes.x, eyes.y
        res.append(self.vision(x, y, self.food.x, self.food.y, 20, 20))
       
        # Left down
        x, y = eyes.x, eyes.y
        res.append(self.vision(x, y, self.food.x, self.food.y, -20, 20))
        
       
        # Left up
        x, y = eyes.x, eyes.y
        res.append(self.vision(x, y, self.food.x, self.food.y, -20, -20))


        # Tail distances
        x, y = eyes.x, eyes.y
        res.append(self.try_tail(x, y, 20, 0))
        
        x, y = eyes.x, eyes.y
        res.append(self.try_tail(x, y, -20, 0))
        
        x, y = eyes.x, eyes.y
        res.append(self.try_tail(x, y, 0, 20))

        x, y = eyes.x, eyes.y
        res.append(self.try_tail(x, y, 0, -20))

        x, y = eyes.x, eyes.y
        res.append(self.try_tail(x, y, 20, -20))

        x, y = eyes.x, eyes.y
        res.append(self.try_tail(x, y, 20, 20))

        x, y = eyes.x, eyes.y
        res.append(self.try_tail(x, y, -20, 20))

        x, y = eyes.x, eyes.y
        res.append(self.try_tail(x, y, -20, -20))

        res.append(self.direction)

        vec = np.array(res).reshape(-1, 1)
        return vec / 1166
        
        



    def vision(self, x, y, x_target, y_target, x_trend, y_trend):
        resu = -1
        x_init = x
        y_init = y
        while True:
            if x > 1000 or y > 600 or x < 0 or y < 0:
                break
            if x == x_target and y == y_target:
                resu = np.sqrt(np.square(x - x_init) + np.square(y - y_init))
                break
            x += x_trend
            y += y_trend
        return resu




    def tail_detect(self, x, y):
        res = False
        for body in self.snek_body:
            if body.x == x and body.y == y:
                res = True
                break
        return res

    
    def try_tail(self, x, y, x_trend, y_trend):
        x_init = x
        y_init = y
        resu = -1
        while True:
            if x > 1000 or y > 600 or x < 0 or y < 0:
                break
            if self.tail_detect(x, y):
                resu = np.sqrt(np.square(x - x_init) + np.square(y - y_init))
                break
            x += x_trend
            y += y_trend
        return resu


    def predict(self, inputs):
        return np.argmax(self.brain.feedforward(inputs))

        