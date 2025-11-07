import main
from pgzero.actor import Actor
from pgzero.animation import animate

class Player(Actor):
    def __init__(self, image, pos=(0,0), anchor=('center', 'center'), max_health = 3, on_death = lambda: print("dead")):
        super().__init__(image, pos, anchor)
        self.animations = {
            'idle_left': ['player_idle_1', 'player_idle_2', 'player_idle_3', 'player_idle_4'],
            'walk_left': ['player_walk_1', 'player_walk_2', 'player_walk_3', 'player_walk_4', 'player_walk_5', 'player_walk_6', 'player_walk_7', 'player_walk_8'],
            'idle_right': ['player_idle_right_1', 'player_idle_right_2', 'player_idle_right_3', 'player_idle_right_4'],
            'walk_right': ['player_walk_right_1', 'player_walk_right_2', 'player_walk_right_3', 'player_walk_right_4', 'player_walk_right_5', 'player_walk_right_6', 'player_walk_right_7', 'player_walk_right_8']
        }
        self.current_animation = 'idle'
        self.direction = 'left'
        self.image = self.animations[self.current_animation + "_" + self.direction][0]
        self.max_health = max_health
        self.current_health = max_health
        self.dead = False
        self.on_death = on_death
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
        self.set_state('walk')
        if new_x != self.x // tile_size:
            if self.x // tile_size < new_x:
                self.direction = 'right'
            else:
                self.direction = 'left'
        # to the person reviewing the code: you can increase the move duration to see the move animation entirely
        animate(self, pos = (new_x * tile_size + tile_size / 2, new_y * tile_size + tile_size / 2), duration = 0.1, tween = 'bounce_start_end', on_finished = lambda: self.set_state('idle'))
    
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