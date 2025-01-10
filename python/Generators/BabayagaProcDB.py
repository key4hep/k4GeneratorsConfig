from .ProcDBBase import ProcDBBase

class BabayagaProcDB(ProcDBBase):
    """BabayagaProcDB class"""

    def __init__(self, process):
        super().__init__(process)
        self.process = process

    def write_DBInfo(self):
        # choose as function of generatorDBLabel
        label = self.process.get_generatorDBLabel()
        if label == "11_11_11_11":
            self.write_Difermion()
        if label == "11_11_13_13":
            self.write_Difermion()
        if label == "11_11_22_22":
            self.write_Diphoton()

    def write_Difermion(self):
        self.runout = ""

    def write_Diphoton(self):
        self.runout = ""

    def get_run_out(self):
        return self.runout

    def get_proc_out(self):
        return self.procout

    def remove_option(self, opt):
        lines = self.runout.split("\n")
        filter_lines = [line for line in lines if opt not in line]
        self.runout = "\n".join(filter_lines)
