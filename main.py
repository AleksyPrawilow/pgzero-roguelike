import random
import pgzrun
from pgzero.actor import Actor
from pgzero.keyboard import keys
from player import Player
from enemy import Enemy
from map_generator import MapGenerator
from transition_handler import TransitionHandler
from camera import Camera

WIDTH = 1280
HEIGHT = 720
TILE = 64

enemies = []
items = []
keys_items = []
player_x = 0
player_y = 0
required_keys = 2
keys_collected = 0
gui_opacity = 1
current_room = 0
changing_rooms = False
in_menu = True
show_pause = False
current_menu_option = 0
current_pause_option = 0
music_enabled = True

map_generator = MapGenerator()
transition_handler = TransitionHandler()
camera = Camera(WIDTH, HEIGHT)
generated_map = []
player_x = 0
player_y = 0
exit_x = 0
exit_y = 0
music.play('menu')

def on_player_death():
    transition_handler.fade(0.5, lambda: print("Transition finished"))

def restart():
    global player, player_x, player_y, gui_opacity, current_room
    player = Player('player', on_death = on_player_death)
    player_x = 13
    player_y = 13
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
    camera.set_position(player_x * TILE + TILE / 2, player_y * TILE + TILE / 2)
    generated_map = map_generator.generate_map(3, 3)
    add_items_and_enemies()
    current_room += 1

def add_items_and_enemies():
    global keys_items, exit_x, exit_y, items
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
    print(keys_items)
    # positions not used for the keys will be used for potions
    items = keys_items[required_keys:]
    items = items[:random.randint(0, 1)]
    keys_items = keys_items[:required_keys]

def next_room():
    global changing_rooms
    changing_rooms = True
    player.heal(1)

    def on_transition_finished():
        global changing_rooms
        generate_map()
        transition_handler.fade(0, lambda: print("next room"))
        changing_rooms = False
        transition_handler.fade_announcement(1, lambda: transition_handler.fade_announcement(0, lambda: print("Finished")))
    sounds.exit.play()
    transition_handler.fade(1, on_transition_finished)

restart()

