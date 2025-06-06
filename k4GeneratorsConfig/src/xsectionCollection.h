#ifndef K4GENERATORSCONFIG_XSECTIONCOLLECTION_H
#define K4GENERATORSCONFIG_XSECTIONCOLLECTION_H

#include <vector>

#include "analysisHistos.h"
#include "xsection.h"

namespace k4GeneratorsConfig {
class xsectionCollection {
public:
  xsectionCollection();
  xsectionCollection(const xsectionCollection&);
  xsectionCollection& operator=(const xsectionCollection&);
  ~xsectionCollection();

  void Execute();
  void makeCollections();
  void orderCollections();
  bool compareLength(xsection, xsection);
  bool compareLexical(xsection, xsection);
  bool compareLexical(analysisHistos, analysisHistos);

  unsigned int NbOfSuccesses();
  unsigned int NbOfFailures();

  void Write2Root(std::string);

  void Print(bool onlyOK = false);
  void PrintSummary(std::ostream& output = std::cout) const;

private:
  std::vector<k4GeneratorsConfig::xsection> m_xsectionCollection;
  std::vector<k4GeneratorsConfig::analysisHistos> m_analysisHistosCollection;
  unsigned int m_validCounter;
  unsigned int m_invalidCounter;
};
} // namespace k4GeneratorsConfig

#endif
