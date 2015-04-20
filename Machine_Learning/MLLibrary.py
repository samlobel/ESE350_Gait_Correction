# import json



# sampleLength = 4500
# fsr = 1000
# winsize = 3
# windisp = 1.5

# numWins = 1 + (sampleLength/fsr - winsize) / windisp

# def numWindows(sl, fsr, ws, wd):
#   return (1 + (sl/fsr - ws) / wd)


# def numWinsFromDataList(data, fsr, ws, wd):
#   return numWindows(len(data), fsr, ws,wd)




# 








"""

I think that I'm going to need dynamic time warping to match up steps. 
It looks like it's going to be REALLY tough if I don't preprocess into one value.
Although, the least I can really do is preprocess into two values. 
Let's just say that we have one number, which is the average force position
of the feet. I need to use dynamic time warping to line it up, and then I get a
distance value

It's not actually that bad in multiple dimensions. We just need to write up a distance
formula that takes in all of the points. Then we use k-nearest neighbor clustering.

Tasks ahead 
-break data into steps
-write step-comparison metric
-make kNN object from training data
-write methods to compare test data to training data
-have ways to return sensible data

"""


# global numberContinuousToStart = 10
# global missesAllowedForStart = 1
# global numberContinuousToEnd = 10
# global missesContinousToEnd = 0

def footIsDown(oneTimeData):
  # As of now, I'll do it by saying that there are 2 or more sensors activated. 
  total = len(oneTimeData)
  activated = 0;
  for value in oneTimeData:
    if value > 0.1:
      activated += 1
  return activated >= 2





def makeWouldTurnOnOrOffArray(onOffArray, whichOne, numToLookAhead, missesAllowed):
  # THIS METHOD COULD BE A LOT MORE EFFICIENT. BUT I DON'T REALLY CARE RIGHT NOW.
  # Pass in onOffArray, then if you're looking for True or False, the numToLookAhead
  # and the missesAllowed. whichOne=True means you're looking for wouldTurnOn.

  # numToLookAhead = 10
  # missesAllowed = 2
  wouldTurnOnOrOffArray = [False for i in onOffArray]
  length = len(onOffArray)

  if missesAllowed >= numToLookAhead:
    raise Exception("missesAllowed >= numToLookAhead")
  if length <= numToLookAhead:
    raise Exception("length less than numToLookAhead")


  for i in range(0, length - numToLookAhead):
    total = onOffArray[i: i+10].count(whichOne)
    if total <= numToLookAhead - missesAllowed:
      wouldTurnOnArray[i] = True
  return wouldTurnOnArray



def filterTupleListForMinAndMaxLength(tupleList, minLen, maxLen):
  filteredList = []
  for tup in tupleList:
    if not (tup[1] - tup[0] < minLen or tup[1] - tup[0] > maxLen):
      filteredList.append(tup)

  return filteredList


def breakContinuousDataIntoSteps(data):
  # it's really a question of where to draw the dividing lines. We want to start
  # the process when they hit the back heel. And end the process when they pick up
  # off of the toe. Maybe we can say that we start when there are 9 out of ten
  # readings in a row that have been actual values for more than 3 sensors, and 
  # stop reading when there are nine out of ten readings that are nothing.

  # first, construct a parallel array that tells you if you're on or off.

  minTupleLength = 10
  maxTupleLength = 60
  numToLookAhead = 10
  missesAllowed = 2

  onOffArray = [footIsDown(singleData) for singleData in data]
  wouldTurnOnArray = makeWouldTurnOnOrOffArray(onOffArray, True, numToLookAhead, missesAllowed)
  wouldTurnOffArray = makeWouldTurnOnOrOffArray(onOffArray, False, numToLookAhead, missesAllowed)

  length = len(onOffArray)


  listOfStartStopTuples = []
  i = 0
  # should scan through and find start points, then scan through and find end points
  # and then make a list of those.
  while i < length - 1: 
    if wouldTurnOnArray[i]:
      j = i + 1
      while j < length:
        if wouldTurnOffArray[j]:
          listOfStartStopTuples.append((i,j))
          i = j + 1
          break

  tuplesFilteredBySequenceLength = filterTupleListForMinAndMaxLength(listOfStartStopTuples, minTupleLength, maxTupleLength)

  listOfSteps = [data[tup[0]: tup[1]]]

  return listOfSteps



  # At the end, throw out everything that's over some time and below some other time.



