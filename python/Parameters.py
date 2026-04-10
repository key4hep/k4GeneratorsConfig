# Based on Feynrules and UFO formats


class Parameter:
    require_args = ["name", "value", "isParticleProperty"]

    def __init__(self, name, value, isParticleProperty):
        args = (name, value, isParticleProperty)
        for i, prop in enumerate(self.require_args):
            setattr(self, prop, args[i])
        # keep a global list of parameters
        self.updateList(name)

    @staticmethod
    def set_info(name, value):
        for _, v in globals().items():
            if isinstance(v, Parameter) and v.name == name:
                v.value = value

    @staticmethod
    def get_info(name):
        for _, v in globals().items():
            if isinstance(v, Parameter) and v.name == name:
                return v
        raise ValueError(f"Could not find Parameter with name {name}")

    @staticmethod
    def updateList(name):
        for o,v in globals().items():
            if o=="ParametersList" and isinstance(v, list):
                v.append(name)

# list of required parameters
ParametersList = []

#default parameter and mass values

alphaEMMZM1 = Parameter(
    name="alphaEMMZM1",
    value=127.9,
    isParticleProperty=False
)

alphaEMMZ = Parameter(
    name="alphaEMMZ",
    value=1/alphaEMMZM1.value,
    isParticleProperty=False
)

alphaEMLOM1 = Parameter(
    name="alphaEMLOM1",
    value=1.32184e+02,
    isParticleProperty=False
)

alphaEMLO = Parameter(
    name="alphaEMLO",
    value=1/alphaEMLOM1.value,
    isParticleProperty=False
)

alphaEMM1 = Parameter(
    name="alphaEMM1",
    value=137.035999139,
    isParticleProperty=False
)

alphaEM = Parameter(
    name="alphaEM",
    value=1/alphaEMM1.value,
    isParticleProperty=False
)

GFermi = Parameter(
    name="GFermi",
    value=0.0000116637,
    isParticleProperty=False
)

sin2thetaLO = Parameter(
    name="sin2thetaLO",
    value=0.223013,
    isParticleProperty=False
)

sin2theta = Parameter(
    name="sin2theta",
    value=0.23155,
    isParticleProperty=False
)

sin2thetaEff = Parameter(
    name="sin2thetaEff",
    value=0.23155,
    isParticleProperty=False
)

alphaSMZ = Parameter(
    name="alphaSMZ",
    value=0.1184,
    isParticleProperty=False
)

VEV = Parameter(
    name="VEV",
    value=246,
    isParticleProperty=False
)

MZ = Parameter(
    name="MZ",
    value=91.1876,
    isParticleProperty=True
)

WZ = Parameter(
    name="WZ",
    value=2.4952,
    isParticleProperty=True
)

MW = Parameter(
    name="MW",
    value=80.379,
    isParticleProperty=True
)

WW = Parameter(
    name="WW",
    value=2.085,
    isParticleProperty=True
)

MB = Parameter(
    name="MB",
    value=4.7,
    isParticleProperty=True
)

ymb = Parameter(
    name="ymb",
    value=MB.value/VEV.value,
    isParticleProperty=True
)

MT = Parameter(
    name="MT",
    value=172,
    isParticleProperty=True
)

WT = Parameter(
    name="WT",
    value=1.50833649,
    isParticleProperty=True
)

ymt = Parameter(
    name="ymt",
    value=MT.value/VEV.value,
    isParticleProperty=True
)

MH = Parameter(
    name="MH",
    value=125,
    isParticleProperty=True
)

WH = Parameter(
    name="WH",
    value=0.00407,
    isParticleProperty=True
)


MU_R = Parameter(
    name="MU_R",
    value=91.188,
    isParticleProperty=False
)

