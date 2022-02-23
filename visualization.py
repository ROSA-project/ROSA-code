#import Libraries for Visualization
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import pandas as pd

def x_arrow(x,phi) -> list:
    """  
    Calculate the horizontal points(x in Cartesian) of an arrow and insert it into a list
    
    Args:
        x   : Horizontal point at the beginning of the arrow
        phi : Angle between arrow and horizontal axis of Cartesian coordinates (By degree)

    returns:
        List of five horizontal points of an arrow
    """
    x_data = []
    arrow_length = 0.2
    x_data.append(x)
    x_data.append(x + arrow_length*np.cos(np.deg2rad(phi)))
    x_data.append(x + arrow_length*np.cos(np.deg2rad(phi)) -0.1*arrow_length*np.cos(np.deg2rad(phi-37)))
    x_data.append(x + arrow_length*np.cos(np.deg2rad(phi)))
    x_data.append(x + arrow_length*np.cos(np.deg2rad(phi)) -0.1*arrow_length*np.cos(np.deg2rad(phi+37)))
    return x_data

def y_arrow(y,phi) -> list:
    """  
    Calculate the Vertical points(y in Cartesian) of an arrow and insert it into a list
    
    Args:
        y   : Vertical point at the beginning of the arrow
        phi : Angle between arrow and horizontal axis of Cartesian coordinates (By degree)

    returns:
        List of five Vertical points of an arrow
    """
    y_data = []
    arrow_length = 0.2
    y_data.append(y)
    y_data.append(y + arrow_length*np.sin(np.deg2rad(phi)))
    y_data.append(y + arrow_length*np.sin(np.deg2rad(phi)) - 0.1*arrow_length*np.sin(np.deg2rad(phi-37)))
    y_data.append(y + arrow_length*np.sin(np.deg2rad(phi)))
    y_data.append(y + arrow_length*np.sin(np.deg2rad(phi)) -0.1*arrow_length*np.sin(np.deg2rad(phi+37)))
    return y_data

# Define the figure , axis and graph element for animation
fig = plt.figure()
ax = plt.axes(xlim =(-2,2),ylim = (-2,2))
Ln, = ax.plot([],[])

# initialization function: plot the background of each frame
def init():
    Ln.set_data([],[])
    return Ln,

# Read an Excel file that contains information about
# time, position of the beginning point of the arrow and the angle 
# and put it in a variable
data = pd.read_excel("Book1.xlsx")

def animate(i):
    """ animate the data of Excel File

    Args:
        i : Excel file rows index

    returns:
        Updated figure's object
    """
    x_data = x_arrow(data["x"][i],data["phi"][i] + 90)
    y_data = y_arrow(data["y"][i],data["phi"][i]+ 90)
    Ln.set_data(x_data, y_data)
    return Ln,

# Call the animator function 
anim = ani.FuncAnimation(fig, animate, np.arange(0,len(data["time"])),
                        init_func=init,interval=(data["time"][1]-data["time"][0]) * 1000 ,
                        repeat = False )
plt.grid(ls = "--")
plt.show()