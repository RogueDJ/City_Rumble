import pygame,sys,random,mysql.connector
from pygame.locals import *
from player import Player
from enemy import *
pygame.init()
clock = pygame.time.Clock()
WINDOW_SIZE = (1280,720) #velicina ekrana
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
pygame.display.set_caption("City Rumble")
background = pygame.image.load("City_Rumble/bgrd.png")
scaled_backround = pygame.transform.scale(background, WINDOW_SIZE)
bager = pygame.image.load("City_Rumble/bager.png")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 35)
score = 0
enemy_list = []
block_list = []
bullet_list = []

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="HighScoresDB"
)

cursor = db.cursor()
class falling_block:
    def __init__(self):
        self.block_speed = 2
        self.block_spawn_timer = 0
        self.block_spawn_interval = 60
    def create_falling_block(self):
        x = random.randint(0, WINDOW_SIZE[0] - 50)
        y = 0
        rect = pygame.Rect(x, y, 50, 50)
        block_list.append(rect)
def get_high_scores():
    cursor.execute("SELECT name, score, time FROM HighScores ORDER BY score DESC LIMIT 10")
    return cursor.fetchall()

def insert_high_score(name, score, time):
    cursor.execute("INSERT INTO HighScores (name, score, time) VALUES (%s, %s, %s)", (name, score, time))
    db.commit()
def death_screen():
    screen.fill(WHITE)
    screen.blit
    death_text = FONT.render("Game Over", True, BLACK)
    previous_score_text = FONT.render(f" Score: {score}", True, BLACK)
    input_text = FONT.render("Enter Your Name:", True, BLACK)

    #Show high scores
    high_scores = get_high_scores()
    y_position = 300
    number = 1
    for name, scores, time in high_scores:
        previous_score_text = FONT.render(f"{number}. Name: {name}: Score: {scores}, Time: {time}", True, BLACK)
        screen.blit(previous_score_text, (400, y_position))
        Number += 1
        y_position += 35

    screen.blit(death_text, (500, 100))
    screen.blit(input_text, (400, 250))
    pygame.display.update()

#Calling classes
block = falling_block()
player = Player(640,645)
enemy = Enemy(0,648,2,0,250)
start_time = pygame.time.get_ticks()
#Game Loop
while True: 
    screen.blit(scaled_backround,(0,0))
    screen.blit(bager,(1000,720-bager.get_height()))
    screen.blit(player.player_image,(player.x,player.y))
#moving and boundaries
    if player.moving_right == True and player.x< WINDOW_SIZE[0] - player.player_image.get_width():
        player.x += player.speed
    if player.moving_left == True and player.x > 0: 
        player.x -= player.speed
    if player.y + player.player_image.get_height() > WINDOW_SIZE[1]:
        player.y = 645
#Jump mechanic
    if player.jumping == True:
        if player.jump_count >= -10:
            neg = 1
            if player.jump_count < 0:
                neg = -1
            player.y -= (player.jump_count ** 2) * 0.4 * neg
            player.jump_count -= 1
        else:
            player.jumping = False
            player.jump_count = 10  
#Sliding
    if player.sliding == True and player.moving_right == True and player.x < 1200:
        player.player_image = player.slide_right
        player.rect = pygame.Rect(player.x,player.y,player.player_image.get_width(),player.player_image.get_height())
        player.y = 680 
        if player.slide_count >= -5:
            neg = 1
            if player.slide_count < 0:
                neg = -1
            player.x +=(player.slide_count ** 2) * 0.1 * neg
        else:
            player.sliding = False
            player.y = 635
            player.slide_count = 5
    if player.sliding == True and player.moving_left == True and player.x > 40 :
        player.player_image = player.slide_left
        player.rect = pygame.Rect(player.x,player.y,player.player_image.get_width(),player.player_image.get_height())
        player.y = 680 
        if player.slide_count >= -5:
            neg = 1
            if player.slide_count < 0:
                neg = -1
            player.x -= (player.slide_count ** 2) * 0.1 * neg
        else:
            player.sliding = False
            player.y = 635
            player.slide_count = 5


#Kicking mechanic
    player.change_direction()
    if player.direction == "right" and player.kicking == True:
        if player.kick_count > 0:
            player.player_image = player.right_kick
            player.rect = pygame.Rect(player.x,player.y,player.player_image.get_width(),player.player_image.get_height())
            player.kick_count -= 1
        else:
            player.kicking = False
            player.kick_count = 2
    elif player.direction == "left" and player.kicking == True:
        if player.kick_count > 0:
            player.player_image = player.left_kick
            player.rect = pygame.Rect(player.x,player.y,player.player_image.get_width(),player.player_image.get_height())
            player.kick_count -= 1
        else:
            player.kicking = False
            player.kick_count = 2
            
        
            
        
#Adjusting 
    player.rect.x = player.x
    player.rect.y = player.y
    enemy.rect.x = enemy.x
    enemy.rect.y = enemy.y
#Block config
    if block.block_spawn_timer <= 0:
        block.create_falling_block()
        block.block_spawn_timer = block.block_spawn_interval
    else:
        block.block_spawn_timer -= 1

    for rect in block_list:
        pygame.draw.rect(screen, (255, 0, 0), rect)
        rect.y += block.block_speed
