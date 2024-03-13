class MadgraphProcDB:
    """MadgraphProcDB class"""
    def __init__(self, process):
        self.process = process
        self.runout = ""
        self.procout = ""

    def write_DBInfo(self):
        # choose as function of generatorDBLabel
        label = self.process.get_generatorDBLabel()
        if ( label == "12_12" ):
            self.runout += self.write_Difermion()
        if ( label == "13_13" ):
            self.runout += self.write_Difermion()
        if ( label == "14_14" ):
            self.runout += self.write_Difermion()
        if ( label == "15_15" ):
            self.runout += self.write_Difermion()
        if ( label == "16_16" ):
            self.runout += self.write_Difermion()
        if ( label == "12_12" ):
            self.runout += self.write_Difermion()
        elif ( label == "23_25" ):
            self.runout += self.write_run_ZH()

    def write_Difermion(self):
        out = ""
        return out


    def get_run_out(self):
        return self.runout

    def get_proc_out(self):
        return self.procout

    def write_run_ZH(self):
        out  = "set WZ 0\n" 
        out += "set WH 0\n"
        return out


    def remove_option(self,opt):
        lines = self.runout.split("\n")
        filter_lines = [line for line in lines if opt not in line]
        self.runout = "\n".join(filter_lines)
