# Based on Feynrules and UFO formats


class Parameter:
    require_args = ["name", "value", "texname"]

    def __init__(self, name, value, texname):
        args = (name, value, texname)
        for i, name in enumerate(self.require_args):
            setattr(self, name, args[i])


# This is a default parameter object representing the renormalization scale (MU_R).
MU_R = Parameter(name="MU_R", value=91.188, texname="\\text{\\mu_r}")


aEWM1 = Parameter(name="aEWM1", value=127.9, texname="\\text{aEWM1}")


Gf = Parameter(name="GFermi", value=0.0000116637, texname="G_f")

aS = Parameter(name="aS", value=0.1184, texname="\\alpha _s")

ymb = Parameter(name="ymb", value=4.7, texname="\\text{ymb}")

ymt = Parameter(name="ymt", value=172, texname="\\text{ymt}")

MZ = Parameter(name="MZ", value=91.1876, texname="\\text{MZ}")

MT = Parameter(
    name="MT",
    value=172,
    texname="\\text{MT}",
)

MB = Parameter(
    name="MB",
    value=4.7,
    texname="\\text{MB}",
)

MH = Parameter(
    name="MH",
    value=125,
    texname="\\text{MH}",
)

WZ = Parameter(
    name="WZ",
    value=2.4952,
    texname="\\text{WZ}",
)

WW = Parameter(
    name="WW",
    value=2.085,
    texname="\\text{WW}",
)

WT = Parameter(
    name="WT",
    value=1.50833649,
    texname="\\text{WT}",
)

WH = Parameter(
    name="WH",
    value=0.00407,
    texname="\\text{WH}",
)

aEW = Parameter(name="aEW", value="1/aEWM1", texname="\\alpha _{\\text{EW}}")


MW = Parameter(name="MW", value=80.379, texname="M_W")


MH = Parameter(name="MH", value=125, texname="M_H")
