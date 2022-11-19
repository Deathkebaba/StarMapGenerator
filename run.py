from generators import jitterGenerator as generator
from mapVisualizer import visualize3d

map = generator.run()
visualize3d(map)
map.to_csv("datadump/map.csv")
