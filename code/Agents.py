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

    def step(self):
        choices = [-1, 0, 1, 2]
        self.light = random.choice(choices)

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