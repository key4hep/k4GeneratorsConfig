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

        # choose as function of DBTag
        tag = self.process.get_DBTag()
        if tag == [[-11,11],[-1,1]]:
            self.write_Difermion(1)
        elif tag == [[-11,11],[-2,2]]:
            self.write_Difermion(2)
        elif tag == [[-11,11],[-3,3]]:
            self.write_Difermion(3)
        elif tag == [[-11,11],[-4,4]]:
            self.write_Difermion(4)
        elif tag == [[-11,11],[-5,5]]:
            self.write_Difermion(5)
        elif tag == [[-11,11],[-6,6]]:
            self.write_Ditop()
        elif tag == [[-11,11],[-12,12]]:
            self.write_Difermion(12)
        elif tag == [[-11,11],[-13,13]]:
            self.write_Difermion(13)
        elif tag == [[-11,11],[-14,14]]:
            self.write_Difermion(14)
        elif tag == [[-11,11],[-15,15]]:
            self.write_Difermion(15)
        elif tag == [[-11,11],[-16,16]]:
            self.write_Difermion(16)
        elif tag == [[-11,11],[22,22]]:
            self.write_Diphoton()
        elif tag == [[-11,11],[23,23]]:
            self.write_ZZ()
        elif tag == [[-11,11],[24,24]]:
            self.write_WW()
        elif tag == [[-11,11],[23,25]]:
            self.write_run_ZH()
        elif tag == [[-11,11],[-12,12,25]]:
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

