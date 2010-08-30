import vars,sys
from numpy import *
#from unicurses import *

def MakePath(x1,y1,x2,y2):
	#0	Scanned and closed
	#1	Not scanned
	#2	Scanned and open to be considered
	vars.AI_Open=ones((vars.map1.sizeX,vars.map1.sizeY))
	vars.AI_OpenList=[]
	vars.AI_Pathlist=[]
	vars.AI_Map=ones((vars.map1.sizeX,vars.map1.sizeY))
	vars.AI_G=ones((vars.map1.sizeX,vars.map1.sizeY))
	#self.AI_H=ones((self.sizeX,self.sizeY))
	#self.AI_F=ones((self.sizeX,self.sizeY))
	vars.exit_found=False
	
	max_x=1
	max_y=1
	
	start_node=Node(x1,y1,0,noparent=True)
	
	for y in range(vars.map1.sizeY):
		for x in range(vars.map1.sizeX):
			vars.AI_G[x,y]=0
			vars.AI_Map[x,y]=0
	
	#Scan the starting area
	xdist=-(max_x)
	ydist=-(max_y)
	while ydist<=(max_y):
		while xdist<=(max_x):
			if xdist==0 and ydist==0:
				vars.AI_Open[x1,y1]=0
			else:
				if y1+ydist<vars.map1.sizeY and x1+xdist<vars.map1.sizeX:
					#If walkable
					if vars.map1.Map[x1+xdist,y1+ydist]==1 or vars.map1.Map[x1+xdist,y1+ydist]==4:
						#Changed to 'Scanned and Open'
						#self.AI_Open[x1+xdist,y1+ydist]=2
						#Create node here
						temp=Node(x1+xdist,y1+ydist,abs(xdist)+abs(ydist),parent=start_node,status=2)
						temp.FindDist(x2,y2)
						#Calculate moves required
						#Might not need this if I'm already giving the node a G value
						vars.AI_G[x1+xdist,y1+ydist]=temp.g
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
				return vars.AI_Pathlist
			else:
				#Search for new areas around next_node
				SearchArea(next_node,x2,y2)
		
		step+=1
		if step>=step_max:
			next_node=start_node
			step=0
			fail+=1
		if fail>=10:
			vars.TOPBAR='FAILED'
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