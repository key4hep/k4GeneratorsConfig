#include <fstream>
#include <iostream>

#include "pythiaUserHooks.h"

pythiaUserHooks::pythiaUserHooks(std::string filename) : m_isValid(true) {
  // add here the reading of the selector cuts
  std::cout << "pythiaUserHooks to restrict phase space instantiated from file " << filename << std::endl;

  std::string line;
  std::string delimiter = " ";
  std::ifstream theFile(filename);
  if (theFile.is_open()) {
    while (getline(theFile, line)) {
      //      std::cout << line << std::endl;
      size_t pos = 0;
      std::string token;
      // first read to decode if it's a 1 or 2 particle selector
      pos = line.find(delimiter);
      unsigned int nPartSelector;
      if (pos != std::string::npos) {
        token = line.substr(0, pos);
        nPartSelector = atoi(token.c_str());
        line.erase(0, pos + delimiter.length());
      } else {
        break;
      }
      m_NbOfParticles.push_back(nPartSelector);
      if (nPartSelector == 1) {
        for (unsigned int i = 0; i < 3; i++) {
          pos = line.find(delimiter);
          if (pos != std::string::npos) {
            token = line.substr(0, pos);
            switch (i) {
            case 0:
              m_PDGID1.push_back(atoi(token.c_str()));
              break;
            case 1:
              m_Type.push_back(token);
              break;
            case 2:
              m_Comparator.push_back(token);
              break;
            default:
              break;
            }
            line.erase(0, pos + delimiter.length());
          }
        }
        // put the rest into the value
        m_Value.push_back(atof(line.c_str()));
        // keep the size of all vectors in sync
        m_PDGID2.push_back(0);
      } else if (nPartSelector == 2) {
        for (unsigned int i = 0; i < 4; i++) {
          pos = line.find(delimiter);
          if (pos != std::string::npos) {
            token = line.substr(0, pos);
            switch (i) {
            case 0:
              m_PDGID1.push_back(atoi(token.c_str()));
              break;
            case 1:
              m_PDGID2.push_back(atoi(token.c_str()));
              break;
            case 2:
              m_Type.push_back(token);
              break;
            case 3:
              m_Comparator.push_back(token);
              break;
            default:
              break;
            }
            line.erase(0, pos + delimiter.length());
          }
        }
        // put the rest into the value
        m_Value.push_back(atof(line.c_str()));
      }
    }
  } else {
    std::cout << "pythiaUserHooks::file could not be opened, not applying user cuts" << std::endl;
    m_isValid = false;
  }

  // check consistency
  if (m_NbOfParticles.size() != m_PDGID1.size() || m_PDGID1.size() != m_PDGID2.size() ||
      m_PDGID1.size() != m_Value.size() || m_Value.size() != m_Type.size()) {
    m_isValid = false;
    std::cout << "Inconsistent definition of 1 particle selector in pythiaUserHooks" << std::endl;
  }

  print();
}
pythiaUserHooks::~pythiaUserHooks() {}

bool pythiaUserHooks::canVetoProcessLevel() { return true; }

bool pythiaUserHooks::doVetoProcessLevel(Pythia8::Event& event) {
  // if the selectors are not configured correctly, do not veto...
  if (!m_isValid)
    return false;
  // ensure that the veto is called
  for (unsigned int i = 0; i < event.size(); i++) {
    Particle part1 = event[i];
    if (part1.status() > 0) {
      // if we see a veto reason do not waist time and return a veto, otherwirse continue
      if (Veto1ParticleSelector(part1.e(), part1.px(), part1.py(), part1.pz(), part1.id())) {
        return true;
      }
    }
    for (unsigned int j = 0; j < event.size(); j++) {
      Particle part2 = event[j];
      if (i != j && part1.status() > 0 && part2.status() > 0) {
        if (Veto2ParticleSelector(part1.e(), part1.px(), part1.py(), part1.pz(), part1.id(), part2.e(), part2.px(),
                                  part2.py(), part2.pz(), part2.id())) {
          return true;
        }
      }
    }
  }

  return false;
}

