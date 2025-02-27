import abc

class ProcDBBase(abc.ABC):
    """GeneratorBase class"""

    def __init__(self, procinfo):

        # general settings of the class
        self.procinfo = procinfo
        self.rundict       = dict()
        self.procdict      = dict()
        self.particlesdict = dict()

    def execute(self):
        return
        
    def getDict(self):
        fulldict = dict()
        fulldict.update(self.rundict)
        fulldict.update(self.procdict)
        fulldict.update(self.particlesdict)
        return fulldict

    def getDictParameters(self):
        fulldict = dict()
        fulldict.update(self.rundict)
        fulldict.update(self.procdict)
        return fulldict

    def getDictRun(self):
        return self.rundict

    def getDictProc(self):
        return self.procdict

    def getDictParticles(self):
        return self.particlesdict

    def removeOption(self, opt):
        for myDict in self.rundict,self.procdict,self.particlesdict:
            try:
                del myDict[opt]
            except KeyError:
                pass
