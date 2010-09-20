import vars,random,sys,time,threading
try:
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
except:
	from curses import *
	vars.screen = initscr()
	noecho()
	cbreak()
	curs_set(0)
	vars.screen.keypad(1)
	start_color()
	init_pair(1, COLOR_GREEN, COLOR_BLACK)
	init_pair(2, COLOR_CYAN, COLOR_BLACK)
	init_pair(3, COLOR_RED, COLOR_BLACK)
import newmapgen as map
import functions as funcs
import alife
import threads

vars.TOPBAR='ZoneEngine'
vars.running=True
vars.curses=True

random.seed()
ticks=0

vars.map1=map.Map(80,25)
vars.map1.Generate()
vars.map1.Draw()
vars.player=alife.Player()

adam = alife.NPC()
vars.player._isplayer=True

#adam=classes.Character(gender='Male',name='Adam',age=20)
#eve=classes.Character(gender='Female',name='Eve',age=20)
#vars.player=classes.Character(isplayer=True,name='Player',gender="Male")

#iwepDagger=classes.Item(owner=vars.player,name='Dagger')
#iwepSword=classes.Item(owner=vars.player,name='Sword')

#funcs.Parents_MakeChild(eve,adam)
#vars.player.Draw()

class GameThread(threading.Thread):
	def run(self):
		while 1:
			while vars.paused:
				pass
			for char in vars.character:
				vars.map1.DrawPos(char.x,char.y)
				char.Tick()
				#char.Draw()
			funcs.DrawStringColor(3,vars.TOPBAR,bold=True)
			refresh()
			time.sleep(0.1)
			if vars.running==False:
				endwin()
				sys.exit()

GameThread().start()
threads.PlayerInput().start()
