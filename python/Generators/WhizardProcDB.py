import copy
from .ProcDBBase import ProcDBBase

class WhizardProcDB(ProcDBBase):
    """WhizardProcDB class"""

    def __init__(self, process):
        super().__init__(process)
        self.process = process

    def execute(self):
        # choose as function of DBTag
        tag   = copy.deepcopy(self.process.get_DBTag())
        # allow for e+e- and mu+mu- initial state
        if tag[0] == [-11.11] or tag[0] == [-13,13]:
            tag[0] = [-11,11]
        # process specific settings
        if tag == [ [-11,11], [23,25]]:
            self.write_ZH()

    def write_ZH(self):
        self.rundict['?resonance_history'] = "true\n"
        self.rundict['resonance_on_shell_limit'] = 16
        self.rundict['resonance_on_shell_turnoff'] = 2
        self.rundict['resonance_on_shell_turnoff'] = 2

