import Tkinter
from time import sleep
from pprint import pprint
from Queue import Queue
from threading import Thread

root = Tkinter.Tk()

w, h = root.winfo_screenwidth() * 3 / 4, root.winfo_screenheight() * 3 / 4 
canvas = Tkinter.Canvas(root, width=w,height=h)
canvas.pack(side='right')

currentpos_queue = Queue()





lineArrayOne = [[392.0, 194.0, 433.0, 504.0], [480.0, 193.0, 475.0, 496.0], [505.0, 503.0, 558.0, 194.0], [430.0, 481.0, 509.0, 481.0], [423.0, 428.0, 519.0, 433.0], [410.0, 331.0, 533.0, 331.0], [396.0, 225.0, 554.0, 224.0]]


ballPosOne = [0.5,0.5,0.5,0.5,0.5,0.5,0.5]
ballPosTwo = [1.0,1.0,1.0,1.0,1.0,1.0,1.0]
ballPosAdjustable = [1.0,1.0,1.0,1.0,1.0,1.0,1.0]


lines = []

ourLineArray = lineArrayOne
ourBallPosArray = ballPosAdjustable

for coords in ourLineArray:
	line = canvas.create_line(coords)
	lines.append(line)

balls = []

def getCoordsForLineAndPos(line,pos,canvas):
    # pos is 0 to 1
    cs = canvas.coords(line)
    center_pos = (pos*cs[2] + (1 - pos)*cs[0], pos*cs[3] + (1 - pos)*cs[1] )
    ul = (center_pos[0] - 10, center_pos[1] -10)
    lr = (center_pos[0] + 10, center_pos[1] +10)
    return ul[0],ul[1],lr[0],lr[1]

def createBallForLineAndPos(line,pos, canv):
    coords = getCoordsForLineAndPos(line,pos,canvas)
    ball = canvas.create_oval(coords, fill="#FF0000")
    return ball

for i in range(0,len(lines)):
	# coords = getCoordsForLineAndPos(lines[i], ballPosOne[i], canvas)
	# ball = createBallForLineAndPos(lines[i], ballPosOne[[i], canvas)
	# ball = createBallForLineAndPos(line,pos, canvas)
	ball = createBallForLineAndPos(lines[i], ourBallPosArray[i], canvas)
	balls.append(ball)


def moveBallToNewPos(lines, newPos, ballArr, canvas):
	for i in range(0,len(lines)):
		cs = getCoordsForLineAndPos(lines[i], newPos[i], canvas)
		canvas.coords(ballArr[i], cs)



def posOneButton():
	moveBallToNewPos(lines, ballPosOne,balls,canvas)

def posTwoButton():
	moveBallToNewPos(lines, ballPosTwo,balls,canvas)


def upClicked(e):
	global ballPosAdjustable
	pprint(ballPosAdjustable)
	if(ballPosAdjustable[0] > 0.99):
		print("At Top")
		return
	else:
		for i in range(0, len(ballPosAdjustable)):
			ballPosAdjustable[i] += 0.01
		moveBallToNewPos(lines, ballPosAdjustable, balls, canvas)

def downClicked(e):
	global ballPosAdjustable
	pprint(ballPosAdjustable)
	if(ballPosAdjustable[0] < 0.01):
		print("At Bottom")
		return
	else:
		for i in range(0, len(ballPosAdjustable)):
			ballPosAdjustable[i] -= 0.01
		# map(lambda x : x - 0.1, ballPosAdjustable)
		pprint(ballPosAdjustable)
		moveBallToNewPos(lines, ballPosAdjustable, balls, canvas)






menuBar = Tkinter.Frame(root,width=100, height=h, bg="#FFFFFF")
menuBar.pack(side='left')

b=Tkinter.Button(menuBar, text="EditMode", width=10, command=posOneButton)
c=Tkinter.Button(menuBar, text="GoodBye",width=10, command=posTwoButton)

b.pack(side='top')
c.pack(side='top')



root.bind("<Up>", upClicked)
root.bind("<Down>", downClicked)





root.resizable(width=False, height=False)

root.mainloop()


# while True:
# 	print "Here"
# 	sleep(1.0)
# 	# ourBallPosArray = ballPosOne
# 	moveBallToNewPos(lines, ballPosOne, balls, canvas)
# 	sleep(1.0)
# 	# ourBallPosArray = ballPosOne
# 	moveBallToNewPos(lines, ballPosTwo, balls, canvas)

