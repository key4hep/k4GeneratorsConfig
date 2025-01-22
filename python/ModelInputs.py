class ModelInputs:
    """A Standard Model Input"""

    def __init__(self):

        # define the variables
        self.m_couplings = {}
        self.m_masses    = {}
        self.m_widths    = {}

        # now the default definitions
        couplings    = ["alphaEM-1(MZ)", "GFermi", "alphaS(MZ)MSbar"]
        couplingsVal = [128.9, 1.2e-6, 0.119]

        massesName = ["MZPole", "MWPole", "MbMbMSbar", "MTPole", "MTauPole", "MHiggsPole"]
        massesPDG  = [23, 24, 5, 6, 15, 25]
        massesVal  = [91.19, 80.305, 4.25, 172.5, 1.777, 125.]

        widthsName = ["HiggsWidth", "ZWidth", "WWidth"]
        widthsPDG  = [25, 23, 24]
        widthsVal  = [0.0045, 2.5, 2.0]

        # add them to the structure:
        if len(couplings) == len(couplingsVal):
            for name,val in zip(couplings, couplingsVal):
                self.m_couplings[name] = val
        else:
            print("ModelInputs unequal vector sizes for couplings")
            print("Standard couplings not used")
            

        if len(massesName) == len(massesPDG) == len(massesVal):
            for pdg,val in zip(massesPDG, massesVal):
                self.m_masses[pdg] = val
        else:
            print("ModelInputs unequal vector sizes for masses")
            print("Standard masses not used")

        if len(widthsName) == len(widthsPDG) == len(widthsVal):
            for pdg,val in zip(widthsPDG, widthsVal):
                self.m_widths[pdg] = val
        else:
            print("ModelInputs unequal vector sizes for widths")
            print("Standard widths not used")


    def getParticleData(self,userParticleData):

        particleData = {}
        # create the particle data from the standard input
        for pdg, mass in self.m_masses.items():
            particleData[pdg] = dict(mass=mass,width=0)
        # we might have widths defined, but not the mass
        for pdg, width in self.m_widths.items():
            if pdg in particleData:
                particleData[pdg]["width"] = width
            else:
                particleData[pdg] = dict(mass=0,width=width)

        for pdg in userParticleData:
            # check if the particle is already there, if not create the dict
            mass  = userParticleData[pdg].get("mass",0.)
            width = userParticleData[pdg].get("width",0.)
            if pdg in particleData:
                particleData[pdg]["mass"]  = mass
                particleData[pdg]["width"] = width 
            else:
                particleData[pdg] = dict(mass=mass,width=width)

        return particleData

    def print(self):
        
        # printing using For Loop
        for key, value in self.m_couplings.items():
            print(f"{key}: {value}")

        # printing using For Loop
        for key, value in self.m_masses.items():
            print(f"{key}: {value}")

        # printing using For Loop
        for key, value in self.m_widths.items():
            print(f"{key}: {value}")

