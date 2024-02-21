class Selectors():
	"""Selector Class"""
	def __init__(self, name, selector):
		self.name = name
		self.LoadSelector(selector)

	def LoadSelector(self, selector):
		for key,value in selector.items():
			setattr(self, key.lower(), value)
	

	def get_Flavours(self):
		try:
			return getattr(self, "flavour")
		except:
			print(f"No Flavour found in selector {self.name}")

	def get_Max(self):
		try:
			return getattr(self, "max")
		except:
			print(f"No maximum found in selector {self.name}")

	def get_Min(self):
		try:
			return getattr(self, "min")
		except:
			print(f"No minimum found in selector {self.name}")

	def get_MinMax(self):
		return self.get_Min(), self.get_Max()