import classes,vars,random,sys,time
import functions as funcs
import newmapgen as map

try:
	if sys.argv[1]=='-curses':
		vars.curses=True
except IndexError:
	print "No curses."

vars.TOPBAR='ZoneEngine'

vars.curses=True

if vars.curses==True:
	from unicurses import *
	vars.screen = initscr()
	noecho()
	cbreak()
	curs_set(0)
	keypad(vars.screen, True)
	start_color()
	init_pair(1, COLOR_GREEN, COLOR_BLACK)
	init_pair(2, COLOR_CYAN, COLOR_BLACK)
	init_pair(3, COLOR_RED, COLOR_BLACK)

random.seed()
ticks=0

vars.map1=map.Map(80,25)
vars.map1.Generate()
vars.map1.Draw()

adam=classes.Character(gender='Male',name='Adam',age=20)
eve=classes.Character(gender='Female',name='Eve',age=20)
#adam1=classes.Character(gender='Male',name='Adam1',age=20)
#eve1=classes.Character(gender='Female',name='Eve1',age=20)
player=classes.Character(isplayer=True,name='Player',gender="Male")

funcs.Parents_MakeChild(eve,adam)
#funcs.Parents_MakeChild(eve1,adam1)

while ticks<100:
	for char in vars.character:
		vars.map1.DrawPos(char.x,char.y)
		char.Tick()
	ticks+=1
	funcs.DrawStringColor(3,vars.TOPBAR)
	if vars.curses: refresh()
	time.sleep(0.01)

if vars.curses: endwin()
