// main07.cc is a part of the PYTHIA event generator.
// Copyright (C) 2024 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// Keywords: two-body decay; astroparticle; python; matplotlib

#include "Pythia8/Pythia.h"
#include "Pythia8Plugins/HepMC3.h"
#include <unistd.h>

using namespace Pythia8;

//==========================================================================

int main(int argc, char** argv) {

  // read the options
  std::string filename = "Pythia.dat";
  std::string lhefilename = "Pythia.lhe";
  std::string hepmcFile = "Pythia.hepmc";
  int c;
  while ((c = getopt(argc, argv, "f:l:o:")) != -1)
    switch (c) {
    case 'f':
      filename = optarg;
      break;
    case 'l':
      lhefilename = optarg;
      break;
    case 'o':
      hepmcFile = optarg;
      break;
    case 'h':
      std::cout << "Usage: pythiaLHERunner -h -f filename -l filename" << std::endl;
      std::cout << "-h: print this help" << std::endl;
      std::cout << "-f filename: input file containing the pythia commands" << std::endl;
      std::cout << "-l filename: input file containing the LHE events" << std::endl;
      std::cout << "-o filename: output file containing the hepmc events" << std::endl;
      exit(0);
    default:
      exit(0);
    }
  // check existence of the file:
  std::ifstream infile(filename);
  if (infile.fail()) {
    std::cout << "pythiaLHERunner:: input file with name " << filename << " not found. Exiting" << std::endl;
    exit(0);
  }

  // check existence of the file:
  std::ifstream inLHEfile(filename);
  if (inLHEfile.fail()) {
    std::cout << "pythiaLHERunner:: input file with name " << lhefilename << " not found. Exiting" << std::endl;
    exit(0);
  }
  // Pythia generator.
  Pythia pythia;
  // add the write hepmc flag to the settings
  pythia.settings.addFlag("Main:writeHepMC", false);
  // Read in the rest of the settings and data from a separate file.
  pythia.readFile(filename);

  // check for hepmc
  const bool hepmc = pythia.flag("Main:writeHepMC");
  std::cout << "HEPMC file name is " << hepmcFile << std::endl;
  Pythia8::Pythia8ToHepMC ToHepMC;
  if (hepmc)
    ToHepMC.setNewFile(hepmcFile);

  // this is the command to tell PYTHIA where to find the lhe file
  std::stringstream ss;
  ss << "Beams:LHEF = " << lhefilename;
  std::cout << "pythiaLHERunner:: LHE file is " << ss.str() << std::endl;
  pythia.readString(ss.str());

  // If Pythia fails to initialize, exit with error.
  if (!pythia.init()) {
    std::cout << "pythiaLHERunner:: failed to initialize Pythia after reading event" << std::endl;
    exit(0);
  }

  int nEvent = pythia.mode("Main:numberOfEvents");
  int nAbort = pythia.mode("Main:timesAllowErrors");

  // Begin infinite event loop - to be exited at end of file.
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
        //  xsecptr = make_shared<HepMC3::GenCrossSection>();
        //  ToHepMC.getEventPtr()->set_cross_section(xsecptr);
        //}
        // correction the cross section by trial and attempts (temporary fix)
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
        break;
      }

      if (++iAbort >= nAbort) {
        std::cout << " Event generation aborted prematurely at event " << iEvent << std::endl;
        std::cout << " LHA input:" << std::endl;
        pythia.LHAeventList();
        break;
      }
    }
    // End of event loop.
  }
  // Final statistics.
  pythia.stat();

  // Done.
  return 0;
}
