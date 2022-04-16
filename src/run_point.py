import sys
sys.path.append(r"simulator")
sys.path.append(r"visualizer")
from world import World
from visualization import Visualizer


world = World(" ","sample_room.json")
world.run()
side = 12
visualization = Visualizer(side, "sample_room.json")
visualization.visualize()