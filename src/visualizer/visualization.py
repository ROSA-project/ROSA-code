import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json
import sys
sys.path.append(r"src\simulator")
from object import ObjectId


class Visualizer:
    # TODO for Mehdi: please write something more proper.
    # Currently: Define the figure , axes and ... for animation

    def __init__(self, side: float, json_filename: str):
        """after creating a object of this class,construct figure , axes , graphic element  and read a file
                
        Args:
            side: Half the length of an axis
            json_filename: Name and format of the json file containing visualization data
        """
        # define a figure
        self.figure = plt.figure() 
        # define axes for x and y in cartecian
        self.axes = plt.axes(xlim=(-side, side), ylim=(-side, side))
        self.line = self.axes.plot([], [])
        self.lines2d = []
        self.data = dict()
        self.plot_arrows = True
        self.__vis_output_filename = json_filename

        try:
            with open(json_filename, "r") as f:
                self.data = json.load(f)
        except (OSError, IOError) as e:
            print("Error in opening file ", self.__vis_output_filename)
            raise e

        if self.plot_arrows:
            shapes_num_factor = 2
        else:
            shapes_num_factor = 1

        for i in range(len(self.data["shapes"]) * shapes_num_factor):
            obj = self.axes.plot([], [])[0]
            self.lines2d.append(obj)
        
        # TODO: It is currently hardcoded, it will be set by the user later
        # The angle between large length of arrow and small length of its head
        self.__arrow_head_angle = 37
        # The propotin between large length of the arrow and small length of its head
        self.__arrow_head_proportion = 0.1

    # TODO for Mehdi: The function documentation doesn't seem to describe the right
    #  parameters
    def __arrow_points(self, moment: int, oid: ObjectId, arrow_length: float) -> tuple:
        """Calculates the points(x,y in Cartesian) of an arrow and inserts it into a list
        
        Args:
            x: Horizontal point at the beginning of the arrow
            y: Vertical point at the beginning of the arrow
            phi: Angle between arrow and horizontal axis of Cartesian coordinates (By degree)
    
        Returns:
            A tuple of type (list, list). The first list contains horizontal points (x),
            and the secend list has vertical points
        """
        x = self.data[str(moment)][oid][0]
        y = self.data[str(moment)][oid][1]
        phi = self.data[str(moment)][oid][2]

        x_data = [x]
        x_data.append(x + arrow_length*np.cos(np.deg2rad(phi)))
        x_data.append(x_data[1] - self.__arrow_head_proportion*arrow_length*np.cos(
            np.deg2rad(phi+self.__arrow_head_angle)))
        x_data.append(x_data[1])
        x_data.append(x_data[1] - self.__arrow_head_proportion*arrow_length*np.cos(
            np.deg2rad(phi-self.__arrow_head_angle)))

        y_data = [y]
        y_data.append(y + arrow_length*np.sin(np.deg2rad(phi)))
        y_data.append(y_data[1] - self.__arrow_head_proportion*arrow_length*np.sin(
            np.deg2rad(phi+self.__arrow_head_angle)))
        y_data.append(y_data[1])
        y_data.append(y_data[1] - self.__arrow_head_proportion*arrow_length*np.sin(
            np.deg2rad(phi-self.__arrow_head_angle)))
        return x_data, y_data
    
    def __cube(self, time: int, oid: ObjectId) -> tuple:
        """Function for visualizing object shapes(cube)
        Args:
            time : time in the input visualization file
            oid : Object's id
        return:
            lists of x and y (in cartesian) for objects (Shapes of cube)
        """
        inf = self.data["shapes"][oid]["dimension"]
        r = np.sqrt((inf[0]**2 + inf[1]**2)/4)
        teta = np.arctan(inf[1]/inf[0])
        x_data, y_data =[], []
        for i in [teta, np.pi-teta, np.pi+teta, -teta , teta]:
            x_data.append(self.data[str(time)][oid][0] +
                          r * np.cos(np.deg2rad(self.data[str(time)][oid][2]) + i))
            y_data.append(self.data[str(time)][oid][1] +
                          r * np.sin(np.deg2rad(self.data[str(time)][oid][2]) + i))
        return x_data, y_data

    def __cylinder(self, moment: int, oid: ObjectId):
        """Function for visualizing object shapes(cylinder)
        Args:
            moment : for Moment inside the file
            oid : ID of object
        return:
            lists of x and y (in cartesian) for objects (Shapes of cylinder)
        """
        step = 0.06
        l = np.arange(0, 2*np.pi+step/4, step)
        radius = self.data["shapes"][oid]["dimension"][0]
        x_data = radius*np.cos(l) + self.data[str(moment)][oid][0]
        y_data = radius*np.sin(l) + self.data[str(moment)][oid][1]
        return x_data, y_data

    def __animate(self, time_index: int):
        
        frame_interval = 0.025
        step_round = 3
        time_instance = ("{:."+str(step_round)+"f}").format(time_index*frame_interval)
        x_data, y_data = [], []
        for oid in self.data["shapes"]:
            s = self.data["shapes"][oid]
            if s["type"] == "Cube":
                data = self.__cube(time_instance, oid)
                x_data.append(data[0])
                y_data.append(data[1])
                arrow_length = s["dimension"][0]/2
            elif s["type"] == "Cylinder":
                data = self.__cylinder(time_instance, oid)
                x_data.append(data[0])
                y_data.append(data[1])     
                arrow_length = s["dimension"][0]

            data = self.__arrow_points(time_instance, oid, arrow_length)
            x_data.append(data[0])
            y_data.append(data[1])     
        
        for i in range(int(len(self.lines2d)/2)):
            self.lines2d[2*i+1].set_color(f"{self.lines2d[2*i].get_color()}")

        i = 0
        for self.line in self.lines2d:
            self.line.set_data(x_data[i], y_data[i])
            i += 1

        return self.lines2d

    def visualize(self):
        """ visualize the data and animate
        """
        frame_interval = 0.025
        animated = animation.FuncAnimation(self.figure,  # input a figure for animation
                                         self.__animate,  # input method to update figure for each frame
                                         np.arange(len(self.data)-1),  # Enter a list for the previous method for each frame
                                         interval=frame_interval*1000  # the frame (by mili-sec)
                                         # Nothic: blit=True means only re-draw the parts that have changed.
                                         ,blit = True
                                        ,repeat = False ) # No repetition
        plt.grid(ls="--")
        plt.show()
        # TODO saeed: works on my macbook but needs a closer look, 
        # it seems to be platform dependent.
        writervideo = animation.PillowWriter(fps=1/frame_interval)
        animated.save('v0_robot.gif', writer=writervideo)
