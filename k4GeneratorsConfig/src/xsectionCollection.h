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
  void Print();

 private:
  std::vector<k4GeneratorsConfig::xsection> m_xsectionCollection;

};
}

#endif
