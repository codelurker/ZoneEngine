#!/usr/bin/env python
#New ALife

class ALife(object):
	def __init__(self):
		#Public range
		self.name=['','']
		self.gender='null'
		self.race='null'
		self.age=0
		self.birthplace=None
		
		#Stat range
		self.strength=0
		self.dexterity=0

		#Private range
		self._id=0
		
		self.debug_show_stats()

class NPC(ALife):
	def debug_show_stats(self):
		print self.name
		print self.gender
		print self.race
		print self.age
		print self.birthplace
		print self.strength
		print self.dexterity
		print self._id

adam = NPC()
