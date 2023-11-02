import pygame
from pygame.locals import *
import random

from pygame.sprite import *
pygame.init()

height = 500
width = 500
# mau game
gray =(100, 100, 100)
green = (0, 187, 18)
yellow = (255, 233, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# set kích thước màn chơi
screen = pygame.display.set_mode((height, width))
# ----------- THEM DOI TUONG GAME -------------

# tao bien
speed = 2
score = 0
lane_move_y = 0
player_x = 250
player_y = 400
game_over = False


# kích thước đường xe chạy
road_width = 300
road = (100, 0, road_width, height)

# lane
lane_left = 150
lane_center = 250
lane_right = 350
lanes = [lane_left, lane_center, lane_right]

# Biên đường
street_width = 10
street_height = 100
edge_left = (95, 0, street_width, height)
edge_right = (395, 0, street_width, height)

# khởi tạo dối tượng nhân vật chính
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        # scale images
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

# Đối tượng nhân vật chính
class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('./images/car.png')
        super().__init__(image, x, y)

player_group = pygame.sprite.Group()
Vehicle_group = pygame.sprite.Group()
# Tạo xe 
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# Tao xe luu thong
list_image = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_image = []

for name in list_image:
    image = pygame.image.load('images/' + name) 
    vehicle_image.append(image)

crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()

# Cai dat fps
fps = 120
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Điều khiển xe
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > lane_left:
                player.rect.x -=100
            if event.key == K_RIGHT and player.rect.center[0] < lane_right:
                player.rect.x +=100
            # xử lý va chạm
            for vehicle in Vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    game_over = True
    if pygame.sprite.spritecollide(player, Vehicle_group, True):
        game_over = True
        crash_rect.center = [player.rect.center[0], player.rect.top]

    clock.tick(70)
    
    # Đổ màu nền
    screen.fill(green)
    # vẽ road - đường chạy
    pygame.draw.rect(screen, gray, road)

    # Vẽ biên đường
    pygame.draw.rect(screen, yellow, edge_left)
    pygame.draw.rect(screen, yellow, edge_right)

    lane_move_y += speed *2
    if lane_move_y >= street_height * 2:
        lane_move_y = 0
    for j in range(street_height * -2, height, street_height * 2):
        pygame.draw.rect(screen, white, (lane_left + 45, j+ lane_move_y, street_width, street_height))
        pygame.draw.rect(screen, white, (lane_center + 45, j+ lane_move_y, street_width, street_height))
    

    # Vẽ nhân vật chính
    player_group.draw(screen)

    # Ve xe luu thong tren duong
    if len(Vehicle_group) < 2:
        add_vehicle = True
        for vehicle in Vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False
        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(vehicle_image)
            vehicle = Vehicle(image, lane, height / -2)
            Vehicle_group.add(vehicle)

    # cho xe chay
    for vehicle in Vehicle_group:
        vehicle.rect.y += speed
        # xoa xe luu thong
        if vehicle.rect.top >=height:
            vehicle.kill()
            score +=1
            # Tang do kho game
            if score > 0 and score % 5 == 0:
                speed += 1

    Vehicle_group.draw(screen)

    # thêm điểm
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render(f'Score: {score}', True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 40)
    screen.blit(text, text_rect)

    if game_over:
        screen.blit(crash, crash_rect)
        pygame.draw.rect(screen, red, (0, 50, width, 100))
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'Game Over! Play again? (Y/N)', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width/2, 100)
        screen.blit(text, text_rect)

    pygame.display.update()

    while game_over:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                game_over = False
                running = False
            if event.type == KEYDOWN:
                if event.key == K_y:
                    # reset game
                    game_over = False
                    score = 0
                    speed = 2
                    Vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                if event.key == K_n:
                    game_over = False
                    running = False
pygame.quit()