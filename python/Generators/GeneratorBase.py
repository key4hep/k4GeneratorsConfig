class GeneratorBase:
    """GeneratorBase class"""
    def __init__(self,procinfo, settings,name):

        self.procinfo = procinfo
        self.settings = settings
        self.name = name

        self.fullprocname = f"{self.procinfo.get('procname')}"
        self.outdir = f"{procinfo.get('OutDir')}/{self.name}/{self.procinfo.get('procname')}"
        self.outfileName = f"Run_{self.procinfo.get('procname')}"
        self.key4hepfile = f"{self.outdir}/Run_{self.procinfo.get('procname')}"

        if self.procinfo.get("isrmode"):
            self.outfileName  += "_ISR"
            self.key4hepfile  += "_ISR"
            self.fullprocname += "_ISR"

            if self.procinfo.get_Beamstrahlung() is not None:
                self.outfileName += "_BST"
                self.key4hepfile += "_BST"
                self.fullprocname += "_BST"

        self.outfile = f"{self.outdir}/{self.outfileName}"
