import pgzrun
import random
import math

# Constants
WIDTH = 800
HEIGHT = 600
SIZE_TANK = 25
SIZE_BLOCK = 50
BUTTON_LEVEL_UP_POS = (275, 400)
BUTTON_QUIT_POS = (525, 400)
BACKGROUND_OUTSIDE_POS = (WIDTH / 2 + 400, HEIGHT / 2)
INSTRUCTION_POS = (150, 100)
WALL_PROBABILITY = 50  # Probability of creating a wall (percentage)

# Actors
button_level_up = Actor("level_up")
button_quit = Actor("quit")
background_outside = Actor("background")
instruction = Actor("instruction")

# Global Variables
walls = []
irons = []
enemy_bullets = []
enemies = []
speed_list = []
laser_list = []
explosion_list = []
hp_list = []
death_tank_list = []
kame = []

number_of_enemies = 5
level = 3
direction_moving_background = 1

game_over = False
level_up = False
start_the_game = True
run_piano = False
level_boss = False

# Variables to show text "Boss"
show_boss_text = False  # Controls whether the "Boss" text is displayed
boss_text_scale = 1.0   # Scale factor for the "Boss" text
countdown_text = None   # Countdown text ("3", "2", "1", "Play")

# Initialize button positions
button_level_up.pos = BUTTON_LEVEL_UP_POS
button_quit.pos = BUTTON_QUIT_POS
background_outside.pos = BACKGROUND_OUTSIDE_POS
instruction.pos = INSTRUCTION_POS

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
        original_pos = self.image.pos
        movement = {
            left: (-1, 0, 180),
            right: (1, 0, 0),
            up: (0, -1, 90),
            down: (0, 1, 270)
        }
        for key, (dx, dy, angle) in movement.items():
            if key and self in our_tank:
                self.image.x += dx * (2 + self.boost_speed)
                self.image.y += dy * (2 + self.boost_speed)
                self.image.angle = angle
                break

        in_bounds = (SIZE_TANK <= self.image.x <= WIDTH - SIZE_TANK) and \
                    (SIZE_TANK <= self.image.y <= HEIGHT - SIZE_TANK)
        
        if self.image.collidelist(walls) != -1 or self.image.collidelist(irons) != -1 or not in_bounds:
            self.image.pos = original_pos
            
        self._check_collisions()

    def _check_collisions(self):
        for speed in speed_list[:]:
            if speed.colliderect(self.image):
                speed_list.remove(speed)
                if self.boost_speed != 2:
                    self.boost_speed += 2
                    clock.schedule_unique(self.reset_boost, 5.0)

        for laser in laser_list[:]:
            if laser.colliderect(self.image):
                laser_list.remove(laser)
                self.has_laser = True

        for health in hp_list[:]:
            if health.colliderect(self.image):
                hp_list.remove(health)
                self.hp = min(self.max_hp, self.hp + 20)

    def shoot_bullet(self, key, bullet_color):
        if key and self in our_tank:
            if self.has_laser:
                sounds.lazer.play()
                self.shoot_laser()
                self.has_laser = False
                self.boost_speed = -2
                clock.schedule_unique(self.reset_boost, 0.5)
                self.bullets_holdoff = 50
            elif self.bullets_holdoff == 0:
                self._create_bullet(bullet_color)
                self.bullets_holdoff = 20

        self.bullets_holdoff = max(0, self.bullets_holdoff - 1)
        self._update_bullets()

    def _create_bullet(self, bullet_color):
        bullet = Actor(bullet_color)
        bullet.angle = self.image.angle
        offset = {
            0: (SIZE_TANK, 0),
            180: (-SIZE_TANK, 0),
            90: (0, -SIZE_TANK),
            270: (0, SIZE_TANK)
        }
        dx, dy = offset[bullet.angle]
        bullet.pos = (self.image.x + dx, self.image.y + dy)
        self.bullets.append(bullet)

    def _update_bullets(self):
        for bullet in self.bullets[:]:
            angle_rad = math.radians(bullet.angle)
            bullet.x += 3 * math.cos(angle_rad)
            bullet.y -= 3 * math.sin(angle_rad)

            if not (0 <= bullet.x <= WIDTH and 0 <= bullet.y <= HEIGHT):
                self.bullets.remove(bullet)
                continue

            self._check_bullet_collisions(bullet)

    def _check_bullet_collisions(self, bullet):
        global level_up, level_boss

        if level_boss:
            # Check collision with the boss
            if bullet.colliderect(tank_boss.image) and boss_list:
                tank_boss.hp -= 10
                sounds.collide_boss.play()
                if tank_boss.hp <= 0:
                    display_explosion(boss_list, 0, 'explosion3')
                    boss_list.remove(tank_boss)
                self.bullets.remove(bullet)
                return

        # Check collision with walls
        walls_index = bullet.collidelist(walls)
        if walls_index != -1:
            sounds.gun10.play()
            del walls[walls_index]
            self.bullets.remove(bullet)
            return
        
        #check collision with irons
        irons_index = bullet.collidelist(irons)
        if irons_index != -1:
            sounds.gun10.play()
            self.bullets.remove(bullet)
            return

        # Check collision with enemies
        enemy_index = bullet.collidelist([enemy.image for enemy in enemies])
        if enemy_index != -1:
            enemies[enemy_index].hp -= 10
            if enemies[enemy_index].hp <= 0:
                sounds.exp.play()
                display_explosion(enemies, enemy_index, 'explosion4')
                tank_is_dead(enemies, enemy_index)
            self.bullets.remove(bullet)
            return

        # Check collision with AI tanks
        ai_index = bullet.collidelist([ai_tank.image for ai_tank in ai_tanks])
        if ai_index != -1:
            ai_tanks[ai_index].hp -= 10
            if ai_tanks[ai_index].hp <= 0:
                sounds.exp.play()
                display_explosion(ai_tanks, ai_index, 'explosion4')
                tank_is_dead(ai_tanks, ai_index)
            self.bullets.remove(bullet)
            return

    def shoot_laser(self):
        global level_up, level_boss, boss_list
        kame1 = Actor("kame1")
        kame1.angle = self.image.angle
        offset = {
            0: (200, 0),
            180: (-200, 0),
            90: (0, -200),
            270: (0, 200)
        }
        dx, dy = offset[kame1.angle]
        kame1.pos = (self.image.x + dx, self.image.y + dy)
        kame.append(kame1)
        clock.schedule_unique(remove_kame, 0.5)

        if level_boss:
            self._laser_collisions_boss(kame1)
        else:
            self._laser_collisions_enemies(kame1)

    def _laser_collisions_boss(self, kame1):
        if kame1.colliderect(tank_boss.image) and boss_list:
            tank_boss.hp -= 50
            if tank_boss.hp <= 0:
                display_explosion(boss_list, 0, 'explosion3')
                boss_list.remove(tank_boss)
        enemy_indices = kame1.collidelistall([enemy.image for enemy in enemies])
        for index in sorted(enemy_indices, reverse=True):
            enemies[index].hp -= 50
            if enemies[index].hp <= 0:
                display_explosion(enemies, index, 'explosion4')
                tank_is_dead(enemies, index)

    def _laser_collisions_enemies(self, kame1):
        for kamejoko in kame[:]:
            iron_indices = kamejoko.collidelistall(irons)
            if iron_indices:
                kame.remove(kamejoko)
                continue   
            
            wall_indices = kamejoko.collidelistall(walls)
            for index in sorted(wall_indices, reverse=True):
                del walls[index]

            enemy_indices = kamejoko.collidelistall([enemy.image for enemy in enemies])
            for index in sorted(enemy_indices, reverse=True):
                enemies[index].hp -= 50
                if enemies[index].hp <= 0:
                    display_explosion(enemies, index, 'explosion4')
                    tank_is_dead(enemies, index)
            
            ai_indices = kamejoko.collidelistall([ai_tank.image for ai_tank in ai_tanks])
            for index in sorted(ai_indices, reverse=True):
                ai_tanks[index].hp -= 50
                if ai_tanks[index].hp <= 0:
                    display_explosion(ai_tanks, index, 'explosion4')
                    tank_is_dead(ai_tanks, index)

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
        self.original_x, self.original_y = self.image.pos
        if self.move_count > 0:
            self.move_count -= 1
            movement = {
                0: (2, 0),
                180: (-2, 0),
                90: (0, -2),
                270: (0, 2)
            }
            dx, dy = movement.get(self.image.angle, (0, 0))
            self.image.x += dx
            self.image.y += dy
        else:
            choice = random.randint(0, 2)
            if choice == 0:
                self.move_count = 30
            elif choice == 1:
                self.image.angle = random.choice([0, 90, 180, 270])
            else:
                self._shoot_random_bullets()

        # Check for collisions or out-of-bounds
        if self.image.x < 100 or self.image.x > (WIDTH - 100) or self.image.y < 100 or self.image.y > (HEIGHT - 100) or self.image.collidelist(walls) != -1 or self.image.collidelist(irons) != -1:
            self.image.x, self.image.y = self.original_x, self.original_y
            self.move_count = 0

        # Check collision with ally tanks
        ally_index = self.image.collidelist([tank.image for tank in our_tank])
        if ally_index != -1:
            self._handle_tank_collision(ally_index)

    def _handle_tank_collision(self, ally_index):
        global level_boss, game_over
        hit_tank = our_tank[ally_index]
        tank_is_dead(our_tank, ally_index)
        sounds.exp.play()
        if hit_tank in our_tank:
            our_tank.remove(hit_tank)
            if not our_tank:
                sounds.game_over.play()
                level_boss = False
                game_over = True

    def _shoot_random_bullets(self):
        if self.bullets_holdoff == 0:
            for _ in range(random.randint(1, 5)):
                bullet_type = 'bullet_boss_super' if random.randint(0, 10) == 0 else 'bullet_boss_normal'
                bullet = Actor(bullet_type)
                bullet.angle = self.image.angle + random.randint(-45, 45)
                bullet.pos = self.image.pos
                self.bullets.append(bullet)
            self.bullets_holdoff = 1
        else:
            self.bullets_holdoff = max(0, self.bullets_holdoff - 1)

    def shoot_bullet(self):
        global game_over, our_tank, level_boss
        for bullet in self.bullets[:]:
            angle_rad = math.radians(bullet.angle)
            bullet.x += 5 * math.cos(angle_rad)
            bullet.y -= 5 * math.sin(angle_rad)

            if not (0 <= bullet.x <= WIDTH and 0 <= bullet.y <= HEIGHT):
                self.bullets.remove(bullet)
                continue
            
            # Check for collision with iron blocks
            iron_index = bullet.collidelist(irons)
            if iron_index != -1:  # Collision detected
                self.bullets.remove(bullet)  # Remove the bullet
                continue

            ally_index = bullet.collidelist([tank.image for tank in our_tank])
            if ally_index != -1:
                self._handle_bullet_collision(bullet, ally_index)

    def _handle_bullet_collision(self, bullet, ally_index):
        global game_over, level_boss
        damage = 50 if bullet.image == 'bullet_boss_super' else 20
        our_tank[ally_index].hp -= damage
        sounds.gun9.play()
        if our_tank[ally_index].hp <= 0:
            tank_is_dead(our_tank, ally_index)
        self.bullets.remove(bullet)
              
        if not our_tank:
            sounds.game_over.play()
            level_boss = False
            game_over = True

