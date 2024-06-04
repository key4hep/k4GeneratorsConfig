class CirceHelper():
    """CirceHelper class"""
    def __init__(self,accel,sqrts):

        self.File = "cepc240.circe"
        self.circeData = [ ("cepc",240), ("cepc",250), ("ilc",240), ("ilc",250), ("ilc",350), ("ilc",500),("clic",1000),("clic",1000)]

        self.calculateFile(accel,sqrts)

    def calculateFile(self,accel,sqrts):

        dbSqrts    = 0
        deltaSqrts = 9999999
        for item in self.circeData:
            if accel.lower() == item[0]:
                if abs(sqrts-item[1]) < deltaSqrts:
                    deltaSqrts = abs(sqrts-item[1])
                    dbSqrts    = item[1]
                    self.File = f"{accel.lower()}{dbSqrts}.circe"

    def getFile(self):
        return self.File
