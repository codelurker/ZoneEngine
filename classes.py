import vars,random
import functions as funcs
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
			print self.name+' is now '+str(self.age)
			self.ticks=0
		if self.age==50:
			del vars.character[funcs.FindInList(self,vars.character)]
			print self.name+' has died. Removing '+str(self.id)
		
		if len(self.children)<2 and self.gender=="Female":
			if random.randint(0,50)<=8:
				child=self.HasChild()
		self.ticks+=1
	
	def Level(self,value=1):
		self.level+=value
	
	def HasChild(self,thefather=vars.VOID):
		child=Character(mother=self,father=thefather)
		self.children.append(child)
		print self.name+' ('+str(self.id)+')'+' gives birth to '+child.name+' ('+str(child.id)+')'
		return child
			
	def ShowStats(self):
		print 'Name: \t\t'+self.name
		print 'Race: \t\t'+self.race
		print 'Gender: \t'+self.gender
		#print 'Age: \t\t'+str(self.age)
		#print 'Level: \t\t'+str(self.level)
		print 'Skills:'
		for entry in self.skills:
			print '\t'+entry
		print 'Diseases:'
		for entry in self.diseases:
			print '\t'+entry
		print "MaleHuman: "+str(self.Self_SocialMaleHuman)
		print "FemaleHuman: "+str(self.Self_SocialFemaleHuman)
		print "MaleElf: "+str(self.Self_SocialMaleElf)
		print "FemaleElf: "+str(self.Self_SocialFemaleElf)