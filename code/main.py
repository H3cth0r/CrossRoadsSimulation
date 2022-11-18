import mesa as ms
from Models import *
from Agents import *
import matplotlib.pyplot as plt

model = RoomModel(1)
model.step()

def agent_PT(agent):
	if type(agent) == GrassAgent:
		PT = {"Shape": "rect","Color": "green","Filled": "true","Layer": 0,"w": 1,"h":1}
	elif type(agent) == TrafficLightAgent:
		if agent.light == 0:
			PT = {"Shape": "circle","Color": "red","Filled": "true","Layer": 1,"r" : 0.5}
		elif agent.light == 1:
			PT = {"Shape": "circle","Color": "yellow","Filled": "true","Layer": 1,"r" : 0.5}
		else:
			PT = {"Shape": "circle","Color": "white","Filled": "true","Layer": 1,"r" : 0.5}
	else:
		PT = {"Shape": "rect", "Color": "red", "Filled": "true", "Layer": 1, "w": 1, "h":1}
		
	return PT

grid = ms.visualization.CanvasGrid(agent_PT, 32, 32, 700, 700)

chart_currents = ms.visualization.ChartModule(
	[

	],
	canvas_height=300,
	data_collector_name="datacollector_currents"
)

server = ms.visualization.ModularServer(RoomModel, [grid, chart_currents], "Vacuum Room Model", {"nCars":3})
server.port = 8521
server.launch()

