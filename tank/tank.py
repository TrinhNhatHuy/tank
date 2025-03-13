import pgzrun
import random

WIDTH = 800
HEIGHT = 600
SIZE_TANK = 25
walls=[]
bullets=[]
bullets_holdoff = 0
enemy_move_count = 0
enemy_bullets = []
game_over = False
level_up = False
enemies = []
number_of_enemies = 5
level = 0

tank = Actor('tank_blue')
tank2 = Actor('tank_dark')
background = Actor('grass')

def start_game(number_of_enemies):
    global game_over, level_up, enemies, bullets, bullets_holdoff, enemy_bullets,walls
    game_over=False
    level_up = False
    enemies = []
    walls = []
    bullets = []
    bullets_holdoff = 0
    enemy_bullets = []
    
#enemy tank
    for i in range(number_of_enemies):
        enemy = Actor('tank_red')
        posi = i*100 + 50
        
        while (posi > WIDTH):
            posi -= WIDTH
        enemy.x = posi
        enemy.y = SIZE_TANK
        enemy.angle =270
        enemies.append(enemy)
#ally tank
    tank.pos = (WIDTH/2 + 50, HEIGHT - SIZE_TANK)
    tank.angle = 90
    
    tank2.pos = (WIDTH/2 - 50, HEIGHT - SIZE_TANK)
    tank2.angle = 90
#set up environment
    for x in range(16):
        for y in range(10):
            if random.randint(0,100) < 50:
                wall = Actor('wall')
                wall.x = x*50 + SIZE_TANK
                wall.y = y*50 +SIZE_TANK*3
                walls.append(wall)
#set up ally tank
def tank_set():
    move_tank(tank, keyboard.left, keyboard.right, keyboard.up, keyboard.down)
    move_tank2(tank2, keyboard.a,keyboard.d,keyboard.w, keyboard.s)
    
def move_tank2(tank, left, right, up, down):  
    original_x = tank.x
    original_y = tank.y
    if left:
        tank.x = tank.x -6
        tank.angle =180
    elif right:
        tank.x = tank.x +6
        tank.angle = 0
    elif up:
        tank.y = tank.y - 6
        tank.angle = 90
    elif down:
        tank.y =  tank.y + 6
        tank.angle =270
        
    if tank.collidelist(walls)!= -1:
        tank.x = original_x
        tank.y = original_y
    if tank.x < SIZE_TANK or tank.x>(WIDTH-SIZE_TANK)or tank.y < SIZE_TANK or tank.y > (HEIGHT-SIZE_TANK):  
        tank.x = original_x
        tank.y = original_y
    
def move_tank(tank, left, right, up, down):  
    original_x = tank.x
    original_y = tank.y
    if left:
        tank.x = tank.x -2
        tank.angle =180
    elif right:
        tank.x = tank.x +2
        tank.angle = 0
    elif up:
        tank.y = tank.y - 2
        tank.angle = 90
    elif down:
        tank.y =  tank.y + 2
        tank.angle =270
        
    if tank.collidelist(walls)!= -1:
        tank.x = original_x
        tank.y = original_y
    if tank.x < SIZE_TANK or tank.x>(WIDTH-SIZE_TANK)or tank.y < SIZE_TANK or tank.y > (HEIGHT-SIZE_TANK):  
        tank.x = original_x
        tank.y = original_y
#setup ally bullet
def tank_bullets_set():
    global bullets_holdoff
    shoot_bullet(tank, lambda:keyboard.l)
    shoot_bullet2(tank2, lambda:keyboard.f)
    
def shoot_bullet2(tank, key):
    global bullets_holdoff,level_up
    
    if bullets_holdoff==0 and key:
        
        bullet = Actor ('bulletdark2')
        bullet.angle = tank.angle
        if bullet.angle == 0:
            bullet.pos = (tank.x + SIZE_TANK, tank.y)
        elif bullet.angle == 180:
            bullet.pos = (tank.x - SIZE_TANK, tank.y)
        elif bullet.angle == 90:
            bullet.pos = (tank.x, tank.y - SIZE_TANK)
        elif bullet.angle ==270:
            bullet.pos = (tank.x, tank.y + SIZE_TANK)
        bullets.append(bullet)
        bullets_holdoff = 50
    else:
        bullets_holdoff -= 1
    
    for bullet in bullets:
        if bullet.angle == 0:
            bullet.x += 20
        if bullet.angle ==180:
            bullet.x -= 20
        if bullet.angle == 90:
            bullet.y -= 20
        if bullet.angle == 270:
            bullet.y += 20
    
    for bullet in bullets[:]:
        walls_index = bullet.collidelist(walls)
        if walls_index != -1:
            del walls[walls_index]
            bullets.remove(bullet)
        
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y >HEIGHT:
            bullets.remove(bullet)
        
        enemy_index = bullet.collidelist(enemies)
        if enemy_index != -1:
            del enemies[enemy_index]
            bullets.remove(bullet)
            continue
        
        if not enemies:
            level_up = True

