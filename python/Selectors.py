import math


class Selectors:
    """Selector Class"""

    def __init__(self, process, name, selector):
        # define the standard names for single and double applications
        self.oneParticleKeys = ["pt", "et", "energy", "rap", "eta", "theta"]
        self.twoParticleKeys = ["mass", "angle", "deltaeta", "deltarapidity", "deltaphi", "deltar"]
        
        self.process = process
        self.name = name
        self.NParticle = 0
        self.LoadSelector(selector)
        self.CalculateAllOutputs()

    def LoadSelector(self, selector):
        if selector:
            for key, value in selector.items():
                setattr(self, key.lower(), value)
            # in addition to the user settings keep the number of particles
            if self.name.lower() in self.oneParticleKeys:
                self.NParticle = 1
            if self.name.lower() in self.twoParticleKeys:
                self.NParticle = 2

    def CalculateAllOutputs(self):
        # do something only for these units:
        unitmap = {"deg", "rad", "eta"}
        if self.get_unit() in unitmap:
            # first copy the stuff:
            min = 0.0
            max = 0.0
            try:
                min = getattr(self, "min")
            except:
                min = 0.0
            setattr(self, "min" + self.get_unit(), min)
            try:
                max = getattr(self, "max")
            except:
                max = 0.0
            setattr(self, "max" + self.get_unit(), max)
            # now take care of the rest:
            if self.get_unit() == "deg":
                self.Deg2Rad()
                self.Deg2Eta()
            elif self.get_unit() == "rad":
                self.Rad2Deg()
                self.Rad2Eta()
            elif self.get_unit() == "eta":
                self.Eta2Deg()
                self.Eta2Rad()

    def get_Flavours(self):
        try:
            return getattr(self, "flavour")
        except:
            print(f"No Flavour found in selector {self.name}")

    def get_Max(self, unit=""):
        try:
            maximum = getattr(self, "max" + unit)
            if unit == "eta":
                return format(maximum, ".8f")
            else:
                return maximum
        except:
            return format(1e6, "1.3f")
            # print(f"No maximum found in selector {self.name}.")

    def get_Min(self, unit=""):
        try:
            minimum = getattr(self, "min" + unit)
            if unit == "eta":
                return format(minimum, ".8f")
            else:
                return minimum
        except:
            return format(-1e6, "1.3f")
            # print(f"No minimum found in selector {self.name}")

    def get_unit(self):
        try:
            return getattr(self, "unit")
        except:
            return ""

    def get_MinMax(self, unit=""):
        return self.get_Min(unit), self.get_Max(unit)

    def Rad2Deg(self):
        # convert rad to deg
        angleMin = self.get_Min() * 180.0 / math.pi
        angleMax = self.get_Max() * 180.0 / math.pi
        setattr(self, "mindeg", angleMin)
        setattr(self, "maxdeg", angleMax)

    def Rad2Eta(self):
        # convert from theta to eta (min/max exchange)
        thetaMin = self.get_Min()
        thetaMax = self.get_Max()
        etaMax = -math.log(math.tan(thetaMin / 2.0))
        etaMin = -math.log(math.tan(thetaMax / 2.0))
        setattr(self, "maxeta", etaMax)
        setattr(self, "mineta", etaMin)

    def Deg2Rad(self):
        # deg to rad
        angleMin = self.get_Min() * math.pi / 180.0
        angleMax = self.get_Max() * math.pi / 180.0
        setattr(self, "minrad", angleMin)
        setattr(self, "maxrad", angleMax)

    def Deg2Eta(self):
        # deg to rad
        self.Deg2Rad()
        angleMin = self.get_Min("rad")
        angleMax = self.get_Max("rad")
        etaMax = -math.log(math.tan(angleMin / 2.0))
        etaMin = -math.log(math.tan(angleMax / 2.0))
        setattr(self, "mineta", etaMin)
        setattr(self, "maxeta", etaMax)

    def Eta2Rad(self):
        # convert from theta to eta (min/max exchange)
        etaMin = self.get_Min()
        etaMax = self.get_Max()
        thetaMax = 2.0 * math.atan(math.exp(-etaMin))
        thetaMin = 2.0 * math.atan(math.exp(-etaMax))
        setattr(self, "maxrad", thetaMax)
        setattr(self, "minrad", thetaMin)

    def Eta2Deg(self):
        # convert from theta to eta (min/max exchange)
        self.Eta2Rad()
        thetaMin = self.get_Min("rad") * 180.0 / math.pi
        thetaMax = self.get_Max("rad") * 180.0 / math.pi
        setattr(self, "maxdeg", thetaMax)
        setattr(self, "mindeg", thetaMin)
