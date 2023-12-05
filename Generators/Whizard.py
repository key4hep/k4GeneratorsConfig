import Particles


class whizard():
	"""Whizard class"""
	def __init__(self,procinfo):
		self.name = "Whizard"
		self.version = "x.y.z"
		self.procinfo = procinfo
		self.ext = "sin"
		self.file = ""
		self.outdir = procinfo.get("OutDir")+"/Whizard"
		self.outfile = '{0}/Run_{1}.{2}'.format(self.outdir, 
												self.procinfo.get("procname"), 
												self.ext)


	def WriteProcess(self):
		self.whizBeam1 = self.PdgToWhizard(self.procinfo.GetBeamFlavour(1))
		self.whizBeam2 = self.PdgToWhizard(self.procinfo.GetBeamFlavour(2))
		self.finalstate = ""
		for p in self.procinfo.GetFinalPDGList():
			self.finalstate+=self.PdgToWhizard(p)
			if p is not self.procinfo.GetFinalPDGList()[-1]:
				self.finalstate+=", "
		self.process = "model = {0}\n".format(self.procinfo.get("Model"))
		if self.procinfo.get("ISRMode"):
			self.process += "?isr_handler =  {0}\n".format("true")
			self.process += "beams = {0},  {1} => isr,isr\n".format(self.whizBeam1,self.whizBeam2)
			isrmass = Particles.GetParticle(self.procinfo.GetBeamFlavour(1)).mass
			self.process += "isr_mass = {}".format(isrmass)
			# print(Particles.GetParticle(11).mass)
		else:
			self.process += "?isr_handler =  {0}\n".format("false")
		self.process += "n_events = {0}\n".format(self.procinfo.get("Events"))
		self.process += " sqrts = {0} GeV\n".format(self.procinfo.get("sqrts"))
		self.process += "process proc = {0}, {1} => {2}\n".format(self.whizBeam1,self.whizBeam2,self.finalstate)
		for p in self.procinfo.GetDataParticles():
			for attr in dir(p):
				if not callable(getattr(p, attr)) and not attr.startswith("__"):
					name = self.IsWhizardParticleData(attr)
					if name is not None:
						value = getattr(p, attr)
						if name=="MASS":
							# Have to remove +- for particles/antiparticles
							pname = self.PdgToWhizard(p.get("pdg_code"))
							replac= ["+", "-", "1", "2", "3"]
							for r in replac: 	
								pname = pname.replace(r, "")
							data = "m{0} = {1}\n".format(pname,value)
							self.process += data
						# print(p.get("pdg_code"), name ,value)

	def WriteIntegrate(self):
		self.intgrate = "simulate (proc) { iterations = 5:5000}"


	def WriteFile(self):
		self.WriteProcess()
		self.process +="compile\n"
		self.WriteIntegrate()
		# self.ptext += "}(processes)\n"
		# self.run += "}(run)\n"
		self.file=self.process+self.intgrate
		with open(self.outfile,"w+") as file:
			file.write(self.file)
		# # print(self.file)

	def IsWhizardParticleData(self, d):
		name=None
		if d=="mass":
			name="MASS"
		if d=="width":
			name = "WIDTH"
		return name

	def PdgToWhizard(self, pdg):
		apdg = abs(pdg)
		if type(pdg) is int:
			if apdg>=11 and apdg<=16:
				if pdg>0:
					if pdg%2==0: #Neutrinos
						return "n{}".format((apdg-11)// 2 + 1)
					else: 
						return "e{}".format((apdg-11)// 2 + 1)
				else:
					if pdg%2==0: #Neutrinos
						return "N{}".format((apdg-11)// 2 + 1)
					else:
						return "E{}".format((apdg-11)// 2 + 1)
			elif apdg > 20:
				if pdg == 23:
					return "Z"
				elif pdg == 25:
					return "H"
				elif pdg == 24:
					return "W-"
				elif pdg == -24:
				 	return "W+"
			elif apdg <= 6:
				return self.WhizardQuarks(pdg)
				

			else:
				return "Cant find whizard id for pdg {}".format(pdg)

	def WhizardQuarks(self,pdg):
		apdg = abs(pdg)
		if apdg==1:
			q = "d"
		elif apdg==2:
			q="u"
		if apdg==3:
			q = "s"
		elif apdg==4:
			q="c"
		if apdg==5:
			q = "b"
		elif apdg==6:
			q="t"
		if pdg < 0:
			return q.capitalize()
		else:
			return q 

	# def SetWhizardMass(self):
