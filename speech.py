import re

#Speech banks
#included in source for now
greeting_postive=['Good %timeofday%, %other.name%.']
greeting_neutral=['Hello, %other.name%.']
greeting_negative=['%ignore%']

class dummy:
	def __init__(self,name):
		self.name=name

a = dummy('Adam')
b = dummy('Eve')

class Conversation:
	def __init__(self,a,b):
		self.weight=0
		self.a=a
		self.b=b

def Greeting(a,b):
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
	temp=a.name+': '+string
	found=re.findall('%(.*?)%', string)
	for entry in found:
		temp=temp.replace(entry,GetVariable(a,b,entry))
	temp=temp.replace('%','')
	print temp

def GetVariable(a,b,entry):
	if entry=='timeofday':
		return 'afternoon'
	elif entry=='other.name':
		return b.name

RenderResponse(a,b,greeting_postive[0])
	