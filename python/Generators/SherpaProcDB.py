class SherpaProcDB:
    """SherpaProcDB class"""

    def __init__(self, process):
        self.process = process
        self.runout = ""
        self.procout = ""

    def write_DBInfo(self):
        # choose as function of generatorDBLabel
        label = self.process.get_generatorDBLabel()
        if label == "1_1":
            self.write_Difermion()
        if label == "2_2":
            self.write_Difermion()
        if label == "3_3":
            self.write_Difermion()
        if label == "4_4":
            self.write_Difermion()
        if label == "5_5":
            self.write_Difermion()
            self.runout += " MASSIVE[5] 1\n"
        if label == "6_6":
            self.write_Difermion()
            self.runout += " MASSIVE[6] 1\n"
        if label == "12_12":
            self.write_Difermion()
        if label == "13_13":
            self.write_Difermion()
        if label == "14_14":
            self.write_Difermion()
        if label == "15_15":
            self.write_Difermion()
            self.runout += " MASSIVE[15] 1\n"
        if label == "16_16":
            self.write_Difermion()
        if label=="23_23":
            self.write_ZZ()
        if label=="24_24":
            self.write_WW()
        if label == "23_25":
            self.write_ZH()
        if label=="25_23":
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

    def get_run_out(self):
        return self.runout

    def get_proc_out(self):
        return self.procout

    def remove_option(self, opt):
        lines = self.runout.split("\n")
        filter_lines = [line for line in lines if opt not in line]
        self.runout = "\n".join(filter_lines)
