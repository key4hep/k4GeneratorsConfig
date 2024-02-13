class MadgraphProcDB:
	"""MadgraphProcDB class"""
	def __init__(self, process):
		self.process = process
		self.runout = ""
		self.procout = ""

	def write_DBInfo(self):
		if ( self.process.get('procname') == "Difermion" ):
			self.runout += self.write_Difermion()
		elif ( self.process.get('procname') == "ZH" ):
			self.runout += self.write_run_ZH()

	def write_Difermion(self):
		out = ""
		return out


	def get_run_out(self):
		return self.runout

	def get_proc_out(self):
		return self.procout

	def write_run_ZH(self):
		out  = "set WZ 0\n" 
		out += "set WH 0\n"
		return out


	def remove_option(self,opt):
		lines = self.runout.split("\n")
		filter_lines = [line for line in lines if opt not in line]
		self.runout = "\n".join(filter_lines)
