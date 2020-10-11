import numpy as np
import networkx as nx
import xlsxwriter
import math

def read_gt(gt_file, nodes):
    with open(('final_datasets/complex_datasets/gold_standard/' + gt_file + '.txt'), 'r') as f:
        gt_raw = []
        for item in f:
            gt_raw.append(item.split())

    if gt_file == 'sgd':
        # determine ground truth communities
        gt_comms = []
        gt_nodes = []
        for g in gt_raw:
            gt_comms.append(str(g[1]))
            gt_nodes.append(str(g[0]))
        gt_comms = list(set(gt_comms))
        gt_nodes = list(set(gt_nodes))

        # append to "nodes" the nodes not in it but found in gt_nodes
        ex_nodes_count = 0
        for gn in gt_nodes:
            if gn not in nodes:
                nodes.append(gn)
                ex_nodes_count += 1

        # form ground truth theta
        gt_theta = np.zeros((len(nodes), len(gt_comms)))
        for g in gt_raw:
            n_index = nodes.index(g[0])
            c_index = gt_comms.index(g[1])
            gt_theta[n_index, c_index] = 1.0

    elif gt_file == 'mips_3_100':
        # append to "nodes" the nodes not in it but found in gt_nodes
        gt_nodes = set()
        for g in gt_raw:
            gt_nodes.update(g)

        ex_nodes_count = 0
        for gn in gt_nodes:
            if gn not in nodes:
                nodes.append(gn)
                ex_nodes_count += 1

        # form ground truth theta
        gt_theta = np.zeros((len(nodes), len(gt_raw)))
        for j in range(len(gt_raw)):
            for cn in gt_raw[j]:
                n_index = nodes.index(cn)
                gt_theta[n_index, j] = 1.0

    return gt_theta, ex_nodes_count, nodes

def calc_mmr(pred_c, gt_c, dataset, gt_dataset):
    # predicted and ground truth comms count
    pred_count = pred_c.shape[1]
    gt_count = gt_c.shape[1]

    # create bipartite graph
    G = nx.Graph()
    G.add_nodes_from(range(pred_count + gt_count))

    for i in range(pred_count):
        for j in range(gt_count):
            predvec = pred_c[:, i]
            gtvec = gt_c[:, j]
            w = (np.dot(predvec, gtvec)/(np.dot(np.linalg.norm(predvec), np.linalg.norm(gtvec))))**2
            G.add_edge(i, j + pred_count, weight = w)
    print('created weighted bipartite graph using predicted and ground truth communities')

    matching = list(nx.algorithms.max_weight_matching(G))
    # save matching
    with open('matching_' + dataset + '_' + gt_dataset + '.txt', 'w') as fp:
        for row in matching:
            fp.write(str(row) + '\n')
    print('computed and saved max weight matching')

    mmr = 0
    for e in matching:
        mmr += G.get_edge_data(e[0], e[1])['weight']

    mmr /= gt_count
    return mmr

def calc_frac(pred_c, gt_c):
    # predicted and ground truth comms count
    pred_count = pred_c.shape[1]
    gt_count = gt_c.shape[1]

    match_count = 0
    for i1 in range(gt_count):
        for j1 in range(pred_count):
            gtvec = gt_c[:, i1]
            predvec = pred_c[:, j1]
            curr_match = (np.dot(predvec, gtvec) / (np.dot(np.linalg.norm(predvec), np.linalg.norm(gtvec)))) ** 2
            if curr_match >= 0.25:
                match_count += 1
                break
    return match_count/gt_count

def calc_acc(pred_c, gt_c):
    # predicted and ground truth comms count
    pred_count = pred_c.shape[1]
    gt_count = gt_c.shape[1]
    t = np.zeros((gt_count, pred_count))
    for i1 in range(gt_count):
        for j1 in range(pred_count):
            t[i1, j1] = np.dot(gt_c[:, i1], pred_c[:, j1])

    sn_num = 0.0
    sn_den = 0.0
    for q in range(gt_count):
        sn_num += np.max(t[q, :])
        sn_den += np.sum(gt_c[:, q])
    sn = sn_num / sn_den

    ppv_num = 0.0
    ppv_den = 0.0
    for j1 in range(pred_count):
        ppv_num += np.max(t[:, j1])
        ppv_den += np.sum(t[:, j1])
    ppv = ppv_num / ppv_den

    return math.sqrt(sn*ppv)

#-----------------------------------------------------------------------------------------------------
# parameter choices
# select dataset from: krogan2006_core, krogan2006_extended, collins2007
dataset = 'krogan2006_core'

# select validation (ground truth) dataset from: mips_3_100, sgd
gt_dataset = 'mips_3_100'

discard_small = False
cs_tol = 0.0 # threshold for comm size based on third largest entry in community vector

