import os, stat


class GeneratorBase:
    """GeneratorBase class"""

    def __init__(self, procinfo, settings, name, inputFileExtension):
        self.procinfo = procinfo
        self.settings = settings
        self.name = name
        self.inputFileExtension = inputFileExtension

        self.outdir = (
            f"{procinfo.get('OutDir')}/{self.name}/{self.procinfo.get('procname')}"
        )
        self.GeneratorDatacardBase = f"{self.procinfo.get('procname')}"
        self.key4hepScript = f"{self.outdir}/Run_{self.procinfo.get('procname')}"

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

        # set up for key4hep run of event generation
        self.key4hep_config = "#!/usr/bin/env bash\n"
        self.key4hep_config += 'if [ -z "${KEY4HEP_STACK}" ]; then\n'
        self.key4hep_config += (
            "    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh\n"
        )
        self.key4hep_config += "fi\n\n"

        self.analysis = self.write_analysis()

    def write_analysis(self):
        # write the analysis part based on the final state
        analysis = "\n"
        finalStateList = self.procinfo.get_final_pdg_list()
        if len(finalStateList) == 2:
            analysis += "$K4GenBuildDir/bin/analyze2f -a {0} -b {1} ".format(
                finalStateList[0], finalStateList[1]
            )
        else:
            return ""
        analysis += "-i {0}.edm4hep -o {0}.root\n".format(self.GeneratorDatacardBase)
        if self.settings.IsRivet():
            yodaout = self.settings.yodaoutput + f"/{self.procinfo.get('procname')}.yoda"
            analysis += f"rivet" 
            for ana in self.settings.analysisname:
                analysis += f" -a {ana}"
            analysis+=f" -o {yodaout} {self.procinfo.get('procname')}.{self.procinfo.get('output_format')}\n"
        return analysis

    def write_GeneratorDatacard(self, content):
        with open(self.GeneratorDatacard, "w+") as file:
            file.write(content)

    def write_Key4hepScript(self, content):
        # append the analysis to the content
        content += self.analysis
        # open the file for the evgen generation in EDM4HEP format
        with open(self.key4hepScript, "w+") as file:
            # set up KEY4HEP
            file.write(self.key4hep_config)
            # the generator specific part
            file.write(content)
        # make the script executable
        os.chmod(self.key4hepScript, os.stat(self.key4hepScript).st_mode | stat.S_IEXEC)
