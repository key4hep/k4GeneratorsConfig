import os, stat

class GeneratorBase:
    """GeneratorBase class"""
    def __init__(self,procinfo, settings,name,inputFileExtension):

        self.procinfo = procinfo
        self.settings = settings
        self.name = name
        self.inputFileExtension = inputFileExtension

        self.fullprocname  = f"{self.procinfo.get('procname')}"
        self.outdir        = f"{procinfo.get('OutDir')}/{self.name}/{self.procinfo.get('procname')}"
        self.outfileName   = f"Run_{self.procinfo.get('procname')}"
        self.key4hepScript = f"{self.outdir}/Run_{self.procinfo.get('procname')}"

        if self.procinfo.get("isrmode"):
            self.outfileName    += "_ISR"
            self.key4hepScript  += "_ISR"
            self.fullprocname   += "_ISR"

            if self.procinfo.get_Beamstrahlung() is not None:
                self.outfileName   += "_BST"
                self.key4hepScript += "_BST"
                self.fullprocname  += "_BST"

        self.outfile = f"{self.outdir}/{self.outfileName}"
        
        # take care of the extensions of the filenames
        self.outfile       += "."+self.inputFileExtension
        self.outfileName   += "."+self.inputFileExtension
        self.key4hepScript += ".sh"

    def write_Key4hepScript(self,content):
        # write the generator specific content to the KEY4HEP execution script
        with open(self.key4hepScript, "w+") as file:
            file.write(content)
        os.chmod(self.key4hepScript, os.stat(self.key4hepScript).st_mode | stat.S_IEXEC)

