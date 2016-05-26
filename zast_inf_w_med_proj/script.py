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

distance_inflammation = np.array([np.linalg.norm(row[:6] - avg_inflammation[:6]) for row in inflammation])
distance_nephritis = np.array([np.linalg.norm(row[:6] - avg_nephritis[:6]) for row in nephritis])
distance_helthy_ne = np.array([np.linalg.norm(row[:6] - avg_nephritis[:6]) for row in healthy])
distance_helthy_in = np.array([np.linalg.norm(row[:6] - avg_inflammation[:6]) for row in healthy])

print "inflammation"
print "\n".join("{:<14} - {}".format(d, i) for i, d in sorted(zip(inflammation, distance_inflammation), key=lambda z: z[1]))
print "\n\nhealthy to inflammation"
print "\n".join("{:<14} - {}".format(d, i) for i, d in sorted(zip(healthy, distance_helthy_in), key=lambda z: z[1]))
print "\n\nnephritis"
print "\n".join("{:<14} - {}".format(d, i) for i, d in sorted(zip(nephritis, distance_nephritis), key=lambda z: z[1]))
print "\n\nhealthy to nephritis"
print "\n".join("{:<14} - {}".format(d, i) for i, d in sorted(zip(healthy, distance_helthy_ne), key=lambda z: z[1]))
