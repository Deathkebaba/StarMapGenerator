#before maudi optimized
import pandas as pd
import math
from pandas import DataFrame
from random import gauss
import time

#os.chdir('data')

#Generates Coordinates for a star
def createStar(size):
    starCoordinates = [round(gauss(0,size),2),round(gauss(0,size),2),round(gauss(0,size/6),2)]
    star = pd.Series(starCoordinates, index=['x','y','z'])
    return star

#checks distance to closest star
def checkdist(listofstars, star):
    xdf = listofstars['x'] - star['x']
    ydf = listofstars['y'] - star['y']
    zdf = listofstars['z'] - star['z']
    squaredf = (xdf**2 + ydf**2 + zdf**2)
    rootdf = squaredf**(0.5)
    minimumDistance = rootdf.min()
    return minimumDistance

#checks distance to center
def checkdistcenter (star):
    result = math.sqrt(star['x']**2+star['y']**2+star['z']**2)
    return result

def run(numberOfStars = 5000, starDistance = 15, size = 200 ,centerDistance = 100, failsafe = 40):
    #creates the Dataframe that will contain the stars, adds the first star
    stars_map = DataFrame(columns=['x','y','z'])
    blackhole = star = pd.Series([0,0,0], index=['x','y','z'])
    stars_map.loc[len(stars_map)] = blackhole
    failsafeCounter = 0
    errorcount = 0
    timer1Start = time.time()

    #checks if star is eligible, then adds it to the dataframe
    while (len(stars_map.index) < numberOfStars) :
        print('\r',f'Goal: {numberOfStars} Star: {len(stars_map.index):6d}  Failsafecounter: {failsafeCounter:2d} time: {time.time()-timer1Start:.2f}', end='')
        newStar = createStar(size)
        if (checkdistcenter(newStar)>centerDistance) : 
            if(checkdist(stars_map,newStar) > starDistance):
                stars_map.loc[len(stars_map)] = newStar
                failsafeCounter = 0
                continue
        failsafeCounter += 1
        errorcount += 1
        if failsafeCounter == failsafe :
            print("failed to find another star")
            break

    timer1End = time.time()

    print("goal number of stars: {}\nnumber of stars created: {} \nfailed starbirths: {}\ntime needed for calculations: {}s".format(numberOfStars,len(stars_map.index),errorcount,round((timer1End-timer1Start),2)))
    stars_map.index.name = 'starID'
    print(stars_map)
    return stars_map

if __name__ =="__main__":
    run()