def compareTwoTimeStamps(ts1, ts2):

  cost = 0
  for i in range(ts1,ts2):
    if ts1[i] < 0 and ts2[i] < 0:
      continue
    elif ts1[i] < 0 or ts2[i] < 0:
      cost += 1
      # That's a debatable design decision
      continue
    else:
      difference = (ts1[i] - ts2[i])**2;
      cost += difference
  return cost



def makeCostMatrix(arr1, arr2, costFunction):
  matrix = [[costFunction(val1,val2) for val1 in arr1] for val2 in arr2]
  return matrix


def DTWCostWithCostFunction(arr1, arr2, costFunction):
  makeCostMatrix = makeCostMatrix(arr1,arr2,costFunction)
  dtwMatrix = [[100000000 for i in range(len(arr1))] for j in range(len(arr2))]
  dtwMatrix[0][0] = 0

  for i in range(len(arr1)):
    for j in range(len(arr2)):
      cost = costFunction(arr1[i],arr2[j])
      dtwMatrix[i][j] = cost + min([dtwMatrix[i-1][j],dtwMatrix[i][j-1],dtwMatrix[i-1][j-1]])

  return dtwMatrix[len(arr1)-1][len(arr2)-1]



class kNNObject:

  namingDict = {0 : 'normal', 1:'pronated', 2:'supinated'}

  def __init__(self):
    self.trainingData = []

  def train(self, data):
    self.trainingData.extend(data)
    # training data will be a list of tuples of class versus step array (category, stepArray)

  def trainFromFile(self, fileName):
    # file data: how about the first line is the type. And the rest is just csv for timestamps
    # (not yet converted to steps)
    f = open(fileName, 'r')
    stepType = int(f.readLine().rstrip())
    # dataArray = []
    # for line in f:
    #   toAppend = (stepType, [float(val) for val in line.rstrip().split(',')])
    #   dataArray.append(toAppend)

    rawArray = [[float(val) for val in line.rstrip().split(',')] for line in f]
    stepArray = breakContinuousDataIntoSteps(rawArray)
    categorizedSteps = [(stepType, step) for step in stepArray]
    self.trainingData.extend(categorizeSteps)
    f.close()




  def findSimilarityBreakdown(self, step, k):
    ourData = [(DTWCostWithCostFunction(step, datapoint[1], compareTwoTimeStamps), datapoint[0])
        for datapoint in self.trainingData]
    sortedData = sorted(ourData)
    # (comparisonCost, category)

    trackingDict = {}
    trackingDict[0] = 0;
    trackingDict[1] = 0;
    trackingDict[2] = 0;
    
    for i in range(k):
      if trackingDict[sortedData[i][1]] == 0:
        trackingDict[sortedData[i][1]] += 1 
      else:
        trackingDict[sortedData[i][1]] += 1.0 / trackingDict[sortedData[i][0]]

    breakdown = [(trackingDict[i], i) for i in range(3)]
    return breakdown

  def categorize(self, step, k):
    breakdown = self.findSimilarityBreakdown(step, k)
    maxType = max(breakdown)
    return kNNObject.namingDict[maxType[1]]

  def categorizeSteps(self, steps, k):
    nameToStepCount = {'normal' : 0, 'pronated' : 0, 'supinated' : 0}
    for step in steps:
      maxType = self.categorize(step, k)
      nameToStepCount[maxType] += 1
    return nameToStepCount

  def categorizeFileOfSteps(self, file, k):
    f = open(fileName, 'r')
    # stepType = int(f.readLine().rstrip())
    dataArray = [[float(val) for val in line.rstrip().split(',')] for line in f]
    # toAppend = []
    # for line in f:
    #   toAppend = 
    #   dataArray.append(toAppend)
    # self.trainingData.extend(dataArray)
    f.close()




  def prettySimilarityString(self, step, k):
    breakdown = self.findSimilarityBreakdown(step, k)
    return "Supination:   " + str(breakdown[2][1]) + "Normal:   " + str(breakdown[0][1]) +
        "Pronation:   " + str(breakdown[0][1])




















# NEXT UP, IMPLEMENT K-NEAREST-NEIGHBORS ALGORITHM.


