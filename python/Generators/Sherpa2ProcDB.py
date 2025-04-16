from .ProcDBBase import ProcDBBase

class Sherpa2ProcDB(ProcDBBase):
    """Sherpa2ProcDB class"""

    def __init__(self, process):
        super().__init__(process)
        self.process = process

    def execute(self):
        # choose as function of generatorDBLabel
        label = self.process.get_generatorDBLabel()
        if label == "11_11_5_5":
            self.rundict['MASSIVE[5]'] = 1
        if label == "11_11_6_6":
            self.rundict['MASSIVE[6]'] = 1
        if label == "11_11_15_15":
            self.rundict['MASSIVE[15]'] = 1
        # the electroweak scheme is common to all implemented processes so far
        self.rundict['EW_SCHEME'] = 3


