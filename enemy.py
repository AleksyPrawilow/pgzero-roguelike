import main
from pgzero.actor import Actor
from pgzero.animation import animate
from player import Player
import random
import math

class Enemy(Actor):
    def __init__(self, image, pos=(0,0), anchor=('center', 'center')):
        super().__init__(image, pos, anchor)
        # animations
        self.animations = {
            'idle_left': ['enemy_idle_left_1', 'enemy_idle_left_2', 'enemy_idle_left_3', 'enemy_idle_left_4', 'enemy_idle_left_5'],
            'walk_left': ['enemy_walk_left_1', 'enemy_walk_left_2', 'enemy_walk_left_3', 'enemy_walk_left_4'],
            'idle_right': ['enemy_idle_1', 'enemy_idle_2', 'enemy_idle_3', 'enemy_idle_4', 'enemy_idle_5'],
            'walk_right': ['enemy_walk_1', 'enemy_walk_2', 'enemy_walk_3', 'enemy_walk_4']
        }
        self.current_animation = 'idle'
        self.direction = 'right'
        self.image = self.animations[self.current_animation + "_" + self.direction][0]
        self.fps = 12
        self.frame_index = 0
        main.clock.schedule_interval(self.advance_frame, 1 / self.fps)
    
    def advance_frame(self):
        frames = self.animations[self.current_animation + "_" + self.direction]
        self.frame_index = (self.frame_index + 1) % len(frames)
        self.image = frames[self.frame_index]
    
    def set_state(self, new_state = 'walk'):
        self.current_animation = new_state
        self.frame_index = 0
        self.image = self.animations[self.current_animation + "_" + self.direction][0]
    
    def move(self, new_x, new_y, tile_size):
        self.set_state("walk")
        if new_x != self.x // tile_size:
            if self.x // tile_size < new_x:
                self.direction = 'right'
            else:
                self.direction = 'left'
        # once again, the animation duration can be modifier to better see the animation
        animate(self, pos = (new_x * tile_size + tile_size / 2, new_y * tile_size + tile_size / 2), duration = 0.2, tween = 'bounce_start_end', on_finished = lambda: self.set_state('idle'))
    
    def move_towards_player(self, player_x, player_y, tile_size, generated_map, player):
        # check if the player is close enough
        if abs(self.x - (player_x * tile_size + tile_size / 2)) > tile_size * 7 or abs(self.y - (player_y * tile_size + tile_size / 2)) > tile_size * 7:
            return
        # check if can reach player to attack, the enemy attacks if within 1 tile, no diagonals allowed
        if math.sqrt((self.x - (player_x * tile_size + tile_size / 2))**2 + (self.y - (player_y * tile_size + tile_size / 2))**2) <= tile_size:
            player.damage(1)
            main.sounds.enemy_attack.play()
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