from .ProcDBBase import ProcDBBase

class BabayagaProcDB(ProcDBBase):
    """BabayagaProcDB class"""

    def __init__(self, process):
        super().__init__(process)
        self.process = process

    def execute(self):
        # not used by Babayaga
        pass
