import vars,random
import functions as funcs
from unicurses import *
vars.ID=0
random.seed()

init_pair(1, COLOR_GREEN, COLOR_BLACK)
init_pair(2, COLOR_CYAN, COLOR_BLACK)
init_pair(3, COLOR_RED, COLOR_BLACK)

class Void:
	def __init__(self):
		self.x=1
		self.y=1
		self.name="VOID"
vars.VOID=Void()

class Item:
	def __init__(self,name='null',type='null',x=-1,y=-1,owner=None):
		self.name=name
		self.type=type
		self.x=x
		self.y=y
		self.owner=owner
		
		if owner!=None:
			owner.GiveItem(self)

class Character:
	def __init__(self,isplayer=False,initial=False,father=vars.VOID,mother=vars.VOID,gender="",name="null",race="null",age=0):
		#Tech jargon
		self.isplayer=isplayer
		self.id=funcs.ID_Give()
		self.x=mother.x
		self.y=mother.y
		self.last_x=0
		self.last_y=0
		self.ticks=0
		vars.character.append(self)
		self.sprite='@'
		
		#Character history
		self.age=age
		self.birthspot=[self.x,self.y]
		self.mother=mother
		self.father=father
		self.race=race
		if self.race=="null":
			self.race=funcs.Parents_GetRace(self.mother,self.father)
		else:
			self.race=race
		if gender=="":
			self.gender=funcs.Parents_BirthGender(self.mother,self.father)
		else:
			self.gender=gender
		if name=="null":
			self.name=funcs.Race_GetNameFromGender(self.race,self.gender)
		else:
			self.name=name
		
		##Character stats
		self.level=0
		#Does the child inherit any experience from its parents?
		self.experience=funcs.Parents_GetExperience(self.mother,self.father)
		#Did the child inherit any diseases/defects?
		self.diseases=funcs.Parents_GetDiseases(self.mother,self.father)
		#If not, what's the chance some developed on their own?
		if not len(self.diseases):
			self.diseases=funcs.Disease_BornWith()
		#What skills will the child inherit?
		self.skills=funcs.Parents_GetSkillsFromParents(self.mother,self.father)
		#Skills naturally received via race:
		self.skills=funcs.Parents_GetSkillsFromRace(self.race)
		
		##Personality
		#How well can the character get along with others? (1-100)
		self.Self_SocialFemaleHuman=50
		self.Self_SocialFemaleElf=50
		self.Self_SocialMaleHuman=50
		self.Self_SocialMaleElf=50
		funcs.Self_GetSocial(self)
		
		#The mental state of the character.
		#1 - Suicidal
		#2 - Depressed
		#3 - Down
		#4 - Content
		#5 - Well
		#6 - Good
		#Self_MentalState is gradiently controlled by Self_Mental.
		self.Self_MentalState=4
		self.Self_Mental=40
		
		#Tracking
		self.status='ready'
		self.children=[]
		
		#Inventory
		self.inventory=[]
		
		funcs.Self_PutOnMap(self)
	
	def GetInput(self):
		finished=False
		while finished==False:
			key=wgetch(vars.screen)
			if key==KEY_UP:
				if vars.map1.Map[self.x,self.y-1]==4 or vars.map1.Map[self.x,self.y-1]==1:
					vars.map1.DrawPos(self.x,self.y)
					self.y-=1
				finished=True
			elif key==KEY_DOWN:
				if vars.map1.Map[self.x,self.y+1]==4 or vars.map1.Map[self.x,self.y+1]==1:
					vars.map1.DrawPos(self.x,self.y)
					self.y+=1
				finished=True
			elif key==KEY_LEFT:
				if vars.map1.Map[self.x-1,self.y]==4 or vars.map1.Map[self.x-1,self.y]==1:
					vars.map1.DrawPos(self.x,self.y)
					self.x-=1
				finished=True
			elif key==KEY_RIGHT:
				if vars.map1.Map[self.x+1,self.y]==4 or vars.map1.Map[self.x+1,self.y]==1:
					vars.map1.DrawPos(self.x,self.y)
					self.x+=1
				finished=True
			elif key==ord('i'):
				a=1
				funcs.DrawStringColor(2,'Inventory',x=0,y=0)
				for item in self.inventory:
					funcs.DrawString(str(a)+') '+item.name,y=a)
					a+=1
				refresh()
			elif key==ord('q'):
				vars.running=False
				finished=True
	
	def Tick(self):
		if self.ticks==20:
			self.age+=1
			funcs.DrawString(self.name+' is now '+str(self.age))
			self.ticks=0
		if self.age==50:
			del vars.character[funcs.FindInList(self,vars.character)]
			funcs.DrawString(self.name+' has died. Removing '+str(self.id))
		
		if len(self.children)<1 and self.gender=="Female":
			if random.randint(0,50)<=8:
				child=self.HasChild()

		if not self.isplayer:
			self.MoveRandomize()
		self.Draw()
		self.ticks+=1

	def MoveRandomize(self,xm=True,ym=True):
		num=int(random.choice('2648'))
		if num==2 and (self.y+1)<vars.map1.sizeY:
			if vars.map1.Map[self.x,self.y+1]==4 or vars.map1.Map[self.x,self.y+1]==1:
				self.y+=1
		elif num==4 and (self.x-1)<vars.map1.sizeX:
			if vars.map1.Map[self.x-1,self.y]==4 or vars.map1.Map[self.x-1,self.y]==1:
				self.x-=1
		elif num==6 and (self.x+1)<vars.map1.sizeX:
			if vars.map1.Map[self.x+1,self.y]==4 or vars.map1.Map[self.x+1,self.y]==1:
				self.x+=1
		elif num==8 and (self.y-1)<vars.map1.sizeY:
			if vars.map1.Map[self.x,self.y-1]==4 or vars.map1.Map[self.x,self.y-1]==1:
				self.y-=1

	def Draw(self):
		if vars.curses:
			funcs.DrawStringColor(2,self.sprite,x=self.x,y=self.y,bold=True,noclear=False)
		if self.isplayer:
			vars.map1.RedrawAll(1,pos=(self.x,self.y))
			#for dist in range(3):
			xdist=-2
			ydist=-2
			while ydist<=2:
				while xdist<=2:
					if xdist==0 and ydist==0:
						pass
					else:
						if vars.map1.Map[self.x+xdist,self.y+ydist]==1: funcs.DrawString('.',x=self.x+xdist,y=self.y+ydist,noclear=False)
					#if vars.map1.Map[self.x+dist,self.y-1]==1: funcs.DrawString('.',x=self.x+dist,y=self.y-1,noclear=False)
					#if not tdist==0:
					#	if vars.map1.Map[self.x+dist,self.y]==1: funcs.DrawString('.',x=self.x+dist,y=self.y,noclear=False)
					#if vars.map1.Map[self.x+dist,self.y+1]==1: funcs.DrawString('.',x=self.x+dist,y=self.y+1,noclear=False)
					#if xdist<2:
					xdist+=1
				if xdist>=2:
					xdist=-2
				ydist+=1

	def Level(self,value=1):
		self.level+=value
	
	def HasChild(self,thefather=vars.VOID):
		child=Character(mother=self,father=thefather)
		self.children.append(child)
		funcs.DrawString(self.name+' ('+str(self.id)+')'+' gives birth to '+child.name+' ('+str(child.id)+')')
		return child
	
	def GiveItem(self,item):
		self.inventory.append(item)
	
	def ShowStats(self):
		funcs.DrawString('Name: \t\t'+self.name)
		funcs.DrawString('Race: \t\t'+self.race)
		funcs.DrawString('Gender: \t'+self.gender)
		#print 'Age: \t\t'+str(self.age)
		#print 'Level: \t\t'+str(self.level)
		funcs.DrawString('Skills:')
		for entry in self.skills:
			funcs.DrawString('\t'+entry)
		funcs.DrawString('Diseases:')
		for entry in self.diseases:
			funcs.DrawString('\t'+entry)
		funcs.DrawString("MaleHuman: "+str(self.Self_SocialMaleHuman))
		funcs.DrawString("FemaleHuman: "+str(self.Self_SocialFemaleHuman))
		funcs.DrawString("MaleElf: "+str(self.Self_SocialMaleElf))
		funcs.DrawString("FemaleElf: "+str(self.Self_SocialFemaleElf))
