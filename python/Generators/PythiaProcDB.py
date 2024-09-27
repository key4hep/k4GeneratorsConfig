class PythiaProcDB:
    """PythiaProcDB class"""

    def __init__(self, process):
        self.process = process
        self.runout = ""
        self.procout = ""

    def write_DBInfo(self):
        # general stuff
        self.runout += "Main:timesAllowErrors = 5          ! allow a few failures before quitting\n"
        # ! 2) Settings related to output in init(), next() and stat().
        self.runout += "Init:showChangedSettings = on      ! list changed settings\n"
        self.runout += (
            "Init:showChangedParticleData = on  ! list changed particle data\n"
        )
        self.runout += (
            "Next:numberCount = 1000            ! print message every n events\n"
        )
        self.runout += (
            "Next:numberShowInfo = 1            ! print event information n times\n"
        )
        self.runout += (
            "Next:numberShowProcess = 1         ! print process record n times\n"
        )
        self.runout += (
            "Next:numberShowEvent = 1           ! print event record n times\n"
        )
        # !4) Tell that also long-lived should decay.
        # 13:mayDecay   = true                 ! mu+-
        self.runout += "211:mayDecay  = true                 ! pi+-\n"
        self.runout += "321:mayDecay  = true                 ! K+-\n"
        self.runout += "130:mayDecay  = true                 ! K0_L\n"
        # self.runout +="2112:mayDecay = true                 ! n\n"

        # choose as function of generatorDBLabel
        label = self.process.get_generatorDBLabel()
        if label == "1_1":
            self.write_Difermion(1)
        elif label == "2_2":
            self.write_Difermion(2)
        elif label == "3_3":
            self.write_Difermion(3)
        elif label == "4_4":
            self.write_Difermion(4)
        elif label == "5_5":
            self.write_Difermion(5)
        elif label == "6_6":
            self.write_Ditop()
        elif label == "12_12":
            self.write_Difermion(12)
        elif label == "13_13":
            self.write_Difermion(13)
        elif label == "14_14":
            self.write_Difermion(14)
        elif label == "15_15":
            self.write_Difermion(15)
        elif label == "16_16":
            self.write_Difermion(16)
        elif label == "22_22":
            self.write_Diphoton()
        elif label == "23_23":
            self.write_ZZ()
        elif label == "24_24":
            self.write_WW()
        elif label == "23_25":
            self.write_run_ZH()

    def write_Difermion(self, pdg):
        self.procout = "WeakSingleBoson:ffbar2gmZ = on\n"
        self.procout += "22:onMode = off\n"
        self.procout += f"22:onIfAny = {pdg}\n"
        self.procout += "23:onMode = off\n"
        self.procout += f"23:onIfAny = {pdg}\n"

    def write_Diphoton(self):
        self.procout = "PromptPhoton:ffbar2gammagamma = on\n"

    def write_ZZ(self):
        self.procout = "WeakDoubleBoson:ffbar2gmZgmZ = on\n"
        self.procout += "23:onMode = on\n"
        
    def write_WW(self):
        self.procout = "WeakDoubleBoson:ffbar2WW = on\n"
        self.procout += "24:onMode = on\n"
    
    def write_run_ZH(self):
        self.procout = "HiggsSM:ffbar2HZ = on\n"
        self.procout += "25:onMode = on\n"
        self.procout += "23:onMode = on\n"

    def write_Ditop(self):
        self.procout = "Top:ffbar2ttbar(s:gmZ) = on\n"
        self.procout += "6:onMode = on\n"

    def get_run_out(self):
        return self.runout

    def get_proc_out(self):
        return self.procout

    def remove_option(self, opt):
        lines = self.runout.split("\n")
        filter_lines = [line for line in lines if opt not in line]
        self.runout = "\n".join(filter_lines)
