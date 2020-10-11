import numpy as np
import xlrd
from numpy import savetxt

# select dataset from: krogan2006_core, krogan2006_extended, collins2007
dataset = 'krogan2006_extended'

# read ppi data
ppi = []
with open('final_datasets/ppi_datasets/datasets/' + dataset + '.txt', 'r') as f:
    for line in f:
        ppi.append(line.split())
print('finished reading ppi data from txt file')

# determine unique proteins, i.e. nodes
nodes = list(set([r[0] for r in ppi] + [r[1] for r in ppi]))
n = len(nodes)
print('nodes found: ' + str(n))

# save nodes
with open('nodes_' + dataset + '.txt', 'w') as fp:
    for item in nodes:
        fp.write("%s\n" % item)
print('finished saving nodes for dataset ' + dataset)

P = np.identity(n)
for r in ppi:
    row_index = nodes.index(r[0])
    col_index = nodes.index(r[1])
    P[row_index][col_index] = float(r[2])
    P[col_index][row_index] = P[row_index][col_index]

assert np.trace(P) == n
assert np.linalg.norm(P-np.transpose(P)) <= 0.000001
np.save('p_' + dataset + '.npy', P)
print('computed and saved P for ' + dataset + ' dataset')

