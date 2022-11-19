from numpy.random import normal
from pandas import DataFrame
from .helpers import calculateDistance, center


def jitterer(df: DataFrame, shift: float = 2) -> DataFrame:
    """Shifts each value in a DataFrame by a normal distribution random value.

    Args:
        df (DataFrame): The DataFrame you want to shift.
        shift (float, optional): Standard deviation of the normal distribution used for the jitter. Defaults to 2.

    Returns:
        DataFrame: The shifted Dataframe.
    """
    x = len(df.index)
    y = len(df.columns)
    jitterdf = DataFrame(normal(0, shift, [x, y]), columns=df.columns)
    jitterdf.index = df.index
    df = df - jitterdf
    df.index.name = "starID"
    return df


def run(stepSize=16, shift=10, outerBound=300, innerBound=100, width=80) -> DataFrame:
    """Generates point cloud shaped like the center slice of a sphere. Points are generated  in ordered cubic grid, then shifted with normal distributed random numbers.

    Args:
        stepSize (int, optional): Average distance between points. Defaults to 5.
        shift (int, optional): Standard deviation of the normal distribution used for shifting the points. Defaults to 10.
        outerBound (int, optional): Outer bound of the sphere. Defaults to 300.
        innerBound (int, optional): Intter bound of the shere. Defaults to 100.
        width (int, optional): Thickness of the center slice. Defaults to 80.

    Returns:
        DataFrame: The final table of points.
    """
    # listlenght = (2 * outerBound / stepSize) ^ 3
    width /= 2
    list = []
    for x in range(-outerBound, outerBound, stepSize):
        for y in range(-outerBound, outerBound, stepSize):
            for z in range(-outerBound, outerBound, stepSize):
                list.append([x, y, z])

    x = DataFrame(list, columns=["x", "y", "z"])
    x = calculateDistance(x, center())
    x = x.loc[
        (x.distance < outerBound)
        & (x.distance > innerBound)
        & (x.z < width)
        & (x.z > -width)
    ].drop(columns="distance")

    x = jitterer(x, shift)
    print(x)
    return x