def draw():
    screen.clear()
    screen.fill((0, 0, 0))
    if in_menu:
        screen.draw.text("PG-Zero\nRoguelike", (WIDTH / 2, HEIGHT / 2 - 48), fontsize = 64,  anchor = (0.5, 0.5), color = "white", owidth = 2, ocolor = "black")
        screen.draw.text(f"{"> " if current_menu_option == 0 else ""}Play{" <" if current_menu_option == 0 else ""}", (WIDTH / 2, HEIGHT / 2 + 16), fontsize = 24,  anchor = (0.5, 0.5), color = "white", owidth = 1, ocolor = "black")
        screen.draw.text(f"{"> " if current_menu_option == 1 else ""}Music: {"ON" if music_enabled else "OFF"}{" <" if current_menu_option == 1 else ""}", (WIDTH / 2, HEIGHT / 2 + 40), fontsize = 24,  anchor = (0.5, 0.5), color = "white", owidth = 1, ocolor = "black")
        screen.draw.text(f"{"> " if current_menu_option == 2 else ""}Exit{" <" if current_menu_option == 2 else ""}", (WIDTH / 2, HEIGHT / 2 + 64), fontsize = 24,  anchor = (0.5, 0.5), color = "white", owidth = 1, ocolor = "black")
        screen.draw.text("Use arrows or WASD to move. Space to select. C to drink a potion.\nCreated by Aleksy Prawiłow(Aleksey Pravilov)", (WIDTH / 2, HEIGHT - 32), fontsize = 18,  anchor = (0.5, 0.5), color = "white", owidth = 1, ocolor = "black")
    else:
        for y in range(len(generated_map)):
            for x in range(len(generated_map[y])):
                if generated_map[y][x].type == 'empty':
                    continue
                room = generated_map[y][x].room_plan
                for j in range(len(room)):
                    for i in range(len(room[j])):
                        world_x = x * TILE * 9 + i * TILE + 32
                        world_y = y * TILE * 9 + j * TILE + 32
                        screen_pos = camera.world_to_screen(world_x, world_y)
                        if room[j][i] == 0:
                            pass
                        if room[j][i] == 1:
                            screen.blit('wall', screen_pos)
                        elif room[j][i] == 2:
                            screen.blit('trap', screen_pos)
                        elif room[j][i] == 3:
                            screen.blit('floor', screen_pos)
                            # place a key
                        elif room[j][i] == 4:
                            screen.blit('floor', screen_pos)
                        elif room[j][i] == 9:
                            screen.blit('exit', screen_pos)
        for key_item in keys_items:
            world_x = key_item[0] * TILE
            world_y = key_item[1] * TILE
            screen_x, screen_y = camera.world_to_screen(world_x, world_y)
            screen.blit('key', (screen_x + 32, screen_y + 32))
        for item in items:
            world_x = item[0] * TILE
            world_y = item[1] * TILE
            screen_x, screen_y = camera.world_to_screen(world_x, world_y)
            screen.blit('potion', (screen_x + 32, screen_y + 32))
        for enemy in enemies:
            camera.draw_actor(enemy)
        camera.draw_actor(player)
    # GUI
    # transitions overlay
    overlay = screen.surface.copy()
    overlay.fill((0, 0, 0))
    overlay.set_alpha(transition_handler.transition_overlay_opacity * 255)
    screen.blit(overlay, (0, 0))
    if not in_menu:
        for heart in range(player.current_health):
            surface = images.heart
            surface.set_alpha(gui_opacity * 255)
            screen.blit(surface, (12 + heart * 64, 12))
        for i in range(player.available_steps):
            surface = images.footstep
            surface.set_alpha(gui_opacity * 255)
            screen.blit(surface, (12 + i * 64, 12 + 64))
        for i in range(player.potions):
            surface = images.potion
            surface.set_alpha(gui_opacity * 255)
            screen.blit(surface, (12 + i * 64, 12 + 128))
        for key in range(keys_collected):
            surface = images.key.copy()
            surface.set_alpha(gui_opacity * 255)
            screen.blit(surface, (12 + key * 64, 12 + 192 if player.potions > 0 else 12 + 128))
        if show_pause:
            pause_overlay = screen.surface.copy()
            pause_overlay.fill((0, 0, 0))
            pause_overlay.set_alpha(128)
            screen.blit(pause_overlay, (0, 0))
            screen.draw.text("Game Paused", (WIDTH / 2, HEIGHT / 2 - 48), fontsize = 48,  anchor = (0.5, 0.5), color = "white", owidth = 2, ocolor = "black")
            screen.draw.text(f"{"> " if current_pause_option == 0 else ""}Resume{" <" if current_pause_option == 0 else ""}", (WIDTH / 2, HEIGHT / 2 + 16), fontsize = 24,  anchor = (0.5, 0.5), color = "white", owidth = 1, ocolor = "black")
            screen.draw.text(f"{"> " if current_pause_option == 1 else ""}Music: {"ON" if music_enabled else "OFF"}{" <" if current_pause_option == 1 else ""}", (WIDTH / 2, HEIGHT / 2 + 40), fontsize = 24,  anchor = (0.5, 0.5), color = "white", owidth = 1, ocolor = "black")
            screen.draw.text(f"{"> " if current_pause_option == 2 else ""}Exit{" <" if current_pause_option == 2 else ""}", (WIDTH / 2, HEIGHT / 2 + 64), fontsize = 24,  anchor = (0.5, 0.5), color = "white", owidth = 1, ocolor = "black")
            screen.draw.text("Use arrows or WASD to move. Space to select. C to drink a potion.\nCreated by Aleksy Prawiłow(Aleksey Pravilov)", (WIDTH / 2, HEIGHT - 32), fontsize = 18,  anchor = (0.5, 0.5), color = "white", owidth = 1, ocolor = "black")
        # death screen
        screen.draw.text("YOU DIED...", (WIDTH / 2, HEIGHT / 2 - 48), fontsize = 48,  anchor = (0.5, 0.5), color = "red", owidth = 2, ocolor = "black", alpha = 1 - gui_opacity)
        screen.draw.text(f"Dungeons cleared: {current_room - 1}", (WIDTH / 2, HEIGHT / 2 - 12), fontsize = 24,  anchor = (0.5, 0.5), color = "white", owidth = 1, ocolor = "black", alpha = 1 - gui_opacity)
        screen.draw.text("Press 'R' to restart.", (WIDTH / 2, HEIGHT / 2 + 12), fontsize = 24,  anchor = (0.5, 0.5), color = "white", owidth = 1, ocolor = "black", alpha = 1 - gui_opacity)
        # announcement
        screen.draw.text(f"Dungeon floor {current_room}", (WIDTH / 2, HEIGHT / 2), fontsize = 64,  anchor = (0.5, 0.5), color = "white", owidth = 2, ocolor = "black", alpha = transition_handler.announcement_opacity)

