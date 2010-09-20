import vars,random,classes
try:
	from unicurses import *
	init_pair(1, COLOR_GREEN, COLOR_BLACK)
	init_pair(2, COLOR_CYAN, COLOR_BLACK)
	init_pair(3, COLOR_RED, COLOR_BLACK)
except:
	pass

random.seed()

def ID_Give():
	vars.ID+=1
	return vars.ID

def Disease_BornWith():
	diseases=[]
	diseases.append(vars.disease_listName[random.randint(0, len(vars.disease_listName)-1)])
	return diseases

def Parents_GetDiseases(mother,father):
	diseases=[]
	return diseases

def Parents_GetRace(mother,father):
	return "Human"

def Parents_GetExperience(mother,father):
	return 0

def Parents_MakeChild(mother1,father1):
	child=classes.Character(mother=mother1,father=father1)
	mother1.children.append(child)
	father1.children.append(child)
	DrawString(mother1.name+' ('+str(mother1.id)+')'+' gives birth to '+child.name+' ('+str(child.id)+')')
	return child

def Parents_BirthGender(mother,father):
	rannum=int(random.choice('01'))
	if rannum==0:
		return "Male"
	else:
		return "Female"

def Parents_GetSkillsFromParents(mother,father):
	skills=[]
	return skills

def Parents_GetSkillsFromRace(race):
	skills=[]
	return skills

def Race_GetNameFromGender(race,gender):
	if race=='Human':
		if gender=="Male":
			return random.sample(vars.malename,1)[0]
		else:
			return random.sample(vars.femalename,1)[0]
	else:
		if gender=="Male":
			return random.sample(vars.malename,1)[0]
		else:
			return random.sample(vars.femalename,1)[0]

def Self_GetSocial(character):
	if character.race=="Human":
		character.Self_SocialMaleHuman+=10
		character.Self_SocialFemaleHuman+=10
		character.Self_SocialMaleElf-=15
		character.Self_SocialFemaleElf-=15
		if character.gender=="Male":
			character.Self_SocialMaleHuman+=10
			character.Self_SocialFemaleHuman-=5
			character.Self_SocialMaleElf+=5
			character.Self_SocialFemaleElf-=10
		else:
			character.Self_SocialMaleHuman-=5
			character.Self_SocialFemaleHuman+=10
			character.Self_SocialMaleElf-=10
			character.Self_SocialFemaleElf+=5
	else:
		character.Self_SocialMaleHuman-=15
		character.Self_SocialFemaleHuman-=15
		character.Self_SocialMaleElf+=10
		character.Self_SocialFemaleElf+=10
		if character.gender=="Male":
			character.Self_SocialMaleHuman+=5
			character.Self_SocialFemaleHuman-=10
			character.Self_SocialMaleElf+=10
			character.Self_SocialFemaleElf-=5
		else:
			character.Self_SocialMaleHuman-=10
			character.Self_SocialFemaleHuman+=5
			character.Self_SocialMaleElf-=5
			character.Self_SocialFemaleElf+=10

def Self_PutOnMap(character):
	for y1 in range(vars.map1.sizeY):
			for x1 in range(vars.map1.sizeX):
				if vars.map1.Map[x1,y1]==4:
					if random.randint(1,20)<3:
						character.x=x1
						character.y=y1
						return

def FindInList(what,list):
	i=0
	for entry in list:
		if entry==what:
			return i
		i+=1

def DrawList(list):
	num=1
	for entry in list:
		vars.screen.addstr(1, num, str(entry))
		if num==10:
			num+=1
		else:
			num=1

def ClearLine(start,dist,y):
	for a in range(dist):
		mvaddstr(y,start+a," ")

def DrawString(string1,bold=False,x=0,y=0,noclear=True):
	if vars.curses:
		if noclear: ClearLine(len(string1),80,y)
		if bold==True: attron(A_BOLD)
		mvaddstr(y,x,string1)
		if bold==True: attroff(A_BOLD)
	else:
		print string1

def DrawStringColor(color,string1,bold=False,x=0,y=0,noclear=True):
	if vars.curses:
		if noclear: ClearLine(len(string1),80,y)
		if bold==True: attron(A_BOLD)
		attron(COLOR_PAIR(color))
		mvaddstr(y,x,string1)
		attroff(COLOR_PAIR(color))
		if bold==True: attroff(A_BOLD)
	else:
		print string1
