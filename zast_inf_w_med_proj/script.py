from pprint import pprint as pp
import numpy as np


file_path = "data/diagnosis.data"

converters = {i: lambda s: 0 if s == 'no' else 1 for i in range(0, 8)}
converters[0] = lambda n: float(n.replace(",", "."))

array = np.loadtxt(file_path, delimiter="\t", converters=converters)

inflammation = array[(array[:,6] == 1)]
nephritis = array[(array[:,7] == 1)]
healthy = array[(array[:,7] == 0) & (array[:,6] == 0)]
avg_inflammation = np.average(inflammation, axis=0)
avg_nephritis = np.average(nephritis, axis=0)

distance_inflammation = np.array([np.linalg.norm(row - avg_inflammation) for row in inflammation])
distance_nephritis = np.array([np.linalg.norm(row - avg_nephritis) for row in nephritis])
distance_helthy_ne = np.array([np.linalg.norm(row - avg_nephritis) for row in healthy])
distance_helthy_in = np.array([np.linalg.norm(row - avg_inflammation) for row in healthy])

print "\n".join("{} - {}".format(d, i) for i, d in zip(inflammation, distance_inflammation))
print "\n\n"
print "\n".join("{} - {}".format(d, i) for i, d in zip(nephritis, distance_nephritis))
print "\n\n"
print "\n".join("{} - {}".format(d, i) for i, d in zip(healthy, distance_helthy_ne))
print "\n\n"
print "\n".join("{} - {}".format(d, i) for i, d in zip(healthy, distance_helthy_in))
