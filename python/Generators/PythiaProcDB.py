from .ProcDBBase import ProcDBBase

class PythiaProcDB(ProcDBBase):
    """PythiaProcDB class"""

    def __init__(self, process):
        super().__init__(process)
        self.process = process

    def execute(self):
        # general stuff
        self.rundict['Main:timesAllowErrors'] = 5
        # ! 2) Settings related to output in init(), next() and stat().
        self.rundict['Init:showChangedSettings'] = "on"
        self.rundict['Init:showChangedParticleData'] = "on"
        self.rundict['Next:numberCount'] = 1000
        self.rundict['Next:numberShowInfo'] = 1
        self.rundict['Next:numberShowProcess'] = 1
        self.rundict['Next:numberShowEvent'] = 1
        # !4) Tell that also long-lived should decay.
        # 13:mayDecay   = true                 ! mu+-
        self.rundict['211:mayDecay']  = "true"
        self.rundict['321:mayDecay']  = "true"
        self.rundict['130:mayDecay']  = "true"

        # choose as function of generatorDBLabel
        label = self.process.get_generatorDBLabel()
        if label == "11_11_1_1":
            self.write_Difermion(1)
        elif label == "11_11_2_2":
            self.write_Difermion(2)
        elif label == "11_11_3_3":
            self.write_Difermion(3)
        elif label == "11_11_4_4":
            self.write_Difermion(4)
        elif label == "11_11_5_5":
            self.write_Difermion(5)
        elif label == "11_11_6_6":
            self.write_Ditop()
        elif label == "11_11_12_12":
            self.write_Difermion(12)
        elif label == "11_11_13_13":
            self.write_Difermion(13)
        elif label == "11_11_14_14":
            self.write_Difermion(14)
        elif label == "11_11_15_15":
            self.write_Difermion(15)
        elif label == "11_11_16_16":
            self.write_Difermion(16)
        elif label == "11_11_22_22":
            self.write_Diphoton()
        elif label == "11_11_23_23":
            self.write_ZZ()
        elif label == "11_11_24_24":
            self.write_WW()
        elif label == "11_11_23_25":
            self.write_run_ZH()
        elif label == "11_11_12_12_25":
            self.write_run_Hnunu()

    def write_Difermion(self, pdg):
        self.procdict['WeakSingleBoson:ffbar2gmZ'] = "on"
        self.procdict['22:onMode']  = "off"
        self.procdict['22:onIfAny'] = f"{pdg}"
        self.procdict['23:onMode']  = "off"
        self.procdict['23:onIfAny'] = f"{pdg}"

    def write_Diphoton(self):
        self.procdict['PromptPhoton:ffbar2gammagamma'] = "on"

    def write_ZZ(self):
        self.procdict['WeakDoubleBoson:ffbar2gmZgmZ'] = "on"
        self.procdict['23:onMode'] = "on"

    def write_WW(self):
        self.procdict['WeakDoubleBoson:ffbar2WW'] = "on"
        self.procdict['24:onMode'] = "on"

    def write_run_ZH(self):
        self.procdict['HiggsSM:ffbar2HZ'] = "on"
        self.procdict['25:onMode'] = "on"
        self.procdict['23:onMode'] = "on"

    def write_run_Hnunu(self):
        self.procdict['HiggsSM:ff2Hff(t:WW)'] = "on"
        self.procdict['HiggsSM:ffbar2HZ'] = "on"
        self.procdict['25:onMode'] = "on"
        self.procdict['23:onMode'] = "off"
        self.procdict['23:onIfAny'] = "12"

    def write_Ditop(self):
        self.procdict['Top:ffbar2ttbar(s:gmZ)'] = "on"
        self.procdict['6:onMode'] = "on"

