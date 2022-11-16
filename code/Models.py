import mesa as ms
from Agents import *



class RoomModel(ms.Model):
    def __init__(self):
        super().__init__()
        self.schedule = ms.time.RandomActivation(self)
        self.grid = ms.space.MultiGrid(32, 32, torus=False)
        
        counter = 0
        for x in range(32):
            for y in range(32):
                pasto = GrassAgent(counter, self)
                if (x >= 0 and x < 15) and ((y >= 0 and y < 15) or y>=17 and y < 32):
                    self.grid.place_agent(pasto, (x, y))
                elif (x >= 17 and x < 232) and ((y>=0 and y < 15) or y>= 17 and y < 32):
                    self.grid.place_agent(pasto, (x, y))
                counter += 1

        self.datacollector_currents = ms.DataCollector({
            "Wealthy Agents": RoomModel.current_weathy_agents,
            "Non Wealthy Agents": RoomModel.current_non_weathy_agents,
        }) 

    @staticmethod
    def current_weathy_agents(model) -> int:
        """Return the total of number of weathy agents
		
		Args:
			model (RoomModel): tee simulation model
			
		Returns:
			int: Num of wealthy agents"""
        return sum([1 for agent in model.schedule.agents if agent.id > 0])

    @staticmethod
    def current_non_weathy_agents(model) -> int:
        """Return the total of number of weathy agents
		
		Args:
			model (RoomModel): tee simulation model
			
		Returns:
			int: Num of wealthy agents"""

        return sum([1 for agent in model.schedule.agents if agent.id == 0])