class IronBlock:
    def __init__(self, x, y):
        self.image = Actor("iron")
        self.image.pos = (x, y)
    
    def draw(self):
        self.image.draw()

class AITank:
    def __init__(self, image, hp):
        self.image = Actor(image)
        self.hp = hp
        self.max_hp = hp
        self.bullets = []
        self.bullets_holdoff = 0
        self.move_count = 0
        self.stuck_count = 0 

    # Move the AI tank towards the nearest player's tank
    def move_tank(self):
        if not our_tank:
            return

        # Find the nearest player's tank
        nearest_tank = min(our_tank, key=lambda tank: self._distance_to(tank.image))
        target_x = nearest_tank.image.x
        target_y = nearest_tank.image.y

        # Calculate the new direction using pathfinding
        new_direction = self.calculate_new_direction(
            walls, int(target_x / SIZE_BLOCK), int(target_y / SIZE_BLOCK)
        )
        if new_direction is not None:
            self.image.angle = new_direction

        # Move in the calculated direction
        self.move_forwards()

        # Check for collisions or out-of-bounds
        if self.image.collidelist(walls) != -1 or self.image.collidelist(irons) != -1 or \
           not (SIZE_TANK <= self.image.x <= WIDTH - SIZE_TANK and SIZE_TANK <= self.image.y <= HEIGHT - SIZE_TANK):
            self.move_backwards()
            self.stuck_count += 1
            if self.stuck_count > 5:  # If stuck for 5 consecutive moves
                self.image.angle = random.choice([0, 90, 180, 270])
                self.stuck_count = 0  # Reset stuck counter
        else:
            self.stuck_count = 0  # Reset stuck counter if not stuck

    # Shoot a bullet toward the nearest player's tank
    def shoot_bullet(self):
        if not our_tank or self.bullets_holdoff > 0:
            self.bullets_holdoff = max(0, self.bullets_holdoff - 1)
            return

        # Find the nearest player's tank
        nearest_tank = min(our_tank, key=lambda tank: self._distance_to(tank.image))
        dx = nearest_tank.image.x - self.image.x
        dy = nearest_tank.image.y - self.image.y

        # Calculate the angle to the player's tank
        angle = math.degrees(math.atan2(-dy, dx))

        # Create and shoot a bullet
        bullet = Actor('bulletgreen2')
        bullet.angle = angle
        bullet.pos = self.image.pos
        self.bullets.append(bullet)
        self.bullets_holdoff = 50  # Cooldown before the next shot

    # Update the AI tank's bullets
    def update_bullets(self):
        for bullet in self.bullets[:]:
            angle_rad = math.radians(self.image.angle)
            bullet.x += 5 * math.cos(angle_rad)
            bullet.y -= 5 * math.sin(angle_rad)

            # Remove bullets out of bounds
            if not (0 <= bullet.x <= WIDTH and 0 <= bullet.y <= HEIGHT):
                self.bullets.remove(bullet)
                continue

            # Check collisions with walls
            wall_index = bullet.collidelist(walls)
            if wall_index != -1:
                sounds.gun10.play()
                del walls[wall_index]
                self.bullets.remove(bullet)
                continue
                
            #check collision with irons
            iron_index = bullet.collidelist(irons)
            if iron_index != -1:
                self.bullets.remove(bullet)
                continue

            # Check collisions with player's tanks
            ally_index = bullet.collidelist([tank.image for tank in our_tank])
            if ally_index != -1:
                our_tank[ally_index].hp -= 20
                if our_tank[ally_index].hp <= 0:
                    sounds.exp.play()
                    display_explosion(our_tank, ally_index, 'explosion4')
                    tank_is_dead(our_tank, ally_index)
                self.bullets.remove(bullet)
                continue

    # Calculate the distance to a target Actor
    def _distance_to(self, target):
        dx = target.x - self.image.x
        dy = target.y - self.image.y
        return math.sqrt(dx**2 + dy**2)

    def calculate_new_direction(self, walls, dest_x, dest_y):
        map_grid = [[0 for _ in range(WIDTH // SIZE_BLOCK)] for _ in range(HEIGHT // SIZE_BLOCK)]

        # Mark walls as obstacles
        for wall in walls:
            map_x = int(wall.x / SIZE_BLOCK)
            map_y = int(wall.y / SIZE_BLOCK)
            map_grid[map_y][map_x] = 1

        # BFS queue
        queue = [{
            "x": int(self.image.x / SIZE_BLOCK),
            "y": int(self.image.y / SIZE_BLOCK),
            "moves": []
        }]

        while queue:
            current = queue.pop(0)
            if current["x"] == dest_x and current["y"] == dest_y:
                if current["moves"]:
                    return current["moves"][0]  # Return the first move in the path
                return None

            # Mark the current position as visited
            map_grid[current["y"]][current["x"]] = 1

            # Add neighbors to the queue
            neighbors = self.add_neighbors(current, map_grid)
            queue.extend(neighbors)

        return None

    # Add neighbors to the BFS queue
    def add_neighbors(self, current, map_grid):
        neighbors = []
        directions = [
            {"dx": -1, "dy": 0, "angle": 180},  # Left
            {"dx": 1, "dy": 0, "angle": 0},    # Right
            {"dx": 0, "dy": -1, "angle": 90},  # Up
            {"dx": 0, "dy": 1, "angle": 270}   # Down
        ]

        for direction in directions:
            new_x = current["x"] + direction["dx"]
            new_y = current["y"] + direction["dy"]

            if 0 <= new_x < WIDTH // SIZE_BLOCK and 0 <= new_y < HEIGHT // SIZE_BLOCK:
                if map_grid[new_y][new_x] == 0:  # Not visited and not a wall
                    new_moves = current["moves"] + [direction["angle"]]
                    neighbors.append({"x": new_x, "y": new_y, "moves": new_moves})

        return neighbors

    # Move the tank forwards based on its current angle
    def move_forwards(self):
        
        if self.image.angle == 0:  # Right
            self.image.x += 1
        elif self.image.angle == 180:  # Left
            self.image.x -= 1
        elif self.image.angle == 90:  # Up
            self.image.y -= 1
        elif self.image.angle == 270:  # Down
            self.image.y += 1

    # Move the tank backwards based on its current angle
    def move_backwards(self):
        if self.image.angle == 0:  # Right
            self.image.x -= 1
        elif self.image.angle == 180:  # Left
            self.image.x += 1
        elif self.image.angle == 90:  # Up
            self.image.y += 1
        elif self.image.angle == 270:  # Down
            self.image.y -= 1

# Add AI tanks to the game
ai_tanks = []

tank_blue = Tank('tank_blue', 100)
tank_sand = Tank('tank_sand', 100)
tank_blue.image.pos = (WIDTH/2 + 50, HEIGHT - SIZE_TANK)
tank_blue.image.angle = 90
tank_sand.image.pos = (WIDTH/2 - 50, HEIGHT - SIZE_TANK)
tank_sand.image.angle = 90
our_tank = [tank_blue, tank_sand]
tank_boss = Boss('tank_boss', 500)
boss_list = [tank_boss]

background = Actor('grass')

# Reset shared game state variables
def reset_game_state():
    """Reset all shared game state variables."""
    global run_piano, enemies, enemy_bullets, walls, death_tank_list, our_tank, speed_list, laser_list, hp_list, kame, explosion_list, irons, ai_tanks, tank_boss, boss_list, level_boss

    # Stop any ongoing sounds
    sounds.piano.stop()
    run_piano = False

    # Clear all game objects
    enemies.clear()
    walls.clear()
    enemy_bullets.clear()
    speed_list.clear()
    laser_list.clear()
    hp_list.clear()
    death_tank_list.clear()
    kame.clear()
    explosion_list.clear()
    irons.clear()
    ai_tanks.clear()

    # Reset ally tanks
    initialize_ally_tanks()

    # Reset boss tank only if it's a boss level
    if level_boss:
        tank_boss = Boss('tank_boss', 500)
        boss_list = [tank_boss]
        tank_boss.image.pos = (WIDTH / 2, 150)  # Reset position
        tank_boss.image.angle = 270
    else:
        boss_list.clear()  # Ensure boss_list is empty during non-boss levels

# Initialize ally tanks
def initialize_ally_tanks():
    global tank_blue, tank_sand, our_tank
    tank_blue = Tank('tank_blue', 100)
    tank_sand = Tank('tank_sand', 100)
    our_tank = [tank_blue, tank_sand]

    tank_blue.image.pos = (WIDTH / 2 + 50, HEIGHT - SIZE_TANK)
    tank_blue.image.angle = 90

    tank_sand.image.pos = (WIDTH / 2 - 50, HEIGHT - SIZE_TANK)
    tank_sand.image.angle = 90

def create_walls():
    for x in range(16):
        for y in range(10):
            if random.randint(0, 100) < WALL_PROBABILITY:
                wall = Actor('wall')
                wall.x = x * 50 + SIZE_TANK
                wall.y = y * 50 + SIZE_TANK * 3
                walls.append(wall)

# Start a regular game level
def start_game(number_of_enemies):
    reset_game_state()
    initialize_ally_tanks()

    # Initialize enemy tanks
    for i in range(number_of_enemies):
        enemy = Enemy('tank_red', 30 + level * 5)
        posi = i * 100 + 50
        while posi > WIDTH:
            posi -= WIDTH
        enemy.image.x = posi
        enemy.image.y = SIZE_TANK
        enemy.image.angle = 270
        enemies.append(enemy)

    # Set up environment
    create_walls()
    clock.schedule_unique(add_laser, 20)
    clock.schedule_unique(add_speed, 15)
    clock.schedule_unique(add_hp,10)

# Start a game level with AI tanks
def start_game_with_ai(number_of_enemies, number_of_ai_tanks):
    reset_game_state()
    initialize_ally_tanks()

    # Initialize enemy tanks
    for i in range(number_of_enemies):
        enemy = Enemy('tank_red', 30 + level * 5)
        posi = i * 100 + 50
        while posi > WIDTH:
            posi -= WIDTH
        enemy.image.x = posi
        enemy.image.y = SIZE_TANK
        enemy.image.angle = 270
        enemies.append(enemy)

    # Initialize AI tanks
    for i in range(number_of_ai_tanks):
        ai_tank = AITank('tank_green', 50)
        ai_tank.image.x = random.randint(SIZE_TANK, WIDTH - SIZE_TANK)
        ai_tank.image.y = SIZE_TANK
        ai_tanks.append(ai_tank)

    # Set up environment
    create_walls()
    clock.schedule_unique(add_laser, 20)
    clock.schedule_unique(add_speed, 15)
    clock.schedule_unique(add_hp, 10)

def add_iron_block(x, y):
    block = IronBlock(x, y)
    irons.append(block.image)


# Start a boss level
def start_boss():
    global show_boss_text, boss_text_scale, countdown_text, boss_list
    reset_game_state()

    # Show "Boss" text with animation
    show_boss_text = True
    boss_text_scale = 1.0
    countdown_text = None
    clock.schedule_interval(_animate_boss_text, 0.1)  # Animate "Boss" text every 0.1s

def _animate_boss_text():
    global boss_text_scale, countdown_text
    boss_text_scale += 0.5
    if boss_text_scale >= 3.0:  # Once the text reaches maximum size
        clock.unschedule(_animate_boss_text)
        countdown_text = "3"
        clock.schedule_unique(_start_countdown, 1.0)  # Start countdown after 1 second

def _start_countdown():
    global countdown_text
    if countdown_text == "3":
        countdown_text = "2"
        clock.schedule_unique(_start_countdown, 1.0)
    elif countdown_text == "2":
        countdown_text = "1"
        clock.schedule_unique(_start_countdown, 1.0)
    elif countdown_text == "1":
        countdown_text = "Play"
        clock.schedule_unique(_initialize_boss, 1.0)
        clock.schedule_unique(initialize_ally_tanks, 1.0)

def _initialize_boss():
    global tank_boss, boss_list, show_boss_text, countdown_text
    show_boss_text = False  # Stop showing the "Boss" text
    countdown_text = None   # Clear the countdown text

    # Initialize boss tank
    tank_boss = Boss('tank_boss', 500)
    boss_list = [tank_boss]

    tank_boss.image.pos = (WIDTH / 2, 150)
    tank_boss.image.angle = 270
    
    # Place iron blocks at specific locations for the boss level.
    iron_positions = [
        (WIDTH / 2 - 150, HEIGHT / 2 ),
        (WIDTH / 2 - 150, HEIGHT / 2 + 50),
        (WIDTH / 2 + 150, HEIGHT / 2 ),
        (WIDTH / 2 + 150, HEIGHT / 2 + 50)
    ]
    for pos in iron_positions:
        add_iron_block(pos[0], pos[1])
        
    # Schedule power-ups and additional enemies
    clock.schedule_unique(add_laser, 20)
    clock.schedule_unique(add_speed, 15)
    clock.schedule_unique(add_hp, 10)
    if level_boss and boss_list:
        clock.schedule_unique(add_enemy, 5)

# set up ally tank
def tank_set():
    tank_blue.move_tank(keyboard.left, keyboard.right, keyboard.up, keyboard.down)
    tank_sand.move_tank(keyboard.a, keyboard.d, keyboard.w, keyboard.s)

def tank_bullets_set():
    tank_blue.shoot_bullet(keyboard.l, 'bulletblue2')
    tank_sand.shoot_bullet(keyboard.f, 'bulletsand2')

def remove_kame():
        kame.clear()

# Enemy Management
def boss_set():
    tank_boss.move_tank()
    tank_boss.shoot_bullet()

# Handle enemy movement and shooting
def enemy_set():
    for enemy in enemies:
        original_x, original_y = enemy.image.x, enemy.image.y
        choice = random.randint(0, 2)

        if enemy.move_count > 0:
            enemy.move_count -= 1
            movement = {
                0: (2, 0),
                180: (-2, 0),
                90: (0, -2),
                270: (0, 2)
            }
            dx, dy = movement.get(enemy.image.angle, (0, 0))
            enemy.image.x += dx
            enemy.image.y += dy

            # Check for collisions or out-of-bounds
            if enemy.image.x < SIZE_TANK or enemy.image.x > (WIDTH - SIZE_TANK) or \
               enemy.image.y < SIZE_TANK or enemy.image.y > (HEIGHT - SIZE_TANK) or \
               enemy.image.collidelist(walls) != -1 or enemy.image.collidelist(irons) != -1:
                enemy.image.x, enemy.image.y = original_x, original_y
                enemy.move_count = 0
        elif choice == 0:
            enemy.move_count = 30
        elif choice == 1:
            enemy.image.angle = random.choice([0, 90, 180, 270])
        else:
            if enemy.bullets_holdoff == 0:
                bullet = Actor('bulletred2')
                bullet.angle = enemy.image.angle
                bullet.pos = enemy.image.pos
                enemy_bullets.append(bullet)
                enemy.bullets_holdoff = 20
            else:
                enemy.bullets_holdoff = max(0, enemy.bullets_holdoff - 1)

# Handle enemy bullet movement and collisions
def enemy_bullets_set():
    global game_over
    for bullet in enemy_bullets[:]:
        angle_rad = math.radians(bullet.angle)
        bullet.x += 5 * math.cos(angle_rad)
        bullet.y -= 5 * math.sin(angle_rad)

        # Remove bullets out of bounds
        if not (0 <= bullet.x <= WIDTH and 0 <= bullet.y <= HEIGHT):
            enemy_bullets.remove(bullet)
            continue

        # Check collisions with walls
        wall_index = bullet.collidelist(walls)
        if wall_index != -1:
            sounds.gun10.play()
            del walls[wall_index]
            enemy_bullets.remove(bullet)
            continue #skip further check for this bullet
        
        iron_index = bullet.collidelist(irons)
        if iron_index != -1:
            sounds.gun10.play()
            enemy_bullets.remove(bullet)
            continue
        
        if bullet.x < 0 or bullet.x >WIDTH or bullet.y < 0 or bullet.y >HEIGHT:
            enemy_bullets.remove(bullet)
            continue

        # Check collisions with ally tanks
        ally_index = bullet.collidelist([tank.image for tank in our_tank])
        if ally_index != -1:
            our_tank[ally_index].hp -= 20
            if our_tank[ally_index].hp <= 0:
                sounds.exp.play()
                display_explosion(our_tank, ally_index, 'explosion4')
                tank_is_dead(our_tank, ally_index)
            enemy_bullets.remove(bullet)
            continue

        # Check if all ally tanks are destroyed
        if not our_tank:
            sounds.game_over.play()
            game_over = True
            enemies.clear()
            break

def tank_is_dead(list, index):
    global death_tank_list
    if index < 0 or index >= len(list) or not list:
        return
    death_tank = Actor('tank_dark')
    death_tank.pos = list[index].image.pos
    death_tank.angle = list[index].image.angle
    death_tank_list.append(death_tank)
    del list[index]

def display_explosion(list, index ,image):
    global explosion_list
    if index < 0 or index >= len(list) or not list:
        return
    explosion = Actor(image)
    explosion.pos = list[index].image.pos
    explosion_list.append(explosion)
    clock.schedule_unique(remove_explosion, 0.5)

def remove_explosion():
    explosion_list.clear()

def add_laser():
    global laser_list
    if not game_over:
        laser_new = Actor("lazer")
        laser_new.pos = (random.randint(0,16)*50 + 25, random.randint(0,12)*50 + 25)
        laser_list.append(laser_new)
        clock.schedule(add_laser,20)
    return

def add_hp():
    global hp_list
    if not game_over:
        hp_new = Actor("health")
        hp_new.pos = (random.randint(0,16)*50 + 25, random.randint(0,12)*50 + 25)
        hp_list.append(hp_new)
        clock.schedule(add_hp,10)
    return

def add_speed():
    global speed_list
    if not game_over:
        speed_new = Actor("speed")
        speed_new.pos = (random.randint(0,16)*50 + 25, random.randint(0,12)*50 + 25)
        speed_list.append(speed_new)
        clock.schedule(add_speed,15)
    return

def add_enemy():
    global enemies
    if not game_over and level_boss and boss_list:
        new_enemy = Enemy("tank_red", 20)
        new_enemy.image.pos = (tank_boss.image.x + random.randint(0,1)*150 -75, tank_boss.image.y+ random.randint(0,1)*150 - 75)
        enemies.append(new_enemy)
        clock.schedule(add_enemy, random.randint(5,10))
    return

def play_piano():
    """Play the piano sound if the game is in a non-playing state."""
    if start_the_game or game_over or level_up:
        sounds.piano.play()

def on_mouse_down(pos):
    global game_over, level_up, level, start_the_game, level_boss

    # start first game
    if start_the_game and button_level_up.collidepoint(pos): 
        start_the_game = False
        start_game(number_of_enemies)

    # restart game when game is over
    elif button_level_up.collidepoint(pos) and game_over:
        level = 1
        game_over = False
        level_up = False
        level_boss = False
        start_game(number_of_enemies)

    # level up
    elif button_level_up.collidepoint(pos) and level_up:
        if level % 3 == 0:
            level += 1
            level_up = False
            level_boss = True
            start_boss()
        elif level >= 4:
            level += 1
            level_up = False
            start_game_with_ai(number_of_enemies + level // 2, level - 4)
        else:
            level += 1
            level_up = False
            start_game(number_of_enemies + level // 2)

    elif button_quit.collidepoint(pos):  # Quit
        import sys
        sys.exit()

def update():
    global run_piano, direction_moving_background, level_up, level_boss
    if not enemies and not level_boss and not level_up and not start_the_game:
        sounds.level_up.play()
        level_up = True
    if level_boss and not boss_list:
        level_boss = False

    # Refine the condition for playing the piano sound
    if not run_piano and (start_the_game or game_over or level_up):
        clock.schedule_unique(play_piano, 1.0)
        run_piano = True

    if (start_the_game or game_over or not enemies and not level_boss):
        background_outside.x -= 0.5 * direction_moving_background
        if background_outside.right == 800 or background_outside.right == 1600:
            direction_moving_background *= -1

    if not game_over and not level_up:  # Regular update if the game is not over
        tank_set()
        tank_bullets_set()
        enemy_set()
        enemy_bullets_set()
        for ai_tank in ai_tanks:
            ai_tank.move_tank()
            ai_tank.shoot_bullet()
            ai_tank.update_bullets()
        if boss_list and level_boss and not show_boss_text:
            boss_set()

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
    # display the first screen
    if start_the_game:
        background_outside.draw()
        screen.draw.text('TANK GAME', (WIDTH/2-200, HEIGHT/2-50), color = (255,25,100), fontsize = 100)
        button_level_up.draw()
        button_quit.draw()
        screen.draw.text('START', center=button_level_up.center, fontsize=30, color="white")
        screen.draw.text('QUIT', center=button_quit.center, fontsize=30, color="white")
        instruction.draw()
    
    # display if game is over
    elif game_over:
        background_outside.draw()
        button_level_up.draw()
        button_quit.draw()
        screen.draw.text('RESTART', center=button_level_up.center, fontsize=30, color="white")
        screen.draw.text('QUIT', center=button_quit.center, fontsize=30, color="white")

        screen.draw.text('LOSE!', (300,250), color = (255,0,0), fontsize = 100)

    # display if game is won
    elif level_up and (not level_boss):
        background_outside.draw()
        button_level_up.draw()
        button_quit.draw()
        screen.draw.text("LEVEL UP", center=button_level_up.center, fontsize=30, color="white")
        screen.draw.text("QUIT", center=button_quit.center, fontsize=30, color="white")

        screen.draw.text('YOU WON',(240,250),color=(0,255,255), fontsize=100)
    
    # display warning before boss level
    elif show_boss_text:
        screen.clear()
        background.draw()
        if countdown_text:
            screen.draw.text(countdown_text, center=(WIDTH / 2, HEIGHT / 2), fontsize=100, color="red")
        else:
            screen.draw.text("BOSS", center=(WIDTH / 2, HEIGHT / 2), fontsize=int(50 * boss_text_scale), color="red")
    
    # display the game
    else:
        screen.clear()
        background.draw()
        screen.draw.text('Level : ' + str(level) ,(10, HEIGHT - 35),color = (255,255,100), fontsize = 40)
        for death_tank in death_tank_list:
            death_tank.draw()
        for wall in walls:
            wall.draw()
        for iron in irons:
            iron.draw()
        for tank in our_tank:
            tank.image.draw()
            draw_hp_bar(tank, 40, 3)
        for enemy in enemies:
            enemy.image.draw()
            draw_hp_bar(enemy, 40, 3)
        for ai_tank in ai_tanks:
            ai_tank.image.draw()
            draw_hp_bar(ai_tank, 40, 3)
            for bullet in ai_tank.bullets:
                bullet.draw()
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
        for health in hp_list:
            health.draw()
        for speed in speed_list:
            speed.draw()
        for kamejoko in kame: 
            kamejoko.draw()
        for explosion in explosion_list:
            explosion.draw()
        if level_boss and boss_list:
            for boss in boss_list:
                boss.image.draw()
            draw_hp_bar(tank_boss,200, 10)
            for bullet in tank_boss.bullets:
                bullet.draw()

pgzrun.go()