from .ProcDBBase import ProcDBBase

class KKMCProcDB(ProcDBBase):
    """KKMCProcDB class"""

    def __init__(self, process):
        super().__init__(process)
        self.process = process

    def write_DBInfo(self):
        # choose as function of generatorDBLabel
        label = self.process.get_generatorDBLabel()
