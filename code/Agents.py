import mesa as ms
from Models import *

class GrassAgent(ms.Agent):
    def __init__(self, id_t, model):
        super().__init__(id_t, model)
        self.id = id_t

class VaccumAgentModel(ms.Agent):
    myCoordinates = (0, 0)
    def __init__(self, id_t, model):
        super().__init__(id_t, model)
        self.id = id_t

    def move(self):
        next_move = self.model.grid.get_neighborhood(
		    self.pos, moore = True, include_center = False
	    )
        new_position = self.random.choice(next_move)
        self.model.grid.move_agent(self, new_position)
    def step(self):
        pass

