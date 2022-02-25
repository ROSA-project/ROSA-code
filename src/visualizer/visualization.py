#import Libraries for Visualization
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import os
os.system("cls")


class Visualizer:   

    # Define the figure , axes and graph element for animation
    __figure = plt.figure()
    __axes = plt.axes(xlim =(-2.5,2.5),ylim = (-2.5,2.5))
    __line2D, = __axes.plot([],[])


    # Read an Excel file that contains information about
    # time, position of the beginning point of the arrow and the angle 
    # and put it in a variable
    __data = pd.read_excel("Data_of_arrow.xlsx")


    def __private_x_arrow(self,x,phi) -> list:
        """  
        Calculate the horizontal points(x in Cartesian) of an arrow and insert it into a list
        
        Args:
            x   : Horizontal point at the beginning of the arrow
            phi : Angle between arrow and horizontal axis of Cartesian coordinates (By degree)
    
        returns:
            List of five horizontal points of an arrow
        """
        x_data = [x]
        arrow_length = 0.2
        x_data.append(x + arrow_length*np.cos(np.deg2rad(phi)))
        x_data.append(x + arrow_length*np.cos(np.deg2rad(phi)) -0.1*arrow_length*np.cos(np.deg2rad(phi+37)))
        x_data.append(x + arrow_length*np.cos(np.deg2rad(phi)))
        x_data.append(x + arrow_length*np.cos(np.deg2rad(phi)) -0.1*arrow_length*np.cos(np.deg2rad(phi-37)))
        return x_data


    def __private_y_arrow(self,y,phi) -> list:
        """  
        Calculate the Vertical points(y in Cartesian) of an arrow and insert it into a list
        
        Args:
            y   : Vertical point at the beginning of the arrow
            phi : Angle between arrow and horizontal axis of Cartesian coordinates (By degree)
    
        returns:
            List of five Vertical points of an arrow
        """
        y_data = [y]
        arrow_length = 0.2
        y_data.append(y + arrow_length*np.sin(np.deg2rad(phi)))
        y_data.append(y + arrow_length*np.sin(np.deg2rad(phi)) - 0.1*arrow_length*np.sin(np.deg2rad(phi+37)))
        y_data.append(y + arrow_length*np.sin(np.deg2rad(phi)))
        y_data.append(y + arrow_length*np.sin(np.deg2rad(phi)) -0.1*arrow_length*np.sin(np.deg2rad(phi-37)))
        return y_data


    def __private_animate(self,frame):
        """ animate the data of Excel File

        Args:
            frame : Excel File rows index
 
        returns:
            Updated figure's object
        """
        x_data = self.__private_x_arrow(self.__data["x"][frame],self.__data["phi"][frame])
        y_data = self.__private_y_arrow(self.__data["y"][frame],self.__data["phi"][frame])
        self.__line2D.set_data(x_data, y_data)
        return self.__line2D,


    def visualize(self):
        """ visualize the data and animate

        Args:
            nothing

        returns:
            animation of data

        """
        animated = animation.FuncAnimation(self.__figure,
                                         self.__private_animate, np.arange(0,len(self.__data["time"])),
                                         interval=(self.__data["time"][1] - self.__data["time"][0])*1000
                                        ,repeat = False )
        plt.grid(ls = "--")
        plt.show()
