import gzip
from collections import defaultdict
import numpy 
from random import sample, randint
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

def readGz(f):
  for l in gzip.open(f):
    yield eval(l)

def predict(user, item, b_u, b_i, a):
  try:
    u = userIds[user]
    i = itemIds[item]
    return a + b_u[u] + b_i[i]
  except KeyError:
    return a

def lfm_main(x_train, b_u, b_i, a, iterate_times, labmda):
  for _ in range(iterate_times):
    for j in range(len(x_train)):
      u = x_train[j][0]
      i = x_train[j][1]
      userItems = userItem[u]
      b_u[u] = (- a * len(userItems) - b_i[userItems].sum() + R[u,userItems].sum()) / (labmda + len(userItems))
      itemUsers = itemUser[i]
      b_i[i] = (- a * len(itemUsers) - b_u[itemUsers].sum() + R[itemUsers, i].sum()) / (labmda + len(itemUsers))     
  return a, b_i, b_u

data = list(readGz('train.json.gz'))

users = list(set([d['reviewerID'] for d in data]))
items = list(set([d['itemID'] for d in data]))
num_users = len(users)
num_items = len(items)
userIds = dict(zip(users, range(num_users)))
itemIds = dict(zip(items, range(num_items)))

R = numpy.zeros((num_users, num_items))
nums = numpy.zeros((num_users, num_items))
userItem = defaultdict(list)
itemUser = defaultdict(list)
for d in data:
  u = userIds[d['reviewerID']]
  i = itemIds[d['itemID']]
  R[u][i] = d['rating']
  nums[u][1] += 1
  userItem[u].append(i)
  itemUser[i].append(u)

nums[nums == 0] = 1
R /= nums 

x_train = numpy.array([[userIds[d['reviewerID']], itemIds[d['itemID']]] for d in data])
y_train = numpy.array([d['rating'] for d in data])

b_u = numpy.random.random((num_users,))
b_i = numpy.random.random((num_items))
a = y_train.mean()

a, b_i, b_u= lfm_main(x_train, b_u, b_i, a, 30, 20)


predictions = open("predictions_Rating.txt", 'w')
for l in open("pairs_Rating.txt"):
  if l.startswith("reviewerID"):
    predictions.write(l) 
    continue
  u,i = l.strip().split('-')
  p = predict(u, i , b_u, b_i, a)
  predictions.write(u + '-' + i + ',' + str(p) + '\n')
predictions.close()