binary_memberships = True # whether to consider binary or fractional memberships
rounding_tol = 0.5 # quantity for rounding fractional data to binary
merge_comms = True
merge_tol = 0.8
#-----------------------------------------------------------------------------------------------------

# load nodes list
with open(('nodes_' + dataset + '.txt'), 'r') as f:
    nodes = []
    for item in f:
        nodes.append(item.strip('\n'))
gt_comms, ex_nodes_count, nodes = read_gt(gt_dataset, nodes)
print('computed ground truth communities for ' + gt_dataset)

# load cvx opt solutions
optsols = np.load('opt_sols_' + dataset + '.npy')
n = optsols.shape[1]
k = optsols.shape[0]
optsols = np.transpose(np.squeeze(optsols, axis = 2))
print('finished loading cvx optimal solutions')
print('original # of communities: ' + str(k))

# convert opt sols to 0-1
if binary_memberships:
    optsols = (optsols > rounding_tol).astype(int)
    print('rounded fractional memberships to obtain binary memberships')

# remove communities based on their third largest values
if discard_small:
    i = 0
    rem = 0
    while i < optsols.shape[1]:
        c = optsols[:, i]
        c = np.sort(c)
        if c[-3] <= cs_tol:
            optsols = np.delete(optsols, i, axis = 1)
            rem += 1
        else:
            i += 1
    print('# of communities after removing communities with <= 2 nodes: ' + str(k-rem))

# remove duplicate communities
optsols = np.unique(optsols, axis=1)
print('# of communities after removing duplicates: ' + str(optsols.shape[1]))

# merge highly overlapping communities
if merge_comms and binary_memberships:
    num_merges = 1
    while num_merges > 0:
        num_merges = 0
        for i in range(optsols.shape[1]):
            j = i+1
            while j in range(i+1, optsols.shape[1]):
                ovr = (np.dot(optsols[:, i], optsols[:, j]))**2
                ovr /= np.sum(optsols[:, i])
                ovr /= np.sum(optsols[:, j])
                if ovr >= merge_tol:
                    optsols[:, i] = np.maximum(optsols[:, i], optsols[:, j])
                    optsols = np.delete(optsols, j, axis=1)
                    num_merges += 1
                else:
                    j += 1
    # check no highly overlapping communities remain
    ovr = np.zeros((optsols.shape[1], optsols.shape[1]))
    for i in range(optsols.shape[1]):
        for j in range(optsols.shape[1]):
            if i != j:
                curr_ovr = (np.dot(optsols[:, i], optsols[:, j]))**2
                curr_ovr /= (np.linalg.norm(optsols[:, i]))**2
                curr_ovr /= (np.linalg.norm(optsols[:, j]))**2
                ovr[i, j] = curr_ovr
    assert np.max(ovr) < merge_tol
    print('# of communities after merging highly overlapping ones: ' + str(optsols.shape[1]))

if binary_memberships and discard_small:
    assert np.min(np.sum(optsols, axis=0)) >= 3.0

# pad optsols for extra nodes found in ground truth data to obtain predicted communities
pred_comms = np.concatenate((optsols, np.zeros((ex_nodes_count, optsols.shape[1]))))

print('smallest predicted community size: ' + str(np.min(np.sum(pred_comms, axis=0))))
print('largest predicted community size: ' + str(np.max(np.sum(pred_comms, axis=0))))

# save bipartite graph data
# save nodes
with open('nodes_' + dataset + '_' + gt_dataset + '.txt', 'w') as fp:
    for item in nodes:
        fp.write("%s\n" % item)
np.save('pred_comms_' + dataset + '_' + gt_dataset + '.npy', pred_comms)
np.save('gt_comms_' + dataset + '_' + gt_dataset + '.npy', gt_comms)
print('finished saving bipartite graph data')

# obtain three scores - mmr, frac, acc
# obtain mmr
mmr = calc_mmr(pred_comms, gt_comms, dataset, gt_dataset)
print('mmr: ' + str(mmr))

# obtain frac
frac = calc_frac(pred_comms, gt_comms)
print('frac: ' + str(frac))

# obtain acc
acc = calc_acc(pred_comms, gt_comms)
print('geo accuracy: ' + str(acc))

comp_score = mmr + frac + acc
print('composite score: ' + str(comp_score))

# # save a sample community vector
# sample_com_vec = np.ndarray.tolist(pred_comms[:, 120])
# sample = []
# for i in range(len(nodes)):
#     sample.append([nodes[i], sample_com_vec[i]])
# with xlsxwriter.Workbook('sample.xlsx') as wb:
#     ws = wb.add_worksheet()
#     for row_num, data in enumerate(sample):
#         ws.write_row(row_num, 0, data)
