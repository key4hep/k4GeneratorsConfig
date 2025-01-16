from .ProcDBBase import ProcDBBase

class SherpaProcDB(ProcDBBase):
    """SherpaProcDB class"""

    def __init__(self, process):
        super().__init__(process)
        self.process = process

    def write_DBInfo(self):
        # choose as function of generatorDBLabel
        label = self.process.get_generatorDBLabel()
        if label == "11_11_1_1":
            self.write_Difermion()
        if label == "11_11_2_2":
            self.write_Difermion()
        if label == "11_11_3_3":
            self.write_Difermion()
        if label == "11_11_4_4":
            self.write_Difermion()
        if label == "11_11_5_5":
            self.write_Difermion()
            self.rundict['MASSIVE[5]'] = 1
        if label == "11_11_6_6":
            self.write_Difermion()
            self.rundict['MASSIVE[6]'] = 1
        if label == "11_11_12_12":
            self.write_Difermion()
        if label == "11_11_13_13":
            self.write_Difermion()
        if label == "11_11_14_14":
            self.write_Difermion()
        if label == "11_11_15_15":
            self.write_Difermion()
            self.rundict['MASSIVE[15]'] = 1
        if label == "11_11_16_16":
            self.write_Difermion()
        if label=="11_11_23_23":
            self.write_ZZ()
        if label=="11_11_24_24":
            self.write_WW()
        if label == "11_11_23_25":
            self.write_ZH()
        if label=="11_11_12_12_25":
            self.write_Hnunu()
        if label=="11_11_23_25_25":
            self.write_ZH()
        # the electroweak scheme is common to all implemented processes so far
        self.rundict['EW_SCHEME'] = 3
        
            
    def write_Difermion(self):
        # Use Gmu scheme as default
        self.rundict['MASS[24]']  = 80.419
        self.rundict['WIDTH[24]'] = 2.0476

    def write_ZZ(self):
        # Use Gmu scheme as default
        self.rundict['MASS[24]']  = 80.419
        self.rundict['WIDTH[24]'] = 2.0476

    def write_WW(self):
        # Use Gmu scheme as default
        self.rundict['MASS[24]']  = 80.419
        self.rundict['WIDTH[24]'] = 2.0476

    def write_ZH(self):
        self.rundict['WIDTH[25]'] = 0
        self.rundict['WIDTH[23]'] = 0

    def write_Hnunu(self):
        self.rundict['WIDTH[25]'] = 0
        self.rundict['MASS[24]']  = 80.419
        self.rundict['WIDTH[24]'] = 2.0476

    def write_ZHH(self):
        self.rundict['WIDTH[25]'] = 0
        self.rundict['WIDTH[23]'] = 0

