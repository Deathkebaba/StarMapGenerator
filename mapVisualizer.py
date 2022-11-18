from pandas import DataFrame
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def visualize(mapdf: DataFrame):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(0,0,0,s=30,c='k')
    ax.scatter(mapdf.x, mapdf.y, mapdf.z, s=0.1, c='w')
    ax.set_facecolor('k')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    #Setting the axis size
    x = max(mapdf['x'], key=abs)
    y = max(mapdf['y'], key=abs)
    z = max(mapdf['z'], key=abs)
    omega = max([x,y,z], key = abs)    
    ax.set_xlim([omega, omega*(-1)])
    ax.set_ylim([omega, omega*(-1)])
    ax.set_zlim([omega, omega*(-1)])
    plt.show()
