import pgzrun
import random
import math

WIDTH = 800
HEIGHT = 600
SIZE_TANK = 25
button_level_up = Actor("level_up") # Rect(200, 400, 150, 50)  (x, y, width, height)
button_quit = Actor("quit") # Rect(450, 400, 150, 50)
button_level_up.pos = (275, 400)
button_quit.pos = (525, 400)
background_outside = Actor("background")
background_outside.pos = (WIDTH/2 + 400, HEIGHT/2)

instruction = Actor("instruction")
instruction.pos = (150,100)

walls = []
enemy_bullets = []
enemies = []
speed_list = []
laser_list = []
death_tank_list = []

number_of_enemies = 5
level = 1
direction_moving_background = 1

game_over = False
level_up = False
start_the_game = True
run_piano = False
level_boss = False

class Tank:
    def __init__(self, image, hp):
        self.image = Actor(image)
        self.hp = hp
        self.max_hp = hp
        self.bullets = []
        self.bullets_holdoff = 0
        self.boost_speed = 0
        self.has_laser = False

    def move_tank(self, left, right, up, down):
        original_x = self.image.x
        original_y = self.image.y
        if left and self in our_tank:
            self.image.x = self.image.x - (2 + self.boost_speed)
            self.image.angle =180
        elif right and self in our_tank:
            self.image.x = self.image.x + (2 + self.boost_speed)
            self.image.angle = 0
        elif up and self in our_tank:
            self.image.y = self.image.y - (2 + self.boost_speed)
            self.image.angle = 90
        elif down and self in our_tank:
            self.image.y =  self.image.y + (2 + self.boost_speed)
            self.image.angle =270
            
        if self.image.collidelist(walls)!= -1:
            self.image.x = original_x
            self.image.y = original_y
        if self.image.x < SIZE_TANK or self.image.x>(WIDTH-SIZE_TANK)or self.image.y < SIZE_TANK or self.image.y > (HEIGHT-SIZE_TANK):  
            self.image.x = original_x
            self.image.y = original_y
            
        for speed in speed_list[:]:
            if speed.colliderect(self.image):
                speed_list.remove(speed)
                if (self.boost_speed != 2):
                    self.boost_speed += 2
                    clock.schedule_unique(self.reset_boost, 5.0)
        
        for laser in laser_list[:]:
            if laser.colliderect(self.image):
                laser_list.remove(laser)
                self.has_laser = True

    def shoot_bullet(self, key, bullet_color):
        global level_up, level_boss
        
        if self.has_laser and key and self in our_tank:
            sounds.lazer.play()
            self.shoot_laser()
            self.has_laser = False
            self.boost_speed = -2
            clock.schedule_unique(self.reset_boost, 0.5)
            self.bullets_holdoff = 50
            
        elif self.bullets_holdoff == 0 and key and self in our_tank: 
            bullet = Actor (bullet_color)
            bullet.angle = self.image.angle
            if bullet.angle == 0:
                bullet.pos = (self.image.x + SIZE_TANK, self.image.y)
            elif bullet.angle == 180:
                bullet.pos = (self.image.x - SIZE_TANK, self.image.y)
            elif bullet.angle == 90:
                bullet.pos = (self.image.x, self.image.y - SIZE_TANK)
            elif bullet.angle ==270:
                bullet.pos = (self.image.x, self.image.y + SIZE_TANK)
            self.bullets.append(bullet)
            self.bullets_holdoff = 20
        else:
            self.bullets_holdoff = max(0, self.bullets_holdoff - 1)
        
        for bullet in self.bullets:
            if bullet.angle == 0:
                bullet.x += 3
            if bullet.angle ==180:
                bullet.x -= 3
            if bullet.angle == 90:
                bullet.y -= 3
            if bullet.angle == 270:
                bullet.y += 3
        if level_boss:
            for bullet in self.bullets[:]:
                if bullet.colliderect(tank_boss.image):
                    tank_boss.hp -= 10
                    sounds.collide_boss.play()
                    if tank_boss.hp <= 0:
                        level_boss = False
                    self.bullets.remove(bullet)
        else:
            for bullet in self.bullets[:]:
                walls_index = bullet.collidelist(walls)
                if walls_index != -1:
                    sounds.gun10.play()
                    del walls[walls_index]
                    self.bullets.remove(bullet)
                
                if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y >HEIGHT:
                    self.bullets.remove(bullet)
                
                enemy_index = bullet.collidelist([enemy.image for enemy in enemies])
                if enemy_index != -1:
                    enemies[enemy_index].hp -= 10
                    if enemies[enemy_index].hp <= 0:
                        sounds.exp.play()
                        tank_is_dead(enemies, enemy_index)
                    self.bullets.remove(bullet)
                    continue
                
                if (not enemies) and (not level_boss):
                    sounds.level_up.play()
                    level_up = True

    def shoot_laser(self):
        global level_up, level_boss
        
        kame1 = Actor("kame1")
        kame1.angle = self.image.angle
        if kame1.angle == 0:
            kame1.pos = (self.image.x + 200, self.image.y)
        elif kame1.angle == 180:
            kame1.pos = (self.image.x - 200, self.image.y)
        elif kame1.angle == 90:
            kame1.pos = (self.image.x, self.image.y - 200)
        elif kame1.angle ==270:
            kame1.pos = (self.image.x, self.image.y + 200)
        kame.append(kame1)
        clock.schedule_unique(remove_kame, 0.5)
        
        if level_boss:
            if kame1.colliderect(tank_boss.image):
                tank_boss.hp -= 50
                if tank_boss.hp <= 0:
                    sounds.exp.play()
                    level_boss = False
        else:
            for kamejoko in kame[:]:
                wall_indices = kamejoko.collidelistall(walls)
                for index in sorted(wall_indices, reverse=True):  # Delete from the end to avoid index shift
                    del walls[index]  

                # Get all collided enemies
                enemy_indices = kamejoko.collidelistall([enemy.image for enemy in enemies])
                for index in sorted(enemy_indices, reverse=True):  
                    enemies[index].hp -= 50
                    if enemies[index].hp <= 0:
                        tank_is_dead(enemies, index)
                
                if (not enemies) and (not level_boss):
                    sounds.level_up.play()
                    level_up = True

    def reset_boost(self):
        self.boost_speed = 0

