#include <iostream>
#include <fstream>

#include "pythiaUserHooks.h"

pythiaUserHooks::pythiaUserHooks(std::string filename) : m_isValid(true){
  // add here the reading of the selector cuts
  std::cout << "pythiaUserHooks to restrict phase space instantiated from file " << filename << std::endl;

  std::string line;
  std::string delimiter = " ";
  std::ifstream theFile(filename);
  if ( theFile.is_open() ){
    while( getline(theFile,line) ){
      //      std::cout << line << std::endl;
      size_t pos = 0;
      std::string token;
      // first read to decode if it's a 1 or 2 particle selector
      pos = line.find(delimiter);
      unsigned int nPartSelector;
      if ( pos != std::string::npos ) {
	token = line.substr(0, pos);
	nPartSelector = atoi(token.c_str());
	line.erase(0, pos + delimiter.length());
      }
      else {
	break;
      }
      if ( nPartSelector == 1 ){
	for (unsigned int i=0; i<3; i++){
	  pos = line.find(delimiter);
	  if ( pos != std::string::npos ){
	    token = line.substr(0, pos);
	    switch (i){
	    case 0:
	      m_sel1PDGID.push_back(atoi(token.c_str()));
	      break;
	    case 1:
	      m_sel1Type.push_back(token);
	      break;
	    case 2:
	      m_sel1Comparator.push_back(token);
	      break;
	    default:
	      break;
	    }
	    line.erase(0, pos + delimiter.length());
	  }
	}
	// put the rest into the value
	m_sel1Value.push_back(atof(line.c_str()));
      }
    }
  }
  else {
    std::cout << "pythiaUserHooks::file could not be opened, not applying user cuts" << std::endl;
    m_isValid = false;
  }

  // check consistency
  if ( m_sel1Value.size() != m_sel1PDGID.size() || m_sel1PDGID.size() != m_sel1Type.size() || m_sel1PDGID.size() != m_sel1Value.size() ){
    m_isValid = false;
    std::cout << "Inconsistent definition of 1 particle selector in pythiaUserHooks" << std::endl;
  }

  print();
}
pythiaUserHooks::~pythiaUserHooks(){}

bool pythiaUserHooks::canVetoProcessLevel(){
  return true;
}

bool pythiaUserHooks::doVetoProcessLevel(Pythia8::Event& event){
  // if the selectors are not configured correctly, do not veto...
  if ( !m_isValid ) return false;
  // ensure that the veto is called
  for (unsigned int i=0; i< event.size(); i++){
    Particle part = event[i];
    if ( part.status() > 0 ) {
      // if we see a veto reason do not waist time and return a veto, otherwirse continue
      if ( Veto1Selector(part.e(),part.px(),part.py(),part.pz(),part.id()) ) return true;
    }
  }
  
  return false;
}

bool pythiaUserHooks::Veto1Selector(double energy, double px, double py, double pz, int pdg){

  bool vetoed = false;
  for (unsigned int i=0; i<m_sel1PDGID.size(); i++){
    if ( pdg == m_sel1PDGID[i] ){
      double value = 0.;
      if ( m_sel1Type[i].find("PT") != std::string::npos ){
	value = PT(px,py);
      }
      else if ( m_sel1Type[i].find("Theta") != std::string::npos ){
	value = ET(energy,px,py,pz);
      }
      else if ( m_sel1Type[i].find("Theta") != std::string::npos ){
	value = Theta(px,py,pz);
      }
      else if ( m_sel1Type[i].find("Eta") != std::string::npos ){
	value = Eta(px,py,pz);
      }
      // now we have the value, we need the comparator
      if ( m_sel1Comparator[i].find(">") != std::string::npos ){
	if ( !(value > m_sel1Value[i]) ) vetoed = true;
      }
      else if ( m_sel1Comparator[i].find("<") != std::string::npos ){
	if ( !(value < m_sel1Value[i]) ) vetoed = true;
      }
      else {
	std::cout << "pythiaUserHooks:: Comparator request unknown " << m_sel1Comparator[i] << std::endl;
      }
    }
  }
  return vetoed;
}

double pythiaUserHooks::PT(double px, double py){

  double pt = px*px+py*py;
  if (pt >= 0 ){
    pt = sqrt(pt);
  }
  else {
    pt = 0;
  }
  return pt;
}
double pythiaUserHooks::ET(double energy, double px, double py, double pz){

  double et = energy * sin(Theta(px,py,pz));
  
  return et;
}
double pythiaUserHooks::Theta(double px, double py, double pz){

  double tantheta = 0.;
  double pt = PT(px,py);
  if ( pz != 0. )
    tantheta = pt/pz;
  double theta = atan(tantheta);

  return theta;
}
double pythiaUserHooks::Eta(double px, double py, double pz){

  double theta = Theta(px,py,pz);
  double eta = -log(tan(theta/2.));

  return eta;
}

void pythiaUserHooks::print(){

  std::cout << "pythiaUserHooks::Single Particle Selectors" << std::endl;
  for (unsigned int i=0; i<m_sel1PDGID.size(); i++){
    std::cout << "PDGID: " << m_sel1PDGID[i] << " ";
    if ( i < m_sel1Type.size() )
      std::cout << "Type: " << m_sel1Type[i] << " ";
    if ( i < m_sel1Comparator.size() )
      std::cout << "Type: " << m_sel1Comparator[i] << " ";
    if ( i < m_sel1Value.size() )
      std::cout << "Value: " << m_sel1Value[i] << " ";
    std::cout << std::endl;
  }
  std::cout << std::endl;
  return;
}
