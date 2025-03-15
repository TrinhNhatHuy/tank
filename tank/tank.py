import pgzrun
import random

WIDTH = 800
HEIGHT = 600
SIZE_TANK = 25
walls = []
bullets_blue = []
bullets_sand = []
bullets_holdoff = 0
bullets_holdoff_blue = 0
bullets_holdoff_sand = 0
enemy_move_count = 0
enemy_bullets = []
enemies = []
speed_list = []
laser_list = []
tank_dealth = []

number_of_enemies = 5
level = 0
boost_blue = 0
boost_sand = 0

game_over = False
level_up = False

has_laser_blue = False
has_laser_sand = False

tank_blue = Actor('tank_blue')
tank_sand = Actor('tank_sand')
our_tank = [tank_blue, tank_sand]
background = Actor('grass')

kame = []

def start_game(number_of_enemies):
    global game_over, level_up, enemies, bullets_blue, bullets_sand, bullets_holdoff, bullets_holdoff_blue, bullets_holdoff_sand, enemy_bullets,walls, tank_dealth, our_tank, speed_list,laser_list,boost_sand, boost_blue,has_laser_blue,has_laser_sand, kame

    game_over=False
    level_up = False
    enemies = []
    walls = []
    bullets_blue =[]
    bullets_holdoff = 0
    bullets_holdoff_sand = 0
    bullets_holdoff_blue = 0
    bullets_sand = []
    enemy_bullets = []
    speed_list = []
    laser_list = []
    boost_sand = 0
    boost_blue = 0
    tank_dealth = []
    has_laser_blue = False
    has_laser_sand = False
    kame = []
    
# enemy tank
    for i in range(number_of_enemies):
        enemy = Actor('tank_red')
        posi = i*100 + 50
        
        while (posi > WIDTH):
            posi -= WIDTH
        enemy.x = posi
        enemy.y = SIZE_TANK
        enemy.angle =270
        enemies.append(enemy)
# ally tank
    tank_blue.pos = (WIDTH/2 + 50, HEIGHT - SIZE_TANK)
    tank_blue.angle = 90
    
    tank_sand.pos = (WIDTH/2 - 50, HEIGHT - SIZE_TANK)
    tank_sand.angle = 90
    our_tank = [tank_blue, tank_sand]
    
# set up environment
    for x in range(16):
        for y in range(10):
            if random.randint(0,100) < 50:
                wall = Actor('wall')
                wall.x = x*50 + SIZE_TANK
                wall.y = y*50 +SIZE_TANK*3
                walls.append(wall)

# set up ally tank
def tank_set():
    move_tank_blue(tank_blue, keyboard.left, keyboard.right, keyboard.up, keyboard.down)
    move_tank_sand(tank_sand, keyboard.a,keyboard.d,keyboard.w, keyboard.s)
    
def move_tank_sand(tank, left, right, up, down):
    global boost_sand, has_laser_sand
    original_x = tank.x
    original_y = tank.y
    if left:
        tank.x = tank.x - (2+boost_sand)
        tank.angle =180
    elif right:
        tank.x = tank.x + (2 + boost_sand)
        tank.angle = 0
    elif up:
        tank.y = tank.y - (2 + boost_sand)
        tank.angle = 90
    elif down:
        tank.y =  tank.y + (2 + boost_sand)
        tank.angle =270
        
    if tank.collidelist(walls)!= -1:
        tank.x = original_x
        tank.y = original_y
    if tank.x < SIZE_TANK or tank.x>(WIDTH-SIZE_TANK)or tank.y < SIZE_TANK or tank.y > (HEIGHT-SIZE_TANK):  
        tank.x = original_x
        tank.y = original_y
        
    for speed in speed_list[:]:
        if speed.colliderect(tank_sand):
            speed_list.remove(speed)
            if (boost_sand != 2):
                boost_sand += 2
                clock.schedule_unique(reset_boost_sand, 5.0)
    
    for laser in laser_list[:]:
        if laser.colliderect(tank_sand):
            laser_list.remove(laser)
            has_laser_sand = True

