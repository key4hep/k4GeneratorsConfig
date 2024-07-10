#include "pythiaUserHooks.h"

pythiaUserHooks::pythiaUserHooks() {
  // add here the reading of the selector cuts
  std::cout << "pythiaUserHooks to restrict phase space instantiated" << std::endl;
}
pythiaUserHooks::~pythiaUserHooks(){}

bool pythiaUserHooks::canVetoProcessLevel(){
  return true;
}

bool pythiaUserHooks::doVetoProcessLevel(Pythia8::Event& event){
  // ensure that the veto is called
  std::cout << "Event record size is " <<  event.size() << std::endl;
  for (unsigned int i=0; i< event.size(); i++){
    Particle part = event[i];
    //    std::cout << "Particle "  << part.id() << " " << part.pT() << std::endl;
  }
  
  return false;
}
