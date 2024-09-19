import Parameters as Param


class Particle:
    """A standard Particle"""

    _required_args = [
        "pdg_code",
        "name",
        "antiname",
        "mass",
        "width",
        "texname",
        "antitexname",
    ]

    def __init__(
        self, pdg_code, name, antiname, mass, width, texname, antitexname, **options
    ):
        args = (pdg_code, name, antiname, mass, width, texname, antitexname)
        assert len(self._required_args) == len(args)

        for i, name in enumerate(self._required_args):
            setattr(self, name, args[i])

        for option, value in options.items():
            setattr(self, option, value)

    def get(self, name):
        return getattr(self, name)

    def set(self, name, value):
        setattr(self, name, value)

    def anti(self):
        out_dic = {}
        for k, v in self.__dict__.items():
            if k not in self._required_args:
                out_dic[k] = -v

        return Particle(
            -self.pdg_code,
            self.antiname,
            self.name,
            self.mass,
            self.width,
            self.antitexname,
            self.texname,
        )

    @staticmethod
    def set_info(pdg, info):
        for name, value in info.items():
            for _, v in globals().items():
                if isinstance(v, Particle) and v.pdg_code == pdg:
                    v.set(name, value)
                if isinstance(v, Particle) and v.has_anti() and v.pdg_code == -pdg:
                    v.set(name, value)

    @staticmethod
    def get_info(pdg):
        for _, v in globals().items():
            if isinstance(v, Particle) and v.pdg_code == pdg:
                return v
        raise ValueError("Could not find Particle with ID {}".format(pdg))

    def print_info(self):
        for name in self._required_args:
            print(name, self.get(name))

    def has_anti(self):
        return self.name != self.antiname

    def name_from_pdg(pdg):
        for _, v in globals().items():
            if isinstance(v, Particle) and v.pdg_code == pdg:
                return v.name
        print(f"{pdg} code not found")


a = Particle(
    pdg_code=22, name="a", antiname="a", mass=0, width=0, texname="a", antitexname="a"
)

Z = Particle(
    pdg_code=23,
    name="Z",
    antiname="Z",
    mass=Param.MZ.value,
    width=Param.WZ.value,
    texname="Z",
    antitexname="Z",
)

W__plus__ = Particle(
    pdg_code=24,
    name="W+",
    antiname="W-",
    spin=3,
    color=1,
    mass=Param.MW.value,
    width=Param.WW.value,
    texname="W+",
    antitexname="W-",
)
W__minus__ = W__plus__.anti()


g = Particle(
    pdg_code=21,
    name="g",
    antiname="g",
    mass=0,
    width=0,
    texname="g",
    antitexname="g",
)

ve = Particle(
    pdg_code=12,
    name="ve",
    antiname="ve~",
    spin=2,
    color=1,
    mass=0,
    width=0,
    texname="ve",
    antitexname="ve~",
)

ve__tilde__ = ve.anti()

vm = Particle(
    pdg_code=14,
    name="vm",
    antiname="vm~",
    mass=0,
    width=0,
    texname="vm",
    antitexname="vm~",
)

vm__tilde__ = vm.anti()

vt = Particle(
    pdg_code=16,
    name="vt",
    antiname="vt~",
    mass=0,
    width=0,
    texname="vt",
    antitexname="vt~",
)

vt__tilde__ = vt.anti()

e__minus__ = Particle(
    pdg_code=11,
    name="e-",
    antiname="e+",
    mass=0.0,
    width=0,
    texname="e-",
    antitexname="e+",
)

e__plus__ = e__minus__.anti()

mu__minus__ = Particle(
    pdg_code=13,
    name="mu-",
    antiname="mu+",
    mass=0,
    width=0,
    texname="mu-",
    antitexname="mu+",
)

mu__plus__ = mu__minus__.anti()

ta__minus__ = Particle(
    pdg_code=15,
    name="ta-",
    antiname="ta+",
    mass=0,
    width=0,
    texname="ta-",
    antitexname="ta+",
)

ta__plus__ = ta__minus__.anti()

u = Particle(
    pdg_code=2,
    name="u",
    antiname="u~",
    mass=0,
    width=0,
    texname="u",
    antitexname="u~",
)

u__tilde__ = u.anti()

c = Particle(
    pdg_code=4,
    name="c",
    antiname="c~",
    mass=0,
    width=0,
    texname="c",
    antitexname="c~",
)

c__tilde__ = c.anti()

t = Particle(
    pdg_code=6,
    name="t",
    antiname="t~",
    mass=Param.MT,
    width=Param.WT,
    texname="t",
    antitexname="t~",
)

t__tilde__ = t.anti()

d = Particle(
    pdg_code=1,
    name="d",
    antiname="d~",
    mass=0,
    width=0,
    texname="d",
    antitexname="d~",
)

d__tilde__ = d.anti()

s = Particle(
    pdg_code=3,
    name="s",
    antiname="s~",
    spin=2,
    color=3,
    mass=0,
    width=0,
    texname="s",
    antitexname="s~",
)

s__tilde__ = s.anti()

b = Particle(
    pdg_code=5,
    name="b",
    antiname="b~",
    spin=2,
    color=3,
    mass=Param.MB.value,
    width=0,
    texname="b",
    antitexname="b~",
)

b__tilde__ = b.anti()

H = Particle(
    pdg_code=25,
    name="H",
    antiname="H",
    mass=Param.MH.value,
    width=Param.WH.value,
    texname="H",
    antitexname="H",
)
