from sklearn import svm
from pprint import pprint
from math import sin, cos, pi


def footIsDown(oneTimeData):
  # As of now, I'll do it by saying that there are 2 or more sensors activated. 
  total = len(oneTimeData)
  activated = 0;
  # print oneTimeData
  for value in oneTimeData:
    if value > 25:
      activated += 1
  # print activated >= 2
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
    # print total
    if total >= numToLookAhead - missesAllowed:
      wouldTurnOnOrOffArray[i] = True
  # pprint(wouldTurnOnOrOffArray)
  return wouldTurnOnOrOffArray


def filterTupleListForMinAndMaxLength(tupleList, minLen, maxLen):
  filteredList = []
  for tup in tupleList:
    # print tup[1] - tup[0]
    if not (tup[1] - tup[0] < minLen or tup[1] - tup[0] > maxLen):
      filteredList.append(tup)

  return filteredList




def rawFileToArrayOfArrays(fileName, isTraining):
  walkingType = None
  f = open(fileName, 'r')
  
  if isTraining:
    walkingType = int(f.readline())
  
  dataArray = []
  for line in f:
    strArray = line.strip().rsplit(', ')
    sampleArray = [int(string) for string in strArray]
    if len(sampleArray) != 5:
      print "funky data: " + str(sampleArray)
      continue
    dataArray.append(sampleArray)
  f.close()
  return (walkingType, dataArray)



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

  minTupleLength = 30
  maxTupleLength = 300
  numToLookAhead = 10
  missesAllowed = 2

  onOffArray = [footIsDown(singleData) for singleData in data]
  wouldTurnOnArray = makeWouldTurnOnOrOffArray(onOffArray, True, numToLookAhead, missesAllowed)
  wouldTurnOffArray = makeWouldTurnOnOrOffArray(onOffArray, False, numToLookAhead, missesAllowed)

  length = len(onOffArray)
  print "length = " + str(length)


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
          # print str(i) + ", " + str(j)
          i = j
          break
        j += 1
    i += 1
  print "Out of deadly breakContinuousDataIntoSteps loop"


  tuplesFilteredBySequenceLength = filterTupleListForMinAndMaxLength(listOfStartStopTuples, minTupleLength, maxTupleLength)
  # pprint(tuplesFilteredBySequenceLength)
  listOfSteps = [data[tup[0]: tup[1]] for tup in tuplesFilteredBySequenceLength]

  print "List of steps is of length: " + str(len(listOfSteps))

  return listOfSteps







def extractFeaturesFromStep(step):
  # Assumes that all of the arrays here are of length 5
  # for now, the only feature is an average... but we could do more
  """
  LIST OF FEATURES
  -average for each potentiometer
  -percentage of time it's off
  --something like splitting the sample into first-half, last-half


  --Yixing's great idea: split it into only transitions
  """


  def split(num):
    if num > 66:
      return 1
    else:
      return 0


  binaryArrayWithBadRow = [[split(num) for num in timeStamp] for timeStamp in step]
  binaryArray = [[array[0]] + [array[2]] + [array[3]] + [array[4]] for array in binaryArrayWithBadRow]
  # pprint(binaryArray)

  def compare(arr1, arr2):
    for i in range(len(arr1)):
      if arr1[i] != arr2[i]:
        return False
    return True

  compressedBinaryArray = []
  mostRecent = binaryArray[0]
  compressedBinaryArray.append(mostRecent)
  for array in binaryArray[1:]:
    if not compare(mostRecent, array):
      mostRecent = array
      compressedBinaryArray.append(mostRecent)

  # pprint(compressedBinaryArray)

  tally = [0 for i in range(16)]

  for array in compressedBinaryArray:
    index = sum([2**i * array[i] for i in range(len(array))])
    tally[index] += 1

  # pprint(tally)

  return tally













  # stepLength  = len(step)
  # sumArray = [0 for i in range(5)]
  # for sample in step:
  #   for j in range(5):
  #     sumArray[j] += sample[j]
  # averageArray = [total / stepLength for total in sumArray]
  # cosineSumArray = [0.0 for i in range(5)]
  # for i in range(stepLength):
  #   for j in range(5):
  #     cosineSumArray[j] += step[i][j] * cos((2*pi * i) / stepLength)
  # cosineArray = [int(total / stepLength) for total in cosineSumArray]
  # sineSumArray = [0.0 for i in range(5)]
  # for i in range(stepLength):
  #   for j in range(5):
  #     sineSumArray[j] += step[i][j] * sin((2*pi * i) / stepLength)
  # sineArray = [int(total / stepLength) for total in sineSumArray]



  # featureArray = []
  # featureArray.extend(averageArray)
  # featureArray.extend(cosineArray)
  # featureArray.extend(sineArray)
  # return featureArray


  # return averageArray



def featuresArrayFromStepArray(stepArray):
  featureArray = []
  for step in stepArray:
    feature = extractFeaturesFromStep(step)
    featureArray.append(feature)
  return featureArray


def rawDataFileToFeatureFile(trainingFile, featureFile, isTraining):
  walkingType, dataArray = rawFileToArrayOfArrays(trainingFile, isTraining)
  arrayOfSteps = breakContinuousDataIntoSteps(dataArray)
  
  # print "\n\n\n\n\ndataArray\n\n\n\n\n"
  # pprint(dataArray)
  # print "\n\n\n\n\narrayOfSteps\n\n\n\n\n"
  # pprint(arrayOfSteps)
  ff = open(featureFile, 'w')
  if isTraining:
    ff.write(str(walkingType) + '\n')

  for step in arrayOfSteps:
    feature = extractFeaturesFromStep(step)
    strFeature = [str(feat) for feat in feature]
    ff.write(', '.join(strFeature) + '\n')

  ff.close()


def featureFileToFeaturesArray(featureFile, isTraining):
  walkingType = None
  ff = open(featureFile, 'r')
  if isTraining:
    walkingType = int(ff.readline())
  featureArray = []
  for line in ff:
    str_feature = line.strip().rsplit(', ')
    feature = [int(num) for num in str_feature]
    featureArray.append(feature)
  ff.close()
  return walkingType, featureArray


def createTrainingSetFromFeatureFiles(arrayOfFeatureFiles):
  categoryArray = []
  featuresArray = []
  for featureFile in arrayOfFeatureFiles:
    ff = open(featureFile)
    walkingType, featureArray = featureFileToFeaturesArray(featureFile, True)
    walkingArray = [walkingType for i in featureArray]
    categoryArray.extend(walkingArray)
    featuresArray.extend(featureArray)
    ff.close()
  return featuresArray, categoryArray





class svmObject:
  def __init__(self):
    self.svm = svm.SVC()
    self.results = []
    self.trained = False

  def trainFromFeatureFiles(self, arrayOfFeatureFiles):
    featuresArray, categoryArray = createTrainingSetFromFeatureFiles(arrayOfFeatureFiles)
    self.svm.fit(featuresArray, categoryArray)
    self.trained = True

  def classifyFeature(self, feature):
    return self.svm.predict(feature)

  def classifyFeatureFile(self, featureFile):
    if not self.trained:
      raise Exception("Can't classify without training!")
    classList = []
    f = open(featureFile, 'r')
    for line in f:
      feature = line.strip().rsplit(', ')
      # if len(feature) != 15:
      #   print "feature length not five: " + str(feature)
      #   continue
      category = self.classifyFeature(feature)
      classList.extend(category)
      self.results.extend(category)
    # NOT DONE
    f.close()
    return classList




























