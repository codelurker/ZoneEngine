import threading
import vars
import functions as funcs


#Input
class PlayerInput(threading.Thread):
	def run(self):
		while vars.running:
			vars.player.GetInput()
			vars.player.Draw()
			funcs.DrawStringColor(3,vars.TOPBAR,bold=True)
