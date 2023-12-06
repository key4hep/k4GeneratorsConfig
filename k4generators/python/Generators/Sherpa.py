class sherpa():
	"""Sherpa class"""
	def __init__(self,procinfo):
		self.name = "Sherpa"
		self.version = "x.y.z"
		self.procinfo = procinfo
		self.ext = "dat"
		self.file = ""
		self.outdir = procinfo.get("OutDir")+"/Sherpa"
		self.outfile = '{0}/Run_{1}.{2}'.format(self.outdir, 
												self.procinfo.get("procname"), 
												self.ext)

	def WriteRun(self):
		self.run = "(run){\n"
		#Set the beams
		ENG = self.procinfo.get("sqrts")/2.
		self.run += " BEAM_1 {0}; BEAM_ENERGY_1 {1}\n".format(self.procinfo.GetBeamFlavour(2),ENG)
		self.run += " BEAM_2 {0}; BEAM_ENERGY_2 {1}\n".format(self.procinfo.GetBeamFlavour(1),ENG)
		self.run += " MODEL {0};\n".format(self.procinfo.get("Model"))
		if self.procinfo.get("ISRMode"):
			self.run += " PDF_LIBRARY {0};\n".format("PDFESherpa")
		else:
			self.run += " PDF_LIBRARY {0};\n".format("None")
		self.run += " EVENTS {0};\n".format(self.procinfo.get("Events"))
		self.run +="\n\n"
		self.run +=" # Add Particle data\n"
		for p in self.procinfo.GetDataParticles():
			for attr in dir(p):
				if not callable(getattr(p, attr)) and not attr.startswith("__"):
					name = self.IsSherpaParticleData(attr)
					if name is not None:
						value = getattr(p, attr)
						data=" {0}[{1}] {2};\n".format(name, p.get("pdg_code"), value)
						self.run += data


	def WriteProcess(self):
		self.ptext = "(processes){\n"
		self.ptext += "  Process {} -> {};".format(self.procinfo.GetInitialPDG(), 
												self.procinfo.GetFinalPDG())
		self.ptext +="\n"
		self.ptext +="  Order ({},{});\n".format(self.procinfo.GetQCDOrder(),
											self.procinfo.GetQEDOrder())
		self.ptext +="  End process;\n"


	def WriteFile(self):
		self.WriteRun()
		self.WriteProcess()
		self.ptext += "}(processes)\n\n"
		self.run += "}(run)\n\n"
		self.file=self.run+self.ptext
		with open(self.outfile,"w+") as file:
			file.write(self.file)

	def IsSherpaParticleData(self, d):
		name=None
		if d=="mass":
			name="MASS"
		if d=="width":
			name = "WIDTH"
		return name