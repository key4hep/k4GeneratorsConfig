#ifndef K4GENERATORSCONFIG_XSECTION2ROOT_H
#define K4GENERATORSCONFIG_XSECTION2ROOT_H

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

#include "differential.h"
#include "xsection.h"

namespace k4GeneratorsConfig {
class xsection2Root {
public:
  xsection2Root();
  xsection2Root(std::string);
  ~xsection2Root();

  void Init();
  void Execute(xsection&);
  void Execute(differential&);
  void Finalize();

  void decodeProcGen();
  void add2Tree(xsection&);
  void writeTree();
  void writeHistos();
  void writeCrossSectionFigures();
  void writeDifferentialFigures();

private:
  TFile* m_file;
  TTree* m_tree;
  std::vector<TH2D*> m_histos;
  std::vector<TProfile*> m_profiles;
  std::vector<TH1D*> m_rms;
  std::vector<TGraphErrors*> m_graphs;
  std::vector<TGraph*> m_graphsDelta;
  std::vector<std::vector<TCanvas*>> m_canvas;
  std::vector<std::vector<std::string>> m_canvasName;

  // data members
  std::string m_process;
  int m_processCode;
  double m_crossSection;
  double m_crossSectionError;
  double m_sqrts;
  std::string m_generator;
  int m_generatorCode;

  std::vector<std::string> m_generatorsList;
  std::vector<std::string> m_processesList;
};
} // namespace k4GeneratorsConfig

#endif
