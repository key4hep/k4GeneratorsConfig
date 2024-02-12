class WhizardProcDB:
	"""WhizardProcDB class"""
	def __init__(self, process):
		self.process = process

	def write_DBInfo(self):
		out = ""
		if ( self.process.get('procname') == "Difermion" ):
			out += self.write_Difermion()
		elif ( self.process.get('procname') == "ZH" ):
			out += self.write_ZH()

		return out

	def write_Difermion(self):
		out = ""
		out += " mW = 80.419 GeV\n"
		out += " wW = 2.0476 GeV\n"
		return out

	def write_ZH(self):
		out  = "?resonance_history = true\n" 
		out += "resonance_on_shell_limit = 16\n"
		out += "resonance_on_shell_turnoff = 2\n"
		out += "resonance_on_shell_turnoff = 2\n"
		return out


