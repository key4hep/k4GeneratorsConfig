class PythiaProcDB:
    """PythiaProcDB class"""
    def __init__(self, process):
        self.process = process
        self.runout = ""
        self.procout = ""

    def write_DBInfo(self):
        # general stuff
        self.runout +="Main:timesAllowErrors = 5          ! allow a few failures before quitting\n"
        # ! 2) Settings related to output in init(), next() and stat().
        self.runout +="Init:showChangedSettings = on      ! list changed settings\n"
        self.runout +="Init:showChangedParticleData = on  ! list changed particle data\n"
        self.runout +="Next:numberCount = 1000            ! print message every n events\n"
        self.runout +="Next:numberShowInfo = 1            ! print event information n times\n"
        self.runout +="Next:numberShowProcess = 1         ! print process record n times\n"
        self.runout +="Next:numberShowEvent = 1           ! print event record n times\n"
        #! 3) Beam parameter settings. Incoming beams do not radiate.
        self.runout +="PDF:lepton = off                   ! no radiation off ficititious e+e-\n"
        # !4) Tell that also long-lived should decay.
        #13:mayDecay   = true                 ! mu+-
        self.runout +="211:mayDecay  = true                 ! pi+-\n"
        self.runout +="321:mayDecay  = true                 ! K+-\n"
        self.runout +="130:mayDecay  = true                 ! K0_L\n"
        #self.runout +="2112:mayDecay = true                 ! n\n"

        # choose as function of generatorDBLabel
        label = self.process.get_generatorDBLabel()
        if ( label == "12_12" ):
            self.write_Difermion()
        if ( label == "13_13" ):
            self.write_Difermion()
        if ( label == "14_14" ):
            self.write_Difermion()
        if ( label == "15_15" ):
            self.write_Difermion()
        if ( label == "16_16" ):
            self.write_Difermion()
        if ( label == "12_12" ):
            self.write_Difermion()
        elif ( label == "23_25" ):
            self.write_run_ZH()

    def write_Difermion(self,):
        self.procout  = "\n"

    def write_run_ZH(self):
        self.procout  = "\n" 

    def get_run_out(self):
        return self.runout

    def get_proc_out(self):
        return self.procout

    def remove_option(self,opt):
        lines = self.runout.split("\n")
        filter_lines = [line for line in lines if opt not in line]
        self.runout = "\n".join(filter_lines)
