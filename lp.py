import numpy as np
from cvxopt import matrix, solvers

# select dataset from: krogan2006_core, krogan2006_extended, collins2007
dataset = 'krogan2006_core'

# load pure nodes
with open(('J_' + dataset + '.txt'), 'r') as f:
    pns = []
    for item in f:
        pns.append(int(item))

P = np.load('p_' + dataset + '.npy')
print('finished loading matrix P for dataset ' + dataset)

n = P.shape[0]
k = len(pns)

D, Q = np.linalg.eigh(P)
V = Q[:, n-k:n]
print('computed ' + str(k) + ' largest eigenvalues/eigenvectors of P')

rhs = [0.0] * (n + 1)
rhs[n] = -1.0
rhs = matrix(rhs)
c = np.ndarray.tolist(np.dot(np.ones(n), V))
c = matrix(c)
opt_sols = []
num_sols = 0
for l in range(k):
    lhs = np.ndarray.tolist(V*-1)
    lhs = lhs + [lhs[pns[l]]]
    lhs = list(map(list, zip(*lhs)))
    lhs = matrix(lhs)

    solvers.options['show_progress'] = False
    sol = solvers.lp(c=c, G=lhs, h=rhs)

    if sol['status'] == 'optimal':
        xopt = np.dot(V, sol['x'])
        xopt /= np.max(xopt)
        opt_sols.append(xopt)
        num_sols += 1

    if l % 10 == 0:
        print('solved ' + str(l) + ' LPs out of ' + str(k))

np.save('opt_sols_' + dataset + '.npy', np.array(opt_sols))
print('determined and saved ' + str(num_sols) + ' optimal solutions')
