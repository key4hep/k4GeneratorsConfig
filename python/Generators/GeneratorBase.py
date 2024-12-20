import os, stat

class GeneratorBase:
    """GeneratorBase class"""

    def __init__(self, procinfo, settings, name, inputFileExtension):

        # general settings of the class
        self.procinfo = procinfo
        self.settings = settings
        self.name = name
        self.inputFileExtension = inputFileExtension

        # define the output directory as function of the OutDir spec + generator name + process name
        self.outdir = (
            f"{procinfo.get('OutDir')}/{self.name}/{self.procinfo.get('procname')}"
        )

        # configure the filenames
        self.GeneratorDatacardBase = f"{self.procinfo.get('procname')}"
        self.key4hepScript = f"{self.outdir}/Run_{self.procinfo.get('procname')}"

        # add ISR and BST if requested
        if self.procinfo.get("isrmode"):
            self.GeneratorDatacardBase += "_ISR"
            self.key4hepScript += "_ISR"

            if self.procinfo.get("beamstrahlung") is not None:
                self.GeneratorDatacardBase += (
                    "_BST" + self.procinfo.beamstrahlung.lower()
                )
                self.key4hepScript += "_BST" + self.procinfo.beamstrahlung.lower()

        # take care of the extensions of the filenames
        self.GeneratorDatacardName = (
            self.GeneratorDatacardBase + "." + self.inputFileExtension
        )
        self.key4hepScript += ".sh"

        # composition of file+directory
        self.GeneratorDatacard = f"{self.outdir}/{self.GeneratorDatacardName}"

        # three types of global variables for the file content
        self.datacardContent = ""
        self.key4hepContent  = ""
        self.analysisContent = "" 
        
        # the KEY4HEP environment setup is independent of the generator, so we can prepare it at the initialization stage:
        self.prepare_key4hepScript()
        
        # the analysis depends only on the process, not on the generator, so we can prepare it at the initialization stage:
        self.prepare_analysisContent()


    def add2generatorDatacard(self,content):
        # data encapsulation: add to the content in the base class
        self.datacardContent += content
       
    def prepare_key4hepScript(self):
        # set up for key4hep run of event generation
        key4hep_config = "#!/usr/bin/env bash\n"
        key4hep_config += 'if [ -z "${KEY4HEP_STACK}" ]; then\n'
        key4hep_config += (
            "    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh\n"
        )
        key4hep_config += "fi\n\n"
        # store it
        self.add2key4hepScript(key4hep_config)

    def add2key4hepScript(self,content):
        # data encapsulation: add to the content in the base class
        self.key4hepContent += content
        
    def prepare_analysisContent(self):
        
        # write the EDM4HEP analysis part based on the final state
        analysis = "\n"
        finalStateList = [int(pdg) for pdg in self.procinfo.get_final_pdg().split(" ")]
        if len(finalStateList) == 2:
            analysis += "$K4GenBuildDir/bin/analyze2f -a {0} -b {1} -i {2}.edm4hep -o {2}.root\n".format(
                finalStateList[0], finalStateList[1], self.GeneratorDatacardBase
            )

        # write the RIVET analysis
        if self.settings.IsRivet():
            yodaout = self.settings.yodaoutput + f"/{self.procinfo.get('procname')}.yoda"
            analysis += f"rivet" 
            for ana in self.settings.analysisname:
                analysis += f" -a {ana}"
            analysis+=f" -o {yodaout} {self.procinfo.get('procname')}.{self.procinfo.get('output_format')}\n"
            
        self.analysisContent = analysis
        
    def write_GeneratorDatacard(self, content):
        with open(self.GeneratorDatacard, "w+") as file:
            file.write(content)

    def write_Key4hepScript(self, content):
        # append the analysis to the content
        content += self.analysisContent
        # open the file for the evgen generation in EDM4HEP format
        with open(self.key4hepScript, "w+") as file:
            # set up KEY4HEP
            file.write(self.key4hepContent)
            # the generator specific part
            file.write(content)
        # make the script executable
        os.chmod(self.key4hepScript, os.stat(self.key4hepScript).st_mode | stat.S_IEXEC)
