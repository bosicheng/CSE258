import os

f=open('res.txt','r')
dict={}
arr=[]
for line in f.readlines():
    name=line.strip().split(": ")[0]
    rating=float(line.strip().split(": ")[-1][:-1])
    dict[rating]=name
    arr.append(rating)
arr.sort(reverse=True)
for i in range(0,10):
    print(dict[arr[i]]+":"+str(arr[i]))
