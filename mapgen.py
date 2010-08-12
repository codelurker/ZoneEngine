import random,numpy,time
from numpy import *
from math import *
import curses
screen = curses.initscr()
curses.noecho()

random.seed()

class Map:
	def __init__(self,sizeX,sizeY):
		self.sizeX=sizeX
		self.sizeY=sizeY
		self.Map=ones((self.sizeX,self.sizeY))
	def Generate(self):
		self.room1=Room(10,10)
		self.room1.MakeRandom()
		self.PlaceRoom(self.room1)
	def PlaceRoom(self,room):
		line=""
		for y in range(room.sizeY):
			for x in range(room.sizeX):
				self.Map[x,y]=room.Tile[x,y]
				line=line+str(room.Tile[x,y])
			line=line+'\n'
	def Draw(self):
		line=""
		for y in range(self.sizeY):
			for x in range(self.sizeX):
				screen.addstr(x, y, Render(self.Map[x,y]))

class Room:
	def __init__(self,X,Y):
		self.sizeX=X
		self.sizeY=Y
		self.Tile=ones((self.sizeX,self.sizeY))
	def MakeRandom(self):
		line=""
		for y in range(self.sizeY):
			for x in range(self.sizeX):
				if self.Tile[x,y]==1:
					if x==0 and y==0: self.Tile[x,y]=2
					if x==self.sizeX-1 or x==0:
						self.Tile[x,y]=3
					if y==self.sizeY-1 or y==0:
						self.Tile[x,y]=3
					if x>0 and x<self.sizeX-1:
						if y>0 and y<self.sizeY-1:
							self.Tile[x,y]=4
				line=line+Render(self.Tile[x,y])
				screen.addstr(x, y, Render(self.Tile[x,y]))
			line=line+'\n'
		#print line

def Render(num):
	if num==1: return " "
	if num==2: return "+"
	if num==3: return "#"
	if num==4: return "."

map1=Map(20,20)
map1.Generate()
key=1
while key!=ord('5'):
	key = screen.getch()
	map1.Draw()
	screen.refresh()
curses.endwin()
