import main
from pgzero.animation import animate

class Camera():
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.windod_height = window_height
        self.x = 0
        self.y = 0
    
    def set_position(self, new_x, new_y):
        animate(self, x = new_x, tween = 'decelerate', duration = 0.5)
        animate(self, y = new_y, tween = 'decelerate', duration = 0.5)

    def world_to_screen(self, global_x, global_y):
        top_left_x = self.x - self.window_width / 2
        top_left_y = self.y - self.windod_height / 2
        sx = int(global_x - top_left_x)
        sy = int(global_y - top_left_y)
        return (sx, sy)
    
    def draw_actor(self, actor, offset_x, offset_y):
        screen_pos = self.world_to_screen(actor.x + offset_x, actor.y + offset_y)
        old_top_left = actor.topleft
        actor.topleft = screen_pos
        actor.draw()
        actor.topleft = old_top_left
    
    def draw_blit(self, image, global_x, global_y):
        screen_pos = self.world_to_screen(global_x, global_y)
        main.screen.blit(image, screen_pos)