#ifndef K4GENERATORSCONFIG_XSECTION2ROOT_H
#define K4GENERATORSCONFIG_XSECTION2ROOT_H

#include "TFile.h"
#include "TTree.h"

#include <string>
#include <unordered_map>

#include "xsection.h"

namespace k4GeneratorsConfig {
class xsection2Root {
 public:
  xsection2Root();
  xsection2Root(std::string);
  ~xsection2Root();

  void Init();
  
  void add2Tree(xsection&);
  void writeTree();


 private:
  TFile *m_file;
  TTree *m_tree;

  // data members
  double m_crossSection;
  double m_crossSectionError;
  double m_sqrts;
  std::string m_generator;
  int m_generatorCode;  

  std::vector<std::string> m_generatorsList;
};
}

#endif