def move_tank_blue(tank, left, right, up, down): 
    global boost_blue, has_laser_blue
    original_x = tank.x
    original_y = tank.y
    if left:
        tank.x = tank.x - (2+ boost_blue)
        tank.angle = 180
    elif right:
        tank.x = tank.x + (2+ boost_blue)
        tank.angle = 0
    elif up:
        tank.y = tank.y - (2+ boost_blue)
        tank.angle = 90
    elif down:
        tank.y =  tank.y + (2+ boost_blue)
        tank.angle = 270
        
    if tank.collidelist(walls)!= -1:
        tank.x = original_x
        tank.y = original_y
    if tank.x < SIZE_TANK or tank.x>(WIDTH-SIZE_TANK)or tank.y < SIZE_TANK or tank.y > (HEIGHT-SIZE_TANK):  
        tank.x = original_x
        tank.y = original_y
        
    for speed in speed_list[:]:
        if speed.colliderect(tank_blue):
            speed_list.remove(speed)

            if (boost_blue != 2):
                boost_blue += 2
                clock.schedule_unique(reset_boost_blue, 5.0)
        
    for laser in laser_list[:]:
        if laser.colliderect(tank_blue):
            laser_list.remove(laser)
            has_laser_blue = True

#setup ally bullet
def tank_bullets_set():
    shoot_bullet_blue(tank_blue, keyboard.l)
    shoot_bullet_sand(tank_sand, keyboard.f)
    
def shoot_bullet_sand(tank, key):
    global bullets_holdoff_sand,level_up, tank_dealth, has_laser_sand, boost_sand
    
    if has_laser_sand and key:
        shoot_laser(tank,enemies, walls)
        has_laser_sand = False
        boost_sand = -2
        clock.schedule_unique(reset_boost_sand, 0.5)
        bullets_holdoff_sand = 50
        
    elif bullets_holdoff_sand == 0 and key: 
        bullet = Actor ('bulletsand2')
        bullet.angle = tank.angle
        if bullet.angle == 0:
            bullet.pos = (tank.x + SIZE_TANK, tank.y)
        elif bullet.angle == 180:
            bullet.pos = (tank.x - SIZE_TANK, tank.y)
        elif bullet.angle == 90:
            bullet.pos = (tank.x, tank.y - SIZE_TANK)
        elif bullet.angle ==270:
            bullet.pos = (tank.x, tank.y + SIZE_TANK)
        bullets_sand.append(bullet)
        bullets_holdoff_sand = 20
    else:
        bullets_holdoff_sand = max(0, bullets_holdoff_sand - 1)
    
    for bullet in bullets_sand:
        if bullet.angle == 0:
            bullet.x += 3
        if bullet.angle ==180:
            bullet.x -= 3
        if bullet.angle == 90:
            bullet.y -= 3
        if bullet.angle == 270:
            bullet.y += 3
    
    for bullet in bullets_sand[:]:
        walls_index = bullet.collidelist(walls)
        if walls_index != -1:
            del walls[walls_index]
            bullets_sand.remove(bullet)
        
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y >HEIGHT:
            bullets_sand.remove(bullet)
        
        enemy_index = bullet.collidelist(enemies)
        if enemy_index != -1:
            death_tank = Actor('tank_dark')
            death_tank.pos = enemies[enemy_index].pos
            tank_dealth.append(death_tank)
            del enemies[enemy_index]
            bullets_sand.remove(bullet)
            continue
        
        if not enemies:
            level_up = True

def shoot_bullet_blue(tank, key):
    global bullets_holdoff_blue,level_up, tank_dealth, has_laser_blue, boost_blue
    
    if has_laser_blue and key:
        shoot_laser(tank,enemies, walls)
        has_laser_blue = False
        bullets_holdoff_blue = 50
        boost_blue = -2
        clock.schedule_unique(reset_boost_blue, 0.5)
        
    elif bullets_holdoff_blue==0 and key:
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
        bullets_blue.append(bullet)
        bullets_holdoff_blue = 20
    else:
        bullets_holdoff_blue = max(0, bullets_holdoff_blue - 1)
    
    for bullet in bullets_blue:
        if bullet.angle == 0:
            bullet.x += 3
        if bullet.angle ==180:
            bullet.x -= 3
        if bullet.angle == 90:
            bullet.y -= 3
        if bullet.angle == 270:
            bullet.y += 3
    
    for bullet in bullets_blue[:]:
        walls_index = bullet.collidelist(walls)
        if walls_index != -1:
            del walls[walls_index]
            bullets_blue.remove(bullet)
        
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y >HEIGHT:
            bullets_blue.remove(bullet)
        
        enemy_index = bullet.collidelist(enemies)
        if enemy_index != -1:
            death_tank = Actor('tank_dark')
            death_tank.pos = enemies[enemy_index].pos
            tank_dealth.append(death_tank)
            del enemies[enemy_index]
            bullets_blue.remove(bullet)
            continue
        
        if not enemies:
            level_up = True

