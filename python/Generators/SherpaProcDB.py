class SherpaProcDB:
	"""SherpaProcDB class"""
	def __init__(self, process):
		self.process = process
		self.runout = ""
		self.procout = ""

	def write_DBInfo(self):
		if ( self.process.get('procname') == "Difermion" ):
			self.write_Difermion()
		elif ( self.process.get('procname') == "ZH" ):
			self.write_run_ZH()

		return self.runout

	def write_Difermion(self):
		self.runout = ""

	def get_run_out(self):
		return self.runout

	def get_proc_out(self):
		return self.procout

	def write_run_ZH(self):
		self.runout  = "WIDTH[25] 0\n" 
		self.runout += "WIDTH[23] 0\n"


