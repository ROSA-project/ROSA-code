import sys
sys.path.append(r"simulator")
sys.path.append(r"visualizer")
from world import World
from visualization import Visualizer
import logger


logger.Logger.initialize("default_log.txt")
map_file = "sample_maps/4walls_1table_1ball_nested.json"
vis_filename = "output_vis.json"
world = World(map_file, vis_filename)
world.run()
logger.Logger.finalize()

side = 5
visualization = Visualizer(side, vis_filename)
visualization.visualize(False)
