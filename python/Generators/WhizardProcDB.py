class WhizardProcDB:
    """WhizardProcDB class"""
    def __init__(self, process):
        self.process = process
        self.out = ""

    def write_DBInfo(self):
        # choose as function of generatorDBLabel
        label = self.process.get_generatorDBLabel()
        if ( label == "12_12" ):
            self.out += self.write_Difermion()
        if ( label == "13_13" ):
            self.out += self.write_Difermion()
        if ( label == "14_14" ):
            self.out += self.write_Difermion()
        if ( label == "15_15" ):
            self.out += self.write_Difermion()
        if ( label == "16_16" ):
            self.out += self.write_Difermion()
        if ( label == "12_12" ):
            self.out += self.write_Difermion()
        elif ( label == "23_25" ):
            self.out += self.write_ZH()

    def write_Difermion(self):
        self.out += "mW = 80.419 GeV\n"
        self.out += "wW = 2.0476 GeV\n"
        return self.out

    def write_ZH(self):
        self.out += "?resonance_history = true\n" 
        self.out += "resonance_on_shell_limit = 16\n"
        self.out += "resonance_on_shell_turnoff = 2\n"
        self.out += "resonance_on_shell_turnoff = 2\n"
        return self.out

    def get_out(self):
        return self.out

    def remove_option(self,opt):
        lines = self.out.split("\n")
        filter_lines = [line for line in lines if opt not in line]
        self.out = "\n".join(filter_lines)
