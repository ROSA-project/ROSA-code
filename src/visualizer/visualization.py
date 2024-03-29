import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json
import random
import sys
sys.path.append(r"src\simulator")
from object import ObjectId


class Visualizer:
    # TODO for Mehdi: please write something more proper.
    # Currently: Define the figure , axes and ... for animation

    def __init__(self, side: float, json_filename: str):
        """after creating an object of this class,construct figure , axes , graphic element  and read a file
                
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

        # notice: The number 2 in the following code is for calculating the maximum number of graphs
        # Suppose each shape has an arrow
        for i in range(2 * len(self.data["shapes"])):
            obj = self.axes.plot([], [])[0]
            self.lines2d.append(obj)
        # Between independent objects, we randomly assign color to each one
        self.__colors = self.__color_info()

        # TODO: It is currently hardcoded, it will be set by the user later
        # The angle between large length of arrow and small length of its head
        self.__arrow_head_angle = 37
        # The proportion between large length of the arrow and small length of its head
        self.__arrow_head_proportion = 0.1

    # TODO for Mehdi: The function documentation doesn't seem to describe the right
    #  parameters
    def __arrow_points(self, moment: str, oid: ObjectId, arrow_length: float) -> tuple:
        """Calculates the points(x,y in Cartesian) of an arrow and inserts it into a list
        
        Args:
            moment
            oid: ID's object from input-file
            arrow_length: length of arrow

        Returns:
            A tuple of type (list, list). The first list contains horizontal points (x),
            and the second list has vertical points
        """
        x = self.data[moment][oid][0]
        y = self.data[moment][oid][1]
        phi = self.data[moment][oid][2]

        x_data = [x]
        x_data.append(x + arrow_length * np.cos(np.deg2rad(phi)))
        x_data.append(x_data[1] - self.__arrow_head_proportion * arrow_length * np.cos(
            np.deg2rad(phi + self.__arrow_head_angle)))
        x_data.append(x_data[1])
        x_data.append(x_data[1] - self.__arrow_head_proportion * arrow_length * np.cos(
            np.deg2rad(phi - self.__arrow_head_angle)))

        y_data = [y]
        y_data.append(y + arrow_length * np.sin(np.deg2rad(phi)))
        y_data.append(y_data[1] - self.__arrow_head_proportion * arrow_length * np.sin(
            np.deg2rad(phi + self.__arrow_head_angle)))
        y_data.append(y_data[1])
        y_data.append(y_data[1] - self.__arrow_head_proportion * arrow_length * np.sin(
            np.deg2rad(phi - self.__arrow_head_angle)))
        return x_data, y_data

    def __cube(self, time: str, oid: ObjectId) -> tuple:
        """Function for visualizing object shapes(cube)
        Args:
            time : time in the input visualization file
            oid : Object's id
        return:
            lists of x and y (in cartesian) for objects (Shapes of cube)
        """
        inf = self.data["shapes"][oid]["dimension"]
        r = np.sqrt((inf[0] ** 2 + inf[1] ** 2) / 4)
        teta = np.arctan(inf[1] / inf[0])
        x_data, y_data = [], []
        for i in [teta, np.pi - teta, np.pi + teta, -teta, teta]:
            x_data.append(self.data[time][oid][0] +
                          r * np.cos(np.deg2rad(self.data[time][oid][2]) + i))
            y_data.append(self.data[time][oid][1] +
                          r * np.sin(np.deg2rad(self.data[time][oid][2]) + i))
        return x_data, y_data

    def __cylinder(self, moment: str, oid: ObjectId):
        """Function for visualizing object shapes(cylinder)
        Args:
            moment : for Moment inside the file
            oid : ID of object
        return:
            lists of x and y (in cartesian) for objects (Shapes of cylinder)
        """
        step = 0.06
        l = np.arange(0, 2 * np.pi + step / 4, step)
        radius = self.data["shapes"][oid]["dimension"][0]
        x_data = radius * np.cos(l) + self.data[moment][oid][0]
        y_data = radius * np.sin(l) + self.data[moment][oid][1]
        return x_data, y_data

    def __avg_length(self, owner: ObjectId) -> float:
        """gives the average between dimensions as the length of arrow
        Args:
            owner: the object ID that we want to draw the arrow
        """
        # TODO : just for now , we need to decide for this
        # notice : I chose the number 0.7 to have the right size for the arrow length
        # in the algorithm below the size is a small value
        sum_dimension, num = 0, 1
        ob = self.data["shapes"][owner]
        if ob is None:
            for oid in self.data["owners"]:
                if self.data["owners"][oid] is owner:
                    sum_dimension = self.__avg_length(oid)
                    num += 1
            return sum_dimension / float(0.7 * num)
        else:
            s = ob["type"]
            if s == "Cube":
                sum_dimension += sum(self.data["shapes"][owner]["dimension"][0:2])
                num += 1
            elif s == "Cylinder":
                sum_dimension += self.data["shapes"][owner]["dimension"][0]
                num += 1
        avg_length = sum_dimension / float(0.7 * num)

        return avg_length

    def __color_info(self) -> dict:
        """Assigns colors randomly to each object (assigned to Owner for compound object)
        """
        list_color = ["b", "g", "r", "c", "m", "y", "k", "#00FFFF", "#7FFFD4", "#0000FF", "#C1F80A",
                      "#8C000F", "#8C000F", "#FF00FF", "#D2691E", "#650021", "#008000", "#06C2AC",
                      "#FE420F", "#AAA662", "#800080", "#F0E68C", "#069AF3", "#01153E", "#FF6347",
                      "#580F41", "#A9561E", "#6E750E", "#C20078", "#9ACD32", "#929591"]
        # obj is a dictionary, have independent object's ID as a key and color's ID as value
        obj = dict()
        for oid in self.data["shapes"]:
            if oid not in self.data["owners"]:
                obj[oid] = random.choice(list_color)
                list_color.remove(obj[oid])
        return obj

    def __animate(self, time_index: int):

        global data
        frame_interval = 0.025
        step_round = 3
        time_instance = ("{:." + str(step_round) + "f}").format(time_index * frame_interval)
        info = dict()  # Sorts the data of each object (by key-value)
        for oid in self.data["shapes"]:
            if self.data["shapes"][oid] is not None:
                s = self.data["shapes"][oid]
                if s["type"] == "Cube":
                    data = self.__cube(time_instance, oid)
                elif s["type"] == "Cylinder":
                    data = self.__cylinder(time_instance, oid)
                info[oid] = [data[0], data[1]]
                if oid not in self.data["owners"]:
                    arrow_length = self.__avg_length(oid)
                    data = self.__arrow_points(time_instance, oid, arrow_length)
                    info[oid].append([data[0], data[1]])
            else:
                arrow_length = self.__avg_length(oid)
                data = self.__arrow_points(time_instance, oid, arrow_length)
                info[oid] = [data[0], data[1]]

        # At the same time as set data into a figure, it also set colors by owners
        index = 0
        for oid in info:
            # here, it's check the top owners to set color
            if oid in self.data["owners"]:
                self.lines2d[index].set_data(info[oid][0], info[oid][1])
                while self.data["owners"][oid] in self.data["owners"]:
                    oid = self.data["owners"][oid]
                self.lines2d[index].set_color(self.__colors[self.data["owners"][oid]])
                index += 1
            else:
                self.lines2d[index].set_data(info[oid][0], info[oid][1])
                self.lines2d[index].set_color(self.__colors[oid])
                if len(info[oid]) == 3:
                    self.lines2d[index + 1].set_data(info[oid][2][0], info[oid][2][1])
                    self.lines2d[index + 1].set_color(self.__colors[oid])
                    index += 1
                index += 1

        return self.lines2d

    def visualize(self, write_to_file: bool):
        """ visualize the data and animate
        """
        frame_interval = 0.025
        animated = animation.FuncAnimation(self.figure,  # input a figure for animation
                                           self.__animate,  # input method to update figure for each frame
                                           np.arange(len(self.data) - 2),
                                           # Enter a list for the previous method for each frame
                                           interval=frame_interval * 1000,  # the frame (by mS)
                                           # Notice: blit=True means only re-draw the parts that have changed.
                                           blit=True,
                                           repeat=False)  # No repetition
        plt.grid(ls="--")
        plt.show()
        # TODO saeed: works on my macbook but needs a closer look, 
        # it seems to be platform dependent.
        if write_to_file:
            writervideo = animation.PillowWriter(fps=1 / frame_interval)
            animated.save('v0_robot.gif', writer=writervideo)
