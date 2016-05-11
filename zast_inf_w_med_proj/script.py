import numpy as np


file_path = "data/diagnosis.data"

converters = {i: lambda s: 0 if s == 'no' else 1 for i in range(0, 8)}
converters[0] = lambda n: float(n.replace(",", "."))

array = np.loadtxt(file_path, delimiter="\t", converters=converters)
