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

class dummy:
	def __init__(self,name,gender,race):
		self.name=name
		self.gender=gender
		self.race=race
		self.Self_SocialFemaleHuman=80
		self.Self_SocialMaleHuman=50
		
a = dummy('Adam','Male','Human')
b = dummy('Eve','Female','Human')

class SpeechClass(object):
	def get(self):
		#print self.line+' ('+str(self.align)+')'
		return self.line
		
class Greeting(SpeechClass):
	def __init__(self,line,align,question=False):
		self.line=line
		self.align=align
		self.type='greeting'
		self.question=question

class Status(SpeechClass):
	def __init__(self,line,align,question=False):
		self.line=line
		self.align=align
		self.type='status'
		self.question=question

greeting_positive.append(Greeting('Good %timeofday%, %other.name%.',1))
greeting_positive.append(Greeting('How are you, %other.name%?',1,question=True))
greeting_neutral.append(Greeting('Hello, %other.name%.',0))
greeting_negative.append(Greeting('%ignore%',-1))

status_positive.append(Status('I\'m %status%, %other.name%.',1))
status_neutral.append(Status('%status%, %other.name%.',1))

class Conversation:
	def __init__(self,a,b,type):
		self.a=a
		self.b=b
		self.type=type
		self.start()
		self.turn='a'
	def start(self):
		self.done=False
		if self.type=='greeting':
			position=GetPosition(self.a,self.b)
			resp=FindGreeting(position)
			RenderResponse(self.a,self.b,resp)
			self.turn='b'
		if self.done==False:
			if resp.type=='greeting':
				if resp.question==True:
					position=GetPosition(self.b,self.a)
					resp=FindStatus(position)
					RenderResponse(self.b,self.a,resp)

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
	elif entry=='status':
		return 'Fine'

#RenderResponse(a,b,greeting_positive[0])
Conversation(a,b,'greeting')