#ifndef K4GENERATORSCONFIG_XSECTIONCOLLECTION_H
#define K4GENERATORSCONFIG_XSECTIONCOLLECTION_H

#include <vector>

#include "xsection.h"

namespace k4GeneratorsConfig {
class xsectionCollection {
 public:
  xsectionCollection();
  xsectionCollection(const xsectionCollection&);
  xsectionCollection& operator=(const xsectionCollection&);
  ~xsectionCollection();

  void Execute();
  void makeCollection();
  void orderCollection();
  bool compareLength(xsection, xsection);
  bool compareLexical(xsection, xsection);
  void Write2Root(std::string);
  void Print(bool onlyOK=false);
  void PrintSummary(std::ostream &output=std::cout) const;

 private:
  std::vector<k4GeneratorsConfig::xsection> m_xsectionCollection;

};
}

#endif
