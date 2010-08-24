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
init_pair(1, COLOR_GREEN, COLOR_BLACK)
init_pair(2, COLOR_GREEN, COLOR_BLACK)
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
		for a in range(13):
			if a>=3:
				temp=Room(random.randint(10,15),random.randint(6,10))
			else:
				temp=Room(random.randint(5,10),random.randint(3,8),no_fill=True)
			self.rooms.append(temp)
			temp.Generate()
			findX=random.randint(2,10)*(a+random.randint(1,5))-3
			findY=random.randint(1,5)*(a+random.randint(1,4))+temp.sizeY-3
			while findX+temp.sizeX>self.sizeX:
				findX=random.randint(2,10)*(a+random.randint(1,5))-3
			while findY+temp.sizeY>self.sizeY:
				findY=random.randint(1,5)*(a+random.randint(1,4))-3
			self.Place(temp,x1=findX,y1=findY)
		#Dig some tunnels
		self.Dig()
	def Place(self,room,x1=0,y1=0):
		for y in range(room.sizeY):
			for x in range(room.sizeX):
				if room.no_fill==False:
					if self.Map[x1+x,y1+y]==1:
						self.Map[x1+x,y1+y]=room.Tile[x,y]
					else:
						if y!=0 and y!=room.sizeY-1 and x!=0 and x!=room.sizeX-1:
							self.Map[x1+x,y1+y]=4
				else:
					#so no_fill = True here
					#Every no_fill section is filled with #'s
					#Can we figure out if this works?
					if self.Map[x1+x,y1+y]>1:
						self.Map[x1+x,y1+y]=3
	def Draw(self):
		for y in range(self.sizeY):
			for x in range(self.sizeX):
				if self.Map[x,y]==1:
					mvaddstr(y, x, Render(self.Map[x,y]))
				if self.Map[x,y]==4:
					attron(COLOR_PAIR(1))
					mvaddstr(y, x, Render(self.Map[x,y]))
					attroff(COLOR_PAIR(1))
				if self.Map[x,y]==3:
					attron(A_ALTCHARSET)
					mvaddstr(y, x, Render(self.Map[x,y]))
					attroff(A_ALTCHARSET)
				if self.Map[x,y]!=3 and self.Map[x,y]!=4 and self.Map[x,y]!=1:
					mvaddstr(y, x, Render(self.Map[x,y]))
	def RedrawAll(self,char,pos):
		for y in range(self.sizeY):
			for x in range(self.sizeX):
				if self.Map[x,y]==char:
					if x==pos[0] and y==pos[1]:
						pass
					else:
						mvaddstr(y, x, Render(self.Map[x,y]))
					
	def DrawPos(self,x,y):
		if self.Map[x,y]==1:
			mvaddstr(y, x, Render(self.Map[x,y]))
		if self.Map[x,y]==4:
			attron(COLOR_PAIR(1))
			mvaddstr(y, x, Render(self.Map[x,y]))
			attroff(COLOR_PAIR(1))
		if self.Map[x,y]==3:
			mvaddstr(y, x, Render(self.Map[x,y]))
		if self.Map[x,y]!=3 and self.Map[x,y]!=4 and self.Map[x,y]!=1:
			mvaddstr(y, x, Render(self.Map[x,y]))
	def Dig(self):
		for y in range(self.sizeY):
			for x in range(self.sizeX):
				try:
					if self.Map[x,y]==5:
						if self.Map[x,y-1]!=1 and self.Map[x,y+1]!=1:
							if self.Map[x-1,y]!=1 and self.Map[x+1,y]!=1:
								self.Map[x,y]=4
					if self.Map[x,y]==6:
						if self.Map[x,y-1]!=1 and self.Map[x,y+1]!=1:
							if self.Map[x-1,y]!=1 and self.Map[x+1,y]!=1:
								self.Map[x,y]=4
							else:
								self.Map[x,y]=4
						else:
							self.Map[x,y]=4
				except:
					pass

class Room:
	def __init__(self,x1,y1,no_fill=False):
		self.sizeX=x1
		self.sizeY=y1
		self.Tile=ones((self.sizeX,self.sizeY))
		self.no_fill=no_fill
	def Generate(self):
		for y in range(self.sizeY):
			for x in range(self.sizeX):
				if self.no_fill==False:
					if x==0 or x==self.sizeX-1:
						if random.randint(0,6)<=3:
							self.Tile[x,y]=5
						else:
							if random.randint(0,40)<=7:
								self.Tile[x,y]=6
							else:
								self.Tile[x,y]=3
					if y==0 or y==self.sizeY-1:
						if random.randint(0,6)<=3:
							self.Tile[x,y]=5
						else:
							if random.randint(0,40)<=7:
								self.Tile[x,y]=6
							else:
								self.Tile[x,y]=3
					if y>0 and y<self.sizeY-1:
						if x>0 and x<self.sizeX-1:
							self.Tile[x,y]=4
				else:
					if x==0 or x==self.sizeX-1:
							self.Tile[x,y]=3
					if y==0 or y==self.sizeY-1:
							self.Tile[x,y]=3
					#if y>0 and y<self.sizeY-1:
					#	if x>0 and x<self.sizeX-1:
					#		self.Tile[x,y]=1
		
def Render(num):
	if num==1: return " "
	if num==2: return "+"
	if num==3: return "#"
	if num==4: return "."
	if num==5: return "#"
	if num==6: return "#"
	if num==7: return "?"

mvaddstr(0, 0, ''+vars.MSG)
refresh()
endwin()