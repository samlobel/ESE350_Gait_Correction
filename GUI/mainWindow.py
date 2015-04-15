import Tkinter
root = Tkinter.Tk()


w, h = root.winfo_screenwidth() * 3 / 4, root.winfo_screenheight() * 3 / 4 

barWidth = 100

canvas = Tkinter.Canvas(root, width=w,height=h)


# startx,starty = 0,0
# endx,endy = 0,0

# mouse_is_down = False
# lineToMove = w.create_line(100,100,200,200)
# lineToMove = None

lines = []
balls = []
relPos = []


inEditMode = True


def getCoordsForLineAndOPos(line,pos):
    # pos is 0 to 1
    cs = line.coords()
    center_pos = (pos*cs[2] + (1 - pos)*cs[0], pos*cs[3] + (1 - pos)*cs[1] )
    ul = (center_pos[0] - 20, center_pos[1] -20)
    lr = (center_pos[0] + 20, center_pos[1] +20)
    return ul[0],ul[1],lr[0],lr[1]

def createBallForLineAndPos(line,pos, canv):
    coords = getCoordsForLineAndOPos(line,pos)
    ball = canvas.create_oval(coords, fill="#FF0000")
    balls.append(ball)





def clicked(event):
    global lines
    global balls
    print "clicked at", event.x, event.y
    startx,starty = event.x, event.y    
    endx,endy = event.x, event.y
    mouse_is_down = True
    lines.append(canvas.create_line(startx,starty,endx,endy))
    print lines   

def unclicked(event):
    global lines
    print "unclicked at", event.x, event.y
    mouse_is_down = False
    print lines

def onPressed(event):
    # print "mouse down"
    endx,endy = event.x, event.y
    mostRecent = lines[len(lines) - 1]
    nowCoords = canvas.coords(mostRecent)
    canvas.coords(mostRecent, nowCoords[0], nowCoords[1], endx, endy)
    print lines



# coord = 10, 50, 240, 210
# arc = w.create_line(coord)
canvas.bind("<Button-1>", clicked)
canvas.bind("<ButtonRelease-1>", unclicked)
canvas.bind("<B1-Motion>", onPressed)





canvas.pack(side='right')


def coordArrayFromLines():
    global lines
    global canvas
    toReturn = map(lambda l : canvas.coords(l), lines)
    print toReturn
    return toReturn



menuBar = Tkinter.Frame(root,width=barWidth, height=h, bg="#FFFFFF")
menuBar.pack(side='left')


def switchEditMode():
    global inEditMode
    inEditMode = not inEditMode
    print inEditMode
    if inEditMode:
        b.config(activebackground="#FFFFFF", bg="#FFFFFF")

    else:
        b.config(activebackground="#000000",bg="#000000")   




b=Tkinter.Button(menuBar, text="EditMode", width=10, command=switchEditMode)
b.config(activebackground="#FFFFFF",bg="#FFFFFF")   

c=Tkinter.Button(menuBar, text="GoodBye",width=10, command=coordArrayFromLines)



# def deleteBalls():
#   global lines
#   global balls
#   global canvas
#   map(lambda b: canvas.delete(b), balls)

# def createBalls():
#   global relPos
#   global balls
#   global lines
#   global canvas









b.pack(side='top')
c.pack(side='top')


# canvas.create_oval(100,200,300,400)

root.resizable(width=False, height=False)


# Code to add widgets will go here...

root.mainloop()