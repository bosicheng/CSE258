import numpy

x=numpy.array([[1,1],[2,2],[3,3],[4,4],[5,5]])
y=numpy.array([3,5,7,9,11])

z=numpy.linalg.lstsq(x,y)
print z
