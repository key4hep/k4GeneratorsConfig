from .ProcDBBase import ProcDBBase

class MadgraphProcDB(ProcDBBase):
    """MadgraphProcDB class"""

    def __init__(self, process):
        super().__init__(process)
        self.process = process

    def write_DBInfo(self):
        # choose as function of generatorDBLabel
        if self.process.get_generatorDBLabel().startswith("11_11") and len(self.process.final) == 2 :
            if abs(self.process.final[0]) <= 16:
                self.runout += self.write_Difermion()
        label = self.process.get_generatorDBLabel()
        if label == "11_11_23_25":
            self.runout += self.write_run_ZH()

    def write_Difermion(self):
        out = ""
        out += f"\nset pt_min_pdg {{{self.process.final[0]}: 0 }}\n"
        return out

    def write_run_ZH(self):
        out = ""
        return out

