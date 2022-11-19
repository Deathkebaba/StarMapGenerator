import numpy as np
import pandas as pd
from time import time
from tqdm import tqdm


def maudi():
    stepSize = 5
    count = 120
    maxN = count**3
    c3 = [
        [int(x / count ** (2) % count), int(x / count % count), int(x % count)]
        for x in range(int(maxN))
    ]


def yassin():
    outerBound = 300
    stepSize = 5
    list = []
    for x in range(-outerBound, outerBound, stepSize):
        for y in range(-outerBound, outerBound, stepSize):
            for z in range(-outerBound, outerBound, stepSize):
                list.append([x, y, z])


def yassin2():
    x = 480
    arr1 = []
    arr2 = []
    arr3 = []
    for i in range(x):
        arr1 += [i]
        arr2 += [i] * x
        arr3 += [i] * x * x
    arr1 *= x * x
    arr2 *= x
    arrFinal = [arr1, arr2, arr3]


# timeStart = time()
# for x in tqdm(range(20)):
#    maudi()
# print(time() - timeStart, "Maudi")
#
#
# timeStart = time()
# for x in tqdm(range(20)):
#    yassin()
# print(time() - timeStart, "yassin")
timeStart = time()
for x in tqdm(range(20)):
    yassin2()
print(time() - timeStart, "yassin")
