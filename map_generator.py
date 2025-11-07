import random
import math

class MapGenerator:
    def generate_map(self, dim_x, dim_y, max_rooms = 6):
        generated_map = []
        # setting all the rooms to empty
        for i in range(dim_y):
            generated_map.append([Room(j, i) for j in range(dim_x)])
        center_room_x = math.floor(dim_x / 2)
        center_room_y = math.floor(dim_y / 2)
        generated_map[center_room_y][center_room_x] = Room(center_room_x, center_room_y, 'start')
        current_x = center_room_x
        current_y = center_room_y
        directions = ['up', 'down', 'left', 'right']
        created_rooms = 1
        while created_rooms < max_rooms:
            direction = random.choice(directions)
            if direction == 'up' and current_y > 0:
                current_y -= 1
            elif direction == 'down' and current_y < dim_y - 1:
                current_y += 1
            elif direction == 'left' and current_x > 0:
                current_x -= 1
            elif direction == 'right' and current_x < dim_x - 1:
                current_x += 1
            if generated_map[current_y][current_x].type == 'empty':
                created_rooms += 1
                generated_map[current_y][current_x] = Room(current_x, current_y, 'room')
        # setting exit room by looking for the most distant room from the center
        max_distance = 0
        exit_x = center_room_x
        exit_y = center_room_y
        for y in range(dim_y):
            for x in range(dim_x):
                if generated_map[y][x].type == 'room':
                    distance = math.sqrt((x - center_room_x) ** 2 + (y - center_room_y) ** 2)
                    if distance > max_distance:
                        max_distance = distance
                        exit_x = x
                        exit_y = y
        generated_map[exit_y][exit_x] = Room(exit_x, exit_y, 'exit')
        # closing walls where there are no adjacent rooms
        for y in range(dim_y):
            for x in range(dim_x):
                if generated_map[y][x].type != 'empty':
                    left = True
                    right = True
                    up = True
                    down = True
                    if x > 0 and generated_map[y][x - 1].type != 'empty':
                        left = False
                    if x < dim_x - 1 and generated_map[y][x + 1].type != 'empty':
                        right = False
                    if y > 0 and generated_map[y - 1][x].type != 'empty':
                        up = False
                    if y < dim_y - 1 and generated_map[y + 1][x].type != 'empty':
                        down = False
                    generated_map[y][x].close_walls(left, right, up, down)
        return generated_map

class Room:
    def __init__(self, x, y, type = 'empty'):
        self.x = x
        self.y = y
        self.type = type
        self.room_plan = []
        # 0 - Floor
        # 1 - Wall
        # 2 - trap
        # 3 - key
        # 4 - enemy
        # 9 - exit

        if type == 'start':
            self.room_plan = [
                [1, 1, 1, 1, 0, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 0, 1, 1, 1, 1],
            ]
        elif type == 'room':
            available_plans = [
                [
                    [1, 1, 1, 1, 0, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 1, 0, 0, 0, 4, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 3, 0, 0, 0, 0],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 4, 0, 0, 0, 1, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 0, 1, 1, 1, 1],
                ]
            ]
            self.room_plan = random.choice(available_plans)
            # randomizing the whole thing a bit
            if random.choice([True, False]):
                self.room_plan.reverse()
        elif type == 'exit':
            self.room_plan = [
                [1, 1, 1, 1, 0, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 9, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 0, 1, 1, 1, 1],
            ]
        elif type == 'empty':
            pass
    def close_walls(self, left, right, up, down):
        if left:
            self.room_plan[4][0] = 1
        if right:
            self.room_plan[4][8] = 1
        if up:
            self.room_plan[0][4] = 1
        if down:
            self.room_plan[8][4] = 1