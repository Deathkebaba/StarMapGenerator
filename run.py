from generators import randomGeneratorBig
from mapVisualizer import visualize

map = randomGeneratorBig.run()
visualize(map)
map.to_csv("datadump/map.csv")