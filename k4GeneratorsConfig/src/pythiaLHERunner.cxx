// Pythia8
#include "Pythia8/Pythia.h"
#include "Pythia8Plugins/HepMC3.h"

// std
#include <string>

// *nix
#include <unistd.h>

int main(int argc, char** argv) {
  // Default values for the command-line arguments
  std::string pythiaCmdFilePath = "Pythia.dat";
  std::string lheFilePath = "Pythia.lhe";
  std::string hepmcFilePath = "Pythia.hepmc";
  bool verbose = false;

  // Read the command-line arguments
  int opt;
  while ((opt = getopt(argc, argv, "f:l:o:vh")) != -1) {
    switch (opt) {
    case 'f':
      pythiaCmdFilePath = std::string(optarg);
      break;
    case 'l':
      lheFilePath = std::string(optarg);
      break;
    case 'o':
      hepmcFilePath = std::string(optarg);
      break;
    case 'v':
      verbose = true;
      break;
    case 'h':
    default:
      std::cout << "Usage: pythiaLHERunner [-h, -v] " << "-f FILEPATH -l FILEPATH [-o FILEPATH]\n"
                << "  -h: print this help and exit\n"
                << "  -v: more verbose output\n"
                << "  -f FILEPATH: input file containing the Pythia " << "commands\n"
                << "  -l FILEPATH: input file containing the LHE events\n"
                << "  -o FILEPATH: output file containing the HepMC events" << std::endl;

      exit(0);
    }
  }

  // Print input/output filepaths
  if (verbose) {
    std::cout << "pythiaLHErunner::INFO: Input Pythia commands file: " << pythiaCmdFilePath << "\n"
              << "      Input LHE events file: " << lheFilePath << "\n"
              << "      HepMC3 output filepath: " << hepmcFilePath << std::endl;
  }

  // Check if the Pythia file can be read
  {
    std::ifstream infile(pythiaCmdFilePath);
    if (!infile.good()) {
      std::cout << "pythiaLHErunner::ERROR: Input Pythia command file with " << "name \"" << pythiaCmdFilePath
                << "\" cannot be read!\n"
                << "                        Aborting..." << std::endl;
      exit(1);
    }
    infile.close();
  }

  // Check if the input LHE file can be read
  {
    std::ifstream inLHEfile(lheFilePath);
    if (!inLHEfile.good()) {
      std::cout << "pythiaLHErunner::ERROR: Input LHE file with name \"" << lheFilePath << "\" cannot be read!.\n"
                << "                        Aborting..." << std::endl;
      exit(1);
    }
    inLHEfile.close();
  }

  // Pythia generator
  Pythia8::Pythia pythia;
  // Add the write hepmc flag to the settings
  pythia.settings.addFlag("Main:writeHepMC", false);
  // Read in the rest of the settings and data from a separate file.
  pythia.readFile(pythiaCmdFilePath);

  // Check for HepMC
  const bool hepmc = pythia.flag("Main:writeHepMC");
  const std::string hepmcFilePathFromCmdFile = pythia.word("Main:HepMCFile");
  Pythia8::Pythia8ToHepMC ToHepMC;
  if (hepmc) {
    ToHepMC.setNewFile(hepmcFilePath);
  }

  // Adding the command to tell PYTHIA where to find the LHE file
  const std::string lheFilePathFromCmdFile = pythia.word("Beams:LHEF");
  std::string lheCmd = "Beams:LHEF = " + lheFilePath;
  pythia.readString(lheCmd);

  // If Pythia fails to initialize, exit with error.
  if (!pythia.init()) {
    std::cout << "pythiaLHErunner::ERROR: Failed to initialize Pythia8!\n"
              << "                        Aborting..." << std::endl;
    exit(1);
  }

  int nEvent = pythia.mode("Main:numberOfEvents");
  int nAbort = pythia.mode("Main:timesAllowErrors");

  // Begin event loop --- to be exited at end of file.
  int iAbort = 0;
  for (int iEvent = 0; iEvent < nEvent; ++iEvent) {
    // Generate event.
    if (pythia.next()) {
      // if (iEvent < 100) pythia.process.list();
      // if (iEvent < 100) pythia.event.list();
      //  event was ok, write to hepmc file
      if (hepmc) {
        // do it in one step:
        ToHepMC.writeNextEvent(pythia);
        // temporary correction:
        // ToHepMC.fillNextEvent(pythia);
        // now retrieve the cross section
        // auto xsecptr = ToHepMC.getEventPtr()->cross_section();
        // if ( !xsecptr ) {
        // double xsec    = pythia.info.sigmaGen() *pythia.info.nTried()/pythia.info.nAccepted() *1e9;
        // double xsecerr = 0.;
        // if ( xsecptr->xsec_errs().size() ){
        //  xsecerr = xsecptr->xsec_errs()[0];
        //}
        // xsecptr->set_cross_section(xsec, xsecerr);
        // now write the event:
        // ToHepMC.writeEvent();
      }

    } else {
      std::cout << "Event rejected " << std::endl;
      pythia.LHAeventList();
      std::cout << "End of rejected event" << std::endl;
      // Leave event loop if at end of file.
      if (pythia.info.atEndOfFile()) {
        std::cout << "pythiaLHERunner:: reached EOF at event " << iEvent << " when " << nEvent << " were expected"
                  << std::endl;
        exit(1);
      }

      if (++iAbort >= nAbort) {
        std::cout << " Event generation aborted prematurely at event " << iEvent << std::endl;
        std::cout << " LHA input:" << std::endl;
        pythia.LHAeventList();
        exit(1);
      }
    }
    // End of event loop.
  }
  // Final statistics.
  pythia.stat();

  // Done.
  if (!hepmc) {
    std::cout << "pythiaLHErunner::WARNING: HepMC output not allowed.\n"
              << "         To allow HepMC output make sure you have this line " << "in your Pythia command file:\n"
              << "           Main:writeHepMC = on" << std::endl;
  }

  if (lheFilePathFromCmdFile != lheFilePath) {
    std::cout << "Provided Pythia command file already specifies input LHE " << "file path \"" << lheFilePathFromCmdFile
              << "\"!";
  }

  if (hepmcFilePathFromCmdFile != hepmcFilePath) {
    std::cout << "Provided Pythia command file already specifies output HepMC " << "file path \""
              << hepmcFilePathFromCmdFile << "\"!";
  }

  // Done
  return 0;
}
