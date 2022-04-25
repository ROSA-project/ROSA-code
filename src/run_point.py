import sys
sys.path.append(r"simulator")
sys.path.append(r"visualizer")
from world import World
from visualization import Visualizer
import logger

logger.Logger.initialize("default_log.txt")
world = World(" ","test.json")
world.run()
logger.Logger.finalize()
side = 5
visualization = Visualizer(side, "test.json")
visualization.visualize()
