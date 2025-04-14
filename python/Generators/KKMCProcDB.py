from .ProcDBBase import ProcDBBase

class KKMCProcDB(ProcDBBase):
    """MadgraphProcDB class"""

    def __init__(self, process):
        super().__init__(process)
        self.process = process

    def execute(self):
        # choose as function of generatorDBLabel
        if self.process.get_generatorDBLabel().startswith("11_11") and len(self.process.final) == 2 :
            if abs(self.process.final[0]) <= 16:
                self.write_Difermion()
        else:
            raise(Exception,"KKMC can only do 2->2")
        label = self.process.get_generatorDBLabel()

    def write_Difermion(self):
        self.rundict['set pt_min_pdg'] = f"{{{self.process.final[0]}: 0 }}"

