import time
from pprint import pprint

def makeBig2dArray():
  x = [[i*i for i in range(1000)] for j in range(1000)]

start = time.clock()
makeBig2dArray()
print time.clock() - start


def readFile():
  f = open('longFile.txt', 'r')
  i = 0
  for line in f:
    # print line
    i += 1



start = time.clock()
readFile()
print time.clock() - start

