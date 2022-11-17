import mesa as ms
from Agents import *
from random import choice


class RoomModel(ms.Model):
    def __init__(self, nCars):
        super().__init__()
        self.schedule = ms.time.BaseScheduler(self)
        self.grid = ms.space.MultiGrid(32, 32, torus=True)
        self.directions = [
            [1,0],
            [0,1],
            [-1,0],
            [0,-1],
        ]
        carsInLane = [0, 0, 0, 0]
        counter = 0
        
        for i in range(nCars):
            invalidDirection = True #delete when multiple cars per lane are available
            while invalidDirection:
                direction = choice(self.directions)
                #up - down - left - right
                distLeft = 14
                if direction[0] == 0:
                    if direction[1] == 1 and carsInLane[0] == 0: #going up
                        startingPos = (16, 0 + carsInLane[0])
                        distLeft -= carsInLane[0]
                        carsInLane[0] += 1
                        invalidDirection = False
                    elif carsInLane[1] == 0: #going down
                        startingPos = (15, 31 - carsInLane[1])
                        distLeft -= carsInLane[1]
                        carsInLane[1] += 1
                        invalidDirection = False
                elif direction[0] == -1  and carsInLane[2] == 0: #going left
                    startingPos = (31 - carsInLane[2], 16)
                    distLeft -= carsInLane[2]
                    carsInLane[2] += 1
                    invalidDirection = False
                elif carsInLane[3] == 0: #going right
                    startingPos = (0 + carsInLane[3], 15)
                    distLeft -= carsInLane[3]
                    carsInLane[3] += 1
                    invalidDirection = False

            """
            direction = choice(self.directions)
                #up - down - left - right
                distLeft = 14
                if direction[0] == 0:
                    if direction[1] == 1: #going up
                        startingPos = (16, 0 + carsInLane[0])
                        distLeft -= carsInLane[0]
                        carsInLane[0] += 1
                    else: #going down
                        startingPos = (16, 31 - carsInLane[1])
                        distLeft -= carsInLane[1]
                        carsInLane[1] += 1
                elif direction[0] == -1: #going left
                    startingPos = (31 - carsInLane[2], 16)
                    distLeft -= carsInLane[2]
                    carsInLane[2] += 1
                else: #going right
                    startingPos = (0 + carsInLane[3], 15)
                    distLeft -= carsInLane[3]
                    carsInLane[3] += 1
            """

            carro = CarAgent(counter, self, 0, 2, direction, distLeft)
            self.schedule.add(carro)
            self.grid.place_agent(carro, startingPos)
            counter += 1

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

    def step(self):
        self.schedule.step()



