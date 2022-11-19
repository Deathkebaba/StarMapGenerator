import numpy as np
import pandas as pd
from .helpers import calculateDistance, center


def jitterer(df:pd.DataFrame, shift:float = 2):
    x = len(df.index)
    y = len(df.columns)
    jitterdf = pd.DataFrame(np.random.normal(0,shift,[x,y]), columns = ['x','y','z'])
    df.index=jitterdf.index
    df = df - jitterdf
    df.index.name='starID'
    return df

def run(stepSize = 5, shift = 10,outerBound = 300, innerBound = 100, width = 80):
    list = []
    for x in range(-outerBound,outerBound,stepSize):
        for y in range(-outerBound,outerBound,stepSize):
            for z in range(-outerBound,outerBound,stepSize):
                list.append([x,y,z])

    x = pd.DataFrame(list,columns=['x','y','z'])
    x = calculateDistance(x,center())
    x = x.loc[(x.distance<outerBound)&(x.distance > innerBound)&(x.z<width)&(x.z>-width)].drop(columns='distance')

    x = jitterer(x, shift)
    print(x)
    return x