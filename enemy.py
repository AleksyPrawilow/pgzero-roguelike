from pgzero.actor import Actor
from pgzero.animation import animate
import random
import math

class Enemy(Actor):
    def move(self, new_x, new_y, tile_size):
        animate(self, pos = (new_x * tile_size + tile_size / 2, new_y * tile_size + tile_size / 2), duration = 0.1, tween = 'bounce_start_end')
    def move_towards_player(self, player_x, player_y, tile_size, generated_map):
        # check if the player is close enough
        if abs(self.x - (player_x * tile_size + tile_size / 2)) > tile_size * 7 or abs(self.y - (player_y * tile_size + tile_size / 2)) > tile_size * 7:
            return
        new_x = self.x // tile_size
        new_y = self.y // tile_size
        # move towards player or randomly
        if random.random() > 0.25:
            # choose if to move in x or y direction
            if abs(player_x - new_x) > abs(player_y - new_y):
                new_x += 1 if player_x > new_x else -1
            else:
                new_y += 1 if player_y > new_y else -1
        else:
            if random.choice([True, False]):
                new_x += random.choice([-1, 1])
            else:
                new_y += random.choice([-1, 1])
        # check for walls
        map_position_x = int(new_x // 9)
        map_position_y = int(new_y // 9)
        room = generated_map[map_position_y][map_position_x]
        room_x = int(new_x % 9)
        room_y = int(new_y % 9)
        while room.room_plan[room_y][room_x] == 1:
            new_x = self.x // tile_size
            new_y = self.y // tile_size
            if random.choice([True, False]):
                new_x += random.choice([-1, 1])
            else:
                new_y += random.choice([-1, 1])
            map_position_x = int(new_x // 9)
            map_position_y = int(new_y // 9)
            room = generated_map[map_position_y][map_position_x]
            room_x = int(new_x % 9)
            room_y = int(new_y % 9)
        self.move(new_x, new_y, tile_size)