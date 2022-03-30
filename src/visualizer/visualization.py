#import Libraries for Visualization
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json
from simulator.object import ObjectId


class Visualizer:   

    # Define the figure , axes and ... for animation

    def __init__(self,side : float,file : str):
        """ 
        after creating a object of this class,construct figure , axes , graphic element  and read a file
                
        Args:
            side : Half the length of an axis
            file : Name and format of json file contains data

        """
        # define a figure
        self.figure = plt.figure() 
        # define an axes for x and y in cartecian
        self.axes = plt.axes(xlim = (-side , side) , ylim = (-side , side))
        self.line = self.axes.plot([],[])
        self.lines2d = []
        try:
            with open(file , "r") as f:
                self.data = json.load(f)
        except:
            print("Eror! can't Open or Read File. please check the path or File Name.",end = " ")
        
        for i in range(len(self.data["Shape"])):
            obj = self.axes.plot([],[])[0]
            self.lines2d.append(obj)
        
        #TODO : It is currently set, it will be set by the user later 
        self.___arrow_length = 0.5 
        # The angle between large length of arrow and small length of its head
        self.__arrow_head_angle = 37
        # The propotin between large length of the arrow and small length of its head
        self.__arrow_head_proportion = 0.1
    
    def __arrow_points(self,x : float,y : float,phi : float) -> list:
        """  
        Calculate the points(x ,y in Cartesian) of an arrow and insert it into a list
        
        Args:
            x   : Horizontal point at the beginning of the arrow
            y   : Vertical point at the beginning of the arrow
            phi : Angle between arrow and horizontal axis of Cartesian coordinates (By degree)
    
        returns:
            tuple of two List . first List is Horizontal points (x) , and secend is vertical points 
        """
        x_data = [x]
        x_data.append(x + self.__arrow_length*np.cos(np.deg2rad(phi)))
        x_data.append(x_data[1] - self.__arrow_head_proportion*self.__arrow_length*np.cos(np.deg2rad(phi+self.__arrow_head_angle)))
        x_data.append(x_data[1])
        x_data.append(x_data[1] -self.__arrow_head_proportion*self.__arrow_length*np.cos(np.deg2rad(phi-self.__arrow_head_angle)))

        y_data = [y]
        y_data.append(y + self.__arrow_length*np.sin(np.deg2rad(phi)))
        y_data.append(y_data[1] - self.__arrow_head_proportion*self.__arrow_length*np.sin(np.deg2rad(phi+self.__arrow_head_angle)))
        y_data.append(y_data[1])
        y_data.append(y_data[1] - self.__arrow_head_proportion*self.__arrow_length*np.sin(np.deg2rad(phi-self.__arrow_head_angle)))
        return x_data , y_data
    
    def __Cube(self,moment : int,objectId) -> tuple:
        """Function for visualizing object shapes(Cube)
        Args:
            moment : for Moment inside the file
            ID : ID of object
        return:
            lists of x and y (in cartesian) for objects (Shapes of Cube)
        """
        inf = self.data["Shape"][str(objectId)]["dimension"]
        r = np.sqrt((inf[0] **2 + inf[1]**2))
        teta = np.arctan(inf[1]/inf[0])
        x_data,y_data =[] , []
        for i in [teta,np.pi-teta,np.pi+teta,-teta , teta]:
            x_data.append(self.data[str(moment)][str(objectId)][0]+r*np.cos(np.deg2rad(self.data[str(moment)][str(objectId)][2])+ i))
            y_data.append(self.data[str(moment)][str(objectId)][1]+r*np.sin(np.deg2rad(self.data[str(moment)][str(objectId)][2])+ i))
        return x_data,y_data

    def __Cylinder(self,moment : int,objectId):
        """Function for visualizing object shapes(Cube)
        Args:
            moment : for Moment inside the file
            ID : ID of object
        return:
            lists of x and y (in cartesian) for objects (Shapes of Cube)
        """
        step = 0.06
        l = np.arange(0,2*np.pi+step/4,step)
        x_data = self.data["shape"][str(objectId)]["dimension"]*(np.cos(l) - self.data[str(moment)][str(objectId)[0]]) 
        y_data = self.data["shape"][str(objectId)]["dimension"]*(np.sin(l) - self.data[str(moment)][str(objectId)[1]])
        return x_data,y_data

    def __animate(self,i : int):

        frame_interval = 0.025
        step_round = 3
        x_data,y_data = [],[]
        for j in self.data["Shape"]:       
            if self.data["Shape"][j]["Shape"] == "Cube":
                x_data.append(self.__Cube(round(i*frame_interval,step_round) ,int(j))[0])
                y_data.append(self.__Cube(round(i*frame_interval,step_round) ,int(j))[1])
                
            if self.data["Shape"][j]["Shape"] == "Cylinder":
                x_data.append(self.__Cylinder(i ,int(j))[0])
                y_data.append(self.__Cylinder(i ,int(j))[1])     
        i = 0
        for self.line in self.lines2d:
            self.line.set_data(x_data[i],y_data[i])
            i += 1
        return self.lines2d


    def visualize(self):
        """ visualize the data and animate

        Args:

            nothing

        returns:
            nothing

        """
        frame_interval = 0.025
        animated = animation.FuncAnimation(self.figure, # input a figure for animation
                                         self.__animate,  # input method to update figure for each frame
                                         np.arange(len(self.data)-1),# Enter a list for the previous method for each frame
                                         interval=frame_interval*1000 # the frame (by mili-sec)
                                         # Nothic: blit=True means only re-draw the parts that have changed.
                                         ,blit = True
                                        ,repeat = False ) # No repetition
        plt.grid(ls = "--")
        plt.show()
