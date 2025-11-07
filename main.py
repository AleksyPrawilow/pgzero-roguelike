import random
import pgzrun
from pgzero.actor import Actor
from pgzero.keyboard import keys
from player import Player
from enemy import Enemy
from map_generator import MapGenerator
from transition_handler import TransitionHandler

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
required_keys = 2
keys_collected = 0
gui_opacity = 1
current_room = 0
changing_rooms = False

map_generator = MapGenerator()
transition_handler = TransitionHandler()
generated_map = []
player_x = 0
player_y = 0
exit_x = 0
exit_y = 0
music.play('ambience')

def restart():
    global player, player_x, player_y, gui_opacity, current_room
    player = Player('player', on_death = lambda: transition_handler.fade(0.5, lambda: print("Trans finished")))
    player_x = 13
    player_y = 13
    player.move(player_x, player_y, TILE)
    transition_handler.fade(0, lambda: print("reset fade"))
    gui_opacity = 1
    current_room = 0
    generate_map()

def generate_map():
    global generated_map, player_x, player_y, keys_collected, current_room
    keys_collected = 0
    enemies.clear()
    keys_items.clear()
    player_x = 13
    player_y = 13
    player.move(player_x, player_y, TILE)
    generated_map = map_generator.generate_map(3, 3)
    add_items_and_enemies()
    current_room += 1

def add_items_and_enemies():
    global keys_items, exit_x, exit_y
    for y in range(len(generated_map)):
        for x in range(len(generated_map[y])):
            room = generated_map[y][x]
            for j in range(len(room.room_plan)):
                for i in range(len(room.room_plan[j])):
                    if room.room_plan[j][i] == 4:
                        enemies.append(Enemy('enemy', (x * 9 * TILE + i * TILE + TILE / 2, y * 9 * TILE + j * TILE + TILE / 2)))
                    elif room.room_plan[j][i] == 3:
                        keys_items.append((x * 9 + i, y * 9 + j))
                    elif room.room_plan[j][i] == 9:
                        exit_x = x * 9 + i
                        exit_y = y * 9 + j
    # leaving only 2 keys on the map
    random.shuffle(keys_items)
    keys_items = keys_items[:required_keys]

def next_room():
    global changing_rooms
    changing_rooms = True

    def on_transition_finished():
        global changing_rooms
        generate_map()
        transition_handler.fade(0, lambda: print("next room"))
        changing_rooms = False
    sounds.exit.play()
    transition_handler.fade(1, on_transition_finished)

restart()

def draw():
    screen.clear()
    screen.fill((0, 0, 0))
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
    # GUI
    # transitions overlay
    overlay = screen.surface.copy()
    overlay.fill((0, 0, 0))
    overlay.set_alpha(transition_handler.transition_overlay_opacity * 255)
    screen.blit(overlay, (0, 0))
    screen.draw.text(f"Keys collected: {keys_collected} / {required_keys}", (12, 12), color = "white", owidth = 1, ocolor = "black", alpha = gui_opacity)
    screen.draw.text(f"Health: {player.current_health} / {player.max_health}", (12, 36), color = "white", owidth = 1, ocolor = "black", alpha = gui_opacity)
    for i in range(steps_before_enemy_move - current_step_count):
        # need to use a surface as blit does not support alpha for some reason
        surface = images.footstep
        surface.set_alpha(gui_opacity * 255)
        screen.blit(surface, (12 + i * 20, 60))
    # death screen
    screen.draw.text("YOU DIED...", (WIDTH / 2, HEIGHT / 2 - 48), fontsize = 48,  anchor = (0.5, 0.5), color = "red", owidth = 2, ocolor = "black", alpha = 1 - gui_opacity)
    screen.draw.text(f"Dungeons cleared: {current_room - 1}", (WIDTH / 2, HEIGHT / 2 - 12), fontsize = 24,  anchor = (0.5, 0.5), color = "white", owidth = 1, ocolor = "black", alpha = 1 - gui_opacity)
    screen.draw.text("Press 'R' to restart.", (WIDTH / 2, HEIGHT / 2 + 12), fontsize = 24,  anchor = (0.5, 0.5), color = "white", owidth = 1, ocolor = "black", alpha = 1 - gui_opacity)

def update():
    global gui_opacity
    if player.dead and gui_opacity > 0:
        gui_opacity -= 0.05

def on_key_down(key):
    global player_x, player_y
    def move_enemies():
        for enemy in enemies:
            enemy.move_towards_player(player_x, player_y, TILE, generated_map, player)
    def move_player():
        global current_step_count, keys_collected
        player.move(player_x, player_y, TILE)
        if (player_x, player_y) in keys_items:
            keys_items.remove((player_x, player_y))
            keys_collected += 1
            sounds.key_pickup.play()
        if player_x == exit_x and player_y == exit_y:
            if keys_collected == required_keys:
                next_room()
        current_step_count += 1
        if current_step_count >= steps_before_enemy_move:
            current_step_count = 0
            move_enemies()
            sounds.footstep.play()
        else:
            sounds.footstep_player.play()
    if changing_rooms:
        return
    if not player.dead:
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
    else:
        if key == keys.R:
            restart()

pgzrun.go()