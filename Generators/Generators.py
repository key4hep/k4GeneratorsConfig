import Sherpa, Whizard



class generators():
	"""Generator class"""
	def __init__(self, genlist):
		self.gens = genlist

	def SetProcessInfo(self, procinfo):
		self.procinfo = procinfo

	def InitalizeGenerators(self):
		if "Sherpa" in self.gens:
			self.sherpa = Sherpa.sherpa(self.procinfo)
			self.sherpa.WriteFile()
		if "Whizard" in self.gens:
			self.whizard = Whizard.whizard(self.procinfo)
			self.whizard.WriteFile()