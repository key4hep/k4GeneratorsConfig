import Particles
import WhizardProcDB
import os, stat

class Whizard:
	"""Whizard class"""
	def __init__(self, procinfo):
		self.name = "Whizard"
		self.version = "x.y.z"
		self.procinfo = procinfo
		self.ext = "sin"
		self.file = ""
		self.outdir = f"{procinfo.get('OutDir')}/Whizard"
		self.outfileName = f"Run_{self.procinfo.get('procname')}.{self.ext}"
		self.outfile = f"{self.outdir}/{self.outfileName}"

		self.procDB = WhizardProcDB.WhizardProcDB(self.procinfo)

		self.executable  = "whizard"
		self.key4hepfile = f"{self.outdir}/Run_{self.procinfo.get('procname')}.sh"

	def write_process(self):
		self.whiz_beam1 = self.pdg_to_whizard(self.procinfo.get_beam_flavour(1))
		self.whiz_beam2 = self.pdg_to_whizard(self.procinfo.get_beam_flavour(2))
		self.finalstate = ", ".join(map(self.pdg_to_whizard, self.procinfo.get_final_pdg_list()))

		self.process = f"model = {self.procinfo.get('model')}\n"

		self.process += f"seed = {self.procinfo.get_rndmSeed()}\n"

		if self.procinfo.get("isr_mode"):
			self.add_process_option("?isr_handler", "true")
			self.process += f"beams = {self.whiz_beam1}, {self.whiz_beam2} => isr,isr\n"
			isrmass = Particles.GetParticle(self.procinfo.get_beam_flavour(1)).mass
			self.add_process_option("isr_mass", isrmass)
		else:
			self.add_process_option("?isr_handler", "false")
		self.add_process_option("n_events", self.procinfo.get("events"))
		self.add_process_option("sqrts", self.procinfo.get("sqrts"))
		self.process += f"process proc = {self.whiz_beam1}, {self.whiz_beam2} => {self.finalstate}\n"
		if self.procinfo.get("decay"):
			self.add_decay()

		for p in self.procinfo.get_data_particles():
			for attr in dir(p):
				if not callable(getattr(p, attr)) and not attr.startswith("__"):
					name = self.is_whizard_particle_data(attr)
					if name is not None:
						value = getattr(p, attr)
						pname = self.pdg_to_whizard(p.get("pdg_code"))
						replac = ["+", "-", "1", "2", "3"]
						for r in replac:
							pname = pname.replace(r, "")
						if name == "MASS":
							dname = f"m{pname}"
						elif name == "WIDTH":
							dname = f"w{pname}"

						self.add_process_option(dname, value)
		if self.procinfo.get("output_format") != "evx":
			self.add_process_option("sample_format", self.procinfo.get("output_format"))
			self.add_process_option("?write_raw","false")
		self.process += self.procDB.write_DBInfo()

	def add_decay(self):
		decay_opt = self.procinfo.get("decay")
		decays=""
		for key in decay_opt:
			if str(key) not in self.procinfo.get_final_pdg():
				print("Particle {0} not found in main process. Decay not allowed".format(key))
			parent = self.pdg_to_whizard(key)
			decays += f" process decay{parent} = {parent} => "
			for child in decay_opt[key]:
				if child is decay_opt[key][-1]:
					decays += self.pdg_to_whizard(child) + ""
				else:
					decays += self.pdg_to_whizard(child) + ", "

			decays +="\n"
		self.process += decays


	def write_integrate(self):
		self.integrate = "simulate (proc) { iterations = 5:5000}"

	def add_process_option(self, key, value):
		if key in self.process:
			print(f"{key} has already been defined in {self.name}.")
			return
		self.process += f" {key} = {value}\n"

	def write_file(self):
		self.write_process()
		self.process += "compile\n"
		self.write_integrate()
		self.file = f"{self.process}{self.integrate}"
		with open(self.outfile, "w+") as file:
			file.write(self.file)

	def write_key4hepfile(self,shell,config):
		key4hepRun = shell+"\n"
		key4hepRun += config+"\n"
		key4hepRun += self.executable+" "+self.outfileName+"\n"
		key4hepRun += f"$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc {self.procinfo.get('procname')}.edm4hep\n"
		with open(self.key4hepfile, "w+") as file:
			file.write(key4hepRun)
		os.chmod(self.key4hepfile, os.stat(self.key4hepfile).st_mode | stat.S_IEXEC)

	def is_whizard_particle_data(self, d):
		name = None
		if d == "mass":
			name = "MASS"
		if d == "width":
			name = "WIDTH"
		return name

	def pdg_to_whizard(self, pdg):
		apdg = abs(pdg)
		if type(pdg) is int:
			if 11 <= apdg <= 16:
				lepton_type = "e" if pdg%2==1 else "n"
				flavor = (apdg - 11) // 2 + 1
				if pdg < 0:
					lepton_type=lepton_type.capitalize() 
				return f"{lepton_type}{flavor}"
			elif apdg > 20:
				particle_mapping = {23: "Z", 25: "H", 24: "W-", -24: "W+"}
				return particle_mapping.get(pdg, f"Cant find whizard id for pdg {pdg}")
			elif apdg <= 6:
				return self.whizard_quarks(pdg)
			else:
				return f"Cant find whizard id for pdg {pdg}"

	def whizard_quarks(self, pdg):
		quark_mapping = {1: "d", 2: "u", 3: "s", 4: "c", 5: "b", 6: "t"}
		q = quark_mapping.get(abs(pdg), "")
		return q.capitalize() if pdg > 0 else q
