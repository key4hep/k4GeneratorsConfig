class WhizardProcDB:
	"""WhizardProcDB class"""
	def __init__(self, process):
		self.process = process
		self.out = ""

	def write_DBInfo(self):
		if ( self.process.get('procname') == "Difermion" ):
			self.out += self.write_Difermion()
		elif ( self.process.get('procname') == "ZH" ):
			self.out += self.write_ZH()

	def write_Difermion(self):
		self.out += "mW = 80.419 GeV\n"
		self.out += "wW = 2.0476 GeV\n"
		return self.out

	def write_ZH(self):
		self.out += "?resonance_history = true\n" 
		self.out += "resonance_on_shell_limit = 16\n"
		self.out += "resonance_on_shell_turnoff = 2\n"
		self.out += "resonance_on_shell_turnoff = 2\n"
		return self.out

	def get_out(self):
		return self.out

	def remove_option(self,opt):
		lines = self.out.split("\n")
		filter_lines = [line for line in lines if opt not in line]
		self.out = "\n".join(filter_lines)
