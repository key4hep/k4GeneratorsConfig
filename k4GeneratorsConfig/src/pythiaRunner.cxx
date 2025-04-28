// main07.cc is a part of the PYTHIA event generator.
// Copyright (C) 2024 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// Keywords: two-body decay; astroparticle; python; matplotlib

// Illustration how to generate various two-body channels from
// astroparticle processes, e.g. neutralino annihilation or decay.
// To this end a "blob" of energy is created with unit cross section,
// from the fictitious collision of two non-radiating incoming e+e-.
// In the accompanying main29.cmnd file the decay channels of this
// blob can be set up. Furthermore, only gamma, e+-, p/pbar and
// neutrinos are stable, everything else is set to decay.
// (The "single-particle gun" of main21.cc offers another possible
// approach to the same problem.)
// Also illustrated output to be plotted by Python/Matplotlib/pyplot.

#include "Pythia8/Pythia.h"
#include "Pythia8Plugins/HepMC3.h"
#include <unistd.h>

#include "pythiaUserHooks.h"

using namespace Pythia8;

//==========================================================================

int main(int argc, char** argv) {
  // usage
  std::string usage = "Usage: pythiaRunner -h -f filename";
  
  // read the options
  std::string filename = "Pythia.dat";
  int c;
  while ((c = getopt(argc, argv, "f:")) != -1)
    switch (c) {
    case 'f':
      filename = optarg;
      break;
    case 'h':
      std::cout << usage << std::endl;
      std::cout << "-h: print this help" << std::endl;
      std::cout << "-f filename: file containing the pythia commands" << std::endl;
      exit(0);
    default:
      std::cerr << "pythiaRunner::Error: unknown argument " << char(c) << std::endl;
      std::cerr << usage << std::endl;
      exit(1);
    }
  // check existence of the file:
  std::ifstream infile(filename);
  if (infile.fail()) {
    std::cout << "pythiaRunner:: input file with name " << filename << " not found. Exiting" << std::endl;
    exit(0);
  }

  // Pythia generator.
  Pythia pythia;
  // add the write hepmc flag to the settings
  pythia.settings.addFlag("Main:writeHepMC", false);
  pythia.settings.addWord("Main:HepMCFile", "pythia");
  pythia.settings.addWord("Main:SelectorsFile", "PythiaSelectors");
  // Read in the rest of the settings and data from a separate file.
  pythia.readFile(filename);

  // setup the Userhooks for PYTHIA
  const std::string selectorFile = pythia.word("Main:SelectorsFile");
  auto pythiaUserHooksPtr = make_shared<pythiaUserHooks>(selectorFile);
  bool success = pythia.setUserHooksPtr(pythiaUserHooksPtr);
  if (!success)
    std::cout << "WARNING::pythiaRunner::setting of UserHooks was unsuccessful: " << std::endl;

  // Initialization.
  pythia.init();

  // check for hepmc
  const bool hepmc = pythia.flag("Main:writeHepMC");
  const std::string hepmcFile = pythia.word("Main:HepMCFile");
  std::cout << "HEPMC file name is " << hepmcFile << std::endl;
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

      if (++iAbort < nAbort)
        continue;
      cout << " Event generation aborted prematurely, owing to error!\n";
      break;
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

/*! derived from main07.cmnd.
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
