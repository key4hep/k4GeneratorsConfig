#ifndef K4GENERATORSCONFIG_EVENTGENERATIONCOLLECTIONS_H
#define K4GENERATORSCONFIG_EVENTGENERATIONCOLLECTIONS_H

#include <vector>
#include <map>

#include "analysisHistos.h"
#include "xsection.h"

namespace k4GeneratorsConfig {
class eventGenerationCollections {
public:
  eventGenerationCollections();
  eventGenerationCollections(const eventGenerationCollections&);
  eventGenerationCollections& operator=(const eventGenerationCollections&);
  ~eventGenerationCollections();

  void Execute(std::string);
  void makeCollections(std::string);
  void orderCollections();
  bool compareLength(xsection, xsection);
  bool compareLexical(xsection, xsection);
  bool compareLexical(analysisHistos, analysisHistos);

  void addSuccess(std::string);
  void addFailure(std::string);

  unsigned int NbOfSuccesses() const;
  unsigned int NbOfFailures() const;

  void Write2Root(std::string, std::string);

  std::vector<std::string> m_log;

  void Print(bool onlyOK = false, std::ostream& output = std::cout) const;
  void PrintRootLog(std::ostream& output = std::cout) const;
  void PrintSummary(std::ostream& output = std::cout) const;

private:
  std::vector<k4GeneratorsConfig::xsection> m_xsectionCollection;
  std::vector<k4GeneratorsConfig::analysisHistos> m_analysisHistosCollection;
  std::map<std::string,unsigned int> m_validCounter;
  std::map<std::string,unsigned int> m_invalidCounter;
};
} // namespace k4GeneratorsConfig

#endif
