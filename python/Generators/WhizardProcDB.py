from .ProcDBBase import ProcDBBase

class WhizardProcDB(ProcDBBase):
    """WhizardProcDB class"""

    def __init__(self, process):
        super().__init__(process)
        self.process = process

    def write_DBInfo(self):
        # choose as function of generatorDBLabel
        label = self.process.get_generatorDBLabel()
        if label == "11_11_12_12":
            self.runout += self.write_Difermion()
        if label == "11_11_13_13":
            self.runout += self.write_Difermion()
        if label == "11_11_14_14":
            self.runout += self.write_Difermion()
        if label == "11_11_15_15":
            self.runout += self.write_Difermion()
        if label == "11_11_16_16":
            self.runout += self.write_Difermion()
        if label == "11_11_12_12":
            self.runout += self.write_Difermion()
        elif label == "11_11_23_25":
            self.runout += self.write_ZH()

    def write_Difermion(self):
        self.runout += "mW = 80.419 GeV\n"
        self.runout += "wW = 2.0476 GeV\n"
        return self.runout

    def write_ZH(self):
        self.runout += "?resonance_history = true\n"
        self.runout += "resonance_on_shell_limit = 16\n"
        self.runout += "resonance_on_shell_turnoff = 2\n"
        self.runout += "resonance_on_shell_turnoff = 2\n"
        return self.runout

