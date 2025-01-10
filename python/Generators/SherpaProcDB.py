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
            self.runout += " MASSIVE[5] 1\n"
        if label == "11_11_6_6":
            self.write_Difermion()
            self.runout += " MASSIVE[6] 1\n"
        if label == "11_11_12_12":
            self.write_Difermion()
        if label == "11_11_13_13":
            self.write_Difermion()
        if label == "11_11_14_14":
            self.write_Difermion()
        if label == "11_11_15_15":
            self.write_Difermion()
            self.runout += " MASSIVE[15] 1\n"
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
        self.runout += " EW_SCHEME 3;\n"
        
            
    def write_Difermion(self):
        self.runout = ""
        # Use Gmu scheme as default
        self.runout += " MASS[24] 80.419;\n"
        self.runout += " WIDTH[24] 2.0476;\n"

    def write_ZZ(self):
        self.runout = ""
        # Use Gmu scheme as default
        self.runout += " MASS[24] 80.419;\n"
        self.runout += " WIDTH[24] 2.0476;\n"

    def write_WW(self):
        self.runout = ""
        # Use Gmu scheme as default
        self.runout += " MASS[24] 80.419;\n"
        self.runout += " WIDTH[24] 2.0476;\n"

    def write_ZH(self):
        self.runout = " WIDTH[25] 0\n"
        self.runout += " WIDTH[23] 0\n"

    def write_Hnunu(self):
        self.runout = " WIDTH[25] 0\n"
        self.runout += " MASS[24] 80.419;\n"
        self.runout += " WIDTH[24] 2.0476;\n"

    def write_ZHH(self):
        self.runout = " WIDTH[25] 0\n"
        self.runout += " WIDTH[23] 0\n"

