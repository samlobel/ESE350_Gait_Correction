import serial
from time import time


def train(trainingLabel, serdevString, whereToSave, listenTime):
  ser = serial.Serial(serdevString)
  ser.flushOutput()
  f = open(whereToSave, 'w')
  f.write(str(trainingLabel) + '\n')
  print "starting read"
  start = time()
  
  for k in range(200):
    a = ser.readline()
    # print a
    # really just a hack, because there's some sort of lag between the last run
    # and this one, every time.
  
  i = 0


  while time() - start < listenTime:
    i += 1
    if i % 500 == 0:
      print str(i) + " lines written"
    a = ser.readline()
    # print a
    array = [l for l in a]
    vals = array[0:5]
    intArray = [ord(l) - 1 for l in vals]
    if len(intArray) != 5:
      # print "funky data: " + str(intArray)
      continue

    strArray = [str(l) for l in intArray]
    csv_line = ', '.join(strArray) + '\n'
    f.write(csv_line)
  f.close()
  ser.close()
  print "comlpeted"


def recordLive(ser, whereToSave, listenTime):
  # only difference is really if it writes a number to the top.
  ser.flushOutput()
  f = open(whereToSave, 'w')
  print "starting read"
  start = time()
  
  for k in range(200):
    a = ser.readline()
    # print a
    # really just a hack, because there's some sort of lag between the last run
    # and this one, every time.
  
  i = 0


  while time() - start < listenTime:
    i += 1
    if i % 500 == 0:
      print str(i) + " lines written"
    a = ser.readline()
    # print a
    # print a
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
  # ser.close()
  print "comlpeted"


def writeState(ser, state):
  ser.write(str(state))
  # ser.close()


def writeStupid(serdevString):
  # ser = serial.Serial(serdevString)
  ser.write('0')
  # ser.close();







