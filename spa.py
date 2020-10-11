import numpy as np

# select dataset from: krogan2006_core, krogan2006_extended, collins2007
dataset = 'krogan2006_core'

P = np.load('p_' + dataset + '.npy')
print('finished loading matrix P for dataset ' + dataset)

n = len(P)

# recommended k value for
# krogran2006_core (validation against SGD): 1350
# krogran2006_core (validation against MIPS): 950
# krogran2006_extended (validation against SGD, MIPS): 1900
# collins2007 (validation against SGD): 800
# collins2007 (validation against MIPS): 450
k = 950

J = []
for j in range(k):
    col_norms = np.sum(np.multiply(P, P), axis = 0)
    max_ind = np.where(col_norms == np.max(col_norms))[0][0]
    J.append(max_ind)
    v = np.reshape(P[:, max_ind], (n, 1))
    mat1 = np.dot(np.transpose(v), P)
    mat2 = np.dot(v, mat1)/(col_norms[max_ind])
    P -= mat2
    if j % 10 == 0:
        print('found ' + str(j) + ' almost pure nodes out of ' + str(k))

# save pure nodes
with open('J_' + dataset + '.txt', 'w') as fp:
    for item in J:
        fp.write("%s\n" % item)
print('finished computing and saving pure nodes for dataset ' + dataset)
