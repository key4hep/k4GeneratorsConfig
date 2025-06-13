#ifndef K4GENERATORSCONFIG_EVENTGENERATIONCOLLECTIONS2ROOT_H
#define K4GENERATORSCONFIG_EVENTGENERATIONCOLLECTIONS2ROOT_H

#include "TCanvas.h"
#include "TFile.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TProfile.h"
#include "TTree.h"

#include <string>
#include <unordered_map>

#include "analysisHistos.h"
#include "xsection.h"

namespace k4GeneratorsConfig {
class eventGenerationCollections2Root {
public:
  eventGenerationCollections2Root();
  eventGenerationCollections2Root(std::string);
  ~eventGenerationCollections2Root();

  void Init();
  void Execute(xsection&);
  void Execute(analysisHistos&);
  void Finalize();

  double prepSqrts(double, double);
  double calculateChi2(std::string, TH1D*, TH1D*);

  void decodeProcGen();
  unsigned int ProcSqrtsID(std::string, double);
  unsigned int ProcSqrtsID(std::pair<std::string, double>);
  double getSqrtsFromProcSqrtsID(unsigned int);
  std::string getProcFromProcSqrtsID(unsigned int);

  unsigned int ProcGenID(std::string, std::string);
  unsigned int ProcGenID(std::pair<std::string, std::string>);
  std::string getGenFromProcGenID(unsigned int);
  std::string getProcFromProcGenID(unsigned int);

  void add2Tree(xsection&);
  void writeTree();
  void writeHistos();
  void writeCrossSectionFigures();
  void writeAnalysisHistosFigures();

  std::vector<std::string> getLog();

private:
  // steers the precision criteria
  const double m_sqrtsPrecision;
  const double m_xsectionMinimal;
  const double m_GeV2MeV;
  double m_EnergyUnitCnv;

  std::vector<std::string> m_log;

  TFile* m_file;
  TTree* m_tree;

  // for the cross section
  std::vector<TGraphErrors*> m_xsectionGraphs;
  std::vector<TGraphErrors*> m_xsectionRMSGraphs;
  std::vector<TGraphErrors*> m_xsectionDeltaGraphs;

  // for the differential distributions
  std::vector<std::vector<TCanvas*>> m_cnvAnalysisHistos;
  std::vector<std::vector<std::string>> m_cnvAnalysisHistosNames;
  std::vector<std::vector<double>> m_analysisHistosChi2;

  // data members
  std::string m_process;
  std::pair<std::string, double> m_procSqrts;
  int m_processCode;
  int m_sqrtsCode;
  double m_crossSection;
  double m_crossSectionError;
  double m_sqrts;
  std::string m_generator;
  int m_generatorCode;

  std::vector<std::string> m_generatorsList;
  std::vector<std::string> m_processesList;
  std::vector<std::pair<std::string, double>> m_procSqrtsList;
  std::vector<std::pair<std::string, std::string>> m_procGenList;
  std::vector<double> m_sqrtsList;
};
} // namespace k4GeneratorsConfig

#endif
