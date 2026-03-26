from .ProcDBBase import ProcDBBase

class MadgraphProcDB(ProcDBBase):
    """MadgraphProcDB class"""

    def __init__(self, process):
        super().__init__(process)
        self.process = process

    def execute(self):
        # choose as function of DBTag
        tag = self.process.get_DBTag()
        initialState = tag[0]
        finalState   = tag[1]
        if initialState == [-11,11] and len(finalState) == 2:
            isFermionPair = all( abs(pdg)<=16 for pdg in finalState)
            if isFermionPair:
                self.write_Difermion()

    def write_Difermion(self):
        self.rundict['set pt_min_pdg'] = f"{{{self.process.final[0]}: 0 }}"

