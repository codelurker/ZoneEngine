import random,numpy,time,vars
from numpy import *
from math import *
from unicurses import *
stdscr = initscr()
noecho()
cbreak()
curs_set(0)
keypad(stdscr, True)
start_color()
random.seed()
vars.MSG="ZoneEngine"
vars.MSG2=">Randomized..."

class Map:
	def __init__(self,sizeX,sizeY):
		self.sizeX=sizeX
		self.sizeY=sizeY
		self.Map=ones((self.sizeX,self.sizeY))
		self.rooms=[]
	def Generate(self):
		#Make some rooms
		for a in range(5):
			temp=Room(random.randint(10,15),random.randint(10,15))
			self.rooms.append(temp)
			temp.Generate()
			findX=random.randint(5,10)*(a+random.randint(1,5))
			findY=random.randint(1,5)*(a+random.randint(1,4))+temp.sizeY
			while findX+temp.sizeX>self.sizeX:
				findX=random.randint(5,10)*(a+random.randint(1,5))
			while findY+temp.sizeY>self.sizeY:
				findY=random.randint(1,5)*(a+random.randint(1,4))
			self.Place(temp,x1=findX,y1=findY)
		#Dig some tunnels
		#self.Dig(self.start_room)
	def Place(self,room,x1=0,y1=0):
		for y in range(room.sizeY):
			for x in range(room.sizeX):
				if self.Map[x1+x,y1+y]==1:
					self.Map[x1+x,y1+y]=room.Tile[x,y]
				else:
					if y!=0 and y!=room.sizeY-1 and x!=0 and x!=room.sizeX-1:
						self.Map[x1+x,y1+y]=4
	def Draw(self):
		for y in range(self.sizeY):
			for x in range(self.sizeX):
				mvaddstr(y, x, Render(self.Map[x,y]))
	def Dig(self,room):
		pass

class Room:
	def __init__(self,x1,y1):
		self.sizeX=x1
		self.sizeY=y1
		self.Tile=ones((self.sizeX,self.sizeY))
	def Generate(self):
		for y in range(self.sizeY):
			for x in range(self.sizeX):
				if x==0 or x==self.sizeX-1:
					if random.randint(0,10)==5:
						self.Tile[x,y]=5
					else:
						self.Tile[x,y]=3
				if y==0 or y==self.sizeY-1:
					if random.randint(0,10)==5:
						self.Tile[x,y]=5
					else:
						self.Tile[x,y]=3
				if y>0 and y<self.sizeY-1:
					if x>0 and x<self.sizeX-1:
						self.Tile[x,y]=4
		
def Render(num):
	if num==1: return " "
	if num==2: return "+"
	if num==3: return "#"
	if num==4: return "."
	if num==5: return "H"

map1=Map(75,25)
map1.Generate()
map1.Draw()
refresh()
endwin()