class Enemy:
    def __init__(self, image, hp):
        self.image = Actor(image)
        self.hp = hp
        self.max_hp = hp
        self.move_count = 0
        self.bullets_holdoff = 0

class Boss:
    def __init__(self, image, hp):
        self.image = Actor(image)
        self.hp = hp
        self.max_hp = hp
        self.bullets_holdoff = 0
        self.move_count = 0
        self.bullets = []
    
    def move_tank(self):
        global level_boss, game_over
        original_x=self.image.x
        original_y =self.image.y
        choice = random.randint(0,2)

        if self.move_count > 0:
            self.move_count -= 1
            if self.image.angle == 0:
                self.image.x += 2
            elif self.image.angle == 180:
                self.image.x -= 2
            elif self.image.angle == 90:
                self.image.y -=2
            elif self.image.angle == 270:
                self.image.y += 2
                
            if self.image.x < 100 or self.image.x > (WIDTH-100) or self.image.y < 100 or self.image.y > (HEIGHT-100):
                self.image.x = original_x
                self.image.y = original_y
                self.move_count = 0
                
            if self.image.collidelist(walls) != -1:
                self.image.x = original_x
                self.image.y = original_y

                self.move_count = 0

        elif choice == 0:
                self.move_count = 30
        elif choice == 1: #enemy tank change direction
                self.image.angle = random.choice([0,90,180,270])     
        else: 
            if self.bullets_holdoff == 0:
                for _ in range(random.randint(1,5)):
                    type_bullet = random.randint(0,10)
                    if type_bullet == 0:
                        bullet = Actor('bullet_boss_super')
                    else:
                        bullet = Actor('bullet_boss_normal')
                    bullet.angle = self.image.angle + random.randint(-45,45)
                    bullet.pos = self.image.pos
                    self.bullets.append(bullet)
                self.bullets_holdoff = 1
            else:
                self.bullets_holdoff = max(0, self.bullets_holdoff - 1)
            
        ally_index = self.image.collidelist([tank.image for tank in our_tank])
        if ally_index != -1:
            hit_tank = our_tank[ally_index]
            tank_is_dead(our_tank, ally_index)
            sounds.exp.play()
            if hit_tank in our_tank:
                our_tank.remove(hit_tank)
                if not our_tank:
                    sounds.game_over.play()
                    level_boss = False
                    game_over = True

    def shoot_bullet(self):
        global game_over, our_tank, level_boss
        for bullet in self.bullets:
            angle_rad = math.radians(bullet.angle)
            bullet.x += 5 * math.cos(angle_rad)
            bullet.y -= 5 * math.sin(angle_rad)
                
        for bullet in self.bullets[:]: #iterate over a copy of the list
            if bullet.x < 0 or bullet.x >WIDTH or bullet.y < 0 or bullet.y >HEIGHT:
                self.bullets.remove(bullet)
                continue

            ally_index = bullet.collidelist([tank.image for tank in our_tank])
            if ally_index != -1:
                if bullet.image == 'bullet_boss_super':
                    our_tank[ally_index].hp -= 50
                    sounds.gun9.play()
                elif bullet.image == 'bullet_boss_normal':
                    our_tank[ally_index].hp -= 20
                    sounds.gun9.play()
                if our_tank[ally_index].hp <= 0:
                    tank_is_dead(our_tank, ally_index)
                self.bullets.remove(bullet)
                continue
            
            if not our_tank:
                sounds.game_over.play()
                level_boss = False
                game_over = True 
                break      

