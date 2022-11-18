import pandas as pd
import math
from random import gauss
from time import time


#Generates Coordinates for a star
def createStar(size):
    #sets universe size
    starCoordinates = [round(gauss(0,size),2),round(gauss(0,size),2),round(gauss(0,size/6),2)]
    star = pd.Series(starCoordinates, index=['x','y','z'])
    return star

#checks distance to closest star
def checkdist(listofstars, star, dist):
    listofstars = listofstars.loc[(listofstars['x'] <=( star['x'] + dist))&(listofstars['x'] >=( star['x'] - dist))&(listofstars['y'] <=( star['y'] + dist))&(listofstars['y'] >=( star['y'] - dist))&(listofstars['z'] <=( star['z'] + dist))&(listofstars['z'] >=( star['z'] - dist))]
    if len(listofstars.index) == 0:
        return dist*2
    xdf = listofstars['x'] - star['x']
    ydf = listofstars['y'] - star['y']
    zdf = listofstars['z'] - star['z']
    squaredf = (xdf**2 + ydf**2 + zdf**2)
    rootdf = squaredf**0.5
    minimumDistance = rootdf.min()
    return minimumDistance

#checks distance to center
def checkdistcenter (star):
    result = math.sqrt(star['x']**2+star['y']**2+star['z']**2)
    return result

def run(numberOfStars = 5000, starDistance = 15, size = 200 ,centerDistance = 100, failsafe = 40):
    #creates layers of DataFrame
    layers= math.floor((size*5 -centerDistance)/starDistance)
    layerDic = {}
    for x in range(layers):
        layerDic[x]=pd.DataFrame(columns=['x','y','z'])
        layerDic[x].index.name = 'starID'

    #variables
    starID = 0
    failsafeCounter = 0
    errorcount = 0
    timer1Start = time()
    print('randomGeneratorBig initiated, generating stars:')

    #checks if star is eligible, then adds it to the dataframe
    while starID < numberOfStars :
        print('\r',f'Goal: {numberOfStars}  Current: {starID:6d}  Failsafecounter: {failsafeCounter:2d} time: {time()-timer1Start:.2f}', end='')
        newStar = createStar(size)
        starCenterDistance =checkdistcenter(newStar)
        if starCenterDistance>centerDistance : 
            layer = min(max(math.floor((starCenterDistance-centerDistance)/starDistance),1),layers-2)
            minDistanceCounter=[2*starDistance]
            for x in range(layer-1,layer+2):
                minDistanceCounter.append(checkdist(layerDic[x],newStar, starDistance))
            if not min(minDistanceCounter) > starDistance:
                failsafeCounter += 1
                errorcount += 1
                if failsafeCounter == failsafe :
                    print("failed to find another star")
                    break
                continue

            layerDic[layer].loc[starID] = newStar
            starID += 1
            failsafeCounter = 0


    timer1End = time()

    print("\nnumber of stars created: {} \nfailed starbirths: {}\ntime needed for calculations: {}s".format(numberOfStars,errorcount,round(timer1End-timer1Start),2))
    stars_map = pd.concat(layerDic).droplevel(0).sort_index()
    print(stars_map)
    return stars_map

if __name__ == '__main__':
    run()