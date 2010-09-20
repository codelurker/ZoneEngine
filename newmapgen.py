import random,numpy,time,vars,math
from numpy import *
from math import *
from unicurses import *
from time import time
"""stdscr = initscr()
noecho()
cbreak()
curs_set(0)
keypad(stdscr, True)
start_color()
init_pair(1, COLOR_GREEN, COLOR_BLACK)
init_pair(2, COLOR_GREEN, COLOR_BLACK)
random.seed()"""
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
					#attron(A_ALTCHARSET)
					mvaddstr(y, x, Render(self.Map[x,y]))
					#attroff(A_ALTCHARSET)
				if self.Map[x,y]!=3 and self.Map[x,y]!=4 and self.Map[x,y]!=1:
					mvaddstr(y, x, Render(self.Map[x,y]))
	def DrawCustom(self,array):
		for y in range(self.sizeY):
			for x in range(self.sizeX):
				mvaddstr(y, x, RenderCustom(array[x,y]))
				#mvaddstr(y, x, str(array[x,y]).rpartition('.')[0])
	def DrawNodes(self):
		for node in vars.AI_Nodes:
			#mvaddstr(node.y, node.x, RenderCustom(node.f))
			mvaddstr(node.y, node.x, '.')
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
							self.Map[x,y]=3
				except:
					pass
		
	def MakePath(self,x1,y1,x2,y2):
		#0	Scanned and closed
		#1	Not scanned
		#2	Scanned and open to be considered
		self.AI_Open=ones((self.sizeX,self.sizeY))
		vars.AI_OpenList=[]
		vars.AI_Pathlist=[]
		vars.AI_Map=ones((self.sizeX,self.sizeY))
		self.AI_G=ones((self.sizeX,self.sizeY))
		self.AI_H=ones((self.sizeX,self.sizeY))
		self.AI_F=ones((self.sizeX,self.sizeY))
		vars.exit_found=False
		
		max_x=1
		max_y=1
		
		start_node=Node(x1,y1,0,noparent=True)
		
		for y in range(self.sizeY):
			for x in range(self.sizeX):
				self.AI_G[x,y]=0
				vars.AI_Map[x,y]=0
		
		#Scan the starting area
		xdist=-(max_x)
		ydist=-(max_y)
		while ydist<=(max_y):
			while xdist<=(max_x):
				if xdist==0 and ydist==0:
					self.AI_Open[x1,y1]=0
				else:
					if y1+ydist<vars.map1.sizeY and x1+xdist<vars.map1.sizeX:
						#If walkable
						if vars.map1.Map[x1+xdist,y1+ydist]==1:
							#Changed to 'Scanned and Open'
							#self.AI_Open[x1+xdist,y1+ydist]=2
							#Create node here
							temp=Node(x1+xdist,y1+ydist,abs(xdist)+abs(ydist),parent=start_node,status=2)
							temp.FindDist(x2,y2)
							#Calculate moves required
							#Might not need this if I'm already giving the node a G value
							self.AI_G[x1+xdist,y1+ydist]=temp.g
				xdist+=1
			if xdist>=(max_x):
				xdist=-(max_x)
			ydist+=1
		
		#GO!
		step_max=50
		step=0
		fail=0

		while vars.exit_found==False:
			#Start scanning open nodes
			next_node=FindLowest()	
			
			if next_node!=None:
				if next_node.x==x2 and next_node.y==y2:
					vars.exit_found=True
				else:
					#Search for new areas around next_node
					SearchArea(next_node,x2,y2)
			
			step+=1
			if step>=step_max:
				next_node=start_node
				step=0
				fail+=1
			if fail>=10:
				sys.exit()

def ShowPath():
	for node in vars.AI_Pathlist:
		mvaddstr(node[1], node[0], '.')