bool pythiaUserHooks::Veto1ParticleSelector(double energy, double px, double py, double pz, int pdg) {

  bool vetoed = false;
  for (unsigned int i = 0; i < m_PDGID1.size(); i++) {
    if (m_NbOfParticles[i] != 1)
      continue;
    if (pdg == m_PDGID1[i]) {
      double value = 0.;
      if (m_Type[i].find("PT") != std::string::npos) {
        value = PT(px, py);
      } else if (m_Type[i].find("ET") != std::string::npos) {
        value = ET(energy, px, py, pz);
      } else if (m_Type[i].find("Rapidity") != std::string::npos) {
        value = Rapidity(energy, pz);
      } else if (m_Type[i].find("Theta") != std::string::npos) {
        value = Theta(px, py, pz);
      } else if (m_Type[i].find("Eta") != std::string::npos) {
        value = Eta(px, py, pz);
      }
      // now we have the value, we need the comparator
      if (m_Comparator[i].find(">") != std::string::npos) {
        if (!(value > m_Value[i]))
          vetoed = true;
      } else if (m_Comparator[i].find("<") != std::string::npos) {
        if (!(value < m_Value[i]))
          vetoed = true;
      } else {
        std::cout << "pythiaUserHooks::Vecto1Particle Comparator request unknown " << m_Comparator[i] << std::endl;
      }
    }
  }
  return vetoed;
}
bool pythiaUserHooks::Veto2ParticleSelector(double energy1, double px1, double py1, double pz1, int pdg1,
                                            double energy2, double px2, double py2, double pz2, int pdg2) {

  bool vetoed = false;
  for (unsigned int i = 0; i < m_PDGID1.size(); i++) {
    if (m_NbOfParticles[i] != 2)
      continue;
    if (pdg1 == m_PDGID1[i] && pdg2 == m_PDGID2[i]) {
      double value = 0.;
      if (m_Type[i].find("Mass") != std::string::npos) {
        value = Mass(energy1, px1, py1, pz1, energy2, px2, py2, pz2);
      } else if (m_Type[i].find("Angle") != std::string::npos) {
        value = Angle(px1, py1, pz1, px2, py2, pz2);
      } else if (m_Type[i].find("DeltaEta") != std::string::npos) {
        value = abs(Eta(px1, py1, pz1) - Eta(px2, py2, pz2));
      } else if (m_Type[i].find("DeltaY") != std::string::npos) {
        value = abs(Rapidity(energy1, pz1) - Rapidity(energy2, pz2));
      } else if (m_Type[i].find("DeltaPhi") != std::string::npos) {
        value = Angle(px1, py1, 0., px2, py2, 0.);
      } else if (m_Type[i].find("DeltaR") != std::string::npos) {
        double deltaPhi = Angle(px1, py1, 0., px2, py2, 0.);
        double deltaEta = abs(Eta(px1, py1, pz1) - Eta(px2, py2, pz2));
        value = sqrt(deltaPhi * deltaPhi + deltaEta * deltaEta);
      }
      // now we have the value, we need the comparator
      if (m_Comparator[i].find(">") != std::string::npos) {
        if (!(value > m_Value[i]))
          vetoed = true;
      } else if (m_Comparator[i].find("<") != std::string::npos) {
        if (!(value < m_Value[i]))
          vetoed = true;
      } else {
        std::cout << "pythiaUserHooks::Veto2Particles Comparator request unknown " << m_Comparator[i] << std::endl;
      }
    }
  }
  return vetoed;
}

double pythiaUserHooks::PT(double px, double py) {

  double pt = px * px + py * py;
  if (pt >= 0) {
    pt = sqrt(pt);
  } else {
    pt = 0;
  }
  return pt;
}
double pythiaUserHooks::ET(double energy, double px, double py, double pz) {

  double et = energy * sin(Theta(px, py, pz));

  return et;
}
double pythiaUserHooks::Rapidity(double energy, double pz) {

  double rap = 0.5 * log((energy + pz) / (energy - pz));

  return rap;
}
double pythiaUserHooks::Theta(double px, double py, double pz) {

  double costheta = 0.;
  double pt = PT(px, py);
  double p = pt * pt + pz * pz;
  if (p >= 0.) {
    p = sqrt(p);
  }
  if (p != 0.) {
    costheta = pz / p;
  }
  double theta = acos(costheta);

  return theta;
}
double pythiaUserHooks::Eta(double px, double py, double pz) {

  double theta = Theta(px, py, pz);
  double eta = -log(tan(theta / 2.));

  return eta;
}
double pythiaUserHooks::Mass(double energy1, double px1, double py1, double pz1, double energy2, double px2, double py2,
                             double pz2) {

  double mass = (energy1 + energy2) * (energy1 + energy2) - (px1 + px2) * (px1 + px2) - (py1 + py2) * (py1 + py2) -
                (pz1 + pz2) * (pz1 + pz2);
  if (mass > 0.) {
    mass = sqrt(mass);
  }
  return mass;
}

double pythiaUserHooks::Angle(double px1, double py1, double pz1, double px2, double py2, double pz2) {
  double top = px1 * px2 + py1 * py2 + pz1 * pz2;
  double bottom = (px1 * px1 + py1 * py1 + pz1 * pz1) * (px2 * px2 + py2 * py2 + pz2 * pz2);
  bottom = sqrt(bottom);

  double angle = 0.;
  if (bottom != 0.) {
    angle = acos(top / bottom);
  }

  return angle;
}

void pythiaUserHooks::print() {

  std::cout << "pythiaUserHooks::Single Particle Selectors" << std::endl;
  for (unsigned int i = 0; i < m_PDGID1.size(); i++) {
    std::cout << "PDGID: " << m_PDGID1[i] << " ";
    if (i < m_PDGID2.size() && m_NbOfParticles[i] == 2)
      std::cout << "PDGID: " << m_PDGID2[i] << " ";
    if (i < m_Type.size())
      std::cout << "Type: " << m_Type[i] << " ";
    if (i < m_Comparator.size())
      std::cout << "Type: " << m_Comparator[i] << " ";
    if (i < m_Value.size())
      std::cout << "Value: " << m_Value[i] << " ";
    std::cout << std::endl;
  }
  std::cout << std::endl;
  return;
}
