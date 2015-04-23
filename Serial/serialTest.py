import serial
from time import time

serdev = '/dev/cu.usbmodem1412'
ser = serial.Serial(serdev)
# print "writing next"

# ser.write("Hi Sam\n")
# print "written"


# inputLength = 5
# maxTime = 30



# f = open('dataTest', 'w')
# start = time()
# print "starting"
# while time() - start < maxTime:
#   print str(time() - start)
#   a = ser.readline()
#   array = [l for l in a]
#   vals = array[0:inputLength]
#   intArray = [ord(l) for l in vals]
#   strArray = [str(l) for l in intArray]
#   csv_line = ', '.join(strArray) + '\n'
#   f.write(csv_line)
#   print "line written"

# f.close()
# print "completed"



"""
THINGS TO ALWAS REMEMBER:

We're sending over stuff that's one higher than it should be. So, we need
to subtract one from it when we convert it back
"""

def train(trainingLabel, serdevString, whereToSave, listenTime):
  ser.flushOutput()
  f = open(whereToSave, 'w')
  f.write(str(trainingLabel) + '\n')
  print "starting read"
  start = time()
  
  for k in range(200):
    a = ser.readline()
  

  i = 0


  while time() - start < listenTime:
    i += 1
    if i % 100 == 0:
      print str(i) + " lines written"
    a = ser.readline()
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
  print "comlpeted"




train(1, '/dev/cu.usbmodem1412', 'trainingDataOne.txt', 10)













# i = 0
# while(i < 10)
# a = ser.readline()
# print a

ser.close()
