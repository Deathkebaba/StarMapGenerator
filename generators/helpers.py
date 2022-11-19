from pandas import DataFrame,Series
import numpy as np

def calculateDistance(points: DataFrame, singlePoint:Series):
    """Returns a copy of points with additional column 'distance, which contains the distance of each point to singlePoint."""
    df = points.copy()
    xdf = points['x'] - singlePoint['x']
    ydf = points['y'] - singlePoint['y']
    zdf = points['z'] - singlePoint['z']
    squaredf = (xdf**2 + ydf**2 + zdf**2)
    df['distance'] = squaredf**(0.5)
    return df

def calculateMinDistance(points: DataFrame, singlePoint:Series):
     df = calculateDistance(points, singlePoint)
     return min(df.distance) 

def calculatMaxDistance(points: DataFrame, singlePoint:Series):
     df = calculateDistance(points, singlePoint)
     return max(df.distance) 

def center():
    return Series([0,0,0], index=['x','y','z'])