// k4GeneratorsConfig
#include "pythiaUserHooks.h"

// Pythia8
#include "Pythia8/Pythia.h"
#include "Pythia8Plugins/HepMC3.h"
#include <unistd.h>

// std
#include <string>

// *nix
#include <unistd.h>

int main(int argc, char** argv) {
  // Default values for the command-line arguments
  std::string pythiaCmdFilePath = "Pythia.dat";
  bool verbose = false;

  // Read the command-line arguments
  int c;
  while ((c = getopt(argc, argv, "f:vh")) != -1) {
    switch (c) {
    case 'f':
      pythiaCmdFilePath = std::string(optarg);
      break;
    case 'v':
      verbose = true;
      break;
    case 'h':
    default:
      std::cout << "Usage: pythiaRunner [-h, -v] -f FILEPATH\n"
                << "  -h: print this help and exit\n"
                << "  -v: more verbose output\n"
                << "  -f FILEPATH: file containing the Pythia commands" << std::endl;

      exit(0);
    }
  }

  // Print input/output filepaths
  if (verbose) {
    std::cout << "pythiaRunner::INFO: Input Pythia command file: " << pythiaCmdFilePath << std::endl;
  }

  // Check if the Pythia file can be read
  {
    std::ifstream infile(pythiaCmdFilePath);
    if (!infile.good()) {
      std::cout << "pythiaRunner::ERROR: Input Pythia command file with name \"" << pythiaCmdFilePath
                << "\" cannot be read!\n"
                << "                     Exiting..." << std::endl;
      exit(1);
    }
    infile.close();
  }

  // Pythia generator
  Pythia8::Pythia pythia;

  // Add the write HepMC flag to the settings
  pythia.settings.addFlag("Main:writeHepMC", false);
  pythia.settings.addWord("Main:HepMCFile", "pythia");
  pythia.settings.addWord("Main:SelectorsFile", "PythiaSelectors");

  // Read in the rest of the settings and data from a separate file
  pythia.readFile(pythiaCmdFilePath);

  // setup the Userhooks for PYTHIA
  const std::string selectorFile = pythia.word("Main:SelectorsFile");
  auto pythiaUserHooksPtr = make_shared<pythiaUserHooks>(selectorFile);
  bool success = pythia.setUserHooksPtr(pythiaUserHooksPtr);
  if (!success) {
    std::cout << "WARNING::pythiaRunner::setting of UserHooks was unsuccessful!" << std::endl;
  }

  // Initialization
  pythia.init();

  // Check for HepMC output
  const bool hepmc = pythia.flag("Main:writeHepMC");
  const std::string hepmcFile = pythia.word("Main:HepMCFile");
  if (verbose) {
    std::cout << "pythiaRunner::INFO: File path of the output HepMC file is \"" << hepmcFile << "\"" << std::endl;
  }
  Pythia8::Pythia8ToHepMC ToHepMC;
  if (hepmc)
    ToHepMC.setNewFile(hepmcFile);

  // Extract settings to be used in the main program.
  int nEvent = pythia.mode("Main:numberOfEvents");
  int nAbort = pythia.mode("Main:timesAllowErrors");

  // Begin event loop.
  int iAbort = 0;
  for (int iEvent = 0; iEvent < nEvent; ++iEvent) {
    // Generate events. Quit if many failures.
    if (!pythia.next()) {
      if (++iAbort < nAbort) {
        continue;
      }

      std::cout << "pythiaRunner::ERROR: Event generation aborted prematurely, owing to error!\n"
                << "                     Aborting..." << std::endl;
      exit(1);
    }

    // event was ok, write to hepmc file
    if (hepmc) {
      ToHepMC.writeNextEvent(pythia);
    }
    // End of event loop.
  }

  // Final statistics.
  pythia.stat();

  // Done.
  return 0;
}

/*
! derived from main07.cmnd.
! This file contains commands to be read in for a Pythia8 run.
! Lines not beginning with a letter or digit are comments.

! 1) Settings used in the main program.
Main:numberOfEvents = 1000         ! number of events to generate
Main:timesAllowErrors = 5          ! allow a few failures before quitting

! 2) Settings related to output in init(), next() and stat().
Init:showChangedSettings = on      ! list changed settings
Init:showChangedParticleData = on  ! list changed particle data
Next:numberCount = 100             ! print message every n events
Next:numberShowInfo = 1            ! print event information n times
Next:numberShowProcess = 1         ! print process record n times
Next:numberShowEvent = 1           ! print event record n times

! 3) Beam parameter settings. Incoming beams do not radiate.
Beams:idA = -11                    ! ficititious incoming e+
Beams:idB = 11                     ! ficititious incoming e-
PDF:lepton = off                   ! no radiation off ficititious e+e-
Beams:eCM = 500.                   ! CM energy of collision

! 4) Tell that also long-lived should decay.
13:mayDecay   = true                 ! mu+-
211:mayDecay  = true                 ! pi+-
321:mayDecay  = true                 ! K+-
130:mayDecay  = true                 ! K0_L
2112:mayDecay = true                 ! n
*/
