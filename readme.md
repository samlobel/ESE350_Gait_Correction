#PROJECT ACHILLES

This is a data collection, analysis, and visualization software kit written by Sam Lobel and Yixing Du.

##Data Collection
We don't want to put too much analytical load on our mBed, so data collection's main task is transmitting the raw input data from the mBed to the computer. Once transmitted, we need to store it in our DataCollection/Data folder with appropriate file names, so that we can access it in the Machine_Learning section. On the mBed side of things, we collect data using sensors and then store it in a text file. 

#####Data Format
There will be both labeled data, which is used for training, and unlabeled data, which is used to classify a person's walking style. The first line of labeled data is the type of walking that was used to generate the dataset (0 for normal, 1 for pronated, and 2 for supinated). The rest of the labeled file is a CSV, where each line is a list of the softPot values collected in one timeStep. An unlabeled datafile is only the CSV part of things.

#####Data Transfer
Data transfer is going to be done over Bluetooth. Our computer will be listening for a file transfer, and when it happens, it will store the file in the data folder. 


##Data Visualization
Data visualizatoin won't be too complicated. It has two components: insole definition and pressure visualization. Insole definition is where you can define the shape of your insole, that can be fed into the visualization software to define your insole nsor positions. Visualization will take in a shape of the insole, and also read in a file to visualize. It'll then output the pressure sensor readings as red dots, on the lines that define your softPot strips.


##Machine Learning
This was definitely the most involved part of the programming. This part of the program had to take in a raw data file, compare it to training data, and output a classification of stride. 

#####Data Sanitization
We needed to go from previously-described raw data to a form of data that represented all of the steps taken in some reading period. This is the equivalent problem of finding domain walls that separate steps, and throwing out everything in between. Defining the beginning of a step as when 2 out of 5 sensors had non-negligible readings for some amount of time, and the end of a step as when they didn't, this problem was reduced to just iterating through an array of raw data timeStamps. The input of this part was a raw data array (an array of timeStamps, where timeStamps are arrays of sensor values), and the output was an array of steps (an array of steps, where steps are arrays of timeStamps, and timeStamps are arrays of sensor values). 

#####Comparing Steps
Once we have our stepArray, we needed a metric for comparing two different steps. A basic machine learning technique for comparing feature lists is treating it as a vector space, and finding some sensible distance metric that tells you sample-closeness. This is what we did to compare timeStamps, but a step is a variable-length sequence of timeStamps, which is a LOT more difficult to deal with. The technique we decided on is called Dynamic Time Warping, which is when you morph the time axis of two samples in order to find the timeStamp lineup that minimizes total comparison costs. It's essentially a dynamic programming problem, where you iterate until you're at the end of each sample, remembering the cost to get to any given comparison point along the way. Using these two metrics in tandem gave us a way to compare steps. Having this metric means that we could then do classification against labeled data.

#####Classifying Walking Style
We settled on a pretty simple machine-learning algorithm called k-Nearest-Neighbor classification. You train this method by inputting all of your labeled steps. When you want to classify an unlabeled step, you compare it to all of the labelled steps, keeping track of its distance from each. Then, you look at the closest k labeled steps. You assign whichever classification is most strongly represented in these k steps to your unlabeled step. After we could classify a single step, we wanted to get a sense of how somebody walks over time. By combining our methods for classifying a single step with our methods to convert a raw file into an array of steps, we could see the representation of each type of step in a walking session.

##SYNTHESIS

Here, I'll describe what the code does at the end of this project, in a perfect world.
Theoretically, everything could be done in GUI. We could have a constant listening thread going that writes to our data thread, and have flags that tell the rest of the program what's going on. In the GUI file, we'd have a knnObject, that would automatically be kept up-to-date with training data. And we'd listen for new files being added to non-training Data. You could click on a file to watch it in the visualizer. As you watched, you'd see important values accumulate.

That sounds pretty close to impossible. We'll probably have a listening mode, and then afterwards have a GUI that visualizes pre-collected data. We'll also have a script that just outputs relevant numbers.







