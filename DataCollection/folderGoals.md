#FOLDER GOALS
##Method List

As a note, it's hard to predict how complicated this section will be. It might have to be written mainly in bash, with file piping and whatnot. Here's to hoping that pyBluez doesn't suck. 

I think we should classify for just one person first, and then maybe expand. It's a little bit unclear whether training data from one person will really work on another.

Alternatively, if we can't get bluetooth to work, we can just plug in the microSD card to our computron and move the files over manually (/write a script to do it for us.)


###acceptTrainingFile
This guy is going to wait for a training file to be transmitted over bluetooth. There will be some EOF signal (maybe two newLines in a row, or an irregular ASCII character), that will tell the method to exit. In all likelihood, we'll call this method by listening for some sort of header.

###acceptDataFile
Like acceptTrainingFile, except it won't be expecting a classification number as its first line.

