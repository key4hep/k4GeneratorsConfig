import os, stat

class Sherpa:
	"""Sherpa class"""
	def __init__(self, procinfo):
		self.name = "Sherpa"
		self.version = "x.y.z"
		self.procinfo = procinfo
		self.ext = "dat"
		self.file = ""
		self.outdir = f"{procinfo.get('OutDir')}/Sherpa"
		self.outfileName = f"Run_{self.procinfo.get('procname')}.{self.ext}"
		self.outfile = f"{self.outdir}/{self.outfileName}"

		self.executable  = "Sherpa -f"
		self.key4hepfile = f"{self.outdir}/Run_{self.procinfo.get('procname')}.sh"

	def write_run(self):
		self.run = "(run){\n"
		ENG = self.procinfo.get("sqrts") / 2.
		beam1_pdg = self.procinfo.get_beam_flavour(1)
		beam2_pdg = self.procinfo.get_beam_flavour(2)

		self.add_run_option("BEAM_1", beam1_pdg)
		self.add_run_option("BEAM_2", beam2_pdg)

		self.add_run_option("BEAM_ENERGY_1", ENG)
		self.add_run_option("BEAM_ENERGY_2", ENG)

		self.add_run_option("MODEL", self.procinfo.get("model"))

		if self.procinfo.get("isr_mode"):
			self.add_run_option("PDF_LIBRARY", "PDFESherpa")
		else:
			self.add_run_option("PDF_LIBRARY", "None")
		self.add_run_option("EVENTS", self.procinfo.get("events"))
		self.run += "\n\n"
		self.run += " # Add Particle data\n"
		for p in self.procinfo.get_data_particles():
			for attr in dir(p):
				if not callable(getattr(p, attr)) and not attr.startswith("__"):
					name = self.is_sherpa_particle_data(attr)
					if name is not None:
						value = getattr(p, attr)
						op_name = f"{name}[{p.get('pdg_code')}]"
						self.add_run_option(op_name, value)
						
		if  self.procinfo.get("output_format") == "hepmc":
			eoutname="HepMC_GenEvent[{0}]".format(self.procinfo.get("procname"))
			self.add_run_option("EVENT_OUTPUT", eoutname)
			
		elif self.procinfo.get("output_format") == "hepmc3":
			eoutname="HepMC3_GenEvent[{0}]".format(self.procinfo.get("procname"))
			self.add_run_option("EVENT_OUTPUT", eoutname)


	def write_process(self):
		self.ptext = "(processes){\n"
		self.ptext += f"  Process {self.procinfo.get_initial_pdg()} -> {self.procinfo.get_final_pdg()};\n"
		self.ptext += f"  Order ({self.procinfo.get_qcd_order()},{self.procinfo.get_qed_order()});\n"
		self.ptext += "  End process;\n"

	def write_file(self):
		self.write_run()
		self.write_process()
		self.ptext += "}(processes)\n\n"
		self.run += "}(run)\n\n"
		self.file = self.run + self.ptext
		with open(self.outfile, "w+") as file:
			file.write(self.file)
		os.chmod(self.key4hepfile, os.stat(self.key4hepfile).st_mode | stat.S_IEXEC)

	def write_key4hepfile(self,shell,config):
		key4hepRun = shell+"\n"
		key4hepRun += config+"\n"
		key4hepRun += self.executable+" "+self.outfileName+"\n"
		with open(self.key4hepfile, "w+") as file:
			file.write(key4hepRun)

	def add_run_option(self, key, value):
		self.run += f" {key} {value};\n"

	def add_process_option(self, key, value):
		self.ptext += f" {key} {value};\n"

	def is_sherpa_particle_data(self, d):
		name = None
		if d == "mass":
			name = "MASS"
		if d == "width":
			name = "WIDTH"
		return name