def shoot_bullet(tank, key):
    global bullets_holdoff,level_up
    
    if bullets_holdoff==0 and key:
        
        bullet = Actor ('bulletblue2')
        bullet.angle = tank.angle
        if bullet.angle == 0:
            bullet.pos = (tank.x + SIZE_TANK, tank.y)
        elif bullet.angle == 180:
            bullet.pos = (tank.x - SIZE_TANK, tank.y)
        elif bullet.angle == 90:
            bullet.pos = (tank.x, tank.y - SIZE_TANK)
        elif bullet.angle ==270:
            bullet.pos = (tank.x, tank.y + SIZE_TANK)
        bullets.append(bullet)
        bullets_holdoff = 20
    else:
        bullets_holdoff -= 1
    
    for bullet in bullets:
        if bullet.angle == 0:
            bullet.x += 5
        if bullet.angle ==180:
            bullet.x -= 5
        if bullet.angle == 90:
            bullet.y -= 5
        if bullet.angle == 270:
            bullet.y += 5
    
    for bullet in bullets[:]:
        walls_index = bullet.collidelist(walls)
        if walls_index != -1:
            del walls[walls_index]
            bullets.remove(bullet)
        
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y >HEIGHT:
            bullets.remove(bullet)
        
        enemy_index = bullet.collidelist(enemies)
        if enemy_index != -1:
            del enemies[enemy_index]
            bullets.remove(bullet)
            continue
        
        if not enemies:
            level_up = True

def enemy_set():
    global enemy_move_count, bullets_holdoff 
    for enemy in enemies:

        original_x=enemy.x
        original_y =enemy.y
        choice = random.randint(0,2)

        if enemy_move_count > 0:
            enemy_move_count -= 1
            if enemy.angle == 0:
                enemy.x += 2
            elif enemy.angle == 180:
                enemy.x -= 2
            elif enemy.angle == 90:
                enemy.y -=2
            elif enemy.angle == 270:
                enemy.y += 2
                
            if enemy.x < SIZE_TANK or enemy.x > (WIDTH-SIZE_TANK) or enemy.y < SIZE_TANK or enemy.y > (HEIGHT-SIZE_TANK) or enemy.collidelist(walls) != -1:
                enemy.x = original_x
                enemy.y = original_y
                enemy_move_count = 0
                
            if enemy.collidelist(walls) != -1:
                enemy.x = original_x
                enemy.y = original_y
                enemy_move_count = 0


        elif choice == 0:
                enemy_move_count =30
        elif choice == 1: #enemy tank change direction
                enemy.angle = random.choice([0,90,180,270])
                
        else: #enemy fire
            if bullets_holdoff == 0:
                bullet = Actor('bulletred2')
                bullet.angle = enemy.angle
                bullet.pos = enemy.pos
                enemy_bullets.append(bullet)
                bullets_holdoff = 40

def enemy_bullets_set():
    global enemies, game_over
    for bullet in enemy_bullets:
        if bullet.angle == 0:
            bullet.x +=5
        if bullet.angle == 180:
            bullet.x -= 5
        if bullet.angle ==90 :
            bullet.y -= 5
        if bullet.angle == 270:
            bullet.y +=5
            
        for bullet in enemy_bullets[:]: #iterate over a copy of the list
            wall_index = bullet.collidelist(walls)
            if wall_index != -1:
                del walls[wall_index]
                enemy_bullets.remove(bullet)
                continue #skip further check for this bullet
            
            if bullet.x < 0 or bullet.x >WIDTH or bullet.y < 0 or bullet.y >HEIGHT:
                enemy_bullets.remove(bullet)
                continue
            
            if bullet.colliderect(tank) or bullet.colliderect(tank2):
                game_over = True 
                enemies = []
                break
            
def update():
    global game_over, level_up, level
    if keyboard.r and game_over: #restart
        start_game(number_of_enemies)
    elif keyboard.r and level_up: #level up
        level += 1
        start_game(number_of_enemies+2*level)
    elif keyboard.q: #quit
        import sys
        sys.exit()
    if not game_over and not level_up: #regular update if gamr is not over
        tank_set()
        tank_bullets_set()
        enemy_set()
        enemy_bullets_set()
        
        
def draw(): 
    global level
    if game_over:
        screen.fill((0,0,0))
        screen.draw.text('LOSE!', (260,250), color = (255,255,255), fontsize = 100)
        screen.draw.text('press \'q\' to exit', (10,10), color = (255,255,255), fontsize = 20)
        screen.draw.text('press \'r\' to restart the game', (10, HEIGHT - 10), color = (255,255,255), fontsize = 20)
    elif len(enemies)==0:
        screen.fill((0,0,0))
        screen.draw.text('YOU WON',(260,250),color=(255,255,255), fontsize=100)
        screen.draw.text('press q to exit', (10,10), color=(255,255,255),fontsize=20)
        screen.draw.text('press r to restart', (10, HEIGHT-10),color = (255,255,255),fontsize=20)
    else:
        
        background.draw()
        screen.draw.text('Level : ' + str(level) ,(WIDTH/2 -80, HEIGHT/2 -50),color = (255,255,100), fontsize = 100)
        tank.draw()
        tank2.draw()
        for wall in walls:
            wall.draw()
        for bullet in bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()
        for bullet in enemy_bullets:
            bullet.draw()
            
start_game(number_of_enemies)
pgzrun.go()
        
                
            
        
                
                
               
    