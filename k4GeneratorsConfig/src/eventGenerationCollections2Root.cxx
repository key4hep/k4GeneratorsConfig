#include "eventGenerationCollections2Root.h"
#include <sstream>

#include "TCanvas.h"
#include "TLegend.h"
#include "TMultiGraph.h"
#include "TStyle.h"

k4GeneratorsConfig::eventGenerationCollections2Root::eventGenerationCollections2Root()
    : m_sqrtsPrecision(1.e-6), m_xsectionMinimal(1.e-12), m_file(0), m_tree(0), m_processCode(-1),
      m_processSqrtsCode(-1), m_crossSection(0), m_crossSectionError(0.), m_sqrts(0.), m_generatorCode(0) {
  m_file = new TFile("eventGenerationSummary.root", "RECREATE");
  Init();
}
k4GeneratorsConfig::eventGenerationCollections2Root::eventGenerationCollections2Root(std::string file)
    : m_sqrtsPrecision(1.e-6), m_xsectionMinimal(1.e-12), m_file(0), m_tree(0), m_processCode(-1),
      m_processSqrtsCode(-1), m_crossSection(0), m_crossSectionError(0.), m_sqrts(0.), m_generatorCode(0) {
  m_file = new TFile(file.c_str(), "RECREATE");
  Init();
}
void k4GeneratorsConfig::eventGenerationCollections2Root::Init() {
  m_tree = new TTree("CrossSections", "cross sections");
  m_tree->Branch("process", &m_process);
  m_tree->Branch("iprocess", &m_processCode, "iprocess/I");
  m_tree->Branch("iprocesssqrts", &m_processSqrtsCode, "iprocesssqrts/I");
  m_tree->Branch("xsec", &m_crossSection, "xsec/D");
  m_tree->Branch("dxsec", &m_crossSectionError, "dxsec/D");
  m_tree->Branch("sqrts", &m_sqrts, "sqrts/D");
  m_tree->Branch("generator", &m_generator);
  m_tree->Branch("igenerator", &m_generatorCode, "igenerator/I");
}
k4GeneratorsConfig::eventGenerationCollections2Root::~eventGenerationCollections2Root() {}
void k4GeneratorsConfig::eventGenerationCollections2Root::Execute(xsection& xsec) {

  m_generator = xsec.Generator();
  m_process = xsec.Process();
  m_sqrts = xsec.SQRTS();
  decodeProcGen();
  add2Tree(xsec);
}
void k4GeneratorsConfig::eventGenerationCollections2Root::Execute(analysisHistos& anaHistos) {
  m_generator = anaHistos.Generator();
  m_process = anaHistos.Process();
  m_sqrts = anaHistos.SQRTS();
  // for safety decode the the process code and the generator
  decodeProcGen();
  // if it's the first occurrence of a set, need to prepare the canvas vector:
  m_cnvAnalysisHistos.resize(m_processesSqrtsList.size());
  m_cnvAnalysisHistosNames.resize(m_processesSqrtsList.size());
  std::stringstream name, desc;
  for (unsigned int iProc = 0; iProc < m_processesSqrtsList.size(); iProc++) {
    // check that it's the correct process
    if (!m_processesSqrtsList[iProc].compare(m_processSqrts)) {
      // that there are histograms
      if (anaHistos.NbOf1DHistos() > 0) {
        // and so far no canvases have been prepared
        if (m_cnvAnalysisHistos[iProc].size() == 0) {
          // prepare the canvases
          for (unsigned int iHisto = 0; iHisto < anaHistos.NbOf1DHistos(); iHisto++) {
            name << m_processesSqrtsList[iProc] << " " << anaHistos.TH1DHisto(iHisto)->GetName();
            desc << "Process: " << m_processesSqrtsList[iProc];
            m_cnvAnalysisHistos[iProc].push_back(new TCanvas(name.str().c_str(), desc.str().c_str()));
            m_cnvAnalysisHistosNames[iProc].push_back(anaHistos.TH1DHisto(iHisto)->GetName());
            name.clear();
            name.str("");
            desc.clear();
            desc.str("");
          }
        }
      }
    }
  }
  // the canvas vector is ready, so we can fill the canvas:
  // - determine the index from the process sqrts
  unsigned int iProc = std::find(m_processesSqrtsList.begin(), m_processesSqrtsList.end(), m_processSqrts) -
                       m_processesSqrtsList.begin();
  // - check that the index is valid (not found==size) and that there are histos to add
  if (iProc < m_processesSqrtsList.size() && anaHistos.NbOf1DHistos() > 0) {
    // now add the histos
    for (auto histo : anaHistos.TH1DHistos()) {
      unsigned int iHisto =
          std::find(m_cnvAnalysisHistosNames[iProc].begin(), m_cnvAnalysisHistosNames[iProc].end(), histo->GetName()) -
          m_cnvAnalysisHistosNames[iProc].begin();
      if (iHisto < m_cnvAnalysisHistos[iProc].size()) {
        m_cnvAnalysisHistos[iProc][iHisto]->cd();
        TH1D* theHisto = anaHistos.TH1DHisto(iHisto);
        desc << m_generator << " " << theHisto->GetTitle();
        theHisto->SetTitle(desc.str().c_str());
        desc.clear();
        desc.str("");
        gStyle->SetOptTitle(0);
        theHisto->SetStats(kFALSE);
        theHisto->SetLineColor(m_generatorCode + 1);
        theHisto->SetMinimum(0);
        theHisto->Draw("SAME");
      }
    }
  }
}
void k4GeneratorsConfig::eventGenerationCollections2Root::decodeProcGen() {

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

  // first determined the sqrts code and add to list
  // copy to work on it
  m_processSqrts = m_process;
  // check consistency
  if (m_processSqrts.find_last_of("_") != std::string::npos) {
    // make sure that _ is not the last character
    if (m_processSqrts.find_last_of("_") + 1 != std::string::npos) {
      // compare to sqrts, but limit precision to something reasonable (set in constructor)
      if (abs(std::stoi(m_processSqrts.substr(m_processSqrts.find_last_of("_") + 1, std::string::npos)) -
              int(m_sqrts * 1000)) /
              int(m_sqrts * 1000) <
          m_sqrtsPrecision) {
        // remove the underscore
        m_processSqrts.erase(m_process.find_last_of("_"), 1);
      } else {
        // comparison not successful, so we add the sqrts
        m_processSqrts += std::to_string(int(m_sqrts * 1000));
      }
    } else {
      m_processSqrts += std::to_string(int(m_sqrts * 1000));
    }
  }
  // assign a code for each process
  if (std::find(m_processesSqrtsList.begin(), m_processesSqrtsList.end(), m_processSqrts) ==
      m_processesSqrtsList.end()) {
    m_processesSqrtsList.push_back(m_processSqrts);
    m_sqrtsList.push_back(m_sqrts);
  }
  m_processSqrtsCode = std::find(m_processesSqrtsList.begin(), m_processesSqrtsList.end(), m_processSqrts) -
                       m_processesSqrtsList.begin();

  // process needs to be processed to remove everything from the subscript on:
  if (m_process.find_last_of("_") != std::string::npos) {
    m_process.erase(m_process.find_last_of("_"));
  }
  // assign a code for each process
  if (std::find(m_processesList.begin(), m_processesList.end(), m_process) == m_processesList.end()) {
    m_processesList.push_back(m_process);
  }

  m_processCode = std::find(m_processesList.begin(), m_processesList.end(), m_process) - m_processesList.begin();
}
void k4GeneratorsConfig::eventGenerationCollections2Root::add2Tree(xsection& xsec) {

  // do things
  m_crossSection = xsec.Xsection();
  m_crossSectionError = xsec.XsectionError();
  m_sqrts = xsec.SQRTS();

  // write to the tree
  m_tree->Fill();
}
void k4GeneratorsConfig::eventGenerationCollections2Root::Finalize() {
  // go to the top root directory
  m_file->cd();
  // the total cross section tree and comparison histos
  writeHistos();
  writeTree();
  // write cross section images
  writeCrossSectionFigures();
  // deal with the analysisHistos distributions
  writeAnalysisHistosFigures();
  // close the file
  m_file->Close();
}
void k4GeneratorsConfig::eventGenerationCollections2Root::writeHistos() {

  std::stringstream name, desc;
  for (auto proc : m_processesList) {
    for (auto gen : m_generatorsList) {
      name << gen << proc;
      desc << gen << "::Process: " << proc << ": CrossSection vs Sqrts";
      m_xsectionGraphs.push_back(new TGraphErrors());
      m_xsectionGraphs.back()->SetName(name.str().c_str());
      name.clear();
      name.str("");
      desc.clear();
      desc.str("");
    }
    // the RMS does not need the loop over the generators
    name << proc << "RMS";
    desc << "Process: " << proc << ": CrossSection vs Sqrts";
    m_xsectionRMSGraphs.push_back(new TGraphErrors());
    m_xsectionRMSGraphs.back()->SetName(name.str().c_str());
    name.clear();
    name.str("");
    desc.clear();
    desc.str("");
  }

  // to calculate per Process and Sqrts average cross section, RMS and number of entries
  m_xsectionMean4ProcessSqrts.resize(m_processesSqrtsList.size(), 0.);
  m_xsectionRMS4ProcessSqrts.resize(m_processesSqrtsList.size(), 0.);
  m_xsectionN4ProcessSqrts.resize(m_processesSqrtsList.size(), 0);
  m_xsectionPROC4ProcessSqrts.resize(m_processesSqrtsList.size(), -1);

  // access the data and write to the histo via the index of the generatorList
  for (unsigned int entry = 0; entry < m_tree->GetEntries(); entry++) {
    // a tree for root analysis
    m_tree->GetEntry(entry);
    // calculate the index of histos and graphs
    unsigned int index = m_generatorCode + m_processCode * m_generatorsList.size();
    // graphs for pecise drawing
    m_xsectionGraphs[index]->AddPoint(m_sqrts, m_crossSection);
    unsigned int lastPoint = m_xsectionGraphs[index]->GetN() - 1;
    m_xsectionGraphs[index]->SetPointError(lastPoint, m_sqrts * 1e-4, m_crossSectionError);
    // process profile, but make sure it's positive and > 1ab
    if (m_crossSection > m_xsectionMinimal) {
      // accumulate the averages and the squares:
      index = m_processSqrtsCode;
      m_xsectionMean4ProcessSqrts[index] += m_crossSection;
      m_xsectionRMS4ProcessSqrts[index] += (m_crossSection * m_crossSection);
      m_xsectionN4ProcessSqrts[index] += 1;
      if (m_xsectionPROC4ProcessSqrts[index] == -1) {
        m_xsectionPROC4ProcessSqrts[index] = m_processCode;
      }
    }
  }

  // now average:
  for (unsigned int iproc = 0; iproc < m_processesSqrtsList.size(); iproc++) {
    if (m_xsectionN4ProcessSqrts[iproc] > 0) {
      // average
      m_xsectionMean4ProcessSqrts[iproc] /= m_xsectionN4ProcessSqrts[iproc];
      // average of squares
      m_xsectionRMS4ProcessSqrts[iproc] /= m_xsectionN4ProcessSqrts[iproc];
      // the RMS
      m_xsectionRMS4ProcessSqrts[iproc] = sqrt(m_xsectionRMS4ProcessSqrts[iproc] -
                                               m_xsectionMean4ProcessSqrts[iproc] * m_xsectionMean4ProcessSqrts[iproc]);
      // now we can fill the entries of the graphs
      if (m_xsectionPROC4ProcessSqrts[iproc] >= 0) {
        double relRMS = m_xsectionRMS4ProcessSqrts[iproc] / m_xsectionMean4ProcessSqrts[iproc];
        m_xsectionRMSGraphs[m_xsectionPROC4ProcessSqrts[iproc]]->AddPoint(m_sqrtsList[iproc], relRMS);
        // set the error on the RMS to 0
        unsigned int lastPoint = m_xsectionRMSGraphs[m_xsectionPROC4ProcessSqrts[iproc]]->GetN() - 1;
        m_xsectionRMSGraphs[m_xsectionPROC4ProcessSqrts[iproc]]->SetPointError(lastPoint, 1.e-6);
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
}
void k4GeneratorsConfig::eventGenerationCollections2Root::writeCrossSectionFigures() {

  std::stringstream name, desc;
  // produce a png
  TCanvas* c1 = new TCanvas("c1", "CrossSectionsCanvas");
  TPad* topPad = new TPad("topPad", "The pad 70% of the height", 0.0, 0.3, 1.0, 1.0, 0);
  TPad* bottomPad = new TPad("bottomPad", "The pad 30% of the height", 0.0, 0.0, 1.0, 0.3, 0);
  topPad->Draw();
  bottomPad->Draw();
  // the canvas is prepared we can now
  for (unsigned int proc = 0; proc < m_processesList.size(); proc++) {
    // top pad
    topPad->cd();
    topPad->SetBottomMargin(0);
    // the cross sections with the graph
    TMultiGraph* mg = new TMultiGraph();
    for (unsigned int gen = 0; gen < m_generatorsList.size(); gen++) {
      unsigned int index = gen + proc * m_generatorsList.size();
      m_xsectionGraphs[index]->SetStats(kFALSE);
      m_xsectionGraphs[index]->SetMarkerStyle(20 + gen);
      m_xsectionGraphs[index]->SetMarkerColor(2 + gen);
      m_xsectionGraphs[index]->SetMarkerSize(1.25);
      mg->Add(m_xsectionGraphs[index], "AP");
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

    // and now the lower part with the RMS/average
    bottomPad->cd();
    bottomPad->SetTopMargin(0);
    bottomPad->SetBottomMargin(0.25);
    // now the graph (only one)
    TMultiGraph* mgRMS = new TMultiGraph();
    m_xsectionRMSGraphs[proc]->SetStats(kFALSE);
    m_xsectionRMSGraphs[proc]->SetMarkerStyle(20);
    m_xsectionRMSGraphs[proc]->SetMarkerColor(kBlack);
    m_xsectionRMSGraphs[proc]->SetMarkerSize(1.25);
    mgRMS->Add(m_xsectionRMSGraphs[proc], "AP");
    mgRMS->Draw("AP");

    //
    mgRMS->GetXaxis()->SetTitle("#sqrt{s} [GeV]");
    mgRMS->GetXaxis()->SetTitleSize(0.12);
    mgRMS->GetXaxis()->SetTitleOffset(0.8);
    mgRMS->GetXaxis()->SetLabelSize(0.1);
    mgRMS->GetYaxis()->SetTitle("RMS/<#sigma>");
    mgRMS->GetYaxis()->SetTitleSize(0.12);
    mgRMS->GetYaxis()->SetTitleOffset(0.4);
    mgRMS->GetYaxis()->SetLabelSize(0.1);

    // generate a name and write a png
    name << m_processesList[proc] << ".png";
    c1->Print(name.str().c_str());

    // clear and delete
    name.clear();
    name.str("");
    delete mg;
    mg = 0;
    delete mgRMS;
    mgRMS = 0;
  }
  delete c1;
}
void k4GeneratorsConfig::eventGenerationCollections2Root::writeAnalysisHistosFigures() {

  // if the canvas is not filled do not try
  if (m_cnvAnalysisHistos.size() == 0)
    return;

  std::stringstream name;
  // now write out the superposed histograms
  for (unsigned int proc = 0; proc < m_processesSqrtsList.size(); proc++) {
    // check that it's the correct process
    for (unsigned int cnvs = 0; cnvs < m_cnvAnalysisHistos[proc].size(); cnvs++) {
      name << m_processesSqrtsList[proc] << m_cnvAnalysisHistosNames[proc][cnvs] << ".png";
      m_cnvAnalysisHistos[proc][cnvs]->BuildLegend();
      m_cnvAnalysisHistos[proc][cnvs]->Print(name.str().c_str());
      name.clear();
      name.str("");
    }
  }
}
void k4GeneratorsConfig::eventGenerationCollections2Root::writeTree() { m_tree->Write(); }
