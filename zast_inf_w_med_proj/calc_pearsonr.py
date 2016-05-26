from scipy.stats import pearsonr
from pprint import pprint as pp
import numpy as np


def load_data():
    file_path = "data/diagnosis.data"
    converters = {i: lambda s: 0 if s == b'no' else 1 for i in range(0, 8)}
    converters[0] = lambda n: float(n.replace(b",", b"."))
    array = np.loadtxt(file_path, delimiter="\t", converters=converters)
    return array


def calc_target(row):
    if row[6] == 0 and row[7] == 0:
        return 3
    elif row[6] == 1 and row[7] == 1:
        return 2
    elif row[6] == 1:
        return 1
    elif row[7] == 1:
        return 0


array = load_data()
target = np.array([calc_target(row) for row in array])
values = [pearsonr(array[:, i], target) for i in range(6)]
pp(values)
