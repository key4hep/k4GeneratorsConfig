#ifndef K4GENERATORSCONFIG_XSECTION_H
#define K4GENERATORSCONFIG_XSECTION_H

#include "podio/ROOTReader.h"

#include <string>

namespace k4GeneratorsConfig {
class xsection {
 public:
  xsection();
  xsection(double,double,std::string,std::string,std::string);
  ~xsection();

  void processFile();

  void setXsection(double);
  void setXsection(double,double);
  void setXsectionError(double);
  void setGenerator(std::string);
  void setProcess(std::string);
  void setFile(std::string);

  double Xsection();
  double XsectionError();
  std::string Generator();
  std::string Process();
  std::string File();

  void Print();

 private:
  double m_xsection;
  double m_xsectionError;
  std::string m_generator;
  std::string m_process;
  std::string m_file;

  podio::ROOTReader *m_reader;

};
}

#endif
