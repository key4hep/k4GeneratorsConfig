from .ProcDBBase import ProcDBBase

class WhizardProcDB(ProcDBBase):
    """WhizardProcDB class"""

    def __init__(self, process):
        super().__init__(process)
        self.process = process

    def execute(self):
        # choose as function of generatorDBLabel
        label = self.process.get_generatorDBLabel()
        if label == "11_11_23_25":
            self.write_ZH()

    def write_ZH(self):
        self.rundict['?resonance_history'] = "true\n"
        self.rundict['resonance_on_shell_limit'] = 16
        self.rundict['resonance_on_shell_turnoff'] = 2
        self.rundict['resonance_on_shell_turnoff'] = 2

