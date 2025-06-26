#include "eventGenerationCollections2Root.h"
#include <sstream>

#include "TCanvas.h"
#include "TGaxis.h"
#include "TLegend.h"
#include "TMultiGraph.h"
#include "TStyle.h"

k4GeneratorsConfig::eventGenerationCollections2Root::eventGenerationCollections2Root()
    : m_sqrtsPrecision(1.e-6), m_xsectionMinimal(1.e-9), m_GeV2MeV(1.e3), m_EnergyUnitCnv(m_GeV2MeV), m_file(0),
      m_tree(0), m_processCode(-1), m_sqrtsCode(-1), m_crossSection(0), m_crossSectionError(0.), m_sqrts(0.),
      m_generatorCode(0) {
  m_file = new TFile("eventGenerationSummary.root", "RECREATE");
  Init();
}
k4GeneratorsConfig::eventGenerationCollections2Root::eventGenerationCollections2Root(std::string file)
    : m_sqrtsPrecision(1.e-6), m_xsectionMinimal(1.e-9), m_GeV2MeV(1.e3), m_EnergyUnitCnv(m_GeV2MeV), m_file(0),
      m_tree(0), m_processCode(-1), m_sqrtsCode(-1), m_crossSection(0), m_crossSectionError(0.), m_sqrts(0.),
      m_generatorCode(0) {
  m_file = new TFile(file.c_str(), "RECREATE");
  Init();
}
void k4GeneratorsConfig::eventGenerationCollections2Root::Init() {
  // some gimmicks to avoid that the axis common exponent is hidden for the bottom figure:
  TGaxis::SetMaxDigits(5);
  TGaxis::SetExponentOffset(-0.08, -0.12, "y");

  // define the generator colors (as offset)
  std::vector<std::string> genNames = {"Madgraph", "Sherpa", "Whizard", "KKMC", "Pythia", "Babayaga"};
  for (unsigned int i = 0; i < genNames.size(); i++) {
    m_generatorColorOffset[genNames[i]] = i;
  }

  // define the root tree
  m_tree = new TTree("CrossSections", "cross sections");
  m_tree->Branch("process", &m_process);
  m_tree->Branch("iprocess", &m_processCode, "iprocess/I");
  m_tree->Branch("sqrts", &m_sqrts, "sqrts/D");
  m_tree->Branch("isqrts", &m_sqrtsCode, "isqrts/I");
  m_tree->Branch("generator", &m_generator);
  m_tree->Branch("igenerator", &m_generatorCode, "igenerator/I");
  m_tree->Branch("xsec", &m_crossSection, "xsec/D");
  m_tree->Branch("dxsec", &m_crossSectionError, "dxsec/D");
}
k4GeneratorsConfig::eventGenerationCollections2Root::~eventGenerationCollections2Root() {}
void k4GeneratorsConfig::eventGenerationCollections2Root::Execute(xsection& xsec) {

  // fill the TREE structure with the predictions and meta data
  m_generator = xsec.Generator();
  m_process = xsec.Process();
  m_sqrts = prepSqrts(xsec.SQRTS(), m_EnergyUnitCnv);
  m_crossSection = xsec.Xsection();
  m_crossSectionError = xsec.XsectionError();
  // derive the indices for simpler nagivation
  mapProcGenSqrts();
  // write to the tree
  m_tree->Fill();
}
void k4GeneratorsConfig::eventGenerationCollections2Root::Execute(analysisHistos& anaHistos) {
  m_generator = anaHistos.Generator();
  m_process = anaHistos.Process();
  m_sqrts = prepSqrts(anaHistos.SQRTS(), m_EnergyUnitCnv);
  // for safety decode the the process code and the generator
  mapProcGenSqrts();
  // if it's the first occurrence of a set, need to resize the canvas vector:
  if (m_cnvAnalysisHistos.size() != m_procSqrtsList.size()) {
    m_cnvAnalysisHistos.resize(m_procSqrtsList.size());
    m_cnvAnalysisHistosNames.resize(m_procSqrtsList.size());
  }
  std::stringstream name, desc;
  unsigned int iProc = ProcSqrtsID(m_procSqrts);
  // check that it's in range
  if (iProc >= m_procSqrtsList.size()) {
    std::cout << "eventGenerationCollections2Root::Execute ERROR " << m_procSqrts.first << " " << m_procSqrts.second
              << " not found for " << m_generator << std::endl;
    return;
  }
  // that there are histograms
  if (anaHistos.NbOf1DHistos() == 0) {
    std::cout << "eventGenerationCollections2Root::Execute ERROR " << m_procSqrts.first << " " << m_procSqrts.second
              << " no TH!Ds found for " << m_generator << std::endl;
    return;
  }
  // and so far no canvases have been prepared
  if (m_cnvAnalysisHistos[iProc].size() == 0) {
    // prepare the canvases
    for (unsigned int iHisto = 0; iHisto < anaHistos.NbOf1DHistos(); iHisto++) {
      name << m_procSqrtsList[iProc].first << (unsigned int)(m_procSqrtsList[iProc].second * m_EnergyUnitCnv) << " "
           << anaHistos.TH1DHisto(iHisto)->GetName();
      desc << "Process: " << m_procSqrtsList[iProc].first << " " << m_procSqrtsList[iProc].second;
      m_cnvAnalysisHistos[iProc].push_back(new TCanvas(name.str().c_str(), desc.str().c_str()));
      m_cnvAnalysisHistos[iProc].back()->cd();
      TPad* topPad = new TPad("topPad", "A bottom histo", 0.0, 0.3, 1.0, 1.0, 0);
      TPad* bottomPad = new TPad("bottomPad", "a bottom histo", 0.0, 0.0, 1.0, 0.3, 0);
      topPad->SetNumber(1);
      topPad->SetBottomMargin(0);
      topPad->Draw();
      bottomPad->SetNumber(2);
      bottomPad->SetTopMargin(0);
      bottomPad->SetBottomMargin(0.25);
      bottomPad->Draw();
      m_cnvAnalysisHistosNames[iProc].push_back(anaHistos.TH1DHisto(iHisto)->GetName());
      name.clear();
      name.str("");
      desc.clear();
      desc.str("");
    }
  }
  // the canvas vector is ready, so we can fill the canvas:
  // now add the histos
  for (auto histo : anaHistos.TH1DHistos()) {
    unsigned int iHisto =
        std::find(m_cnvAnalysisHistosNames[iProc].begin(), m_cnvAnalysisHistosNames[iProc].end(), histo->GetName()) -
        m_cnvAnalysisHistosNames[iProc].begin();
    if (iHisto < m_cnvAnalysisHistos[iProc].size()) {
      m_cnvAnalysisHistos[iProc][iHisto]->cd(1);
      TH1D* theHisto = anaHistos.TH1DHisto(iHisto);
      desc << m_generator << " " << m_process << " " << m_sqrts << " GeV";
      theHisto->SetTitle(desc.str().c_str());
      desc.clear();
      desc.str("");
      gStyle->SetOptTitle(0);
      theHisto->SetStats(kFALSE);
      theHisto->SetLineColor(2 + m_generatorColorOffset[m_generator]);
      theHisto->SetMinimum(0);
      theHisto->Draw("SAME");
      theHisto->GetYaxis()->SetTitleSize(0.06);
      theHisto->GetYaxis()->SetTitleOffset(0.7);
      theHisto->GetYaxis()->SetLabelSize(0.05);
      // x axis turn off the labels
      theHisto->GetXaxis()->SetLabelSize(0);
    }
  }
}
void k4GeneratorsConfig::eventGenerationCollections2Root::mapProcGenSqrts() {

  // remove - from the names
  if (m_generator.find("-") != std::string::npos) {
    m_generator.erase(m_generator.find("-"), 1);
  }
  // remove @ from names
  if (m_generator.find("@") != std::string::npos) {
    m_generator.erase(m_generator.find("@"), 1);
  }
  // remove _ from names
  if (m_generator.find("_") != std::string::npos) {
    m_generator.erase(m_generator.find("_"), 1);
  }

  // assign a code for each generator
  if (std::find(m_generatorsList.begin(), m_generatorsList.end(), m_generator) == m_generatorsList.end()) {
    m_generatorsList.push_back(m_generator);
  }

  m_generatorCode = std::find(m_generatorsList.begin(), m_generatorsList.end(), m_generator) - m_generatorsList.begin();

  // check that the generator has a color offset, if not add it
  if (m_generatorColorOffset.find(m_generator) == m_generatorColorOffset.end()) {
    m_generatorColorOffset[m_generator] = m_generatorColorOffset.size();
  }

  // process needs to be processed to remove everything from the subscript on:
  if (m_process.find_last_of("_") != std::string::npos) {
    m_process.erase(m_process.find_last_of("_"));
  }
  // assign a code for each process
  if (std::find(m_processesList.begin(), m_processesList.end(), m_process) == m_processesList.end()) {
    m_processesList.push_back(m_process);
  }

  m_processCode = std::find(m_processesList.begin(), m_processesList.end(), m_process) - m_processesList.begin();

  // Pair of proc+sqrts
  m_procSqrts = std::pair<std::string, double>{m_process, m_sqrts};
  // assign a code for each process
  if (std::find(m_procSqrtsList.begin(), m_procSqrtsList.end(), m_procSqrts) == m_procSqrtsList.end()) {
    m_procSqrtsList.push_back(m_procSqrts);
  }

  // pair of proc + gen
  std::pair<std::string, std::string> procGen = std::pair<std::string, std::string>{m_process, m_generator};
  // assign a code for each process
  if (std::find(m_procGenList.begin(), m_procGenList.end(), procGen) == m_procGenList.end()) {
    m_procGenList.push_back(procGen);
  }

  // now the sqrts list
  if (std::find(m_sqrtsList.begin(), m_sqrtsList.end(), m_sqrts) == m_sqrtsList.end()) {
    m_sqrtsList.push_back(m_sqrts);
  }
  m_sqrtsCode = std::find(m_sqrtsList.begin(), m_sqrtsList.end(), m_sqrts) - m_sqrtsList.begin();
}
unsigned int k4GeneratorsConfig::eventGenerationCollections2Root::ProcSqrtsID(std::string proc, double sqrts) {
  // get the iterator
  return ProcSqrtsID({proc, sqrts});
}
unsigned int
k4GeneratorsConfig::eventGenerationCollections2Root::ProcSqrtsID(std::pair<std::string, double> procSqrts) {
  // get the iterator
  return std::find(m_procSqrtsList.begin(), m_procSqrtsList.end(), procSqrts) - m_procSqrtsList.begin();
}
std::string k4GeneratorsConfig::eventGenerationCollections2Root::getProcFromProcSqrtsID(unsigned int index) {
  if (index < m_procSqrtsList.size()) {
    return m_procSqrtsList[index].first;
  }
  return "";
}
double k4GeneratorsConfig::eventGenerationCollections2Root::getSqrtsFromProcSqrtsID(unsigned int index) {
  if (index < m_procSqrtsList.size()) {
    return m_procSqrtsList[index].second;
  }
  return 0.;
}
unsigned int k4GeneratorsConfig::eventGenerationCollections2Root::ProcGenID(std::string proc, std::string gen) {
  // get the iterator
  return ProcGenID({proc, gen});
}
unsigned int
k4GeneratorsConfig::eventGenerationCollections2Root::ProcGenID(std::pair<std::string, std::string> procGen) {
  // get the iterator
  return std::find(m_procGenList.begin(), m_procGenList.end(), procGen) - m_procGenList.begin();
}
std::string k4GeneratorsConfig::eventGenerationCollections2Root::getProcFromProcGenID(unsigned int index) {
  if (index < m_procGenList.size()) {
    return m_procGenList[index].first;
  }
  return "";
}
std::string k4GeneratorsConfig::eventGenerationCollections2Root::getGenFromProcGenID(unsigned int index) {
  if (index < m_procGenList.size()) {
    return m_procGenList[index].second;
  }
  return "unknown";
}
void k4GeneratorsConfig::eventGenerationCollections2Root::Finalize() {
  // go to the top root directory
  m_file->cd();
  // the total cross section tree and comparison graphs
  writeXsectionGraphs();
  m_tree->Write();
  // write cross section images
  writeCrossSectionFigures();
  // deal with the analysisHistos distributions
  writeAnalysisHistosFigures();
  // close the file
  m_file->Close();
}
void k4GeneratorsConfig::eventGenerationCollections2Root::writeXsectionGraphs() {

  std::stringstream name, desc;
  for (auto procGen : m_procGenList) {
    std::string proc = procGen.first;
    std::string gen = procGen.second;
    name << gen << proc;
    desc << gen << "::Process: " << proc << ": Cross section vs Sqrts";
    m_xsectionGraphs.push_back(new TGraphErrors());
    m_xsectionGraphs.back()->SetName(name.str().c_str());
    name.clear();
    name.str("");
    desc.clear();
    desc.str("");
    // the DELTA needs the loop over the generators
    name << gen << proc << "Delta";
    desc << "Process: " << proc << ": Delta/average vs Sqrts";
    m_xsectionDeltaGraphs.push_back(new TGraphErrors());
    m_xsectionDeltaGraphs.back()->SetName(name.str().c_str());
    name.clear();
    name.str("");
    desc.clear();
    desc.str("");
  }
  // the RMS does not need the loop over the generators
  for (auto proc : m_processesList) {
    name << proc << "RMS";
    desc << "Process: " << proc << ": RMS/average vs Sqrts";
    m_xsectionRMSGraphs.push_back(new TGraphErrors());
    m_xsectionRMSGraphs.back()->SetName(name.str().c_str());
    name.clear();
    name.str("");
    desc.clear();
    desc.str("");
  }

  // to calculate per Process and Sqrts average cross section, RMS and number of entries
  // structure for the average and RMS of the cross section per Process and sqrts
  std::vector<double> xsectionMean4Process;
  std::vector<double> xsectionRMS4Process;
  std::vector<unsigned int> xsectionN4Process;
  xsectionMean4Process.resize(m_procSqrtsList.size(), 0.);
  xsectionRMS4Process.resize(m_procSqrtsList.size(), 0.);
  xsectionN4Process.resize(m_procSqrtsList.size(), 0);

  // access the data and write to the histo via the index of the generatorList
  for (unsigned int entry = 0; entry < m_tree->GetEntries(); entry++) {
    // a tree for root analysis
    m_tree->GetEntry(entry);
    // calculate the index of histos and graphs
    unsigned int indexProcGen = ProcGenID(m_process, m_generator);
    if (indexProcGen < m_procGenList.size()) {
      // graphs for pecise drawing
      m_xsectionGraphs[indexProcGen]->AddPoint(m_sqrts, m_crossSection);
      unsigned int lastPoint = m_xsectionGraphs[indexProcGen]->GetN() - 1;
      m_xsectionGraphs[indexProcGen]->SetPointError(lastPoint, m_sqrts * m_sqrtsPrecision, m_crossSectionError);
      // process profile, but make sure it's positive and > 1*10^-3 attobarn
      if (m_crossSection > m_xsectionMinimal) {
        // accumulate the averages and the squares:
        unsigned int indexProcSqrts = ProcSqrtsID(m_process, m_sqrts);
        if (indexProcSqrts < m_procSqrtsList.size()) {
          xsectionMean4Process[indexProcSqrts] += m_crossSection;
          xsectionRMS4Process[indexProcSqrts] += (m_crossSection * m_crossSection);
          xsectionN4Process[indexProcSqrts] += 1;
        }
      }
    }
  }

  // now average:
  for (unsigned int iproc = 0; iproc < m_processesList.size(); iproc++) {
    for (unsigned int isqrts = 0; isqrts < m_sqrtsList.size(); isqrts++) {
      unsigned int indexProcSqrts = ProcSqrtsID(m_processesList[iproc], m_sqrtsList[isqrts]);
      if (indexProcSqrts < m_procSqrtsList.size() && xsectionN4Process[indexProcSqrts] > 0) {
        // average
        xsectionMean4Process[indexProcSqrts] /= xsectionN4Process[indexProcSqrts];
        // average of squares
        xsectionRMS4Process[indexProcSqrts] /= xsectionN4Process[indexProcSqrts];
        // the RMS
        xsectionRMS4Process[indexProcSqrts] =
            sqrt(xsectionRMS4Process[indexProcSqrts] -
                 xsectionMean4Process[indexProcSqrts] * xsectionMean4Process[indexProcSqrts]);
        // calculate sigma and error on the estimation of sigma (simplified formula)
        double relRMS = xsectionRMS4Process[indexProcSqrts] / xsectionMean4Process[indexProcSqrts];
        double relRMSError = relRMS / sqrt(2. * xsectionMean4Process[indexProcSqrts]);
        m_xsectionRMSGraphs[iproc]->AddPoint(m_sqrtsList[isqrts], relRMS);
        unsigned int lastPoint = m_xsectionRMSGraphs[iproc]->GetN() - 1;
        m_xsectionRMSGraphs[iproc]->SetPointError(lastPoint, m_sqrtsList[isqrts] * m_sqrtsPrecision, relRMSError);
        for (unsigned int igen = 0; igen < m_generatorsList.size(); igen++) {
          // new index for the deltagraphs
          unsigned int indexProcGen = ProcGenID(m_processesList[iproc], m_generatorsList[igen]);
          if (indexProcGen < m_procGenList.size()) {
            double relDelta = 0.;
            double relDeltaError = 0.;
            // we need to play it safe: we do not know the order of the points, so we loop to determine
            int isqrtsPoint = -1;
            for (int iPoint = 0; iPoint < m_xsectionGraphs[indexProcGen]->GetN(); iPoint++) {
              double sqrts = m_xsectionGraphs[indexProcGen]->GetPointX(iPoint);
              if (abs(sqrts - m_sqrtsList[isqrts]) / sqrts < m_sqrtsPrecision) {
                isqrtsPoint = iPoint;
              }
            }
            // we need to get the data from the generator graph, make sure the data is there
            if (isqrtsPoint > -1 && isqrtsPoint < m_xsectionGraphs[indexProcGen]->GetN()) {
              relDelta =
                  (m_xsectionGraphs[indexProcGen]->GetPointY(isqrtsPoint) - xsectionMean4Process[indexProcSqrts]) /
                  xsectionMean4Process[indexProcSqrts];
              relDeltaError =
                  m_xsectionGraphs[indexProcGen]->GetErrorY(isqrtsPoint) / xsectionMean4Process[indexProcSqrts];
              m_xsectionDeltaGraphs[indexProcGen]->AddPoint(m_sqrtsList[isqrts], relDelta);
              // set the error on the delta to 0
              lastPoint = m_xsectionDeltaGraphs[indexProcGen]->GetN() - 1;
              m_xsectionDeltaGraphs[indexProcGen]->SetPointError(lastPoint, m_sqrtsList[isqrts] * m_sqrtsPrecision,
                                                                 relDeltaError);
            }
          }
        }
      }
    }
  }

  // write the histos out
  for (auto graph : m_xsectionGraphs) {
    graph->Write();
  }
  for (auto graph : m_xsectionRMSGraphs) {
    graph->Write();
  }
  for (auto graph : m_xsectionDeltaGraphs) {
    graph->Write();
  }
}
void k4GeneratorsConfig::eventGenerationCollections2Root::writeCrossSectionFigures() {

  std::stringstream name, desc;
  // produce a png
  TCanvas* c1 = new TCanvas("c1", "CrossSectionsCanvas");
  TPad* topPad = new TPad("topPad", "Cross Section versus sqrts", 0.0, 0.3, 1.0, 1.0, 0);
  TPad* bottomPad = new TPad("bottomPad", "RMS/average versus sqrts", 0.0, 0.0, 1.0, 0.3, 0);
  topPad->SetNumber(1);
  topPad->Draw();
  bottomPad->SetNumber(2);
  bottomPad->Draw();
  // the canvas is prepared we can now proceed to output all processes:
  for (unsigned int iProc = 0; iProc < m_processesList.size(); iProc++) {
    // top pad
    topPad->cd();
    topPad->SetBottomMargin(0);
    // the cross sections with the graph
    TMultiGraph* mg = new TMultiGraph();
    for (unsigned int gen = 0; gen < m_generatorsList.size(); gen++) {
      unsigned int indexProcGen = ProcGenID(m_processesList[iProc], m_generatorsList[gen]);
      if (indexProcGen < m_procGenList.size()) {
        name << m_processesList[iProc] << " " << m_generatorsList[gen];
        m_xsectionGraphs[indexProcGen]->SetName(name.str().c_str());
        m_xsectionGraphs[indexProcGen]->SetStats(kFALSE);
        m_xsectionGraphs[indexProcGen]->SetMarkerStyle(20 + m_generatorColorOffset[m_generatorsList[gen]]);
        m_xsectionGraphs[indexProcGen]->SetMarkerColor(2 + m_generatorColorOffset[m_generatorsList[gen]]);
        m_xsectionGraphs[indexProcGen]->SetMarkerSize(1.25);
        mg->Add(m_xsectionGraphs[indexProcGen], "AP");
        name.clear();
        name.str("");
      }
    }
    // draw and set the stuff for the multigraphs
    mg->Draw("AP");
    mg->GetYaxis()->SetTitle("#sigma [pb]");
    mg->GetYaxis()->SetTitleSize(0.06);
    mg->GetYaxis()->SetTitleOffset(0.7);
    mg->GetYaxis()->SetLabelSize(0.05);
    // x axis turn off the labels
    mg->GetXaxis()->SetLabelSize(0);
    // build the legend of the pad
    topPad->BuildLegend(0.65, 0.65, 0.9, 0.9);

    // the lower part with the RMS/average
    bottomPad->cd();
    bottomPad->SetTopMargin(0);
    bottomPad->SetBottomMargin(0.25);

    // prepare the figures
    m_xsectionRMSGraphs[iProc]->SetStats(kFALSE);
    m_xsectionRMSGraphs[iProc]->SetMarkerStyle(20);
    m_xsectionRMSGraphs[iProc]->SetMarkerColor(kBlack);
    m_xsectionRMSGraphs[iProc]->SetMarkerSize(1.25);

    // now the graph
    TMultiGraph* mgRMS = new TMultiGraph();
    mgRMS->Add(m_xsectionRMSGraphs[iProc], "AP");
    mgRMS->Draw("AP");

    // graph drawn we can work on the axes
    mgRMS->GetXaxis()->SetTitle("#sqrt{s} [GeV]");
    mgRMS->GetXaxis()->SetTitleSize(0.12);
    mgRMS->GetXaxis()->SetTitleOffset(0.8);
    mgRMS->GetXaxis()->SetLabelSize(0.1);
    mgRMS->GetYaxis()->SetTitle("RMS/<#sigma>");
    mgRMS->GetYaxis()->SetTitleSize(0.12);
    mgRMS->GetYaxis()->SetTitleOffset(0.4);
    mgRMS->GetYaxis()->CenterTitle();
    mgRMS->GetYaxis()->SetLabelSize(0.1);

    // generate a name and write a png
    name << m_processesList[iProc] << "wRMS.png";
    c1->Print(name.str().c_str());
    name.clear();
    name.str("");

    // now we do a second figure where we update only the bottom
    bottomPad->cd();
    bottomPad->Clear();

    // the multigraph
    TMultiGraph* mgDelta = new TMultiGraph();
    for (unsigned int gen = 0; gen < m_generatorsList.size(); gen++) {
      unsigned int indexProcGen = ProcGenID(m_processesList[iProc], m_generatorsList[gen]);
      if (indexProcGen < m_procGenList.size()) {
        name << m_processesList[iProc] << " " << m_generatorsList[gen];
        m_xsectionDeltaGraphs[indexProcGen]->SetName(name.str().c_str());
        m_xsectionDeltaGraphs[indexProcGen]->SetStats(kFALSE);
	m_xsectionDeltaGraphs[indexProcGen]->SetMarkerStyle(20 + m_generatorColorOffset[m_generatorsList[gen]]);
        m_xsectionDeltaGraphs[indexProcGen]->SetMarkerColor(2 + m_generatorColorOffset[m_generatorsList[gen]]);
        m_xsectionDeltaGraphs[indexProcGen]->SetMarkerSize(1.25);
        mgDelta->Add(m_xsectionDeltaGraphs[indexProcGen], "AP");
        name.clear();
        name.str("");
      }
    }
    mgDelta->Draw("AP");

    // graph drawn we can work on the axes
    mgDelta->GetXaxis()->SetTitle("#sqrt{s} [GeV]");
    mgDelta->GetXaxis()->SetTitleSize(0.12);
    mgDelta->GetXaxis()->SetTitleOffset(0.8);
    mgDelta->GetXaxis()->SetLabelSize(0.1);
    mgDelta->GetYaxis()->SetTitle("#Delta#sigma/<#sigma>");
    mgDelta->GetYaxis()->SetTitleSize(0.12);
    mgDelta->GetYaxis()->SetTitleOffset(0.4);
    mgDelta->GetYaxis()->CenterTitle();
    mgDelta->GetYaxis()->SetLabelSize(0.1);

    // generate a name and write a png
    name << m_processesList[iProc] << "wDelta.png";
    c1->Print(name.str().c_str());
    name.clear();
    name.str("");

    // delete the pointers
    delete mg;
    mg = nullptr;
    delete mgRMS;
    mgRMS = nullptr;
  }
  delete c1;
}
void k4GeneratorsConfig::eventGenerationCollections2Root::writeAnalysisHistosFigures() {

  // if the canvas is not filled do not try
  if (m_cnvAnalysisHistos.size() == 0)
    return;

  std::stringstream name;
  // first process the histogram averaging
  std::vector<std::vector<TH1D*>> analysisHistosAverage;
  analysisHistosAverage.resize(m_procSqrtsList.size());
  for (unsigned int proc = 0; proc < m_procSqrtsList.size(); proc++) {
    for (unsigned int ihisto = 0; ihisto < m_cnvAnalysisHistos[proc].size(); ihisto++) {
      // calculate the average
      TVirtualPad* topPad = m_cnvAnalysisHistos[proc][ihisto]->cd(1);
      TList* padPrimitives = topPad->GetListOfPrimitives();
      // fetch the histograms TH1D
      unsigned int counter = 0;
      TH1D* generatorAverageHisto = nullptr;
      for (auto obj : *padPrimitives) {
        if (obj->InheritsFrom(TH1D::Class())) {
          // recreate TH1D
          TH1D* generatorHisto = new TH1D(*(TH1D*)obj);
          if (generatorAverageHisto == nullptr) {
            // to avoid memory leaks add the proc number
            name << generatorHisto->GetName() << proc;
            generatorAverageHisto = new TH1D(name.str().c_str(), generatorHisto->GetTitle(),
                                             generatorHisto->GetNbinsX(), generatorHisto->GetBinLowEdge(1),
                                             generatorHisto->GetBinLowEdge(generatorHisto->GetNbinsX() + 1));
            generatorAverageHisto->GetXaxis()->SetTitle(generatorHisto->GetXaxis()->GetTitle());
            name.clear();
            name.str("");
          }
          if (!(generatorAverageHisto->GetSumw2N() > 0))
            generatorAverageHisto->Sumw2(kTRUE);
          generatorAverageHisto->Add(generatorHisto);
          counter++;
        }
      }
      // we got all our histos together, so we can average
      if (counter > 0) {
        generatorAverageHisto->Scale(1. / counter);
      }
      // push_back
      analysisHistosAverage[proc].push_back(generatorAverageHisto);
    }
  }

  // now write out the superposed histograms
  for (unsigned int proc = 0; proc < m_procSqrtsList.size(); proc++) {
    // check that it's the correct process
    for (unsigned int ihisto = 0; ihisto < m_cnvAnalysisHistos[proc].size(); ihisto++) {
      TVirtualPad* topPad = m_cnvAnalysisHistos[proc][ihisto]->cd(1);
      topPad->BuildLegend();
      // we need to get the histo from the top
      TList* padPrimitives = topPad->GetListOfPrimitives();
      // move to the bottom pad
      TVirtualPad* bottomPad = m_cnvAnalysisHistos[proc][ihisto]->cd(2);
      bottomPad->cd();
      // fetch the histograms TH1D
      for (auto obj : *padPrimitives) {
        if (obj->InheritsFrom(TH1D::Class())) {
          // subtract and divide
          TH1D* theDelta = new TH1D(*(TH1D*)obj);
          if (!(theDelta->GetSumw2N() > 0))
            theDelta->Sumw2(kTRUE);
          // calculate the compatbility before operations and output text
          double chi2 = calculateChi2(m_procSqrtsList[proc].first, theDelta, analysisHistosAverage[proc][ihisto]);
          std::stringstream message;
          message << m_procSqrtsList[proc].first << " " << theDelta->GetTitle() << " "
                  << theDelta->GetXaxis()->GetTitle() << " Chi2 = " << chi2;
          m_log.push_back(message.str());
          // subtract average and divide
          theDelta->Add(analysisHistosAverage[proc][ihisto], -1.);
          theDelta->Divide(analysisHistosAverage[proc][ihisto]);
          // draw the histo and set the usual options
          theDelta->Draw("SAME");
          theDelta->GetXaxis()->SetTitle(analysisHistosAverage[proc][ihisto]->GetXaxis()->GetTitle());
          theDelta->GetXaxis()->SetTitleSize(0.12);
          theDelta->GetXaxis()->SetTitleOffset(0.8);
          theDelta->GetXaxis()->SetLabelSize(0.1);
          theDelta->GetYaxis()->SetTitle("#Delta/<N>");
          theDelta->GetYaxis()->SetTitleSize(0.12);
          theDelta->GetYaxis()->SetTitleOffset(0.4);
          theDelta->GetYaxis()->CenterTitle();
          theDelta->GetYaxis()->SetLabelSize(0.1);
        }
      }
      // done, save the canvas
      name << m_procSqrtsList[proc].first << (unsigned int)(m_procSqrtsList[proc].second * m_EnergyUnitCnv)
           << m_cnvAnalysisHistosNames[proc][ihisto] << ".png";
      m_cnvAnalysisHistos[proc][ihisto]->Print(name.str().c_str());
      name.clear();
      name.str("");
    }
  }
}
double k4GeneratorsConfig::eventGenerationCollections2Root::prepSqrts(double sqrts, double unit) {
  return int((sqrts * unit) + 0.5) / unit;
}
double k4GeneratorsConfig::eventGenerationCollections2Root::calculateChi2(std::string procName, TH1D* histo,
                                                                          TH1D* refHisto) {

  if (histo->GetNbinsX() != refHisto->GetNbinsX()) {
    std::cout << "Process " << procName << " chi2 test impossible: number of bins incompatible " << histo->GetNbinsX()
              << " != " << refHisto->GetNbinsX() << std::endl;
    return -1.;
  }
  double chi2 = 0.;
  unsigned int nbOfPoints = 0;
  // loop over all bins inclusing underflow and overflow
  for (int i = 0; i < histo->GetNbinsX() + 2; i++) {
    if (histo->GetBinError(i) != 0. || refHisto->GetBinError(i) != 0.) {
      double deltaChi2 = histo->GetBinContent(i) - refHisto->GetBinContent(i);
      deltaChi2 *= deltaChi2;
      // to be checked whether we say "ref" has not error?
      deltaChi2 /=
          (histo->GetBinError(i) * histo->GetBinError(i) + refHisto->GetBinError(i) * refHisto->GetBinError(i));
      chi2 += deltaChi2;
      nbOfPoints++;
    }
  }

  // divide by the number of measurements
  chi2 /= nbOfPoints;

  return chi2;
}
std::vector<std::string> k4GeneratorsConfig::eventGenerationCollections2Root::getLog() { return m_log; }
