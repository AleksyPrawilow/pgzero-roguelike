from pgzero.animation import animate
from pgzero.animation import Animation

class TransitionHandler():
    def __init__(self):
        self.transition_overlay_opacity = 0
        self.current_animation = 0
        self.announcement_opacity = 0
    def fade(self, new_opacity, on_finished):
        self.current_animation = animate(self, transition_overlay_opacity = new_opacity, tween = 'linear', duration = 0.5, on_finished = on_finished)
    def fade_announcement(self, new_opacity, on_finished):
        animate(self, announcement_opacity = new_opacity, tween = 'linear', duration = 0.5, on_finished = on_finished)