#include "eventGenerationCollections2Root.h"
#include <sstream>

#include "TCanvas.h"
#include "TLegend.h"
#include "TMultiGraph.h"
#include "TStyle.h"

k4GeneratorsConfig::eventGenerationCollections2Root::eventGenerationCollections2Root()
    : m_file(0), m_tree(0), m_processCode(-1), m_processSqrtsCode(-1), m_crossSection(0), m_crossSectionError(0.),
      m_sqrts(0.), m_generatorCode(0) {
  m_file = new TFile("eventGenertionSummary.root", "RECREATE");
  Init();
}
k4GeneratorsConfig::eventGenerationCollections2Root::eventGenerationCollections2Root(std::string file)
    : m_file(0), m_tree(0), m_processCode(-1), m_processSqrtsCode(-1), m_crossSection(0), m_crossSectionError(0.),
      m_sqrts(0.), m_generatorCode(0) {
  m_file = new TFile(file.c_str(), "RECREATE");
  Init();
}
void k4GeneratorsConfig::eventGenerationCollections2Root::Init() {
  m_tree = new TTree("CrossSections", "cross sections");
  m_tree->Branch("process", &m_process);
  m_tree->Branch("iprocess", &m_processCode, "iprocess/I");
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
      if (std::stod(m_processSqrts.substr(m_processSqrts.find_last_of("_") + 1, std::string::npos)) == int(m_sqrts*1000)) {
        // remove the underscore
        m_processSqrts.erase(m_process.find_last_of("_"), 1);
      } else {
        // comparison not successful, so we add the sqrts
        m_processSqrts += std::to_string(int(m_sqrts*1000));
      }
    } else {
      m_processSqrts += std::to_string(int(m_sqrts*1000));
    }
  }
  // assign a code for each process
  if (std::find(m_processesSqrtsList.begin(), m_processesSqrtsList.end(), m_processSqrts) ==
      m_processesSqrtsList.end()) {
    m_processesSqrtsList.push_back(m_processSqrts);
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
      m_histos.push_back(new TH2D(name.str().c_str(), desc.str().c_str(), 600, 0., 600., 1000, 0., 10000.));
      name << "Graph";
      m_graphs.push_back(new TGraphErrors());
      m_graphs[m_graphs.size() - 1]->SetName(name.str().c_str());
      name.clear();
      name.str("");
      desc.clear();
      desc.str("");
    }
    // the profile histograms are per process only: "s" for RMS
    name << proc << "Prof";
    desc << "Process: " << proc << ": CrossSection vs Sqrts";
    m_profiles.push_back(new TProfile(name.str().c_str(), desc.str().c_str(), 6000, 0.001, 600.001, 0., 0., "s"));
    name.clear();
    name.str("");
    name << proc << "RMS";
    m_rms.push_back(new TH1D(name.str().c_str(), desc.str().c_str(), 6000, 0.001, 600.001));
    name.clear();
    name.str("");
    desc.clear();
    desc.str("");
  }

  // access the data and write to the histo via the index of the generatorList
  for (unsigned int entry = 0; entry < m_tree->GetEntries(); entry++) {
    // a tree for root analysis
    m_tree->GetEntry(entry);
    // calculate the index of histos and graphs
    unsigned int index = m_generatorCode + m_processCode * m_generatorsList.size();
    // histos as benchmark
    m_histos[index]->Fill(m_sqrts, m_crossSection, 1.);
    // graphs for pecise drawing
    m_graphs[index]->AddPoint(m_sqrts, m_crossSection);
    unsigned int lastPoint = m_graphs[m_generatorCode + m_processCode * m_generatorsList.size()]->GetN() - 1;
    m_graphs[index]->SetPointError(lastPoint, m_sqrts * 1e-4, m_crossSectionError);
    // process profile, but make sure it's positive and > 1ab
    if (m_crossSection > 1.e-6) {
      m_profiles[m_processCode]->Fill(m_sqrts, m_crossSection);
    }
  }

  // for the profileRms divide by the Central value if 1+0
  for (unsigned int i = 0; i < m_rms.size(); i++) {
    // the number of bins is higher by 2 for the vecto overflow and underflow
    unsigned int nbins = m_profiles[i]->GetNbinsX() + 2;
    std::vector<Double_t> content;
    content.resize(nbins, 0.);
    std::vector<Double_t> error;
    error.resize(nbins, 0.);
    std::vector<Double_t> almostzero;
    almostzero.resize(nbins, 0.);
    for (unsigned int k = 0; k < nbins; k++) {
      content[k] = m_profiles[i]->GetBinContent(k);
      error[k] = m_profiles[i]->GetBinError(k);
      if (content[k] > 0.) {
        error[k] = error[k] / content[k];
        almostzero[k] = 1.e-6;
      }
    }
    m_rms[i]->SetContent(&error[0]);
    m_rms[i]->SetError(&almostzero[0]);
  }

  // write the histos out
  for (auto histo : m_histos) {
    histo->Write();
  }
  for (auto graph : m_graphs) {
    graph->Write();
  }
  for (auto prof : m_profiles) {
    prof->Write();
  }
  for (auto prof : m_rms) {
    prof->Write();
  }
}
void k4GeneratorsConfig::eventGenerationCollections2Root::writeCrossSectionFigures() {

  std::stringstream name, desc;
  // produce a png
  TCanvas* c1 = new TCanvas("c1", "CrossSectionsCanvas");
  for (unsigned int proc = 0; proc < m_processesList.size(); proc++) {
    TMultiGraph* mg = new TMultiGraph();
    for (unsigned int gen = 0; gen < m_generatorsList.size(); gen++) {
      unsigned int index = gen + proc * m_generatorsList.size();
      m_graphs[index]->SetStats(kFALSE);
      m_graphs[index]->SetMarkerStyle(20 + gen);
      m_graphs[index]->SetMarkerColor(gen + 1);
      m_graphs[index]->SetMarkerSize(1.25);
      mg->Add(m_graphs[index], "AP");
    }
    // draw and set the stuff for the multigraphs
    mg->Draw("AP");
    mg->GetXaxis()->SetTitle("#sqrt{s} [GeV");
    mg->GetYaxis()->SetTitle("#sigma [pb]");

    name << m_processesList[proc] << ".png";
    c1->BuildLegend(0.55, 0.55, 0.9, 0.9);
    c1->Print(name.str().c_str());

    // clear and delete
    name.clear();
    name.str("");
    delete mg;
    mg = 0;

    // and now the profile, draw first, then modify
    m_profiles[proc]->Draw();
    m_profiles[proc]->SetStats(kFALSE);
    m_profiles[proc]->SetMarkerStyle(20);
    m_profiles[proc]->SetMarkerColor(kBlue);
    m_profiles[proc]->SetMarkerSize(1.25);
    m_profiles[proc]->GetXaxis()->SetTitle("#sqrt{s} [GeV");
    m_profiles[proc]->GetYaxis()->SetTitle("#sigma [pb]");

    name << m_processesList[proc] << "Profile"
         << ".png";
    c1->Print(name.str().c_str());

    // clear and delete
    name.clear();
    name.str("");

    // and now the profile but as Averae, draw first, then modify
    m_rms[proc]->Draw();
    m_rms[proc]->SetStats(kFALSE);
    m_rms[proc]->SetStats(kFALSE);
    m_rms[proc]->SetMarkerStyle(20);
    m_rms[proc]->SetMarkerColor(kBlue);
    m_rms[proc]->SetMarkerSize(1.25);
    m_rms[proc]->GetXaxis()->SetTitle("#sqrt{s} [GeV");
    m_rms[proc]->GetYaxis()->SetTitle("RMS(Generators)/Average(Generators)");

    name << m_processesList[proc] << "RMS"
         << ".png";
    c1->Print(name.str().c_str());

    // clear and delete
    name.clear();
    name.str("");
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
