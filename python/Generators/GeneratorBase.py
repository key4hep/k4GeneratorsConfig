import os, stat

class GeneratorBase:
    """GeneratorBase class"""
    def __init__(self,procinfo, settings,name,inputFileExtension):

        self.procinfo = procinfo
        self.settings = settings
        self.name = name
        self.inputFileExtension = inputFileExtension

        self.outdir                = f"{procinfo.get('OutDir')}/{self.name}/{self.procinfo.get('procname')}"
        self.GeneratorDatacardBase = f"{self.procinfo.get('procname')}"
        self.key4hepScript         = f"{self.outdir}/Run_{self.procinfo.get('procname')}"

        if self.procinfo.get("isrmode"):
            self.GeneratorDatacardBase += "_ISR"
            self.key4hepScript         += "_ISR"

            if self.procinfo.get_Beamstrahlung() is not None:
                self.GeneratorDatacardBase += "_BST"
                self.key4hepScript         += "_BST"

        # take care of the extensions of the filenames
        self.GeneratorDatacardName = self.GeneratorDatacardBase+"."+self.inputFileExtension
        self.key4hepScript += ".sh"

        # composition of file+directory
        self.GeneratorDatacard = f"{self.outdir}/{self.GeneratorDatacardName}"
        

    def write_Key4hepScript(self,content):
        # write the generator specific content to the KEY4HEP execution script
        with open(self.key4hepScript, "w+") as file:
            file.write(content)
        os.chmod(self.key4hepScript, os.stat(self.key4hepScript).st_mode | stat.S_IEXEC)

    def write_GeneratorDatacard(self,content):
        with open(self.GeneratorDatacard, "w+") as file:
            file.write(content)