tank_blue = Tank('tank_blue', 100)
tank_sand = Tank('tank_sand', 100)
tank_blue.image.pos = (WIDTH/2 + 50, HEIGHT - SIZE_TANK)
tank_blue.image.angle = 90

tank_sand.image.pos = (WIDTH/2 - 50, HEIGHT - SIZE_TANK)
tank_sand.image.angle = 90
our_tank = [tank_blue, tank_sand]
tank_boss = Boss('tank_boss', 500)
background = Actor('grass')

kame = []

def start_game(number_of_enemies):
    global run_piano, enemies, enemy_bullets,walls, death_tank_list, our_tank, speed_list,laser_list, kame, tank_sand, tank_blue
    sounds.piano.stop()
    run_piano = False
    enemies = []
    walls = []
    enemy_bullets = []
    speed_list = []
    laser_list = []
    death_tank_list = []
    kame = []

# ally tank
    tank_blue = Tank('tank_blue', 100)
    tank_sand = Tank('tank_sand', 100)
    our_tank = [tank_blue, tank_sand]

    tank_blue.image.pos = (WIDTH/2 + 50, HEIGHT - SIZE_TANK)
    tank_blue.image.angle = 90
    
    tank_sand.image.pos = (WIDTH/2 - 50, HEIGHT - SIZE_TANK)
    tank_sand.image.angle = 90

# enemy tank
    for i in range(number_of_enemies):
        enemy = Enemy('tank_red', 50)
        posi = i*100 + 50
        
        while (posi > WIDTH):
            posi -= WIDTH
        enemy.image.x = posi
        enemy.image.y = SIZE_TANK
        enemy.image.angle =270
        enemies.append(enemy)
    
# set up environment
    for x in range(16):
        for y in range(10):
            if random.randint(0,100) < 50:
                wall = Actor('wall')
                wall.x = x*50 + SIZE_TANK
                wall.y = y*50 +SIZE_TANK*3
                walls.append(wall)
    
    clock.schedule_unique(add_laser, 20)
    clock.schedule_unique(add_speed, 15)

def start_boss():
    global run_piano, enemies, enemy_bullets,walls, death_tank_list, our_tank, speed_list,laser_list, kame, tank_sand, tank_blue, tank_boss
    sounds.piano.stop()
    run_piano = False
    enemies = []
    walls = []
    enemy_bullets = []
    speed_list = []
    laser_list = []
    death_tank_list = []
    kame = []

# ally tank
    tank_blue = Tank('tank_blue', 100)
    tank_sand = Tank('tank_sand', 100)
    our_tank = [tank_blue, tank_sand]
    tank_boss = Boss('tank_boss', 500)

    tank_boss.image.pos = (WIDTH/2, 150)
    tank_boss.image.angle = 270

    tank_blue.image.pos = (WIDTH/2 + 50, HEIGHT - SIZE_TANK)
    tank_blue.image.angle = 90
    
    tank_sand.image.pos = (WIDTH/2 - 50, HEIGHT - SIZE_TANK)
    tank_sand.image.angle = 90
    
    clock.schedule_unique(add_laser, 5)
    clock.schedule_unique(add_speed, 15)

