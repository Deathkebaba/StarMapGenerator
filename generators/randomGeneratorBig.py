import pandas as pd
from pandas import DataFrame, Series, concat
import math
from random import gauss
from time import time


def createStar(size: float, thickness: float = 1 / 6) -> Series:
    """Create point based on normal distributed spheroid.

    Args:
        size (float): Standard deviation of normal distribution.
        thickness (float, optional): comression of the z-axis. Defaults to 1/6.

    Returns:
        Series: index = ['x','y','z']
    """
    starCoordinates = [
        round(gauss(0, size), 2),
        round(gauss(0, size), 2),
        round(gauss(0, size * thickness), 2),
    ]
    star = Series(starCoordinates, index=["x", "y", "z"])
    return star


def checkdist(listofstars: DataFrame, star: Series, dist: float) -> float:
    """Calculates the distance between a point and a table of points, returns minimum distance. Optimized for if you are looking for a certain distance.

    Args:
        listofstars (DataFrame): The table of points.
        star (Series): The single point.
        dist (float): The distance you want to check for

    Returns:
        float: The minimum distance
    """
    listofstars = listofstars.loc[
        (listofstars["x"] <= (star["x"] + dist))
        & (listofstars["x"] >= (star["x"] - dist))
        & (listofstars["y"] <= (star["y"] + dist))
        & (listofstars["y"] >= (star["y"] - dist))
        & (listofstars["z"] <= (star["z"] + dist))
        & (listofstars["z"] >= (star["z"] - dist))
    ]
    if len(listofstars.index) == 0:
        return dist * 2
    xdf = listofstars["x"] - star["x"]
    ydf = listofstars["y"] - star["y"]
    zdf = listofstars["z"] - star["z"]
    squaredf = xdf**2 + ydf**2 + zdf**2
    rootdf = squaredf**0.5
    minimumDistance = rootdf.min()
    return minimumDistance


def checkdistcenter(star: Series) -> float:
    """Calculates distance between point and [0,0,0]

    Args:
        star (Series): index = ['x','y','z']

    Returns:
        float: distance
    """
    result = math.sqrt(star["x"] ** 2 + star["y"] ** 2 + star["z"] ** 2)
    return result


def run(
    numberOfStars=5000,
    starDistance=15,
    size=200,
    centerDistance=100,
    failsafe=40,
    zCompression=1 / 6,
) -> DataFrame:
    """Creates a spheroid point cloud with a spherical empty center, points are normal distributed.

    Args:
        numberOfStars (int, optional): Mximum amount of points you want to generate. Defaults to 5000.
        starDistance (int, optional): Minimum distance between points. Defaults to 15.
        size (int, optional): Standard deviation of the normal distribution used for generating points. Defaults to 200.
        centerDistance (int, optional): Radius of empty sphere in center. Defaults to 100.
        failsafe (int, optional): Iteration depth before failing to find a fitting point resutls in stop. Defaults to 40.
        zCompression (float, optional): Z-axis compression of the sphere. Defaults to 40.
    Returns:
        DataFrame: The point cloud
    """
    layers = math.floor((size * 5 - centerDistance) / starDistance)
    layerDic = {}
    for x in range(layers):
        layerDic[x] = DataFrame(columns=["x", "y", "z"])
        layerDic[x].index.name = "starID"

    # variables
    starID = 0
    failsafeCounter = 0
    errorcount = 0
    timer1Start = time()
    print("randomGeneratorBig initiated, generating stars:")

    # checks if star is eligible, then adds it to the dataframe
    while starID < numberOfStars:
        print(
            "\r",
            f"Goal: {numberOfStars}  Current: {starID:6d}  Failsafecounter: {failsafeCounter:2d} time: {time()-timer1Start:.2f}",
            end="",
        )
        newStar = createStar(size, thickness=zCompression)
        starCenterDistance = checkdistcenter(newStar)
        if starCenterDistance > centerDistance:
            layer = min(
                max(
                    math.floor((starCenterDistance - centerDistance) / starDistance), 1
                ),
                layers - 2,
            )
            minDistanceCounter = [2 * starDistance]
            for x in range(layer - 1, layer + 2):
                minDistanceCounter.append(checkdist(layerDic[x], newStar, starDistance))
            if not min(minDistanceCounter) > starDistance:
                failsafeCounter += 1
                errorcount += 1
                if failsafeCounter == failsafe:
                    print("failed to find another star")
                    break
                continue

            layerDic[layer].loc[starID] = newStar
            starID += 1
            failsafeCounter = 0

    timer1End = time()

    print(
        "\nnumber of stars created: {} \nfailed starbirths: {}\ntime needed for calculations: {}s".format(
            numberOfStars, errorcount, round(timer1End - timer1Start), 2
        )
    )
    stars_map = concat(layerDic).droplevel(0).sort_index()
    print(stars_map)
    return stars_map


if __name__ == "__main__":
    run()
