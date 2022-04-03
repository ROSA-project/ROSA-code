import sys
sys.path.append(r"simulator")
sys.path.append(r"visualizer")
from world import World
from visualization import Visualizer


world = World(" ","test.json")
world.run()
side = 12
visualization = Visualizer(side, "test.json")
visualization.visualize()