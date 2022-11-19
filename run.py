from generators import jitterGenerator as generator
from mapVisualizer import visualize

map = generator.run()
visualize(map)
map.to_csv("datadump/map.csv")