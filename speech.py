import re,random
random.seed()

#Speech banks
#included in source for now
greeting_positive=[]
greeting_neutral=[]
greeting_negative=[]

status_positive=[]
status_neutral=[]
status_negative=[]

greeting_postive_no_connection=[]
greeting_neutral_no_connection=[]
greeting_negative_no_connection=[]

characters=00000

class thinkers(object):
	def getID():
		#return self.id.partition('.')[2]
		return self.id

class dummy(thinkers):
	def __init__(self,name,gender,race):
		self.name=name
		self.gender=gender
		self.race=race
		self.Self_SocialFemaleHuman=80
		self.Self_SocialMaleHuman=80
		self.brain=[]
		global characters
		self.id='char.'+str(characters)
		characters+=1
	def learn(self,string,type):
		self.brain.append(Knowledge(string,type))
	def remember(self,what):
		for thought in self.brain:
			if thought.string.count(what)>0:
				return thought

class object(thinkers):
	def __init__(self):
		self.id='object.00001'
	
class Knowledge:
	def __init__(self,string,type):
		self.string=string
		self.type=type

a = dummy('Adam','Male','Human')
b = dummy('Eve','Female','Human')

b.learn('%char.00000% has %obj.00001%','knowledge.direct')
print b.remember('char.00000').string

test_object=object()

class SpeechClass(object):
	def get(self):
		return self.line
		
class Greeting(SpeechClass):
	def __init__(self,line,align,question=False,action=True):
		self.line=line
		self.align=align
		self.type='greeting'
		self.question=question

class Status(SpeechClass):
	def __init__(self,line,align,question=False,action=True):
		self.line=line
		self.align=align
		self.type='status'
		self.question=question

class Ignore(SpeechClass):
	def __init__(self,line,align,question=False,action=True):
		self.line=line
		self.align=align
		self.type='ignore'
		self.question=question

greeting_positive.append(Greeting('Good %timeofday%, %other.name%.',1))
greeting_positive.append(Greeting('How are you, %other.name%?',1,question=True))
greeting_neutral.append(Greeting('Hello, %other.name%.',0))
greeting_negative.append(Ignore('<%self.name% ignores you>',0,action=True))

greeting_postive_no_connection.append(Greeting('Hello.',0))
greeting_postive_no_connection.append(Greeting('<%self.name% nods>',0,action=True))
greeting_neutral_no_connection.append(Greeting('<%self.name% looks in your direction>',0,action=True))
greeting_negative_no_connection.append(Ignore('<%self.name% ignores you>',0,action=True))

status_positive.append(Status('I\'m %self.status%, %other.name%.',1))
status_neutral.append(Status('%self.status%, %other.name%.',1))
status_negative.append(Status('That doesn\'t concern you.',1))

class Conversation:
	def __init__(self,a,b,start,goal):
		self.a=a
		self.b=b
		self.start=start
		self.goal=goal
		self.turn='a'
		self.run()
	def run(self):
		self.done=False
		if self.start=='greeting':
			position=GetPosition(self.a,self.b)
			resp=FindGreeting(position)
			RenderResponse(self.a,self.b,resp)
		while self.done==False:
			if resp.type=='greeting':
				if resp.question==True:
					position=GetPosition(self.b,self.a)
					resp=FindStatus(position)
					RenderResponse(self.b,self.a,resp)
			options=GetDialogOptions(self.a,self.b)
			resp=GetUserInput(options,a,b)
			self.done=True
				
def GetDialogOptions(a,b):
	options=['','Heard anything interesting?','I need some help.']
	dialog= ['','rumors','help']
	return options,dialog

def GetUserInput(options,a,b):
	z=0
	for option in options[0]:
		if z!=0: print str(z)+') '+option
		z+=1
	choice=raw_input(":")
	resp=options[1][int(choice)]
	position=GetPosition(a,b)
	if resp=='rumors':
		return RenderResponse(a,b,FindRumor(position))

def GetPosition(a,b):
	#a = you
	#b = them
	if a.race==b.race:
		if b.race=='Human':
			if a.gender==b.gender:
				if a.gender=='Male':
					return a.Self_SocialFemaleHuman
				else:
					return a.Self_SocialMaleHuman
			else:
				if a.gender=='Male':
					return a.Self_SocialFemaleHuman
				else:
					return a.Self_SocialMaleHuman
		else:
			if a.gender==b.gender:
				if a.gender=='Male':
					return a.Self_SocialFemaleElf
				else:
					return a.Self_SocialMaleElf
			else:
				if a.gender=='Male':
					return a.Self_SocialFemaleElf
				else:
					return a.Self_SocialMaleElf

def FindGreeting(value):
	if value>=60:
		return greeting_positive[random.randint(0,len(greeting_positive)-1)]
	elif value>40 and value<60:
		return greeting_neutral[0]
	elif value<=40:
		return greeting_negative[0]

def FindStatus(value):
	if value>=60:
		return status_positive[random.randint(0,len(status_positive)-1)]
	elif value>40 and value<60:
		return status_neutral[0]
	elif value<=40:
		return status_negative[0]

def FindRumor(value):
	if value>=60:
		return status_positive[random.randint(0,len(status_positive)-1)]
	elif value>40 and value<60:
		return status_neutral[0]
	elif value<=40:
		return status_negative[0]

def RenderResponse(a,b,string):
	line=string.get()
	temp=a.name+': '+line
	found=re.findall('%(.*?)%', line)
	for entry in found:
		temp=temp.replace(entry,GetVariable(a,b,entry))
	temp=temp.replace('%','')
	print temp

def GetVariable(a,b,entry):
	if entry=='timeofday':
		return 'afternoon'
	elif entry=='other.name':
		return b.name
	elif entry=='self.status':
		return 'Fine'

Conversation(a,b,'greeting','Follow')