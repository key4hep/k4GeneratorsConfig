class Madgraph:
	"""Madgraph class"""
	def __init__(self, procinfo):
		self.name = "Madgraph"
		self.version = "x.y.z"
		self.procinfo = procinfo
		self.ext = "dat"
		self.file = ""
		self.outdir = f"{procinfo.get('OutDir')}/Madgraph"
		self.outfile = f"{self.outdir}/Run_{self.procinfo.get('procname')}.{self.ext}"

	def write_run(self):
		self.add_header()
		self.add_run_option("import model", self.procinfo.get("model").lower())
		self.mg_particles = list(map(self.pdg_to_madgraph, self.procinfo.get_particles()))
		self.proc=""
		for i in range(len(self.mg_particles)):
			self.proc += f"{self.mg_particles[i]} "
			if i==1:
				self.proc += "> "
		self.add_run_option("generate", self.proc)
		self.add_run_option("launch", None)
		self.add_run_option("set EBEAM", self.procinfo.get("sqrts")/2.)		
		self.set_particle_data()
		self.add_run_option("set nevents", self.procinfo.get("events"))
		self.add_run_option("set output", self.outdir+f"/{self.procinfo.get('procname')}")


	def set_particle_data(self):
		for p in self.procinfo.get_data_particles():
			for attr in dir(p):
				if not callable(getattr(p, attr)) and not attr.startswith("__"):
					name = p.get("name")
					_prop = self.is_mg_particle_data(attr)
					if _prop is not None:
						value = getattr(p, attr)
						op_name = f"set {_prop}{name}"
						self.add_run_option(op_name, value)

	def write_file(self):
		self.write_run()
		self.file = self.run
		with open(self.outfile, "w+") as file:
			file.write(self.file)

	def add_run_option(self, key, value):
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
#************************************************************"\n '''
