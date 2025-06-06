#ifndef K4GENERATORSCONFIG_ANALYSISHISTOS_H
#define K4GENERATORSCONFIG_ANALYSISHISTOS_H

#include <string>

#include "TH1D.h"

namespace k4GeneratorsConfig {
class analysisHistos {
public:
  analysisHistos();
  analysisHistos(const analysisHistos&);
  analysisHistos& operator=(const analysisHistos&);
  ~analysisHistos();

  bool processFile();

  void setSQRTS(double);
  void setGenerator(std::string);
  void setProcess(std::string);
  void setFile(std::string);

  double SQRTS();
  std::string Generator();
  std::string Process();
  std::string File();
  bool isValid();
  TH1D* TH1DHisto(unsigned int);
  unsigned int NbOf1DHistos();

  void Print();

private:
  double m_sqrts;
  std::string m_generator;
  std::string m_process;
  std::string m_file;
  bool m_isValid;
  std::vector<TH1D*> m_listOfHists;
};
} // namespace k4GeneratorsConfig

#endif
