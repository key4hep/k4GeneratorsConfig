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
            self.write_Difermion()
        if label == "11_11_13_13":
            self.write_Difermion()
        if label == "11_11_14_14":
            self.write_Difermion()
        if label == "11_11_15_15":
            self.write_Difermion()
        if label == "11_11_16_16":
            self.write_Difermion()
        if label == "11_11_12_12":
            self.write_Difermion()
        elif label == "11_11_23_25":
            self.write_ZH()

    def write_Difermion(self):
        self.rundict['mW'] = "80.419 GeV"
        self.rundict['wW'] = "2.0476 GeV"

    def write_ZH(self):
        self.rundict['?resonance_history'] = "true\n"
        self.rundict['resonance_on_shell_limit'] = 16
        self.rundict['resonance_on_shell_turnoff'] = 2
        self.rundict['resonance_on_shell_turnoff'] = 2

