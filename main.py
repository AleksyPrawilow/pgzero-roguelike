from pgzero.keyboard import keys
from player import Player
from map_generator import MapGenerator

WIDTH = 640
HEIGHT = 480
TILE = 16

enemies = []
items = []
player_x = 0
player_y = 0

player = Player('player')
map_generator = MapGenerator()
generated_map = map_generator.generate_map(3, 3)
# Setting the initial player position to the center of the map
player_x = 13
player_y = 13
player.move(player_x, player_y, TILE)

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
                    elif room[j][i] == 9:
                        screen.blit('exit', (x * TILE * 9 + i * TILE, y * TILE * 9 + j * TILE))
    for enemy in enemies:
        pass
        #draw enemy
    player.draw()

def update():
    pass

def on_key_down(key):
    global player_x, player_y
    if key == keys.LEFT or key == keys.A:
        player_x -= 1
        player.move(player_x, player_y, TILE)
    elif key == keys.RIGHT or key == keys.D:
        player_x += 1
        player.move(player_x, player_y, TILE)
    elif key == keys.UP or key == keys.W:
        player_y -= 1
        player.move(player_x, player_y, TILE)
    elif key == keys.DOWN or key == keys.S:
        player_y += 1
        player.move(player_x, player_y, TILE)