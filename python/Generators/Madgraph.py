import stat,os
import MadgraphProcDB
from Particles import Particle as part

class Madgraph:
	"""Madgraph class"""
	def __init__(self, procinfo, settings):
		self.name = "Madgraph"
		self.version = "x.y.z"
		self.procinfo = procinfo
		self.settings = settings
		self.ext = "dat"
		self.file = ""
		self.cuts = ""
		self.outdir = f"{procinfo.get('OutDir')}/Madgraph"
		self.outfileName = f"Run_{self.procinfo.get('procname')}.{self.ext}"
		self.outfile = f"{self.outdir}/{self.outfileName}"

		self.executable  = "mg5_aMC"
		self.key4hepfile = f"{self.outdir}/Run_{self.procinfo.get('procname')}.sh"
		self.procDB = MadgraphProcDB.MadgraphProcDB(self.procinfo)
		if settings.get("usedefaults",True):
			self.procDB.write_DBInfo()
		if settings.get_block("selectors"):
			self.cuts="(selector){\n"
			self.write_selectors()

		self.gen_settings = settings.get_block("madgraph")
		if self.gen_settings is not None:
			self.gen_settings = {k.lower(): v for k, v in self.gen_settings.items()}

	def write_run(self):
		self.add_header()
		if self.gen_settings is not None:
			if "model" in self.gen_settings:
				self.add_run_option("import model", self.gen_settings["model"].lower())
			else: 
				self.add_run_option("import model", self.procinfo.get("model").lower())
		else:
			self.add_run_option("import model", self.procinfo.get("model").lower())
		self.mg_particles = list(map(self.pdg_to_madgraph, self.procinfo.get_particles()))
		self.proc=""
		for i in range(len(self.mg_particles)):
			self.proc += f"{self.mg_particles[i]} "
			if i==1:
				self.proc += "> "
		if self.procinfo.get("decay"):
			self.add_decay()
		self.add_run_option("generate", self.proc)
		self.add_run_option("output", self.outdir+f"/{self.procinfo.get('procname')}")
		self.add_run_option("launch", None)
		self.add_run_option("set iseed", self.procinfo.get_rndmSeed())
		self.add_run_option("set EBEAM", self.procinfo.get("sqrts")/2.)		
		self.set_particle_data()
		self.add_run_option("set nevents", self.procinfo.get("events"))
		if self.procinfo.get("isr_mode"):
			if self.procinfo.get_Beamstrahlung() is not None:
				#if self.gen_settings is None:
				#	print("Please set the beamstrahlung parameter as Madgraph:beamstrahlung:---\n\
				#		Options are: cepc240ll, clic3000ll, fcce240ll, fcce365ll, and ilc500ll.\n\
				#		See arxiv 2108.10261 for more details.")
				#	raise(ValueError)
				#else:
				self.add_run_option("set pdlabel", self.get_BeamstrahlungPDLABEL())
			else:
				self.add_run_option("set pdlabel", "isronlyll")
			self.add_run_option("set lpp1", "3")
			self.add_run_option("set lpp2", "-3")
		self.run += self.procDB.get_run_out()


	def get_BeamstrahlungPDLABEL(self):
		ecm   = self.procinfo.get("sqrts")
		accel = self.procinfo.get_Beamstrahlung()
		if abs(ecm-240) < 10:
			if accel.lower() == "cepc":
				return f"{accel.lower()}240ll";
			elif accel.lower() == "fcc":
				return f"{accel.lower()}e240ll";
			else:
				print("No setting found for requested accelerator "+accel+"using FCCE")
				return "fcce240ll"
		elif abs(ecm-365) < 10:
			if accel.lower() == "fcc":
				return f"{accel.lower()}365ll";
			else:
				print("No setting found for requested accelerator "+accel+"using FCCE")
				return "fcc365ll";
		elif abs(ecm-500) < 10:
			if accel.lower() == "ilc":
				return f"{accel.lower()}500ll";
			else:
				print("No setting found for requested accelerator "+accel+"using ILC")
				return "ilc500ll";
		elif abs(ecm-3000) < 10:
			if accel.lower() == "clic":
				return f"{accel.lower()}3000ll";
			else:
				print("No setting found for requested accelerator "+accel+"using CLIC")
				return "clic3000ll";
		else:
			print(f"No Beamstrahlung setting available for MADGRAPH at this energy {ecm}")
			print("Using ILC at 500GeV")
			return "ilc500ll"

	def set_particle_data(self):
		for p in self.procinfo.get_data_particles():
			for attr in dir(p):
				if not callable(getattr(p, attr)) and not attr.startswith("__"):
					name = p.get("name").replace('+', '').replace('-', '')
					_prop = self.is_mg_particle_data(attr)
					if _prop is not None:
						value = getattr(p, attr)
						op_name = f"set {_prop}{name}"
						self.add_run_option(op_name, value)

	def add_decay(self):
		# Simple check first that parents are 
		# in the main process
		decay_opt = self.procinfo.get("decay")
		decays=" "
		for key in decay_opt:
			if str(key) not in self.procinfo.get_final_pdg():
				print("Particle {0} not found in main process. Decay not allowed".format(key))
			parent = part.name_from_pdg(key)
			decays += f", {parent} > "
			for child in decay_opt[key]:
				decays += f"{part.name_from_pdg(child)} "
		self.proc += decays

	def write_selectors(self):
		selectors = getattr(self.settings,"selectors")
		for key,value in selectors.items():
			if key == "pt":
				self.add_one_ParticleSelector(value, "pt")
			elif key == "energy":
				self.add_one_ParticleSelector(value, "e")
			elif key == "rap":
				self.add_one_ParticleSelector(value, "eta")
			elif key == "eta":
				self.add_one_ParticleSelector(value, "eta")	

				# Two particle selectors
			elif key == "mass":
				self.add_two_ParticleSelector(value,"mxx")
			elif key == "angle":
				self.add_two_ParticleSelector(value, "Angle")
			elif key == "deta":
				self.add_two_ParticleSelector(value, "Angle")
			elif key == "drap":
				self.add_two_ParticleSelector(value, "DeltaY")
			elif key == "dphi":
				self.add_two_ParticleSelector(value, "DeltaPhi")
			elif key == "dr":
				self.add_two_ParticleSelector(value, "DeltaR")
			else:
				print(f"{key} not a Sherpa Selector")
		self.cuts+="}(selector)\n"

	def add_two_ParticleSelector(self,sel,name):
		Min,Max = sel.get_MinMax()
		flavs = sel.get_Flavours()
		if len(flavs) == 2:
			f1 = flavs[0]
			f2 = flavs[0]
			if str(f1) not in self.procinfo.get_final_pdg() or str(f2) not in self.procinfo.get_final_pdg():
				return
			sname = f"{name}_min_pdg"
			mincut = f"{f}: {Min}"
			self.add_run_option(sname, value)
			sname = f"{name}_max_pdg"
			maxcut = f"{f}: {Max}"
			self.add_run_option(sname, value)
		else:
			for fl in flavs:
				f1 = fl[0]
				f2 = fl[1]
				if str(f1) not in self.procinfo.get_final_pdg() or str(f2) not in self.procinfo.get_final_pdg():
					continue
				if f1 != -f2:
					print("Cannot set cuts in MadGraph this way.")
				sname = f"{name}_min_pdg"
				mincut = f"{f1}: {Min}"
				self.add_run_option(sname, mincut)
				sname = f"{name}_max_pdg"
				maxcut = f"{f1}: {Max}"
				self.add_run_option(sname, maxcut)

	def add_one_ParticleSelector(self,sel,name):
		Min,Max = sel.get_MinMax()
		f1 = sel.get_Flavours()
		for f in f1:
			sname = f"{name}_min_pdg"
			mincut = f"{f}: {Min}"
			self.add_run_option(sname, mincut)
			sname = f"{name}_max_pdg"
			maxcut = f"{f}: {Max}"
			self.add_run_option(sname, maxcut)

	def write_file(self):
		self.write_run()
		self.file = self.run
		with open(self.outfile, "w+") as file:
			file.write(self.file)

	def write_key4hepfile(self,shell,config):
		key4hepRun = shell+"\n"
		key4hepRun += config+"\n"
		key4hepRun += self.executable+" "+self.outfileName+"\n"
		with open(self.key4hepfile, "w+") as file:
			file.write(key4hepRun)
		os.chmod(self.key4hepfile, os.stat(self.key4hepfile).st_mode | stat.S_IEXEC)

	def add_run_option(self, key, value):
		if key in self.run:
			print(f"{key} has already been defined in {self.name}.")
			return
		if value is not None:
			self.run += f"{key} {value}\n"
		else:
			self.run += f"{key}\n" 

	def pdg_to_madgraph(self, particle):
		return particle.get("name")

	def is_mg_particle_data(self, d):
		if d == "mass":
			return "M"
		if d == "width":
			return "W"
		return None
	
	def add_header(self):
	    self.run = '''#************************************************************
#*                        MadGraph 5                        *
#*                                                          *
#*                *                       *                 *
#*                  *        * *        *                   *
#*                    * * * * 5 * * * *                     *
#*                  *        * *        *                   *
#*                *                       *                 *
#*                                                          *
#*                                                          *
#*    The MadGraph Development Team - Please visit us at    *
#*    https://server06.fynu.ucl.ac.be/projects/madgraph     *
#*                                                          *
#************************************************************
#*                                                          *
#*               Command File for MadGraph 5                *
#*                                                          *
#*     run as ./bin/mg5  filename                           *
#*                                                          *
#************************************************************"\n'''
