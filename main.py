from pgzero.actor import Actor
from pgzero.keyboard import keys
from player import Player
from enemy import Enemy
from map_generator import MapGenerator

WIDTH = 432
HEIGHT = 432
TILE = 16

enemies = []
items = []
keys_items = []
steps_before_enemy_move = 2
current_step_count = 0
player_x = 0
player_y = 0

player = Player('player')
map_generator = MapGenerator()
generated_map = map_generator.generate_map(3, 3)
# Setting the initial player position to the center of the map
player_x = 13
player_y = 13
player.move(player_x, player_y, TILE)

def add_items_and_enemies():
    for y in range(len(generated_map)):
        for x in range(len(generated_map[y])):
            room = generated_map[y][x]
            for j in range(len(room.room_plan)):
                for i in range(len(room.room_plan[j])):
                    if room.room_plan[j][i] == 4:
                        enemies.append(Enemy('enemy', (x * 9 * TILE + i * TILE + TILE / 2, y * 9 * TILE + j * TILE + TILE / 2)))
                    elif room.room_plan[j][i] == 3:
                        keys_items.append((x * 9 + i, y * 9 + j))

add_items_and_enemies()

def draw():
    screen.clear()
    screen.fill((255, 255, 255))
    for y in range(len(generated_map)):
        for x in range(len(generated_map[y])):
            if generated_map[y][x].type == 'empty':
                continue
            room = generated_map[y][x].room_plan
            for j in range(len(room)):
                for i in range(len(room[j])):
                    if room[j][i] == 0:
                        screen.blit('floor', (x * TILE * 9 + i * TILE, y * TILE * 9 + j * TILE))
                    elif room[j][i] == 1:
                        screen.blit('wall', (x * TILE * 9 + i * TILE, y * TILE * 9 + j * TILE))
                    elif room[j][i] == 2:
                        pass # a trap
                    elif room[j][i] == 3:
                        screen.blit('floor', (x * TILE * 9 + i * TILE, y * TILE * 9 + j * TILE))
                        # place a key
                    elif room[j][i] == 4:
                        screen.blit('floor', (x * TILE * 9 + i * TILE, y * TILE * 9 + j * TILE))
                        # place an enemy
                    elif room[j][i] == 9:
                        screen.blit('exit', (x * TILE * 9 + i * TILE, y * TILE * 9 + j * TILE))
    for enemy in enemies:
        enemy.draw()
    for key_item in keys_items:
        screen.blit('key', (key_item[0] * TILE + 4, key_item[1] * TILE + 4))
    player.draw()

def update():
    pass

def on_key_down(key):
    global player_x, player_y
    def move_enemies():
        for enemy in enemies:
            enemy.move_towards_player(player_x, player_y, TILE, generated_map)
    def move_player():
        global current_step_count
        player.move(player_x, player_y, TILE)
        current_step_count += 1
        if current_step_count >= steps_before_enemy_move:
            current_step_count = 0
            move_enemies()

    if key == keys.LEFT or key == keys.A:
        player_x -= 1
        if generated_map[player_y // 9][player_x // 9].room_plan[player_y % 9][player_x % 9] == 1:
            player_x += 1
            return
        move_player()
    elif key == keys.RIGHT or key == keys.D:
        player_x += 1
        if generated_map[player_y // 9][player_x // 9].room_plan[player_y % 9][player_x % 9] == 1:
            player_x -= 1
            return
        move_player()
    elif key == keys.UP or key == keys.W:
        player_y -= 1
        if generated_map[player_y // 9][player_x // 9].room_plan[player_y % 9][player_x % 9] == 1:
            player_y += 1
            return
        move_player()
    elif key == keys.DOWN or key == keys.S:
        player_y += 1
        if generated_map[player_y // 9][player_x // 9].room_plan[player_y % 9][player_x % 9] == 1:
            player_y -= 1
            return
        move_player()