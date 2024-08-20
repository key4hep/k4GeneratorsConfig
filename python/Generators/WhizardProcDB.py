class WhizardProcDB:
    """WhizardProcDB class"""

    def __init__(self, process):
        self.process = process
        self.runout = ""

    def write_DBInfo(self):
        # choose as function of generatorDBLabel
        label = self.process.get_generatorDBLabel()
        if label == "12_12":
            self.runout += self.write_Difermion()
        if label == "13_13":
            self.runout += self.write_Difermion()
        if label == "14_14":
            self.runout += self.write_Difermion()
        if label == "15_15":
            self.runout += self.write_Difermion()
        if label == "16_16":
            self.runout += self.write_Difermion()
        if label == "12_12":
            self.runout += self.write_Difermion()
        elif label == "23_25":
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

    def get_run_out(self):
        return self.runout

    def remove_option(self, opt):
        lines = self.runout.split("\n")
        filter_lines = [line for line in lines if opt not in line]
        self.runout = "\n".join(filter_lines)
