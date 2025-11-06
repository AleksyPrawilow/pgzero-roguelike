from pgzero.actor import Actor
from pgzero.animation import animate

class Player(Actor):
    def move(self, new_x, new_y, tile_size):
        animate(self, pos = (new_x * tile_size + tile_size / 2, new_y * tile_size + tile_size / 2), duration = 0.1, tween = 'bounce_start_end')