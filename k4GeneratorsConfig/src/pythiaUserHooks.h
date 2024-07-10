#ifndef K4GENERATORSCONFIG_PYTHIAUSERHOOKS_H
#define K4GENERATORSCONFIG_PYTHIAUSERHOOKS_H

#include "Pythia8/Pythia.h"

using namespace Pythia8;

class pythiaUserHooks : public UserHooks {

 public:
  //Constructor creates anti-kT jet finder with (-1, R, pTmin, etaMax).
  pythiaUserHooks();
  
  // Destructor deletes anti-kT jet finder and prints histograms.
  ~pythiaUserHooks();
  
 private:
};

#endif
