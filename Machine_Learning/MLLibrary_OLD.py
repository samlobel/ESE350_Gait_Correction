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



INSTEAD, I think it may make more sense to: 
-Break data into steps:
-extract some set of numbers from each of the steps (like averages for each softpot: 
-use an SVM to compare against it.

"""


import serial
from sklearn import svm

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

  # the data is an array of arrays, the inner of which are just data points.
  # we want an array of steps, each step being an array of timeStamps, each
  # timeStamp being an array of datapoints. So it turns a 2d array into a 3d array.

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


# def compareTwoTimeStamps(ts1, ts2):

#   cost = 0
#   for i in range(ts1,ts2):
#     if ts1[i] < 0 and ts2[i] < 0:
#       continue
#     elif ts1[i] < 0 or ts2[i] < 0:
#       cost += 1
#       # That's a debatable design decision
#       continue
#     else:
#       difference = (ts1[i] - ts2[i])**2;
#       cost += difference
#   return cost



# def makeCostMatrix(arr1, arr2, costFunction):
#   matrix = [[costFunction(val1,val2) for val1 in arr1] for val2 in arr2]
#   return matrix


# def DTWCostWithCostFunction(arr1, arr2, costFunction):
#   # costMatrix = makeCostMatrix(arr1,arr2,costFunction)
#   dtwMatrix = [[100000000 for i in range(len(arr1))] for j in range(len(arr2))]
#   dtwMatrix[0][0] = 0

#   for i in range(len(arr1)):
#     for j in range(len(arr2)):
#       cost = costFunction(arr1[i],arr2[j])
#       dtwMatrix[i][j] = cost + min([dtwMatrix[i-1][j],dtwMatrix[i][j-1],dtwMatrix[i-1][j-1]])

#   return dtwMatrix[len(arr1)-1][len(arr2)-1]



# class kNNObject:

#   namingDict = {0 : 'normal', 1:'pronated', 2:'supinated'}

#   def __init__(self):
#     self.trainingData = []

#   def train(self, data):
#     self.trainingData.extend(data)
#     # training data will be a list of tuples of class versus step array (category, stepArray)

#   def trainFromFile(self, fileName):
#     # file data: how about the first line is the type. And the rest is just csv for timestamps
#     # (not yet converted to steps)
#     f = open(fileName, 'r')
#     stepType = int(f.readLine().rstrip())
#     # dataArray = []
#     # for line in f:
#     #   toAppend = (stepType, [float(val) for val in line.rstrip().split(',')])
#     #   dataArray.append(toAppend)

#     rawArray = [[float(val) for val in line.rstrip().split(',')] for line in f]
#     arrayOfSteps = breakContinuousDataIntoSteps(rawArray)
#     stepsWithCategories = [(stepType, step) for step in arrayOfSteps]
#     self.trainingData.extend(stepsWithCategories)
#     f.close()




#   def findSimilarityBreakdown(self, step, k):
#     ourData = [(DTWCostWithCostFunction(step, datapoint[1], compareTwoTimeStamps), datapoint[0])
#         for datapoint in self.trainingData]
#     sortedData = sorted(ourData)
#     # (comparisonCost, category)

#     trackingDict = {}
#     trackingDict[0] = 0;
#     trackingDict[1] = 0;
#     trackingDict[2] = 0;
    
#     for i in range(k):
#       if trackingDict[sortedData[i][1]] == 0:
#         trackingDict[sortedData[i][1]] += 1 
#       else:
#         trackingDict[sortedData[i][1]] += 1.0 / trackingDict[sortedData[i][0]]

#     breakdown = [(trackingDict[i], i) for i in range(3)]
#     return breakdown

#   def categorize(self, step, k):
#     breakdown = self.findSimilarityBreakdown(step, k)
#     maxType = max(breakdown)
#     return kNNObject.namingDict[maxType[1]]

#   def categorizeSteps(self, steps, k):
#     nameToStepCount = {'normal' : 0, 'pronated' : 0, 'supinated' : 0}
#     for step in steps:
#       maxType = self.categorize(step, k)
#       nameToStepCount[maxType] += 1
#     return nameToStepCount

#   def categorizeFileOfSteps(self, fileName, k):
#     f = open(fileName, 'r')
#     # file is already steps. 
#     arrayOfSteps = [[float(val) for val in line.rstrip().split(',')] for line in f]
#     nameToStepCount = self.categorizeSteps(arrayOfSteps)
#     f.close()
#     return nameToStepCount

#   def categorizeRawFile(self, fileName, k):
#     f = open(fileName, 'r')
#     rawArray = [[float(val) for val in line.rstrip().split(',')] for line in f]
#     arrayOfSteps = breakContinuousDataIntoSteps(rawArray)
#     return self.categorizeSteps(arrayOfSteps, k)


#   def prettySimilarityString(self, step, k):
#     breakdown = self.findSimilarityBreakdown(step, k)
#     return "Supination:   " + str(breakdown[2][1]) + "Normal:   " + str(breakdown[0][1]) +\
#         "Pronation:   " + str(breakdown[0][1])






def trainFromSerial(samples, fileName, category):
  print "opening serial"
  serdev = '/dev/cu.usbmodem1412'
  ser = serial.Serial(serdev)
  i = 0
  dataFile = open(fileName, 'w')
  dataFile.write(str(category))
  print "listening"
  while i < samples:
    a = ser.readline()
    print "read " + str(a)
    dataFile.write(a)
    i += 1

  dataFile.close()
  print "completed"


# trainFromSerial(20, 'testFile.txt', 1)



def readRealInfoFromSerial(samples, filName, category):
  print "opening serial"
  serdev = '/dev/cu.usbmodem1412'
  ser = serial.Serial(serdev)






# def waitForHandshake():
#   serdev = '/dev/cu.usbmodem1412'
#   ser = serial.Serial(serdev)
#   while True:
#     a = ser.readline()
#     print "hand-shaker read " + str(a)
#     if a == "handshake":
#       print "Handshook!"
#       break

"""
This is pretty complicated, so we need to plan it out for a bit.

We first need to handshake. Then, we 
No that's stupid

The one transmitting data transmits for 9.5 seconds straight, and then
listens for 0.5 seconds. The other guy listens for 99 percent of his life,
but when he transmits, he does it for 10 seconds. 

The one difficult thing is that we really should continuing to read the data
from the ADC if we want to analy


"""


def rawFileToArrayOfArrays(fileName, isTraining):
  walkingType = None
  f = open(fileName, 'r')
  
  if isTraining:
    walkingType = f.readline()
  
  dataArray = []
  for line in f:
    sampleArray = line.rsplit(', ')
    if len(sampleArray) != 5:
      print "funky data: " + str(sampleArray)
      continue
    dataArray.append(sampleArray)
  f.close()
  return (walkingType, dataArray)


def extractFeaturesFromStep(step):
  # Assumes that all of the arrays here are of length 5
  # for now, the only feature is an average... but we could do more
  """
  LIST OF FEATURES
  -average for each potentiometer
  -percentage of time it's off
  --something like splitting the sample into first-half, last-half
  """
  stepLength  = len(step)
  sumArray = [0 for i in range(5)]
  for sample in step:
    for j in range(5):
      sumArray[j] += sample[j]
  averageArray = [total / stepLength for total in sumArray]
  return averageArray

def stringFromFeature(feature):
  featureString = ', '.join(feature)
  return featureString

def featuresArrayFromStepArray(stepArray):
  featureArray = []
  for step in stepArray:
    feature = extractFeaturesFromStep(step)
    featureArray.push(feature)
  return featureArray


def rawDataFileToFeatureFile(trainingFile, featureFile, isTraining):
  walkingType, dataArray = trainingFileToArrayOfArrays(trainingFile, isTraining)
  arrayOfSteps = breakContinuousDataIntoSteps(dataArray)
  
  ff = open(featureFile, 'w')
  if isTraining:
    ff.write(str(walkingType) + '\n')

  for step in arrayOfSteps:
    feature = extractFeaturesFromStep(step)
    ff.write(', '.join(feature) + '\n')

  ff.close()







def train(trainingLabel, serdevString, whereToSave, listenTime):
  f = open(whereToSave, 'w')
  f.write(str(trainingLabel) + '\n')
  print "starting read"
  start = time()
  i = 0
  while time() - start < listenTime:
    i += 1
    if i % 100 == 0:
      print str(i) + " lines written"
    a = ser.readline()
    array = [l for l in a]
    vals = array[0:5]
    intArray = [ord(l) - 1 for l in vals]
    if len(intArray) != 5:
      print "funky data: " + str(intArray)
      continue

    strArray = [str(l) for l in intArray]
    csv_line = ', '.join(strArray) + '\n'
    f.write(csv_line)
  f.close()
  print "completed"


def fromListenToFeatureFile(trainingLabel, serdevString, featureFileName, listenTime):
  raw_dir = "raw_" + featureFileName
  train(trainingLabel, serdevString, raw_dir, listenTime)
  rawDataTrainingFileToFeatureFile(raw_dir, featureFileName)
  return featureFileName






def createTrainingSetFromFeatureFiles(arrayOfTrainingFiles):
  categoryArray = []
  featuresArray = []
  for names in arrayOfTrainingFiles:
    f = open(arrayOfTrainingFiles, 'r')
    category = int(f.readline())
    for line in f:
      features = line.rsplit(', ')
      featuresArray.append(features)
      categoryArray.append(category)
    f.close()
  return categoryArray, featuresArray




class svmObject:
  def __init__(self):
    self.svm = svm.SVC()
    self.results = []

  def trainFromFeatureFiles(self, arrayOfFeatureFiles):
    categoryArray, featuresArray = createTrainingSetFromFeatureFiles(arrayOfFeatureFiles)
    self.svm.fit(featuresArray, categoryArray)

  def classifyFeature(self, feature):
    return self.svm.predict(feature)

  def classifyFeatureFile(self, featureFile):
    f = open(featureFile, 'r')
    classList = []
    for line in f:
      feature = line.strip().rsplit(', ')
      if len(feature) == 5:
        classification = self.classifyFeature(feature)
        classList.append(classification)
    f.close()
    return classList










"""
Our data assumptions: 
val 1:
val 2:
val 3:
val 4:
val 5:

"""

"""
Now, try and do some SVM stuff I guess.
"""















