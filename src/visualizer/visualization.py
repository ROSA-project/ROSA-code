#import Libraries for Visualization
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json



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

    def __Cube(self,moment : int,ID : int) -> tuple:
        """Function for visualizing object shapes(Cube)
        Args:
            moment : for Moment inside the file
            ID : ID of object
        return:
            lists of x and y (in cartesian) for objects (Shapes of Cube)
        """
        inf = self.data["Shape"][str(ID)]["dimension"]
        r = np.sqrt((inf[0] **2 + inf[1]**2))
        teta = np.arctan(inf[1]/inf[0])
        x_data,y_data =[] , []
        for i in [teta,np.pi-teta,np.pi+teta,-teta , teta]:
            x_data.append(self.data[str(moment)][str(ID)][0]+r*np.cos(np.deg2rad(self.data[str(moment)][str(ID)][2])+ i))
            y_data.append(self.data[str(moment)][str(ID)][1]+r*np.sin(np.deg2rad(self.data[str(moment)][str(ID)][2])+ i))
        return x_data,y_data

    def __Cylinder(self,moment : int,ID : int):
        """Function for visualizing object shapes(Cube)
        Args:
            moment : for Moment inside the file
            ID : ID of object
        return:
            lists of x and y (in cartesian) for objects (Shapes of Cube)
        """
        step = 0.06
        l = np.arange(0,2*np.pi+step/4,step)
        x_data = self.data["shape"][str(ID)]["dimension"]*(np.cos(l) - self.data[str(moment)][str(ID)[0]]) 
        y_data = self.data["shape"][str(ID)]["dimension"]*(np.sin(l) - self.data[str(moment)][str(ID)[1]])
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
