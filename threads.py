import threading
import time
import vars
import functions as funcs

#Input
class PlayerInput(threading.Thread):
	def run(self):
		while vars.running:
			vars.player.GetInput()
			#vars.player.Draw()