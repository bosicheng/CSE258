import gzip
from collections import defaultdict
import random

def readGz(f):
  for l in gzip.open(f):
    yield eval(l)

### Rating baseline: compute averages for each user, or return the global average if we've never seen the user before

allRatings = []
userRatings = defaultdict(list)
for l in readGz("train.json.gz"):
  user,business = l['reviewerID'],l['itemID']
  allRatings.append(l['rating'])
  userRatings[user].append(l['rating'])

globalAverage = sum(allRatings) / len(allRatings)
userAverage = {}
for u in userRatings:
  userAverage[u] = sum(userRatings[u]) / len(userRatings[u])

predictions = open("predictions_Rating.txt", 'w')
for l in open("pairs_Rating.txt"):
  if l.startswith("reviewerID"):
    #header
    predictions.write(l)
    continue
  u,i = l.strip().split('-')
  if u in userAverage:
    predictions.write(u + '-' + i + ',' + str(userAverage[u]) + '\n')
  else:
    predictions.write(u + '-' + i + ',' + str(globalAverage) + '\n')

predictions.close()

### Would-purchase baseline: just rank which businesses are popular and which are not, and return '1' if a business is among the top-ranked
# businessCount, userCount = defaultdict(int),defaultdict(int)
# nonPurchase,purchase=defaultdict(list),defaultdict(list)
# item_categories=defaultdict()
# user_set,item_set=set(),set()
# totalPurchases = 0

# for l in readGz("train.json.gz"):
#   user,business = l['reviewerID'],l['itemID']
#   item_categories[business]=set(l['categories'])
#   user_set.add(user)
#   item_set.add(business)
#   purchase[user].append(business)
#   businessCount[business] += 1
#   userCount[user]+=1
#   totalPurchases += 1

# # non-purchased hash
# valid_if_purchase=0
# while valid_if_purchase<100000:
#   random_user=user_set.pop()
#   print(random_user)
#   user_set.add(random_user)
#   random_item=item_set.pop()
#   item_set.add(random_item)
#   if random_item not in purchase[random_user]:
#     nonPurchase[random_user].append(random_item)
#     valid_if_purchase+=1

# repeat_purchase=defaultdict()
# for user in user_set:
#   temp=set()
#   for item in purchase[user]:
#     for category in item_categories[item]:
#       if category in temp:
#         repeat_purchase[user]=True
#       temp.add(category)
#   if user not in repeat_purchase.keys():
#     repeat_purchase[user]=False

# mostPopular = [(businessCount[x], x) for x in businessCount]
# mostPopular.sort()
# mostPopular.reverse()

# return1 = set()
# count = 0
# for ic, i in mostPopular:
#   count += ic
#   return1.add(i)
#   if count > totalPurchases/2: break

# mostRich = [(userCount[x], x) for x in userCount]
# mostRich.sort()
# mostRich.reverse()
# return2 = set()
# count = 0
# for ic, i in mostRich:
#   count += ic
#   return2.add(i)
#   if count > totalPurchases/2: break

# if_purchase=0
# for key in nonPurchase.keys():
#   for item in nonPurchase[key]:
#     if item in return1 and key in return2:
#       if_purchase+=1
# print(if_purchase)
# print(float(if_purchase/100000))

# predictions = open("predictions_Purchase.txt", 'w')
# for l in open("pairs_Purchase.txt"):
#   if l.startswith("reviewerID"):
#     #header
#     predictions.write(l)
#     continue
#   u,i = l.strip().split('-')
#   if i in return1:
#     predictions.write(u + '-' + i + ",1\n")
#   else:
#     predictions.write(u + '-' + i + ",0\n")

# predictions.close()