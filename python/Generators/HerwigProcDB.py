import copy
from .ProcDBBase import ProcDBBase

class HerwigProcDB(ProcDBBase):
    """HerwigProcDB class"""

    def __init__(self, process):
        super().__init__(process)
        self.process = process

    def execute(self):
        # general stuff
        # choose as function of DBTag
        self.rundict['cd /Herwig/MatrixElements'] = " "
        tag = copy.deepcopy(self.process.get_DBTag())
        if tag[0] == [-11,11]:
            self.rundict['read snippets/EECollider.in'] = " "
        # allow for e+e- and mu+mu- initial state
        if tag[0] == [-11.11] or tag[0] == [-13,13]:
            tag[0] = [-11,11]
        # tag prepared compare
        if tag == [[-11,11],[-1,1]]:
            self.write_Difermion(1)
        elif tag == [[-11,11],[-2,2]]:
            self.write_Difermion(2)
        elif tag == [[-11,11],[-3,3]]:
            self.write_Difermion(3)
        elif tag == [[-11,11],[-4,4]]:
            self.write_Difermion(4)
        elif tag == [[-11,11],[-5,5]]:
            self.write_Difermion(5)
        elif tag == [[-11,11],[-12,12]]:
            self.write_Difermion(12)
        elif tag == [[-11,11],[-13,13]]:
            self.write_Difermion(13)
        elif tag == [[-11,11],[-14,14]]:
            self.write_Difermion(14)
        elif tag == [[-11,11],[-15,15]]:
            self.write_Difermion(15)
        elif tag == [[-11,11],[-16,16]]:
            self.write_Difermion(16)
        elif tag == [[-11,11],[23,23]]:
            self.write_WeakBosonPair(23)
        elif tag == [[-11,11],[24,24]]:
            self.write_WeakBosonPair(24)
        elif tag == [[-11,11],[23,25]]:
            self.write_run_ZH()
        elif tag == [[-11,11],[-12,12,25]]:
            self.write_run_Hnunu()
        else:
            print(f"WARNING: Process {tag} not implemented in HerwigProcDB")

    def write_Difermion(self, pdg):
        MatrixElement = None
        if pdg < 6:
            MatrixElement = "MEee2gZ2qq"
        elif pdg > 10 and pdg < 17:
            MatrixElement = "MEee2gZ2ll"

        # set the matrix element etc:
        if MatrixElement is not None:
            self.procdict['insert SubProcess:MatrixElements 0'] = MatrixElement
            self.procdict[f"set {MatrixElement}:MinimumFlavour"] = f"{pdg}"
            self.procdict[f"set {MatrixElement}:MaximumFlavour"] = f"{pdg}"

    def write_WeakBosonPair(self, pdg):
        MatrixElement = "MEee2VV"
        self.procdict['insert SubProcess:MatrixElements 0'] = MatrixElement
        self.procdict[f"set {MatrixElement}:MinimumFlavour"] = f"{pdg}"
        self.procdict[f"set {MatrixElement}:MaximumFlavour"] = f"{pdg}"
        
    def write_run_ZH(self):
        self.procdict['insert SubProcess:MatrixElements 0'] = "MEee2ZH"

    def write_run_Hnunu(self):
        self.procdict['insert SubProcess:MatrixElements 0'] = "MEee2HiggsVBF"
