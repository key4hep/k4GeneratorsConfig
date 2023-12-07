from Particles import Particles

class Process():
 # """A standard Process"""
	require_args=['initial', 'final', 'sqrts', 'order', 'procname']

	def __init__(self, initial, final, sqrts, order, procname, params, **options):

		args= (initial, final, sqrts, order,procname)
		if len(initial) != 2:
			raise ValueError("Initial state should have 2 particles not {}".format_map(len(initial)))

		for i, name in enumerate(self.require_args):
			setattr(self, name, args[i])

		for setting in dir(params):
			if "__" not in setting:
				setattr(self, setting, getattr(params, setting))

		for (option, value) in options.items():
			setattr(self, option, value)
		self.parts = []
		self.dataparts = []
		self.init = False
			 

	def ProcessInfo(self):
		self.beam1 = Particles.GetInfo(self.initial[0])
		self.beam2 = Particles.GetInfo(self.initial[1])
		self.finfo = {}
		self.parts.append(self.beam1)
		self.parts.append(self.beam2)
		self.proclabel = "{} {} -> ".format(self.beam1.name, self.beam2.name)
		for p in self.final:
			self.finfo[p] = Particles.GetInfo(p)
			self.proclabel+= self.finfo[p].name
			self.proclabel+= " "
			self.parts.append(self.finfo[p])

	def SetParticleData(self,pdata):
		if pdata is None:
			return
		if self.init:
			return  
		for key, value in pdata.items():
			# print(key,value)
			Particles.SetInfo(key,value)
			self.dataparts.append(Particles.GetInfo(key))
		self.init = True

	def GetBeamFlavour(self, beam):
		if beam > 2 or beam < 0:
			raise ValueError("Beam should be 1 or 2 not {}".format(beam))
		if beam==1:
			return self.beam1.get("pdg_code")
		else:
			return self.beam2.get("pdg_code")

	def GetInitialPDG(self):
		return "{0} {1}".format(self.GetBeamFlavour(0),self.GetBeamFlavour(1))

	def GetFinalPDG(self):
		final=""
		for p in self.finfo:
			final+=" {}".format(p)
		return final
	 
	def GetFinalPDGList(self):
		final=[]
		for p in self.finfo:
			final.append(p)
		return final
	 

	def get(self, name):
		return getattr(self, name)

	def GetArgs(self):
		return self.require_args

	def GetParticles(self):
		return self.parts

	def GetDataParticles(self):
		return self.dataparts

	def GetQCDOrder(self):
		return self.get("order")[1]

	def GetQEDOrder(self):
		return self.get("order")[0]

	def GetOutputFormat(self):
		return self.OutputFormat

	def PrintInfo(self):
		out = "Creating Runcards for {} at {} GeV".format(self.proclabel, self.sqrts)
		print(out)
		print("Particles are defined with the follow parametes")
		for p in self.parts:
			p.PrintInfo()


class ProcessParameters:
	
	def __init__(self,settings):
		self.sqrts = settings.GetSqrtS()
		self.Model = settings.GetModel()
		self.Events = settings.GetEventNumber()
		self.ISRMode = settings.GetISRMode()
		self.OutputFormat = settings.GetOutputFormat()
