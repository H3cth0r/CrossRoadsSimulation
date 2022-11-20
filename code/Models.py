import mesa as ms
from Agents import GrassAgent, TrafficLightAgent, ScheduledTrafficLightAgent, CarAgent
from random import choice


class RoomModel(ms.Model):
    def __init__(self, nCars):
        super().__init__()
        #self.schedule = ms.time.BaseScheduler(self)
        self.model_stages = ["stage_one", "stage_two", "stage_three"]
        self.schedule = ms.time.StagedActivation(self, self.model_stages, shuffle=False)

        self.grid = ms.space.MultiGrid(32, 32, torus=True)
        self.directions = [
            [1,0],
            [0,1],
            [-1,0],
            [0,-1],
        ]
        self.velocities = [1, 2, 3, 4]

        """
        # adding traffic light agents to grid
        TFS_0 =   TrafficLightAgent(0, self, 0)
        TFS_1 =   TrafficLightAgent(1, self, 1)
        TFS_2 =   TrafficLightAgent(2, self, 2)
        TFS_3 =   TrafficLightAgent(3, self, 3)

        # connecting traffic light agents to each other
        TFS_list = [TFS_0, TFS_1, TFS_2, TFS_3]
        for tf in TFS_list:
            tf.setTFS(TFS_list)
        """
        TFS_0 =   ScheduledTrafficLightAgent(0, self, 0, 1)
        TFS_1 =   ScheduledTrafficLightAgent(1, self, 1, 7)
        TFS_2 =   ScheduledTrafficLightAgent(2, self, 2, 13)
        TFS_3 =   ScheduledTrafficLightAgent(3, self, 3, 19)

        #for TFL in TFS:self.schedule.add(TFL)
        self.schedule.add(TFS_0)
        self.grid.place_agent(TFS_0, (17, 14))   #up
        self.schedule.add(TFS_1)
        self.grid.place_agent(TFS_1, (14, 17))   #down
        self.schedule.add(TFS_2)
        self.grid.place_agent(TFS_2, (17, 17))   #left
        self.schedule.add(TFS_3)
        self.grid.place_agent(TFS_3, (14, 14))   #right

        carsInLane = [0, 0, 0, 0]
        counter = 4

        for i in range(nCars):
            #direction = choice(self.directions)
            direction = self.directions[i]
            #up - down - left - right
            distLeft = 14
            if direction[0] == 0:
                if direction[1] == 1 and carsInLane[0] == 0: #going up
                    startingPos = (16, 0 + carsInLane[0])
                    distLeft -= carsInLane[0]
                    carsInLane[0] += 1
                    trafficLight = TFS_0
                elif carsInLane[1] == 0: #going down
                    startingPos = (15, 31 - carsInLane[1])
                    distLeft -= carsInLane[1]
                    carsInLane[1] += 1
                    trafficLight = TFS_1
            elif direction[0] == -1  and carsInLane[2] == 0: #going left
                startingPos = (31 - carsInLane[2], 16)
                distLeft -= carsInLane[2]
                carsInLane[2] += 1
                trafficLight = TFS_2
            elif carsInLane[3] == 0: #going right
                startingPos = (0 + carsInLane[3], 15)
                distLeft -= carsInLane[3]
                carsInLane[3] += 1
                trafficLight = TFS_3

            carro = CarAgent(counter, self, 0, choice(self.velocities), direction, distLeft, trafficLight)
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
            "Non Wealthy Agents": RoomModel.current_non_weathy_agents,
        }) 

    @staticmethod
    def current_non_weathy_agents(model) -> int:
        """Return the total of number of weathy agents
		
		Args:
			model (RoomModel): tee simulation model
			
		Returns:
			int: Num of wealthy agents"""

        return sum([1 for agent in model.schedule.agents if agent.id == 0])

    def step(self):
        print("=================")
        self.schedule.step()

