import gzip
import numpy as np

from collections import defaultdict

#get the data
def readGz(f):
  for l in gzip.open(f):
    yield eval(l)

allRatings = []
data=[]
userRatings = defaultdict(list)
for l in readGz("train.json.gz"):
  user,business = l['reviewerID'],l['itemID']
  allRatings.append(l['rating'])
  userRatings[user].append(l['rating'])
  data.append(l)


#shuffle the data
np.random.shuffle(data)


def getPrediction2(alpha,uB,iB,i,j,y_u,y_i,uMap,iMap):
    rating = alpha  + (uB[i] if i in uB else 0)  + (iB[j] if j in iB else 0)
    if i in uMap and j in iMap:
        rating +=np.inner(y_u[uMap[i]],y_i[iMap[j]]) 
    return rating   

#Method to Train The Latent Factor Model. This method doesn't use any Machine Learning library.
def trainLFModel(lam,tData,vData,trials):
    uTrainDict = defaultdict(lambda: defaultdict(int))
    iTrainDict = defaultdict(lambda: defaultdict(int))
    uValidDict = defaultdict(lambda: defaultdict(int))
    # iValidDict = defaultdict(lambda: defaultdict(int))
    uB = defaultdict(float)
    iB = defaultdict(float)
    uMap = defaultdict(int)
    uCount=0
    iMap = defaultdict(int)
    iCount=0
    for i in tData:
        user, item, rating = i['reviewerID'], i['itemID'], i['rating']
        uTrainDict[user][item] = rating
        iTrainDict[item][user] = rating
        if user not in uMap:
            uMap[user]=uCount
            uCount+=1
        if item not in iMap:
            iMap[item]=iCount
            iCount+=1
    for i in vData:
        user, item, rating = i['reviewerID'], i['itemID'], i['rating']
        uValidDict[user][item] = rating
    
    y_u=np.random.normal(scale=1,size=(len(uTrainDict),1))
    y_i=np.random.normal(scale=1,size=(len(iTrainDict),1))


    alpha = 0
    totalTrials=trials
    for _ in range(totalTrials):
        alpha=0
        for i in uTrainDict:
            for j in uTrainDict[i]:
                alpha += uTrainDict[i][j] - uB[i] -iB[j] - np.inner(y_u[uMap[i]],y_i[iMap[j]])
        alpha /= len(tData)
        print(alpha)
        for i in uTrainDict:
            uB[i] = 0
            for j in uTrainDict[i]:
                uB[i] += uTrainDict[i][j]  - alpha - iB[j] - np.inner(y_u[uMap[i]],y_i[iMap[j]])
            uB[i] /= (lam + len(uTrainDict[i])) 
        for j in iTrainDict:
            iB[j] = 0
            for i in iTrainDict[j]:
                iB[j] += iTrainDict[j][i]  -alpha - uB[i] - np.inner(y_u[uMap[i]],y_i[iMap[j]])
            iB[j] /= (lam + len(iTrainDict[j]))
    
        for i in uTrainDict:
            for lf in range(1):
                y_u[uMap[i]][lf] = 0
                for j in uTrainDict[i]:
                    y_u[uMap[i]][lf] += y_i[iMap[j]][lf]*(uTrainDict[i][j]  - alpha - iB[j]  +y_i[iMap[j]][lf]*y_i[iMap[j]][lf]-np.inner(y_u[uMap[i]],y_i[iMap[j]]) )
                    y_u[uMap[i]][lf]  /= (lam + y_i[iMap[j]][lf]*y_i[iMap[j]][lf])
        for j in iTrainDict:
            for lf in range(1):
                y_i[iMap[j]][lf] = 0
                for i in iTrainDict[j]:
                    y_i[iMap[j]][lf] += y_u[uMap[i]][lf]*(uTrainDict[i][j]  - alpha - uB[i] - np.inner(y_u[uMap[i]],y_i[iMap[j]]) +y_u[uMap[i]][lf]*y_u[uMap[i]][lf] )
                    y_i[iMap[j]][lf] /= (lam + y_u[uMap[i]][lf]*y_u[uMap[i]][lf])
    vMSE = 0
    for i in uValidDict:
        for j in uValidDict[i]:
#             vMSE += ((alpha  + (uB[i] if i in uB else 0)  + (iB[j] if j in iB else 0) - uValidDict[i][j]) **2)
            vMSE += ((getPrediction2(alpha,uB,iB,i,j,y_u,y_i,uMap,iMap) - uValidDict[i][j]) **2)
    vMSE /= len(vData)
    print (vMSE)
    return vMSE,alpha,uB,iB,uMap,iMap
print("done")


tData=data[:100000]
vData=data[100000:]
lamdas=[1,2,3,5]
trials=[2]
for i in lamdas:
    tempvMSE=1
    for t in trials:
        tempvMSE,alpha,uB,iB,uMap,iMap=trainLFModel(i,tData,vData,t)
        print ("MSE:"+str(tempvMSE))
        
           
        

