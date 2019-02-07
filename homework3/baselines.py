import gzip
from collections import defaultdict


def readGz(f):
  for l in gzip.open(f):
    yield eval(l)

### Rating baseline: compute averages for each user, or return the global average if we've never seen the user before

allRatings = []
data=[]
userRatings = defaultdict(list)
totalPurchase=0
sum_mse=0
for l in readGz("train.json.gz"):
  user,business = l['reviewerID'],l['itemID']
  allRatings.append(l['rating'])
  userRatings[user].append(l['rating'])
  data.append(l)

tData=data[:100000]
vData=data[100000:]
lamda=1


#   else:
#     if totalPurchase==100000:
#       globalAverage = sum(allRatings_train) / len(allRatings_train)
#     sum_mse+=abs(l['rating']-globalAverage)*abs(l['rating']-globalAverage)
#     totalPurchase+=1

# globalAverage = sum(allRatings_train) / len(allRatings_train)
# userAverage = {}
# for u in userRatings:
#   userAverage[u] = sum(userRatings[u]) / len(userRatings[u])

# print(globalAverage)
# print(sum_mse/100000)
# predictions = open("predictions_Rating.txt", 'w')
# for l in open("pairs_Rating.txt"):
#   if l.startswith("reviewerID"):
#     #header
#     predictions.write(l)
#     continue
#   u,i = l.strip().split('-')
#   if u in userAverage:
#     predictions.write(u + '-' + i + ',' + str(userAverage[u]) + '\n')
#   else:

#     predictions.write(u + '-' + i + ',' + str(globalAverage) + '\n')

# predictions.close()

### Would-purchase baseline: just rank which businesses are popular and which are not, and return '1' if a business is among the top-ranked

# businessCount_train,businessCount_valid = defaultdict(int),defaultdict(int)
# negative_valid=defaultdict(list)
# train,positive_valid=defaultdict(list),defaultdict(list)
# user_set,item_set=set(),set()
# train_user_set=set()
# totalPurchases = 0
# valid_user_set,valid_item_set=set(),set()

# for l in readGz("train.json.gz"):
#   if totalPurchases<100000:
#     user,business = l['reviewerID'],l['itemID']
#     if user not in user_set:
#       user_set.add(user)
#     if business not in item_set:
#       item_set.add(business)
#     train[user].append(business)
#     businessCount_train[business] += 1
#     totalPurchases += 1
#   else:
#     user,business = l['reviewerID'],l['itemID']
#     if user not in valid_user_set:
#       valid_user_set.add(user)
#     if business not in valid_item_set:
#       valid_item_set.add(business)
#     positive_valid[user].append(business)
#     businessCount_valid[business] += 1
#     totalPurchases += 1

# mostPopular = [(businessCount_train[x], x) for x in businessCount_train]
# mostPopular.sort()
# mostPopular.reverse()

# return1 = set()
# count = 0
# for ic, i in mostPopular:
#   count += ic
#   return1.add(i)
#   if count > totalPurchases/2: break

# valid_if_purchase=0
# while valid_if_purchase<100000:
#   random_user=valid_user_set.pop()
#   valid_user_set.add(random_user)
#   random_item=valid_item_set.pop()
#   valid_item_set.add(random_item)
#   if random_item not in train[random_user] :
#     if random_item not in negative_valid[random_user]:
#       negative_valid[random_user].append(random_item)
#       valid_if_purchase+=1



# correction=0
# for user in positive_valid.keys():
#   for item in positive_valid[user]:
#     if item in return1:
#       correction+=1
# print(correction)


# for user in negative_valid.keys():
#   for item in negative_valid[user]:
#     if item not in return1:
#       correction+=1

# print(len(positive_valid))
# print(len(negative_valid))
# print(correction)
# print(float(correction/200000))
# predictions = open("predictions_Purchase.txt", 'w')
# will_buy,total=0,0
# for l in open("pairs_Purchase.txt"):
#   if l.startswith("reviewerID"):
#     #header
#     predictions.write(l)
#     continue
#   u,i = l.strip().split('-')
#   if i in return1:
#     predictions.write(u + '-' + i + ",1\n")
#     will_buy+=1
#     total+=1
#   else:
#     predictions.write(u + '-' + i + ",0\n")
#     total+=1
# print(will_buy)
# print(total)
# print(will_buy/total)

# predictions.close()

### Category prediction baseline: Just consider some of the most common words from each category

# catDict = {
#   "Women": 0,
#   "Men": 1,
#   "Girls": 2,
#   "Boys": 3,
#   "Baby": 4
# }

# predictions = open("predictions_Category.txt", 'w')
# predictions.write("reviewerID-reviewHash,category\n")
# for l in readGz("test_Category.json.gz"):
#   cat = catDict['Women'] # If there's no evidence, just choose the most common category in the dataset
#   words = l['reviewText'].lower()
#   if 'wife' in words:
#     cat = catDict['Women']
#   if 'husband' in words:
#     cat = catDict['Men']
#   if 'daughter' in words:
#     cat = catDict['Girls']
#   if 'son' in words:
#     cat = catDict['Boys']
#   if 'baby' in words:
#     cat = catDict['Baby']
#   predictions.write(l['reviewerID'] + '-' + l['reviewHash'] + "," + str(cat) + "\n")

# predictions.close()
