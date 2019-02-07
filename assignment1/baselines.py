import gzip
from collections import defaultdict
import random


def readGz(f):
  for l in gzip.open(f):
    yield eval(l)

### Would-purchase baseline: just rank which businesses are popular and which are not, and return '1' if a business is among the top-ranked
def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return len(s1.intersection(s2)) / len(s1.union(s2))

user_catagory = defaultdict(list)
item_catagory = defaultdict(list)
business=defaultdict(list)

for l in readGz("train.json.gz"):
    user, item, catagories = l['reviewerID'], l['itemID'], l['categories']
    business[user].append(item)
    for category in catagories:
      for label in category:
        if label not in user_catagory[user]:
          user_catagory[user].append(label)
        if label not in item_catagory[item]:
          item_catagory[item].append(label)
    

predictions = open("predictions_Purchase.txt", 'w')
accur=0
for l in open("pairs_Purchase.txt"):
  if l.startswith("reviewerID"):
    #header
    predictions.write(l)
    continue
  u,i = l.strip().split('-')
  dis=jaccard_similarity(user_catagory[u],item_catagory[i])
  # if count_pos>=count_neg:
  predictions.write(u + '-' + i + ","+ str(1 if dis>0.183 else 0) +"\n")

predictions.close()