This is a data collection, analysis, and visualization software kit written by Sam Lobel and Yixing Du.

##Data Collection
We don't want to put too much analytical load on our mBed, so data collection's main task is transmitting the raw input data from the mBed to the computer. On the mBed side of things, we collect data using sensors and then store it in a text file. 

####Data Format
There will be both labeled data, which is used for training, and unlabeled data, which is used to classify a person's walking style. The first line of labeled data is the type of walking that was used to generate the dataset (0 for normal, 1 for pronated, and 2 for supinated). The rest of the labeled file is a CSV, where each line is a list of the softPot values collected in one timeStep. An unlabelled datafile is only the CSV part of things.

####Data Transfer
Data transfer is going to be done over Bluetooth. Our computer will be listening for a file transfer, and when it happens, it will store the file in the data folder. 