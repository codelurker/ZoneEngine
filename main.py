import classes,vars,random,sys,time
import functions as funcs

try:
	if sys.argv[1]=='-curses':
		vars.curses=True
except IndexError:
	print "No curses."

vars.curses=True

if vars.curses==True:
	from unicurses import *
	vars.screen = initscr()
	noecho()
	cbreak()
	curs_set(0)
	keypad(vars.screen, True)
	start_color()

random.seed()

adam=classes.Character(gender='Male',name='Adam',age=20)
eve=classes.Character(gender='Female',name='Eve',age=20)
adam1=classes.Character(gender='Male',name='Adam1',age=20)
eve1=classes.Character(gender='Female',name='Eve1',age=20)
player=classes.Character(isplayer=True,name='Player',gender="Male")

funcs.Parents_MakeChild(eve,adam)
funcs.Parents_MakeChild(eve1,adam1)

ticks=0

while ticks<250:
	for char in vars.character:
		char.Tick()
	ticks+=1
	#funcs.DrawString(ticks)
	#funcs.DrawList(vars.MsgBox)
	if vars.curses: refresh()
	time.sleep(0.01)

if vars.curses: endwin()
