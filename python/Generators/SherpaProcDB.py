from .ProcDBBase import ProcDBBase

class SherpaProcDB(ProcDBBase):
    """SherpaProcDB class"""

    def __init__(self, process):
        super().__init__(process)
        self.process = process

    def execute(self):
        # the electroweak scheme is common to all implemented processes so far
        self.rundict['EW_SCHEME'] = 3
        # the procdict:
        self.procdict['Order'] = "{QCD: 0, EW: 2}"
        # choose as function of DBTag
        tag = self.process.get_DBTag()
        if tag == [[-11,11],[-5,5]]:
            self.particlesdict['5'] = {'Massive' : 1}
        if tag == [[-11,11],[-6,6]]:
            self.particlesdict['6'] = {'Massive' : 1}
        if tag == [[-11,11],[-15,15]]:
            self.particlesdict['15'] = {'Massive' : 1}
        if tag == [[-11,11],[23,25]]:
            self.particlesdict['23']  = {'Width' : 0}
            self.particlesdict['25']  = {'Width' : 0}
            # b quark has to be made massive
            self.particlesdict['15'] = {'Massive' : 1}
            self.particlesdict['5']  = {'Massive' : 1}
            self.particlesdict['4']  = {'Massive' : 1}


