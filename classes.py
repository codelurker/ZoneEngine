import vars,random
import functions as funcs
from unicurses import *
vars.ID=0

random.seed()

class Void:
	def __init__(self):
		self.x=1
		self.y=1
		self.name="VOID"
vars.VOID=Void()

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
	
	def Tick(self):
		if self.ticks==20:
			self.age+=1
			funcs.DrawString(self.name+' is now '+str(self.age))
			self.ticks=0
		if self.age==50:
			del vars.character[funcs.FindInList(self,vars.character)]
			funcs.DrawString(self.name+' has died. Removing '+str(self.id))
		
		if len(self.children)<2 and self.gender=="Female":
			if random.randint(0,50)<=8:
				child=self.HasChild()

		self.MoveRandomize()
		self.Draw()
		self.ticks+=1

	def MoveRandomize(self,xm=True,ym=True):
		if xm==True:
			mov_x1=random.randint(0,100)
			mov_x=0
			if mov_x1<45:
				mov_x=-1
			else:
				if mov_x1>55:
					mov_x=1
			if mov_x==self.last_x:		
				self.MoveRandomize(xm=True,ym=False)
			else:
				self.last_x=mov_x
				if self.x>0 and self.x<20:
					self.x+=mov_x	
		if ym==True:
			mov_y1=random.randint(0,100)
			mov_y=0
			if mov_y1<45:
				mov_y=-1
			else:
				if mov_y1>55:
					mov_y=1
			if mov_y==self.last_y:
				self.MoveRandomize(xm=False,ym=True)
			else:
				self.last_y=mov_y
				if self.y>0 and self.y<20:
					self.y+=mov_y
		if self.x==0: self.x=1
		if self.y==0: self.y=1
	
	def Draw(self):
		if vars.curses:
			mvaddstr(self.x, self.y, 'O')

	def Level(self,value=1):
		self.level+=value
	
	def HasChild(self,thefather=vars.VOID):
		child=Character(mother=self,father=thefather)
		self.children.append(child)
		funcs.DrawString(self.name+' ('+str(self.id)+')'+' gives birth to '+child.name+' ('+str(child.id)+')')
		return child
			
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
