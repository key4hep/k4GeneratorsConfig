#ifndef K4GENERATORSCONFIG_XSECTION_H
#define K4GENERATORSCONFIG_XSECTION_H

#include "podio/ROOTReader.h"

#include <string>

namespace k4GeneratorsConfig {
class xsection {
 public:
  xsection();
  xsection(double,double,double,std::string,std::string,std::string);
  xsection(const xsection &);
  xsection& operator=(const xsection &);
  ~xsection();

  bool processFile();

  void setXsection(double);
  void setXsection(double,double);
  void setXsectionError(double);
  void setSQRTS(double);
  void setGenerator(std::string);
  void setProcess(std::string);
  void setFile(std::string);

  double Xsection();
  double XsectionError();
  double SQRTS();
  std::string Generator();
  std::string Process();
  std::string File();
  bool isValid();

  void Print();

 private:
  double      m_xsection;
  double      m_xsectionError;
  double      m_sqrts;
  std::string m_generator;
  std::string m_process;
  std::string m_file;
  bool        m_isValid;
  podio::ROOTReader *m_reader;

};
}

#endif