#Enemy AI 
    if enemy.spawn_timer <= 0:
        enemy_list.append(enemy)
        enemy.spawn_timer = enemy.spawn_interval
    else:
        enemy.spawn_timer -= 1
    for enemies in enemy_list:
        if len(enemy_list) > 0:
            screen.blit(enemy.img,(enemy.x,enemy.y))
    else: enemy.spawn_timer -= 1
    if enemy.x < player.x:
        enemy.direction = "right"
        enemy.img = enemy.e_img
    elif enemy.x > player.x:
        enemy.direction = "left"
        enemy.img = enemy.flipped_img
    if enemy.direction == "right" and enemy.x + 500 < player.x:
        enemy.x += enemy.speed
    if enemy.direction == "left" and enemy.x - 500 > player.x:
        enemy.x -= enemy.speed
    
    if enemy.spawn_timer <= 0 and len(enemy_list) > 0 and enemy.direction == "right":
        bullet = Bullet(enemy.x + 20, 670)
        bullet.direction = enemy.direction
        if enemy.spawn_timer <= 0 and enemy.x - 500 < player.x:
            bullet.active = True
            bullet_list.append(bullet)
            enemy.spawn_timer = enemy.spawn_interval

    for bullet in bullet_list:
        bullet.update()
    for bullet in bullet_list:
        pygame.draw.rect(screen, (255, 0, 0), bullet.rect)
    if enemy.spawn_timer <= 0 and len(enemy_list) > 0 and enemy.direction == "left":
        bullet = Bullet(enemy.x - 20, 670)
        bullet.direction = enemy.direction
        if enemy.spawn_timer <= 0 and enemy.x - 500 < player.x:
            bullet.active    = True
            bullet_list.append(bullet)
            enemy.spawn_timer = enemy.spawn_interval
        for bullet in bullet_list:
            bullet.update()
    
    for bullet in bullet_list:
        if len(enemy_list) > 0:
            pygame.draw.rect(screen, (255, 0, 0), bullet.rect)
            
        
        
    
#Updating difficulty
    if score >= 10:
        block.block_spawn_interval = 55
        block.block_speed = 2.5
    if score >= 20:
        block.block_spawn_interval = 50
        block.block_speed = 3
    if score >= 30:
        block.block_spawn_interval = 45
        block.block_speed = 3.5
    if score >= 40:
        block.block_spawn_interval = 40
        block.block_speed = 4
    if score >= 50:
        block.block_spawn_interval = 35
        block.block_speed = 4.5
    for rect in block_list:
        if player.rect.colliderect(rect):
            player.lives -= 1
            block_list.remove(rect)
        elif rect.y > WINDOW_SIZE[1]:  
            block_list.remove(rect)
            score += 1 
    for bullet in bullet_list:
        if bullet.x > 1280 or bullet.x < 0:
            bullet_list.remove(bullet)
        if player.rect.colliderect(bullet):
            player.lives -= 1
            bullet_list.remove(bullet)
    for enemies in enemy_list:
        if player.kicking == True and player.rect.colliderect(enemy.rect):
            score += 5
            enemy_list.remove(enemies)
            enemy.x = random.randint(0,1280)
    
    
#Controls
    for event in pygame.event.get():   
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                player.moving_right = True
            if event.key == K_LEFT:
                player.moving_left = True
            if event.key == K_UP and not player.jumping:
                player.jumping = True
            if event.key == K_DOWN and not player.sliding and not player.jumping:
                player.sliding = True
            if event.key == K_x:
                player.kicking = True
            
                
            # if event.key == K_c 

        if event.type == KEYUP:
            if event.key == K_DOWN:
                player.sliding = False
                player.player_image = player.p_image
                player.rect = pygame.Rect(player.x,player.y,player.player_image.get_width(),player.player_image.get_height())
            if event.key == K_RIGHT:
                player.moving_right = False
            if event.key == K_LEFT:
                player.moving_left = False
            if event.key == K_x:
                player.kicking = False
                player.player_image = player.p_image
                player.rect = pygame.Rect(player.x,player.y,player.player_image.get_width(),player.player_image.get_height())

    #UI
    font = pygame.font.Font(None, 36)
    current_time = pygame.time.get_ticks()
    delta_time = (current_time - start_time) // 1000
    score_text = font.render(f"Score: {score}", True, BLACK)
    lives_text = font.render(f"Lives: {player.lives}", True, BLACK)
    time_text = font.render(f"Time: {delta_time}", True,BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text,(10,40))
    screen.blit(time_text, (10,70))
    #Initalizing death screen
    if player.lives == 0:
        death_screen()
        score_text = FONT.render(f"Score:{score}", False, BLACK)
        time_text = FONT.render(f"Time: {delta_time}", False,BLACK)
        screen.blit(score_text, (450, 150))
        screen.blit(time_text, (600,150))
        player_name = ""
        input_active = True
        while input_active:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        input_active = False
                    elif event.key == K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode
            input_area = pygame.Rect(610, 250, 400, 36)
            pygame.draw.rect(screen, WHITE, input_area)
            input_surface = FONT.render(player_name, True, BLACK)
            screen.blit(input_surface, (610, 250))

            pygame.display.update()
            
        
        insert_high_score(player_name, score, delta_time)
        pygame.quit()
        sys.exit()
#Frame config               
    pygame.display.update() 
    clock.tick(60)  
