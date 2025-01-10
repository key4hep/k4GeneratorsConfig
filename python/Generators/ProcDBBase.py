import abc

class ProcDBBase(abc.ABC):
    """GeneratorBase class"""

    def __init__(self, procinfo):

        # general settings of the class
        self.procinfo = procinfo
        self.runout = ""
        self.procout = ""

    def write_DBInfo(self):
        return
        
    def get_run_out(self):
        return self.runout

    def get_proc_out(self):
        return self.procout

    def remove_option(self, opt):
        lines = self.runout.split("\n")
        filter_lines = [line for line in lines if opt not in line]
        self.runout = "\n".join(filter_lines)
