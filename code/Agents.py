import mesa as ms
from math import ceil
from Models import *
import random

class GrassAgent(ms.Agent):
    def __init__(self, id_t, model):
        super().__init__(id_t, model)
        self.id = id_t

class VaccumAgentModel(ms.Agent):
    myCoordinates = (0, 0)
    def __init__(self, id_t, model):
        super().__init__(id_t, model)
        self.id = id_t
        self.state = False

    def move(self):
        next_move = self.model.grid.get_neighborhood(
		    self.pos, moore = True, include_center = False
	    )
        new_position = self.random.choice(next_move)
        self.model.grid.move_agent(self, new_position)
    def step(self):
        pass
"""
{
    "type": 0,
    "direction": ([1, 0] || [0, 1] || [-1, 0] || [0, -1]),
    "velocity" 2 u/s
}
"""

class TrafficLightAgent(ms.Agent):
    def __init__(self, unique_id, model, lane):
        super().__init__(unique_id, model)
        self.lane = lane    #0 = up, 1 = down, 2 = left, 3 = right
        self.light = 1      #0 = red, 1 = yellow, 2 = green
        new_pos = (17, 14)


    def checkCar(self):
        if self.distLeft == 0:
            self.velocity = 0
        elif self.distLeft <= self.velocity:
            self.velocity = ceil(self.velocity/2)

        dx = (self.direction[0] * self.velocity)
        dy = (self.direction[1] * self.velocity)

        newPos = (self.pos[0] + dx, self.pos[1] + dy)
        self.distLeft -= self.velocity
        self.model.grid.move_agent(self, newPos)
    
    def checkLane(self, coords_before_crossroad, coords_start_of_street):
        if coords_before_crossroad[0] == coords_start_of_street[0]:    # Case horizontal
            it_coords = list(coords_before_crossroad)
            if coords_before_crossroad < coords_start_of_street:
                for i in range(coords_before_crossroad[1], coords_start_of_street[1]):
                    it_coords[1] = i
                    current_cell = self.model.grid.get_cell_list_contents([tuple(it_coords)])
                    car = [obj for obj in current_cell if isinstance(obj, CarAgent)]
                    if len(car)>0:
                        return car[0]
            else:
                for i in reversed(range(coords_start_of_street[1], coords_before_crossroad[1])):
                    it_coords[1] = i
                    current_cell = self.model.grid.get_cell_list_contents([tuple(it_coords)])
                    car = [obj for obj in current_cell if isinstance(obj, CarAgent)]
                    if len(car)>0:
                        return car[0]
        else:
            it_coords = list(coords_before_crossroad)
            if coords_before_crossroad < coords_start_of_street:
                for i in range(coords_before_crossroad[0], coords_start_of_street[0]):
                    it_coords[0] = i
                    current_cell = self.model.grid.get_cell_list_contents([tuple(it_coords)])
                    car = [obj for obj in current_cell if isinstance(obj, CarAgent)]
                    if len(car)>0:
                        return car[0]
            else:
                for i in reversed(range(coords_start_of_street[0], coords_before_crossroad[0])):
                    it_coords[0] = i
                    current_cell = self.model.grid.get_cell_list_contents([tuple(it_coords)])
                    car = [obj for obj in current_cell if isinstance(obj, CarAgent)]
                    if len(car)>0:
                        return car[0]
        return CarAgent(33, self.model, 0, 2, [1, 0], 14)

                



    def checkNextCar(self):
        nextCar = CarAgent(33, self.model, 0, 2, [1, 0], 14)
        if self.lane == 0:
            nextCar = self.checkLane((16, 15), (16, 0))
        elif self.lane == 1:
            nextCar = self.checkLane((15, 17), (15, 31))
        elif self.lane == 2:
            nextCar = self.checkLane((17, 16), (31, 16))
        elif self.lane == 3:
            nextCar = self.checkLane((15, 15), (0, 15))
        print(f"TFL : {self.unique_id},\tlane: {self.lane},\tvel: {nextCar.velocity},\tCar_id: {nextCar.unique_id}, Position: {nextCar.pos}")

    def step(self):
        choices = [0, 1, 2]
        self.light = random.choice(choices)
        self.checkNextCar()

class CarAgent(ms.Agent):

    def __init__(self, unique_id, model, type, velocity, direction, distLeft):
        super().__init__(unique_id, model)
        self.type = type
        self.velocity = velocity
        self.direction = direction
        self.distLeft = distLeft #14


    def move(self):
        if self.distLeft == 0:
            self.velocity = 0
        elif self.distLeft <= self.velocity:
            self.velocity = ceil(self.velocity/2)

        dx = (self.direction[0] * self.velocity)
        dy = (self.direction[1] * self.velocity)

        newPos = (self.pos[0] + dx, self.pos[1] + dy)
        self.distLeft -= self.velocity
        self.model.grid.move_agent(self, newPos)

    def step(self):
        self.move()