def SearchArea(node,end_x,end_y):
	max_x=1
	max_y=1
		
	xdist=-(max_x)
	ydist=-(max_y)
	while ydist<=(max_y):
		while xdist<=(max_x):
			if xdist==0 and ydist==0:
				pass
			else:
				if node.y+ydist<vars.map1.sizeY and node.x+xdist<vars.map1.sizeX:
					#If walkable
					if vars.map1.Map[node.x+xdist,node.y+ydist]==1 or vars.map1.Map[node.x+xdist,node.y+ydist]==4: 
						if vars.AI_Map[node.x+xdist,node.y+ydist]==0:
							#Doesn't take the G value from the parent...
							#It's faster, but I don't know how good it is yet
							temp=Node(node.x+xdist,node.y+ydist,abs(xdist)+abs(ydist),parent=node,status=2)
							#temp=Node(node.x+xdist,node.y+ydist,node.g+(abs(xdist)+abs(ydist)),parent=node,status=2)
							temp.FindDist(end_x,end_y)
			xdist+=1
		if xdist>=(max_x):
			xdist=-(max_x)
		ydist+=1

def FindLowest():
	#Start scanning open nodes
	lowest=None
	current_lowest=None
	for item in vars.AI_OpenList:
		if current_lowest==None:
			current_lowest=item
		else:
			if item.f<current_lowest.f and item.status==2:
				current_lowest=item
				vars.lowest=str(current_lowest.x)+','+str(current_lowest.y)
		
		if current_lowest!=None:
			current_lowest.status=0
	
	if current_lowest==None:
		pass
	else:
		vars.AI_Pathlist.append((current_lowest.x,current_lowest.y))
		return current_lowest

class Node:
	def __init__(self,x1,y1,g,parent=None,status=1,noparent=False):
		self.x=x1
		self.y=y1
		self.g=g
		self.h=0
		self.f=0
		self.status=status
		if noparent==False:
			self.parent=parent
			vars.AI_OpenList.append(self)
			vars.AI_Map[self.x,self.y]=1
		vars.AI_Nodes.append(self)
		
	def FindDist(self,x2,y2):
		#Manhattan method
		self.h=abs(self.x-x2)+abs(self.y-y2)
		self.f=self.g+self.h

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
						if random.randint(0,6)<=1:
							self.Tile[x,y]=5
						else:
							if random.randint(0,40)<=7:
								self.Tile[x,y]=6
							else:
								self.Tile[x,y]=3
					if y==0 or y==self.sizeY-1:
						if random.randint(0,6)<=1:
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
	if num==6: return "?"
	if num==7: return "?"

def RenderCustom(num):
	if num==0: return " "
	if num==1: return "1"
	if num==2: return "2"
	if num==3: return "3"
	if num==4: return "4"
	if num==5: return "5"
	if num==6: return "6"
	if num==7: return "7"
	if num==8: return "8"
	if num==9: return "9"
	if num>=10: return "?"

#map_gen_time = time()
#vars.map1=Map(80,25)
#vars.map1.Generate()
#map_gen_time_end = time()
#vars.map1.Map[18,9]=3
"""start_x=random.randint(5,75)
start_y=random.randint(5,22)
exit_x=random.randint(5,75)
exit_y=random.randint(5,22)
path_gen_time = time()
vars.map1.MakePath(start_x,start_y,exit_x,exit_y)
#vars.map1.DrawCustom(vars.map1.MakePath(20,10,0,0))
vars.map1.Draw()
#vars.map1.DrawNodes()
ShowPath()
path_gen_time_end=time()
mvaddstr(start_y, start_x, 'S')
mvaddstr(exit_y, exit_x, 'F')
mvaddstr(0, 0, ' Map generated in '+str(map_gen_time_end-map_gen_time))
mvaddstr(1, 0, 'Path generated in '+str(path_gen_time_end-path_gen_time))
mvaddstr(2, 0, '            Total '+str((map_gen_time_end-map_gen_time)+(path_gen_time_end-path_gen_time)))"""
#refresh()
#endwin()
