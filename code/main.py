import mesa as ms
from Models import *
from Agents import *
import matplotlib.pyplot as plt

model = RoomModel()
model.step()

def agent_PT(agent):
	if type(agent) == GrassAgent:
		PT = {"Shape": "rect","Color": "green","Filled": "true","Layer": 0,"w": 1,"h":1}
	else:
		PT = {"Shape": "rect", "Color": "red", "Filled": "true", "Layer": 0, "w": 1, "h":1}
		
	return PT

grid = ms.visualization.CanvasGrid(agent_PT, 32, 32, 700, 700)

chart_currents = ms.visualization.ChartModule(
	[
		{"Label": "Wealthy Agents", "Color": "green"},
		{"Label":"Non Wealthy Agents", "Color": "red"},
	],
	canvas_height=300,
	data_collector_name="datacollector_currents"
)

server = ms.visualization.ModularServer(RoomModel, [grid, chart_currents], "Vacuum Room Model")
server.port = 8521
server.launch()