def remove_kame():
    global kame
    for kamejoko in kame:
        kame.remove(kamejoko)

def shoot_laser(tank,enemy_list, wall_list):
    global level_up
    
    kame1 = Actor("kame1")
    kame1.angle = tank.angle
    if kame1.angle == 0:
        kame1.pos = (tank.x + 200, tank.y)
    elif kame1.angle == 180:
        kame1.pos = (tank.x - 200, tank.y)
    elif kame1.angle == 90:
        kame1.pos = (tank.x, tank.y - 200)
    elif kame1.angle ==270:
        kame1.pos = (tank.x, tank.y + 200)
    kame.append(kame1)
    clock.schedule_unique(remove_kame, 0.5)
    
    for kamejoko in kame[:]:
        wall_indices = kamejoko.collidelistall(walls)
        for index in sorted(wall_indices, reverse=True):  # Delete from the end to avoid index shift
            del walls[index]  

        # Get all collided enemies
        enemy_indices = kamejoko.collidelistall(enemies)
        for index in sorted(enemy_indices, reverse=True):  # Delete from the end to avoid index shift
            death_tank = Actor('tank_dark')
            death_tank.pos = enemies[index].pos
            tank_dealth.append(death_tank)  # Store destroyed enemy effect
            del enemies[index]
        
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
                bullets_holdoff = 20
            else:
                bullets_holdoff = max(0, bullets_holdoff - 1)

def enemy_bullets_set():
    global enemies, game_over, our_tank
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

            ally_index = bullet.collidelist(our_tank)
            if ally_index != -1:
                death_tank = Actor('tank_dark')
                death_tank.pos = our_tank[ally_index].pos
                tank_dealth.append(death_tank)
                del our_tank[ally_index]
                enemy_bullets.remove(bullet)
                continue
            
            if not our_tank:
                game_over = True 
                enemies = []
                break

def reset_boost_blue():
    global boost_blue
    boost_blue = 0 

def reset_boost_sand():
    global boost_sand
    boost_sand = 0        
            
def new_laser():
    global laser_list
    laser_new = Actor("lazer")
    laser_new.pos = (random.randint(20,WIDTH-20), random.randint(20,HEIGHT-20))
    laser_list.append(laser_new)
    return

def add_laser():
    global game_over
    if not game_over:
        new_laser()
        clock.schedule(add_laser,2)
    return

def new_speed():
    global speed_list
    speed_new = Actor("speed")
    speed_new.pos = (random.randint(20,WIDTH-20), random.randint(20,HEIGHT-20))
    speed_list.append(speed_new)
    return

def add_speed():
    global game_over
    if not game_over:
        new_speed()
        clock.schedule(add_speed,15)
    return
    
add_laser()
add_speed()
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
        for tank in our_tank:
            tank.draw()
        for wall in walls:
            wall.draw()
        if not has_laser_blue:
            for bullet in bullets_blue:
                bullet.draw()
        if not has_laser_sand:
            for bullet in bullets_sand:
                bullet.draw()
        for enemy in enemies:
            enemy.draw()
        for bullet in enemy_bullets:
            bullet.draw()
        for laser in laser_list:
            laser.draw()
        for speed in speed_list:
            speed.draw()
        for death_tank in tank_dealth:
            death_tank.draw()
        for laser in laser_list:   
            laser.draw()
        for kamejoko in kame: 
            kamejoko.draw()
            
start_game(number_of_enemies)
pgzrun.go()