# set up ally tank
def tank_set():
    tank_blue.move_tank(keyboard.left, keyboard.right, keyboard.up, keyboard.down)
    tank_sand.move_tank(keyboard.a,keyboard.d,keyboard.w, keyboard.s)

#setup ally bullet
def tank_bullets_set():
    tank_blue.shoot_bullet(keyboard.l, 'bulletblue2')
    tank_sand.shoot_bullet(keyboard.f, 'bulletsand2')

def remove_kame():
    kame.clear()

def boss_set():
    tank_boss.move_tank()
    tank_boss.shoot_bullet()

def enemy_set():
    for enemy in enemies:
        original_x=enemy.image.x
        original_y =enemy.image.y
        choice = random.randint(0,2)

        if enemy.move_count > 0:
            enemy.move_count -= 1
            if enemy.image.angle == 0:
                enemy.image.x += 2
            elif enemy.image.angle == 180:
                enemy.image.x -= 2
            elif enemy.image.angle == 90:
                enemy.image.y -=2
            elif enemy.image.angle == 270:
                enemy.image.y += 2
                
            if enemy.image.x < SIZE_TANK or enemy.image.x > (WIDTH-SIZE_TANK) or enemy.image.y < SIZE_TANK or enemy.image.y > (HEIGHT-SIZE_TANK) or enemy.image.collidelist(walls) != -1:
                enemy.image.x = original_x
                enemy.image.y = original_y
                enemy.move_count = 0
                
            if enemy.image.collidelist(walls) != -1:
                enemy.image.x = original_x
                enemy.image.y = original_y

                enemy.move_count = 0

        elif choice == 0:
                enemy.move_count =30
        elif choice == 1: #enemy tank change direction
                enemy.image.angle = random.choice([0,90,180,270])     
        else: #enemy fire
            if enemy.bullets_holdoff == 0:
                bullet = Actor('bulletred2')
                bullet.angle = enemy.image.angle
                bullet.pos = enemy.image.pos
                enemy_bullets.append(bullet)
                enemy.bullets_holdoff = 20
            else:
                enemy.bullets_holdoff = max(0, enemy.bullets_holdoff - 1)

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
            sounds.gun10.play()
            del walls[wall_index]
            enemy_bullets.remove(bullet)
            continue #skip further check for this bullet
        
        if bullet.x < 0 or bullet.x >WIDTH or bullet.y < 0 or bullet.y >HEIGHT:
            enemy_bullets.remove(bullet)
            continue

        ally_index = bullet.collidelist([tank.image for tank in our_tank])
        if ally_index != -1:
            our_tank[ally_index].hp -= 10
            if our_tank[ally_index].hp <= 0:
                sounds.exp.play()
                tank_is_dead(our_tank, ally_index)
            enemy_bullets.remove(bullet)
            continue
        
        if not our_tank:
            sounds.game_over.play()
            game_over = True 
            enemies = []
            break      

def tank_is_dead(list, index):
    global death_tank_list
    death_tank = Actor('tank_dark')
    death_tank.pos = list[index].image.pos
    death_tank.angle = list[index].image.angle
    death_tank_list.append(death_tank)
    del list[index]

def add_laser():
    global game_over, laser_list
    if not game_over:
        laser_new = Actor("lazer")
        laser_new.pos = (random.randint(0,16)*50 + 25, random.randint(0,12)*50 + 25)
        laser_list.append(laser_new)
        clock.schedule(add_laser,2)
    return

def add_speed():
    global game_over, speed_list
    if not game_over:
        speed_new = Actor("speed")
        speed_new.pos = (random.randint(0,16)*50 + 25, random.randint(0,12)*50 + 25)
        speed_list.append(speed_new)
        clock.schedule(add_speed,15)
    return

def play_piano():
    sounds.piano.play()

