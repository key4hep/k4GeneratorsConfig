class CirceHelper:
    """CirceHelper class"""

    def __init__(self, accel, sqrts):
        self.File = "cepc240.circe"
        self.circeData = dict()

        self.addCEPCFile2DB('240', "cepc240.circe")
        self.addCEPCFile2DB('250', "cepc250.circe")

        self.addILCFile2DB('200', "ilc200ee_nobeamspread.circe")
        self.addILCFile2DB('230', "ilc230ee_nobeamspread.circe")
        self.addILCFile2DB('250', "250_SetA_ee024.circe")
        self.addILCFile2DB('350', "ilc350ee_nobeamspread.circe")
        self.addILCFile2DB('500', "ilc500ee_nobeamspread.circe")

        self.addCLICFile2DB( '350', "0.35TeVeeMapPB0.67E0.0Mi0.30.circe")
        self.addCLICFile2DB( '380', "0.38TeVeeMapPB0.67E0.0Mi0.30.circe")
        self.addCLICFile2DB( '500', "0.5TeVeeMapPB0.67E0.0Mi0.30.circe")
        self.addCLICFile2DB('1400', "1.4TeVeeMapPB0.67E0.0Mi0.15.circe")
        self.addCLICFile2DB('3000', "3TeVeeMapPB0.67E0.0Mi0.15.circe")

        self.fillFileName(accel.lower(), str(sqrts))

    def fillFileName(self, accel, sqrts):
        # check for presence of accelerator
        if accel in self.circeData.keys():
            filename = None
            for item in self.circeData[accel]:
                if sqrts in item.keys():
                    filename = item[sqrts]
            if filename is not None:
                self.File = filename
            else:
                self.printErrorExit(accel, sqrts, "sqrts not found in DB")
        else:
            self.printErrorExit(accel, sqrts, "accelerator not found in DB")

    def addCEPCFile2DB(self, sqrts, filename):
        self.addFile2DB('cepc', sqrts, filename)

    def addILCFile2DB(self, sqrts, filename):
        self.addFile2DB('ilc', sqrts, filename)

    def addCLICFile2DB(self, sqrts, filename):
        self.addFile2DB('clic', sqrts, filename)

    def addFile2DB(self, accel, sqrts, filename):
        # check for presence of accelerator
        if accel in self.circeData.keys():
            self.circeData[accel].append({sqrts : filename})
        else:
            self.circeData[accel] = [ {sqrts : filename}]

    def getFile(self):
        return self.File

    def printErrorExit(self, accel, sqrts, message):
        raise RuntimeError(f"CirceHelper::Cannot find settings for accelerator {accel} at sqrts= {sqrts} with message: {message}")
