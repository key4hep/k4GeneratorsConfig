import yaml
import os



class Input:
	"""Class for loading yaml files"""
	def __init__(self, file):
		self.file = file
		self.settings = None
		if not os.path.isfile(file):
			raise FileNotFoundError(file)
		else:
			self.LoadFile()

	def LoadFile(self):
		with open(self.file, 'r') as file:
			self.settings = yaml.safe_load(file)

	def IsEmpty(self, key):
		if key in self.settings:
			return False
		return True

	def Generators(self):
		if self.IsEmpty("Generators"):
			raise ValueError("No Generators set!")
		self.gens = self.settings["Generators"]
		return self.gens

	def GetProcesses(self):
		# print(self.settings["Processess"])
		if len(self.settings["Processess"])==0:
			raise ValueError("No processes defined!")
		else:
			return 	self.settings["Processess"]

	def GetSqrtS(self):
		try:
			return self.settings["SqrtS"]
		except:
			raise ValueError("SqrtS not defined")

	def GetParticleData(self):
		if not self.IsEmpty("ParticleData"):
			return self.settings["ParticleData"]

	def GetModel(self):
		if self.IsEmpty("Model"):
			return "SM"
		else:
			return self.get("Model")

	def GetEventNumber(self):
		if self.IsEmpty("Events"):
			return 0
		else:
			return self.get("Events")

	def GetISRMode(self):
		if self.IsEmpty("ISRMode"):
			return 0
		else:
			return self.get("ISRMode")

	def get(self, key):
		try:
			return self.settings[key]
		except:
			return ValueError