#!/usr/bin/env python
#New ALife
import alife_functions
import alife_speech

#General
import functions as funcs
import vars,astar

try:
	from unicurses import *
except:
	pass

class ALife(object):
	def __init__(self):
		#Public range
		self.name=['','']
		self.gender='null'
		self.race='null'
		self.mother=None
		self.father=None
		self.age=0
		self.birthdate='null'
		self.birthplace=None

		#Private range
		self._id=0			#Used to reference ALife
		self._maxticks=3
		self._ticks=self._maxticks
		self._isplayer=False
		vars.character.append(self)
		
		#Sub-Private range
		self.x=10
		self.y=15
		self.inventory=[]
		
		#Stat range
		self.strength=0
		self.dexterity=0	#Agility/reaction time
		
		#AI range
		self.Self_SocialFemaleHuman=50
		self.Self_SocialFemaleElf=50
		self.Self_SocialMaleHuman=50
		self.Self_SocialMaleElf=50
		
		#A* range
		self.OnPath=False
		self.CurrentPath=None
		self.CurrentPath_Number=0
		
		#Visual range
		self.sprite='@'
		
		#References
		self.first_name=self.name[0]
		self.last_name=self.name[1]

	def Tick(self):
		if self._ticks==0:
			#Actions
			self.Move()
			self._ticks=self._maxticks
		else:
			self._ticks-=1
		
		self.Draw()

	def Move(self):
		if not self._isplayer:
			if self.OnPath==True:
				if self.CurrentPath_Number<len(self.CurrentPath):
					self.x=self.CurrentPath[self.CurrentPath_Number][0]
					self.y=self.CurrentPath[self.CurrentPath_Number][1]
					self.CurrentPath_Number+=1
					#pass
			else:
				self.CurrentPath=astar.MakePath(self.x,self.y,10,10)
				self.CurrentPath_Number=0
				self.OnPath=True
				
	def Draw(self):
		funcs.DrawStringColor(2,self.sprite,x=self.x,y=self.y,bold=True,noclear=False)
		if self._isplayer:
			vars.map1.RedrawAll(1,pos=(self.x,self.y))
			xdist=-2
			ydist=-2
			while ydist<=2:
				while xdist<=2:
					if xdist==0 and ydist==0:
						pass
					else:
						if self.y+ydist<vars.map1.sizeY and self.x+xdist<vars.map1.sizeX:
							if vars.map1.Map[self.x+xdist,self.y+ydist]==1:
								attron(COLOR_PAIR(1))
								funcs.DrawString('.',x=self.x+xdist,y=self.y+ydist,noclear=False)
								attroff(COLOR_PAIR(1))
								noutrefresh(vars.screen)
					xdist+=1
				if xdist>=2:
					xdist=-2
				ydist+=1

class NPC(ALife):
	def debug_show_stats(self):
		print self.name
		print self.gender
		print self.race
		print self.age
		print self.birthdate
		print self.birthplace
		print self.strength
		print self.dexterity
		print self._id

class Player(NPC,ALife):
	def GetInput(self):
		key=wgetch(vars.screen)
		if key==KEY_UP:
			if vars.map1.Map[self.x,self.y-1]==4 or vars.map1.Map[self.x,self.y-1]==1:
				if self.y>0:
					vars.map1.DrawPos(vars.player.x,vars.player.y)
					self.y-=1
					if self.y>10:
						vars.scroll_y-=1
			if vars.paused==True:
				vars.paused=False
		elif key==KEY_DOWN:
			if vars.map1.Map[self.x,self.y+1]==4 or vars.map1.Map[self.x,self.y+1]==1:
				if self.y<vars.map1.sizeY-2:
					vars.map1.DrawPos(vars.player.x,vars.player.y)
					self.y+=1
					if self.y>10:
						vars.scroll_y+=1
			if vars.paused==True:
				vars.paused=False
		elif key==KEY_LEFT:
			if vars.map1.Map[self.x-1,self.y]==4 or vars.map1.Map[self.x-1,self.y]==1:
				if self.x>0:
					vars.map1.DrawPos(vars.player.x,vars.player.y)
					self.x-=1
			if vars.paused==True:
				vars.paused=False
		elif key==KEY_RIGHT:
			if vars.map1.Map[self.x+1,self.y]==4 or vars.map1.Map[self.x+1,self.y]==1:
				if self.x<vars.map1.sizeX-2:
					vars.map1.DrawPos(vars.player.x,vars.player.y)
					self.x+=1
			if vars.paused==True:
				vars.paused=False
		elif key==ord('i'):
			if vars.paused==True:
				vars.paused=False
			else:
				vars.paused=True
			a=1
			funcs.DrawStringColor(2,'Inventory',x=0,y=0)
			for item in self.inventory:
				funcs.DrawString(str(a)+') '+item.name,y=a)
				a+=1
		elif key==ord('q'):
			vars.running=False
		
#adam = NPC()
#adam.debug_show_stats()
