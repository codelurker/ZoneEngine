#!/usr/bin/env python
#New ALife
import alife_functions

class ALife(object):
	def __init__(self):
		#Public range
		self.name=['','']
		self.gender='null'
		self.race='null'
		self.age=0
		self.birthdate='null'
		self.birthplace=None

		#Private range
		self._id=0			#Used to reference ALife
		
		#Stat range
		self.strength=0
		self.dexterity=0	#Agility/reaction time
		
		#References
		self.first_name=self.name[0]
		self.last_name=self.name[1]

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

adam = NPC()
adam.debug_show_stats()
