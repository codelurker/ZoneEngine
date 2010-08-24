import classes,vars,random,sys,time,threading
import functions as funcs
import newmapgen as map

#try:
#	if sys.argv[1]=='-curses':
#		vars.curses=True
#except IndexError:
#	print "No curses."

vars.TOPBAR='ZoneEngine'
vars.running=True
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
vars.player=classes.Character(isplayer=True,name='Player',gender="Male")

iwepDagger=classes.Item(owner=vars.player,name='Dagger')
iwepSword=classes.Item(owner=vars.player,name='Sword')

funcs.Parents_MakeChild(eve,adam)
vars.player.Draw()

class GameThread(threading.Thread):
	def run(self):
		while 1:
			while vars.paused:
				pass
			for char in vars.character:
				vars.map1.DrawPos(char.x,char.y)
				char.Tick()
			funcs.DrawStringColor(3,vars.TOPBAR,bold=True)
			refresh()
			time.sleep(0.2)
			if vars.running==False:
				endwin()
				sys.exit()

GameThread().start()
classes.PlayerInput().start()