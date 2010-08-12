import classes,vars,random,sys
import functions as funcs

try:
	if sys.argv[1]=='-curses':
		vars.curses=True
except IndexError:
	print "No curses."

if vars.curses==True:
	import curses
	vars.screen = curses.initscr()
	curses.noecho()

random.seed()

adam=classes.Character(gender='Male',name='Adam',age=44)
eve=classes.Character(gender='Female',name='Eve',age=44)
adam1=classes.Character(gender='Male',name='Adam1',age=44)
eve1=classes.Character(gender='Female',name='Eve1',age=44)
player=classes.Character(isplayer=True,name='Player',gender="Male")

funcs.Parents_MakeChild(eve,adam)
funcs.Parents_MakeChild(eve1,adam1)

ticks=0

while ticks<150:
	for char in vars.character:
		char.Tick()
	ticks+=1
	funcs.DrawString(ticks)