#import Libraries for Visualization
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd



class Visualizer:   

    # Define the figure , axes and ... for animation

    def __init__(self,side : float,file : str , arrow_length : float ,arrow_head_angle : float ,arrow_head_proprtion : float):
        """ 
        after creating a object of this class,construct figure , axes , graphic element  and read a file
                
        Args:
            side : Half the length of an axis
            file : Name and format of Excel file contains data
            arrow_length :
            arrow_head_angle : The angle between large length of arrow and small length of its head
            arrow_head_propotion: # The propotin between large length of the arrow and small length of its head

        """
        # define a figure
        self.figure = plt.figure() 
        # define an axes for x and y in cartecian
        self.axes = plt.axes(xlim = (-side , side) , ylim = (-side , side))
        # define a graphic 
        self.line2d, = self.axes.plot([],[]) 
        # read the CSV file by pandas madule
        self.data   = pd.read_csv(file)

        self.arrow_length = arrow_length  
        # The angle between large length of arrow and small length of its head
        self.arrow_head_angle = arrow_head_angle 
        # The propotin between large length of the arrow and small length of its head
        self.arrow_head_proportion = arrow_head_proprtion




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
        x_data.append(x + self.arrow_length*np.cos(np.deg2rad(phi)))
        x_data.append(x_data[1] - self.arrow_head_proportion*self.arrow_length*np.cos(np.deg2rad(phi+self.arrow_head_angle)))
        x_data.append(x_data[1])
        x_data.append(x_data[1] -self.arrow_head_proportion*self.arrow_length*np.cos(np.deg2rad(phi-self.arrow_head_angle)))

        y_data = [y]
        y_data.append(y + self.arrow_length*np.sin(np.deg2rad(phi)))
        y_data.append(y_data[1] - self.arrow_head_proportion*self.arrow_length*np.sin(np.deg2rad(phi+self.arrow_head_angle)))
        y_data.append(y_data[1])
        y_data.append(y_data[1] - self.arrow_head_proportion*self.arrow_length*np.sin(np.deg2rad(phi-self.arrow_head_angle)))
        return x_data , y_data


    def __animate(self,i : int):
        """ animate the data of Excel File

        Args:
            i : Excel File rows index
 
        returns:
            Updated figure's object
        """
        x_data = self.__arrow_points(self.data["x"][i],self.data["y"][i],self.data["phi"][i])[0]
        y_data = self.__arrow_points(self.data["x"][i],self.data["y"][i],self.data["phi"][i])[1]
        self.line2d.set_data(x_data, y_data)
        return self.line2d,


    def visualize(self):
        """ visualize the data and animate

        Args:

            nothing

        returns:
            nothing

        """
        
        animated = animation.FuncAnimation(self.figure, # input a figure for animation
                                         self.__animate,  # input method to update figure for each frame
                                         np.arange(0,len(self.data["time"])), # Enter a list for the previous method for each frame
                                         interval=1/60*1000 # the frame (by mili-sec)
                                         # Nothic:(self.data["time"][1]-self.data["time"][0]) Actually is delta-t (The difference between the two times)
                                        ,repeat = False ) # No repetition
        #plt.grid(ls = "--")
        #plt.show()
        writervideo = animation.PillowWriter(fps=60)
        animated.save('v0_robot.gif', writer=writervideo)
        


myVis=Visualizer(0.6,"Data_of_arrow.csv",0.05,30,0.2)
myVis.visualize()