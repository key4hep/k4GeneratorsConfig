#ifndef K4GENERATORSCONFIG_PYTHIAUSERHOOKS_H
#define K4GENERATORSCONFIG_PYTHIAUSERHOOKS_H

// std
#include <string>
#include <vector>
// Pythia8
#include "Pythia8/Pythia.h"

class pythiaUserHooks : public Pythia8::UserHooks {

public:
  // Constructor creates anti-kT jet finder with (-1, R, pTmin, etaMax)
  explicit pythiaUserHooks(std::string);

  // Destructor deletes anti-kT jet finder and prints histograms.
  ~pythiaUserHooks();

  // we work at the parton level
  bool canVetoProcessLevel();
  bool doVetoProcessLevel(Pythia8::Event&);

  bool Veto1ParticleSelector(double, double, double, double, int);
  bool Veto2ParticleSelector(double, double, double, double, int, double, double, double, double, int);

  double PT(double, double);
  double ET(double, double, double, double);
  double Rapidity(double, double);
  double Theta(double, double, double);
  double Eta(double, double, double);

  double Mass(double, double, double, double, double, double, double, double);
  double Angle(double, double, double, double, double, double);

  void print();

private:
  bool m_isValid;

  std::vector<unsigned int> m_NbOfParticles;
  std::vector<int> m_PDGID1;
  std::vector<int> m_PDGID2;
  std::vector<std::string> m_Type;
  std::vector<std::string> m_Comparator;
  std::vector<double> m_Value;
};

#endif
