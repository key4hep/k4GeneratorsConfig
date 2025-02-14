class ReleaseSpec:
    require_args = ["name", "value"]

    def __init__(self, name, value):
        args = (name, value)
        for i, prop in enumerate(self.require_args):
            setattr(self, prop, args[i])
        # keep a global list of parameters
        self.updateList(name)

    @staticmethod
    def set_info(name, value):
        for _, v in globals().items():
            if isinstance(v, ReleaseSpec) and v.name == name:
                v.value = value

    @staticmethod
    def get_info(name):
        for _, v in globals().items():
            if isinstance(v, ReleaseSpec) and v.name == name:
                return v
        raise ValueError(f"Could not find ReleaseSpec with name {name}")

    @staticmethod
    def updateList(name):
        for o,v in globals().items():
            if o=="ReleaseSpecsList" and isinstance(v, list):
                v.append(name)

# list of required parameters
ReleaseSpecsList = []

#default parameter and mass values

key4hepUseNightlies = ReleaseSpec(
    name="key4hepUseNightlies",
    value=False,
)

key4hepReleaseDate = ReleaseSpec(
    name="key4hepReleaseDate",
    value=None,
)

