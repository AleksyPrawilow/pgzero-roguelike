import main
from pgzero.actor import Actor
from pgzero.animation import animate

class Player(Actor):
    def __init__(self, image, pos=(0,0), anchor=('center', 'center'), max_health = 3, on_death = lambda: print("dead")):
        super().__init__(image, pos, anchor)
        self.max_health = max_health
        self.current_health = max_health
        self.dead = False
        self.on_death = on_death
    def move(self, new_x, new_y, tile_size):
        animate(self, pos = (new_x * tile_size + tile_size / 2, new_y * tile_size + tile_size / 2), duration = 0.1, tween = 'bounce_start_end')
    def heal(self, amount):
        self.current_health = min(self.max_health, self.current_health + amount)
        main.sounds.player_heal.play()
    def damage(self, amount):
        self.current_health = max(0, self.current_health - amount)
        if self.current_health == 0:
            self.dead = True
            self.on_death()
            main.sounds.player_death.play()
        else:
            main.sounds.player_hit.play()