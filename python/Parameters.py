# Based on Feynrules and UFO formats


class Parameter:
    require_args = ["name", "value", "isParticleProperty", "texname"]

    def __init__(self, name, value, isParticleProperty, texname):
        args = (name, value, isParticleProperty, texname)
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
    isParticleProperty=False,
    texname="\\text{aEWM1}"
)

alphaEMMZ = Parameter(
    name="alphaEMMZ",
    value=1/alphaEMMZM1.value,
    isParticleProperty=False,
    texname="\\alpha _{\\text{EW}}"
)

alphaEMEWSchemeM1 = Parameter(
    name="alphaEMEWSchemeM1",
    value=1.325070e+02,
    isParticleProperty=False,
    texname="\\text{aEWEWSchemeM1}"
)

alphaEMEWScheme = Parameter(
    name="alphaEMEWScheme",
    value=1/alphaEMEWSchemeM1.value,
    isParticleProperty=False,
    texname="\\alpha _{\\text{EW EWScheme}}"
)

alphaEMM1 = Parameter(
    name="alphaEMM1",
    value=137.035999139,
    isParticleProperty=False,
    texname="\\text{aEW,Q=0,M1}"
)

alphaEM = Parameter(
    name="alphaEM",
    value=1/alphaEMM1.value,
    isParticleProperty=False,
    texname="\\alpha _{\\text{EW,Q=0}}"
)

GFermi = Parameter(
    name="GFermi",
    value=0.0000116637,
    isParticleProperty=False,
    texname="G_f"
)

sin2theta = Parameter(
    name="sin2theta",
    value=0.23155,
    isParticleProperty=False,
    texname="sin ^{2}\\theta"
)

sin2thetaEff = Parameter(
    name="sin2thetaEff",
    value=0.23155,
    isParticleProperty=False,
    texname="sin ^{2}\\theta _{Eff}"
)

alphaSMZ = Parameter(
    name="alphaSMZ",
    value=0.1184,
    isParticleProperty=False,
    texname="\\alpha _s"
)

VEV = Parameter(
    name="VEV",
    value=246,
    isParticleProperty=False,
    texname="\\text{vev}"
)

MZ = Parameter(
    name="MZ",
    value=91.1876,
    isParticleProperty=True,
    texname="\\text{MZ}"
)

WZ = Parameter(
    name="WZ",
    value=2.4952,
    isParticleProperty=True,
    texname="\\text{WZ}"
)

MW = Parameter(
    name="MW",
    value=80.379,
    isParticleProperty=True,
    texname="M_W"
)

WW = Parameter(
    name="WW",
    value=2.085,
    isParticleProperty=True,
    texname="\\text{WW}"
)

MB = Parameter(
    name="MB",
    value=4.7,
    isParticleProperty=True,
    texname="\\text{MB}"
)

ymb = Parameter(
    name="ymb",
    value=MB.value/VEV.value,
    isParticleProperty=True,
    texname="\\text{ymb}"
)

MT = Parameter(
    name="MT",
    value=172,
    isParticleProperty=True,
    texname="\\text{MT}"
)

WT = Parameter(
    name="WT",
    value=1.50833649,
    isParticleProperty=True,
    texname="\\text{WT}"
)

ymt = Parameter(
    name="ymt",
    value=MT.value/VEV.value,
    isParticleProperty=True,
    texname="\\text{ymt}"
)

MH = Parameter(
    name="MH",
    value=125,
    isParticleProperty=True,
    texname="\\text{MH}"
)

WH = Parameter(
    name="WH",
    value=0.00407,
    isParticleProperty=True,
    texname="\\text{WH}"
)


MU_R = Parameter(
    name="MU_R",
    value=91.188,
    isParticleProperty=False,
    texname="\\text{\\mu_r}"
)

