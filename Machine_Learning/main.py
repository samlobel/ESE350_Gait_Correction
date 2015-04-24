import serialRecord
import MLLibrary
from collections import Counter
import time
import serial


# when we run this, we're assuming that we've gotten all the training data already.



"""
Do I have a way to:

- load training data?
- read in walking data to a file?
- turn it into a features-file
- classify individual step-features
- classify a file of features 
- compile that data over time.

"""



def train(trainingLabel, whereToSave, listenTime):
  serdevString = '/dev/cu.usbmodem1412'
  serialRecord.train(trainingLabel, serdevString, whereToSave, listenTime)








def main():
  trainingSets = ['./data/training/normalFeature_1.txt', './data/training/supinateFeature_1.txt','./data/training/pronateFeature_1.txt']
  serdevString = '/dev/cu.usbmodem1412'
  rawFileBaseName = 'data/real/raw'
  featureFileBaseName = 'data/real/feature'


  i = 0

  classifier = MLLibrary.svmObject()
  classifier.trainFromFeatureFiles(trainingSets)
  ser = serial.Serial(serdevString)

  while True:
    rawFileName = rawFileBaseName + '_' + str(i)
    serialRecord.recordLive(ser, rawFileName, 30)
    featureFileName = featureFileBaseName + '_' + str(i)
    MLLibrary.rawDataFileToFeatureFile(rawFileName, featureFileName, False)
    classes = classifier.classifyFeatureFile(featureFileName)
    classesCounted = Counter(classes)
    print classesCounted
    mostCommon = classesCounted.most_common(1)[0]
    print "Most common: " + str(mostCommon)
    serialRecord.writeState(ser, mostCommon)
    # I don't really know how to test if this got through.
    i += 1



# Just so we know,

# Normal is 2
# Pronate is 0
# Supinate is 1


# [a,b,c,d,e] : 
# e is the one that runs down the middle. Starts low at back.
# a is back right to mid left. Starts high at back.
# c is back left to middle right. Starts high at back.
# b is mid left to front right. Starts high at back.
# d is mid left to front right. Starts low at back.


main()


# ser = serial.Serial('/dev/cu.usbmodem1412')
# while True:
#   # serialRecord.writeStupid('/dev/cu.usbmodem1412')
#   while not ser.writable():
#     pass
#   print ser.write('50')

#   time.sleep(0.1)








# # train(0, 'data/training/pronatingtrain_1.txt', 60)
# MLLibrary.rawDataFileToFeatureFile('data/training/pronatingtrain_1.txt', './data/training/pronateFeature_1.txt', True)
# print "pronate trained"

# # train(1, 'data/training/supinatingtrain_1.txt', 60)
# MLLibrary.rawDataFileToFeatureFile('./data/training/supinatingtrain_1.txt', './data/training/supinateFeature_1.txt', True)
# print "supinate trained"

# # train(2, './data/training/normaltrain_1.txt', 60)
# MLLibrary.rawDataFileToFeatureFile('./data/training/normaltrain_1.txt', './data/training/normalFeature_1.txt', True)
# print "normal trained"







