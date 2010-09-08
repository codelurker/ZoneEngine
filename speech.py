import re

#Speech banks
#included in source for now
greeting_positive=[]
greeting_neutral=[]
greeting_negative=[]

class dummy:
	def __init__(self,name):
		self.name=name

a = dummy('Adam')
b = dummy('Eve')

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

greeting_positive.append(Greeting('Good %timeofday%, %other.name%.',1))
greeting_positive.append(Greeting('How are you, %other.name%?',1,question=True))
greeting_neutral.append(Greeting('Hello, %other.name%.',0))
greeting_negative.append(Greeting('%ignore%',-1))

class Conversation:
	def __init__(self,a,b,type):
		#self.weight=0
		self.a=a
		self.b=b
		self.type=type
	def start(self,type):
		self.done=False
		self.log=[]
		while not self.done:
			if len(self.log)==0:
				r=Response(type)
				#r.

def GetGreeting(a,b):
	#a = you
	#b = them
	if a.race==b.race:
		if b.race=='Human':
			if a.gender==b.gender:
				if a.gender=='Male':
					FindGreeting(a.Self_SocialFemaleHuman)
				else:
					FindGreeting(a.Self_SocialMaleHuman)
			else:
				if a.gender=='Male':
					FindGreeting(a.Self_SocialFemaleHuman)
				else:
					FindGreeting(a.Self_SocialMaleHuman)
		else:
			if a.gender==b.gender:
				if a.gender=='Male':
					FindGreeting(a.Self_SocialFemaleElf)
				else:
					FindGreeting(a.Self_SocialMaleElf)
			else:
				if a.gender=='Male':
					FindGreeting(a.Self_SocialFemaleElf)
				else:
					FindGreeting(a.Self_SocialMaleElf)

def FindGreeting(value):
	if value>=60:
		return greeting_postive[0]
	elif value>40 and value<60:
		return greeting_neutral[0]
	elif value<=40:
		return greeting_negative[0]

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

RenderResponse(a,b,greeting_positive[0])
	