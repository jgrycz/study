import numpy as np


def calc_target(row):
    if row[6] == 0 and row[7] == 0:
        return 4
    elif row[6] == 1 and row[7] == 1:
        return 3
    elif row[6] == 1:
        return 2
    elif row[7] == 1:
        return 1


file_path = "data/diagnosis.data"

converters = {i: lambda s: 0 if s == b'no' else 1 for i in range(0, 8)}
converters[0] = lambda n: float(n.replace(b",", b"."))

array = np.loadtxt(file_path, delimiter="\t", converters=converters)
target = np.array([calc_target(row) for row in array])
import pdb; pdb.set_trace()


inflammation = array[(array[:,6] == 1)]
nephritis = array[(array[:,7] == 1)]
healthy = array[(array[:,7] == 0) & (array[:,6] == 0)]
avg_inflammation = np.average(inflammation, axis=0)
avg_nephritis = np.average(nephritis, axis=0)

distance_inflammation = np.array([np.linalg.norm(row[:6] - avg_inflammation[:6]) for row in inflammation])
distance_nephritis = np.array([np.linalg.norm(row[:6] - avg_nephritis[:6]) for row in nephritis])
distance_helthy_ne = np.array([np.linalg.norm(row[:6] - avg_nephritis[:6]) for row in healthy])
distance_helthy_in = np.array([np.linalg.norm(row[:6] - avg_inflammation[:6]) for row in healthy])


# print("inflammation")
# print("\n".join("{:<20} - {}".format(d, i) for i, d in sorted(zip(inflammation, distance_inflammation), key=lambda z: z[1])))
# print("\n\nhealthy to inflammation")
# print("\n".join("{:<20} - {}".format(d, i) for i, d in sorted(zip(healthy, distance_helthy_in), key=lambda z: z[1])))
# print("\n\nnephritis")
# print("\n".join("{:<20} - {}".format(d, i) for i, d in sorted(zip(nephritis, distance_nephritis), key=lambda z: z[1])))
# print("\n\nhealthy to nephritis")
# print("\n".join("{:<20} - {}".format(d, i) for i, d in sorted(zip(healthy, distance_helthy_ne), key=lambda z: z[1])))


# n_array = np.array([row[:6] for row in array])
# print(n_array)
# from sklearn.neighbors import NearestNeighbors
# import numpy as np
# # X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
# nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(n_array)
# distances, indices = nbrs.kneighbors(n_array)
# print(indices)
# print(distances)



print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets

n_neighbors = 15

# import some data to play with
iris = datasets.load_iris()
# X = iris.data[:, :2]  # we only take the first two features. We could
                      # avoid this ugly slicing by using a two-dim dataset
# y = iris.target
X = array[:, :2]
y = target

h = .02  # step size in the mesh

# Create color maps
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF', '#AAAA00'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF', '#000000'])

for weights in ['uniform', 'distance']:
    # we create an instance of Neighbours Classifier and fit the data.
    clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
    clf.fit(X, y)

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, m_max]x[y_min, y_max].
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure()
    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.title("3-Class classification (k = %i, weights = '%s')"
              % (n_neighbors, weights))

plt.show()