def update():
    global gui_opacity
    if player.dead and gui_opacity > 0:
        gui_opacity -= 0.05

def play_pressed():
    def hide_menu():
        global in_menu
        in_menu = False
        music.play('ambience')
        restart()
        transition_handler.fade(0, lambda: print("Lets go"))
    transition_handler.fade(1, lambda: hide_menu())

def music_pressed():
    global music_enabled
    music_enabled = not music_enabled
    music.set_volume(int(music_enabled))

def exit_pressed():
    quit()
    
def on_key_down(key):
    global player_x, player_y, current_menu_option
    if in_menu:
        if key == keys.W or key == keys.UP:
            current_menu_option -= 1
            if current_menu_option < 0:
                current_menu_option = 2
            sounds.key_pickup.play()
        elif key == keys.S or key == keys.DOWN:
            current_menu_option += 1
            if current_menu_option > 2:
                current_menu_option = 0
            sounds.key_pickup.play()
        elif key == keys.SPACE:
            if current_menu_option == 0:
                play_pressed()
            elif current_menu_option == 1:
                music_pressed()
            elif current_menu_option == 2:
                exit_pressed()
    else:
        def move_enemies():
            for enemy in enemies:
                enemy.move_towards_player(player_x, player_y, TILE, generated_map, player)
        def move_player():
            global current_step_count, keys_collected
            remaining_steps = player.available_steps
            player.move(player_x, player_y, TILE)
            camera.set_position(player_x * TILE + TILE/2, player_y * TILE + TILE/2)
            if (player_x, player_y) in keys_items:
                keys_items.remove((player_x, player_y))
                keys_collected += 1
                sounds.key_pickup.play()
            if (player_x, player_y) in items:
                items.remove((player_x, player_y))
                player.potions += 1
                sounds.key_pickup.play()
            if player_x == exit_x and player_y == exit_y:
                if keys_collected == required_keys:
                    next_room()
            if remaining_steps == 0:
                move_enemies()
                sounds.footstep.play()
            else:
                sounds.footstep_player.play()
        if changing_rooms:
            return
        if not player.dead:
            global current_pause_option
            if key == keys.ESCAPE:
                global show_pause
                show_pause = not show_pause
                current_pause_option = 0
            if show_pause:
                if key == keys.W or key == keys.UP:
                    current_pause_option -= 1
                    if current_pause_option < 0:
                        current_pause_option = 2
                    sounds.key_pickup.play()
                elif key == keys.S or key == keys.DOWN:
                    current_pause_option += 1
                    if current_pause_option > 2:
                        current_pause_option = 0
                    sounds.key_pickup.play()
                elif key == keys.SPACE:
                    if current_pause_option == 0:
                        show_pause = False
                        current_pause_option = 0
                    elif current_pause_option == 1:
                        music_pressed()
                    elif current_pause_option == 2:
                        exit_pressed()
                return
            if key == keys.LEFT or key == keys.A:
                player_x -= 1
                tile_id = generated_map[player_y // 9][player_x // 9].room_plan[player_y % 9][player_x % 9]
                if tile_id == 2:
                    player.damage(1)
                if tile_id == 1:
                    player_x += 1
                    return
                move_player()
            elif key == keys.RIGHT or key == keys.D:
                player_x += 1
                tile_id = generated_map[player_y // 9][player_x // 9].room_plan[player_y % 9][player_x % 9]
                if tile_id == 2:
                    player.damage(1)
                if tile_id == 1:
                    player_x -= 1
                    return
                move_player()
            elif key == keys.UP or key == keys.W:
                player_y -= 1
                tile_id = generated_map[player_y // 9][player_x // 9].room_plan[player_y % 9][player_x % 9]
                if tile_id == 2:
                    player.damage(1)
                if tile_id == 1:
                    player_y += 1
                    return
                move_player()
            elif key == keys.DOWN or key == keys.S:
                player_y += 1
                tile_id = generated_map[player_y // 9][player_x // 9].room_plan[player_y % 9][player_x % 9]
                if tile_id == 2:
                    player.damage(1)
                if tile_id == 1:
                    player_y -= 1
                    return
                move_player()
            elif key == keys.C:
                player.use_potion()
        else:
            if key == keys.R:
                restart()