def on_mouse_down(pos):
    global game_over, level_up, level, start_the_game, level_boss
    if start_the_game and button_level_up.collidepoint(pos): # start game
        start_the_game = False
        start_game(number_of_enemies)
    elif button_level_up.collidepoint(pos) and game_over: #restart
        level = 0
        game_over = False
        start_game(number_of_enemies)
    elif button_level_up.collidepoint(pos) and level_up: #level up
        if level%3 == 0:
            level += 1
            level_up = False
            level_boss = True
            start_boss()
        else:
            level += 1
            level_up = False
            start_game(number_of_enemies+2*level-2)    
    elif button_quit.collidepoint(pos): #quit
        import sys
        sys.exit()

def update():
    global run_piano, direction_moving_background
    if not run_piano and (start_the_game or game_over or not enemies and not level_boss):
        clock.schedule_unique(play_piano, 1.0)
        run_piano = True
    if (start_the_game or game_over or not enemies and not level_boss):
        background_outside.x -= 0.5*direction_moving_background
        if background_outside.right == 800 or background_outside.right == 1600: 
            direction_moving_background *= -1

    if not game_over and not level_up: #regular update if gamr is not over
        if level_boss:
            tank_set()
            tank_bullets_set()
            boss_set()
        else:
            tank_set()
            tank_bullets_set()
            enemy_set()
            enemy_bullets_set()

def draw_hp_bar(tank, bar_length, bar_height):
    if tank.image.image == 'tank_boss':
        x = tank.image.x - 80
        y = tank.image.y - 90
    else:
        x, y = tank.image.pos  # Tank position

    hp_ratio = tank.hp / tank.max_hp  # Calculate health percentage
    hp_bar_width = bar_length * hp_ratio  # Scale the bar according to HP

    # Background bar (gray)
    screen.draw.filled_rect(Rect((x - 22.5, y - 32.5), (bar_length+5, bar_height+5)), (50, 50, 50))

    # HP bar (green -> red based on HP)
    hp_color = (255 * (1 - hp_ratio), 255 * hp_ratio, 0)  
    screen.draw.filled_rect(Rect((x - 20, y - 30), (hp_bar_width, bar_height)), hp_color)

def draw(): 
    if start_the_game:
        background_outside.draw()
        screen.draw.text('TANK GAME', (WIDTH/2-200, HEIGHT/2-50), color = (255,25,100), fontsize = 100)
        button_level_up.draw()
        button_quit.draw()
        screen.draw.text('START', center=button_level_up.center, fontsize=30, color="white")
        screen.draw.text('QUIT', center=button_quit.center, fontsize=30, color="white")
        instruction.draw()
    elif game_over:
        background_outside.draw()
        # Draw buttons
        button_level_up.draw()
        button_quit.draw()
        screen.draw.text('RESTART', center=button_level_up.center, fontsize=30, color="white")
        screen.draw.text('QUIT', center=button_quit.center, fontsize=30, color="white")

        screen.draw.text('LOSE!', (300,250), color = (255,0,0), fontsize = 100)
    elif level_up and (not level_boss):
        background_outside.draw()
        # Draw buttons
        button_level_up.draw()
        button_quit.draw()
        screen.draw.text("LEVEL UP", center=button_level_up.center, fontsize=30, color="white")
        screen.draw.text("QUIT", center=button_quit.center, fontsize=30, color="white")

        screen.draw.text('YOU WON',(240,250),color=(0,255,255), fontsize=100)
    else:
        screen.clear()
        background.draw()
        screen.draw.text('Level : ' + str(level) ,(10, HEIGHT - 35),color = (255,255,100), fontsize = 40)
    
        for wall in walls:
            wall.draw()
        for tank in our_tank:
            tank.image.draw()
            draw_hp_bar(tank, 40, 3)
        for enemy in enemies:
            enemy.image.draw()
            draw_hp_bar(enemy, 40, 3)
        if not tank_blue.has_laser:
            for bullet in tank_blue.bullets:
                bullet.draw()
        if not tank_sand.has_laser:
            for bullet in tank_sand.bullets:
                bullet.draw()
        for bullet in enemy_bullets:
            bullet.draw()
        for laser in laser_list:
            laser.draw()
        for speed in speed_list:
            speed.draw()
        for death_tank in death_tank_list:
            death_tank.draw()
        for laser in laser_list:   
            laser.draw()
        for kamejoko in kame: 
            kamejoko.draw()
        if level_boss:
            tank_boss.image.draw()
            draw_hp_bar(tank_boss,200, 10)
            for bullet in tank_boss.bullets:
                bullet.draw()

pgzrun.go()