#!/usr/bin/env python
#New ALife

class ALife(object):
	def __init__(self):
		#Public range
		self.name=['','']
		self.gender=''	
		self.race=''
		self.age=0
		self.birthplace=None
		
		#Stat range
		self.strength=0
		self.dexterity=0

		#Private range
		self._id=0
