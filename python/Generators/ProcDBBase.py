import abc

class ProcDBBase(abc.ABC):
    """GeneratorBase class"""

    def __init__(self, procinfo):

        # general settings of the class
        self.procinfo = procinfo
        self.runout = ""
        self.procout = ""
