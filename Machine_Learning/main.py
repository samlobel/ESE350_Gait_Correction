import serialRecord
import MLLibrary
from collections import Counter


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

  while True:
    rawFileName = rawFileBaseName + '_' + str(i)
    serialRecord.recordLive(serdevString, rawFileName, 30)
    featureFileName = featureFileBaseName + '_' + str(i)
    MLLibrary.rawDataFileToFeatureFile(rawFileName, featureFileName, False)
    classes = classifier.classifyFeatureFile(featureFileName)
    classesCounted = Counter(classes)
    print classesCounted
    print "Most common: " + str(classesCounted.most_common(1)[0])
    i += 1



# Just so we know,

# Normal is 2
# Pronate is 0
# Supinate is 1
main()







# train(0, 'data/training/pronatingtrain_1.txt', 60)

# train(1, 'data/training/supinatingtrain_1.txt', 30)
# MLLibrary.rawDataFileToFeatureFile('./data/training/supinatingtrain_1.txt', './data/training/supinateFeature_1.txt', True)


# train(2, './data/training/normaltrain_1.txt', 30)
# MLLibrary.rawDataFileToFeatureFile('./data/training/normaltrain_1.txt', './data/training/normalFeature_1.txt', True)
  







