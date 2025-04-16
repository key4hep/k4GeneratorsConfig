from .ProcDBBase import ProcDBBase

class SherpaProcDB(ProcDBBase):
    """SherpaProcDB class"""

    def __init__(self, process):
        super().__init__(process)
        self.process = process

    def execute(self):
        # choose as function of generatorDBLabel
        label = self.process.get_generatorDBLabel()
        if label == "11_11_5_5":
            self.particlesdict['5'] = {'Massive' : 1}
        if label == "11_11_6_6":
            self.particlesdict['6'] = {'Massive' : 1}
        if label == "11_11_15_15":
            self.particlesdict['15'] = {'Massive' : 1}
        if label == "11_11_23_25":
            self.particlesdict['23']  = {'Width' : 0}
            self.particlesdict['25']  = {'Width' : 0}
            # b quark has to be made massive
            self.particlesdict['15'] = {'Massive' : 1}
            self.particlesdict['5']  = {'Massive' : 1}
            self.particlesdict['4']  = {'Massive' : 1}
        # the electroweak scheme is common to all implemented processes so far
        self.rundict['EW_SCHEME'] = 3


