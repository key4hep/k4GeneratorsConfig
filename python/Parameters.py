# Based on Feynrules and UFO formats


class Parameter:
    require_args = ["name", "value", "texname"]

    def __init__(self, name, value, texname):
        args = (name, value, texname)
        for i, name in enumerate(self.require_args):
            setattr(self, name, args[i])

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


#default parameter and mass values

alphaEMMZM1 = Parameter(
    name="alphaEMMZM1",
    value=127.9,
    texname="\\text{aEWM1}"
)

alphaEMMZ = Parameter(
    name="alphaEMMZ",
    value=1/alphaEMMZM1.value,
    texname="\\alpha _{\\text{EW}}"
)

GFermi = Parameter(
    name="GFermi",
    value=0.0000116637,
    texname="G_f"
)

sin2theta = Parameter(
    name="sin2theta",
    value=0.22339,
    texname="sin ^{2}\\theta"
)

sin2thetaEff = Parameter(
    name="sin2thetaEff",
    value=0.23155,
    texname="sin ^{2}\\theta"
)

alphaSMZ = Parameter(
    name="alphaSMZ",
    value=0.1184,
    texname="\\alpha _s"
)

VEV = Parameter(
    name="VEV",
    value=246,
    texname="\\text{vev}"
)

MZ = Parameter(
    name="MZ",
    value=91.1876,
    texname="\\text{MZ}"
)

WZ = Parameter(
    name="WZ",
    value=2.4952,
    texname="\\text{WZ}"
)

MW = Parameter(
    name="MW",
    value=80.379,
    texname="M_W"
)

WW = Parameter(
    name="WW",
    value=2.085,
    texname="\\text{WW}"
)

MB = Parameter(
    name="MB",
    value=4.7,
    texname="\\text{MB}"
)

ymb = Parameter(
    name="ymb",
    value=MB.value/VEV.value,
    texname="\\text{ymb}"
)

MT = Parameter(
    name="MT",
    value=172,
    texname="\\text{MT}"
)

WT = Parameter(
    name="WT",
    value=1.50833649,
    texname="\\text{WT}"
)

ymt = Parameter(
    name="ymt",
    value=MT.value/VEV.value,
    texname="\\text{ymt}"
)

MH = Parameter(
    name="MH",
    value=125,
    texname="\\text{MH}"
)

WH = Parameter(
    name="WH",
    value=0.00407,
    texname="\\text{WH}"
)


MU_R = Parameter(
    name="MU_R",
    value=91.188,
    texname="\\text{\\mu_r}"
)

