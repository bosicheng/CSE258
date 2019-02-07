import numpy
import urllib
import scipy.optimize
import random
from math import exp
from math import log
import networkx as nx
import matplotlib.pyplot as plt
import collections



# Karate club
G = nx.karate_club_graph()
nx.draw(G)
# plt.show()
plt.clf()

edges = set()
nodes = set()
for edge in urllib.urlopen("http://jmcauley.ucsd.edu/cse255/data/facebook/egonet.txt", 'r'):
  x,y = edge.split()
  x,y = int(x),int(y)
  edges.add((x,y))
  edges.add((y,x))
  nodes.add(x)
  nodes.add(y)

G = nx.Graph()
for e in edges:
  G.add_edge(e[0],e[1])
# nx.draw(G)
# plt.show()
plt.clf()

print("start bfs")

visited={}
graphs=[]

def BFS(node,nodes,visited):
  graph=set()
  queue=collections.deque([node])
  while queue:
    curr=queue.popleft()
    graph.add(curr)
    visited[curr]=True
    for next_node in nodes:
      if (curr,next_node) in edges and not visited[next_node]:
        queue.append(next_node)
  return graph


for node in nodes:
  visited[node]=False
  print(node)
print("build graphs")
for node in nodes:
  if not visited[node]:
    temp=BFS(node,nodes,visited)
    print(temp)
    graphs.append(temp)
print(graphs)

largest=sorted(list(graphs[0]))
print(largest)
cluster1=largest[:(len(largest)/2)]
cluster2=largest[(len(largest)/2):]
print(cluster1)
print(cluster2)
def normalized_cut(edges,cluster1,cluster2):
  edge_count=0
  degree1,degree2=0,0
  for edge in edges:
    if edge[0] in cluster1 and edge[1] in cluster1:
      degree1+=0.5
    elif edge[0] in cluster2 and edge[1] in cluster2:
      degree2+=0.5
    elif edge[0] in cluster1 and edge[1] in cluster2:
      degree1+=1
      degree2+=1
      edge_count+=1
  print(degree1)
  print(degree2)
  print(edge_count)
  normalized_cut=(edge_count/degree1+edge_count/degree2)/2
  return normalized_cut

minimum=normalized_cut(edges,cluster1,cluster2)
print(minimum)
change1,change2=[],[]
for i in range(len(cluster1)):
  temp1=cluster1[:i]+cluster1[i:]
  temp2=cluster2+[cluster1[i]]
  print(temp1,temp2)
  temp=normalized_cut(edges,temp1,temp2)
  if temp<minimum:
    minimum=temp
    change1.append(cluster1[i])
for move_node in cluster2:
  temp1=cluster1+[cluster2[i]]
  temp2=cluster2[:i]+cluster2[i:]
  temp=normalized_cut(edges,temp1,temp2)
  if temp<minimum:
    minimum=temp
    change2.append(move_node)
for node in change1:
  cluster1.remove(node)
  cluster2.append(node)
for node in change2:
  cluster1.append(node)
  cluster2.remove(node)
print(cluster1)
print(cluster2)
print(minimum)










## Find all 3 and 4-cliques in the graph ###
# cliques3 = set()
# cliques4 = set()
# for n1 in nodes:
#   for n2 in nodes:
#     if not ((n1,n2) in edges): continue
#     for n3 in nodes:
#       if not ((n1,n3) in edges): continue
#       if not ((n2,n3) in edges): continue
#       clique = [n1,n2,n3]
#       clique.sort()
#       cliques3.add(tuple(clique))
#       for n4 in nodes:
#         if not ((n1,n4) in edges): continue
#         if not ((n2,n4) in edges): continue
#         if not ((n3,n4) in edges): continue
#         clique = [n1,n2,n3,n4]
#         clique.sort()
#         cliques4.add(tuple(clique))



# def parseData(fname):
#   for l in urllib.urlopen(fname):
#     yield eval(l)

# print("Reading data...")
# data = list(parseData("http://jmcauley.ucsd.edu/cse190/data/beer/beer_50000.json"))
# print("done")

# def feature(datum):
#   feat = [1, datum['review/taste'], datum['review/appearance'], datum['review/aroma'], datum['review/palate'], datum['review/overall']]
#   return feat

# X = [feature(d) for d in data]
# y = [d['beer/ABV'] >= 6.5 for d in data]

# def inner(x,y):
#   return sum([x[i]*y[i] for i in range(len(x))])

# def sigmoid(x):
#   return 1.0 / (1 + exp(-x))

# ##################################################
# # Logistic regression by gradient ascent         #
# ##################################################

# # NEGATIVE Log-likelihood
# def f(theta, X, y, lam):
#   loglikelihood = 0
#   for i in range(len(X)):
#     logit = inner(X[i], theta)
#     loglikelihood -= log(1 + exp(-logit))
#     if not y[i]:
#       loglikelihood -= logit
#   for k in range(len(theta)):
#     loglikelihood -= lam * theta[k]*theta[k]
#   # for debugging
#   # print("ll =" + str(loglikelihood))
#   return -loglikelihood

# # NEGATIVE Derivative of log-likelihood
# def fprime(theta, X, y, lam):
#   dl = [0]*len(theta)
#   for i in range(len(X)):
#     logit = inner(X[i], theta)
#     for k in range(len(theta)):
#       dl[k] += X[i][k] * (1 - sigmoid(logit))
#       if not y[i]:
#         dl[k] -= X[i][k]
#   for k in range(len(theta)):
#     dl[k] -= lam*2*theta[k]
#   return numpy.array([-x for x in dl])

# cutlen=len(data)/3
# print(cutlen)
# ranstart=random.sample(range(cutlen),1)[0]
# print(ranstart)
# x_train=X[ranstart:(ranstart+cutlen)]
# y_train=y[ranstart:(ranstart+cutlen)]
# x_valid=X[(ranstart+cutlen):(ranstart+2*cutlen)]
# y_valid=y[(ranstart+cutlen):(ranstart+2*cutlen)]
# x_test=X[(ranstart+2*cutlen):]+X[:ranstart]
# y_test=y[(ranstart+2*cutlen):]+y[:ranstart]

# ##################################################
# # Train                                          #
# ##################################################

# def train(lam):
#   theta,_,_ = scipy.optimize.fmin_l_bfgs_b(f, [0]*len(X[0]), fprime, pgtol = 10, args = (x_train, y_train, lam))
#   return theta

# ##################################################
# # Predict                                        #
# ##################################################

# def performance(theta):
#   res_train = [inner(theta,x) for x in x_train]
#   res_valid = [inner(theta,x) for x in x_valid]
#   res_test = [inner(theta,x) for x in x_test]

#   pred_train = [s > 0 for s in res_train]
#   pred_valid = [s > 0 for s in res_valid]
#   pred_test = [s > 0 for s in res_test]

#   correct_train = [(a==b) for (a,b) in zip(pred_train,y_train)]
#   correct_valid = [(a==b) for (a,b) in zip(pred_valid,y_valid)]
#   correct_test = [(a==b) for (a,b) in zip(pred_test,y_test)]

#   acc_train = sum(correct_train) * 1.0 / len(correct_train)
#   acc_valid = sum(correct_valid) * 1.0 / len(correct_valid)
#   acc_test = sum(correct_test) * 1.0 / len(correct_test)
#   return acc_train, acc_valid, acc_test

# ##################################################
# # Validation pipeline                            #
# ##################################################

# lam = 0
# theta = train(lam)
# acc_train, acc_valid, acc_test = performance(theta)
# print("train=" + str(acc_train))
# print("valid=" + str(acc_valid))
# print("test=" + str(acc_test))