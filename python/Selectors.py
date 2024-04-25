import math

class Selectors():
    """Selector Class"""
    def __init__(self, name, selector):
        self.name = name
        self.LoadSelector(selector)

    def LoadSelector(self, selector):
        for key,value in selector.items():
            setattr(self, key.lower(), value)

    def get_Flavours(self):
        try:
            return getattr(self, "flavour")
        except:
            print(f"No Flavour found in selector {self.name}")

    def get_Max(self):
        try:
            return getattr(self, "max")
        except:
            print(f"No maximum found in selector {self.name}.")

    def get_Min(self):
        try:
            return getattr(self, "min")
        except:
            print(f"No minimum found in selector {self.name}")

    def get_unit(self):
        try:
            return getattr(self, "unit")
        except:
            return ""

    def get_MinMax(self):
        return self.get_Min(), self.get_Max()

    def Transform2Eta(self):
        # do nothing if we are at the right unit
        if self.get_unit() == "eta":
            return
        elif self.get_unit() == "rad" or self.get_unit() == "deg":
            self.Theta2Eta()

    def Transform2Rad(self):
        # do nothing if we are at the right unit
        if self.get_unit() == "rad":
            return
        elif self.get_unit() == "deg":
            self.Deg2Rad()
        elif self.get_unit() == "eta":
            self.Eta2Theta()

    def Transform2Deg(self):
        # do nothing if we are at the right unit
        if self.get_unit() == "deg":
            return
        elif self.get_unit() == "rad":
            self.Rad2Deg()
        elif self.get_unit() == "eta":
            self.Eta2Theta()
            self.Rad2Deg()

    def Rad2Deg(self):
        # do nothing if we are at the right unit
        if self.get_unit() == "deg" or self.get_unit() == "eta":
            return
        # convert rad to deg
        angleMin = self.get_Min()*180./math.pi
        angleMax = self.get_Max()*180./math.pi
        setattr(self, "min", angleMin)
        setattr(self, "max", angleMax)
        self.unit = "deg"

    def Deg2Rad(self):
        if self.get_unit() == "rad" or self.get_unit() == "eta":
            return
        # deg to rad
        angleMin = self.get_Min()*math.pi/180.
        angleMax = self.get_Max()*math.pi/180.
        setattr(self, "min", angleMin)
        setattr(self, "max", angleMax)
        setattr(self,"unit","rad")

    def Theta2Eta(self):
        # ensure that we are in radians
        self.Deg2Rad()
        # convert from theta to eta (min/max exchange)
        thetaMin = self.get_Min()
        thetaMax = self.get_Max()
        etaMax = -math.log(math.tan(thetaMin/2.))
        etaMin = -math.log(math.tan(thetaMax/2.))
        setattr(self, "max", etaMax)
        setattr(self, "min", etaMin)
        setattr(self,"unit","eta")

    def Eta2Theta(self):
        # convert from theta to eta (min/max exchange)
        etaMin = self.get_Min()
        etaMax = self.get_Max()
        thetaMax = 2.*math.atan(math.exp(-etaMin))
        thetaMin = 2.*math.atan(math.exp(-etaMax))
        setattr(self, "max", thetaMax)
        setattr(self, "min", thetaMin)
        setattr(self,"unit","rad")
