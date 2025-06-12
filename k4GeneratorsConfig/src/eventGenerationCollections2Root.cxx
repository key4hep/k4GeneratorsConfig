#include "eventGenerationCollections2Root.h"
#include <sstream>

#include "TCanvas.h"
#include "TLegend.h"
#include "TMultiGraph.h"
#include "TStyle.h"

k4GeneratorsConfig::eventGenerationCollections2Root::eventGenerationCollections2Root()
    : m_sqrtsPrecision(1.e-6), m_xsectionMinimal(1.e-12), m_file(0), m_tree(0), m_processCode(-1), m_sqrtsCode(-1),
      m_crossSection(0), m_crossSectionError(0.), m_sqrts(0.), m_generatorCode(0) {
  m_file = new TFile("eventGenerationSummary.root", "RECREATE");
  Init();
}
k4GeneratorsConfig::eventGenerationCollections2Root::eventGenerationCollections2Root(std::string file)
    : m_sqrtsPrecision(1.e-6), m_xsectionMinimal(1.e-12), m_file(0), m_tree(0), m_processCode(-1), m_sqrtsCode(-1),
      m_crossSection(0), m_crossSectionError(0.), m_sqrts(0.), m_generatorCode(0) {
  m_file = new TFile(file.c_str(), "RECREATE");
  Init();
}
void k4GeneratorsConfig::eventGenerationCollections2Root::Init() {
  m_tree = new TTree("CrossSections", "cross sections");
  m_tree->Branch("process", &m_process);
  m_tree->Branch("isqrts", &m_sqrtsCode, "isqrts/I");
  m_tree->Branch("xsec", &m_crossSection, "xsec/D");
  m_tree->Branch("dxsec", &m_crossSectionError, "dxsec/D");
  m_tree->Branch("sqrts", &m_sqrts, "sqrts/D");
  m_tree->Branch("iprocess", &m_processCode, "iprocess/I");
  m_tree->Branch("generator", &m_generator);
  m_tree->Branch("igenerator", &m_generatorCode, "igenerator/I");
}
k4GeneratorsConfig::eventGenerationCollections2Root::~eventGenerationCollections2Root() {}
void k4GeneratorsConfig::eventGenerationCollections2Root::Execute(xsection& xsec) {

  m_generator = xsec.Generator();
  m_process = xsec.Process();
  m_sqrts = int((xsec.SQRTS() * 1.e3) + 0.5) / 1.e3;
  decodeProcGen();
  add2Tree(xsec);
}
void k4GeneratorsConfig::eventGenerationCollections2Root::Execute(analysisHistos& anaHistos) {
  m_generator = anaHistos.Generator();
  m_process = anaHistos.Process();
  m_sqrts = int((anaHistos.SQRTS() * 1.e3) + 0.5) / 1.e3;
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
            TH1D* histo = anaHistos.TH1DHisto(iHisto);
            m_cnvAnalysisHistosNames[iProc].push_back(histo->GetName());
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
        m_cnvAnalysisHistos[iProc][iHisto]->cd(1);
        TH1D* theHisto = anaHistos.TH1DHisto(iHisto);
        desc << m_generator << " " << m_process << " " << m_sqrts << " GeV";
        theHisto->SetTitle(desc.str().c_str());
        desc.clear();
        desc.str("");
        gStyle->SetOptTitle(0);
        theHisto->SetStats(kFALSE);
        theHisto->SetLineColor(2 + m_generatorCode);
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
  m_sqrtsCode = std::find(m_sqrtsList.begin(), m_sqrtsList.end(), m_sqrts) - m_sqrtsList.begin();

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
  m_xsectionMean4Process.resize(m_processesList.size() * m_sqrtsList.size(), 0.);
  m_xsectionRMS4Process.resize(m_processesList.size() * m_sqrtsList.size(), 0.);
  m_xsectionN4Process.resize(m_processesList.size() * m_sqrtsList.size(), 0);
  m_xsectionPROC4Process.resize(m_processesList.size() * m_sqrtsList.size(), -1);

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
      index = m_sqrtsCode + m_processCode * m_generatorsList.size();
      m_xsectionMean4Process[index] += m_crossSection;
      m_xsectionRMS4Process[index] += (m_crossSection * m_crossSection);
      m_xsectionN4Process[index] += 1;
      if (m_xsectionPROC4Process[index] == -1) {
        m_xsectionPROC4Process[index] = m_processCode;
      }
    }
  }

  // now average:
  for (unsigned int iproc = 0; iproc < m_processesList.size(); iproc++) {
    for (unsigned int isqrts = 0; isqrts < m_sqrtsList.size(); isqrts++) {
      unsigned int index = isqrts + iproc * m_sqrtsList.size();
      if (m_xsectionN4Process[index] > 0) {
        // average
        m_xsectionMean4Process[index] /= m_xsectionN4Process[index];
        // average of squares
        m_xsectionRMS4Process[index] /= m_xsectionN4Process[index];
        // the RMS
        m_xsectionRMS4Process[index] =
            sqrt(m_xsectionRMS4Process[index] - m_xsectionMean4Process[index] * m_xsectionMean4Process[index]);
        // now we can fill the entries of the graphs
        if (m_xsectionPROC4Process[index] >= 0) {
          // fill the RMS graphs
          double relRMS = m_xsectionRMS4Process[index] / m_xsectionMean4Process[index];
          m_xsectionRMSGraphs[iproc]->AddPoint(m_sqrtsList[isqrts], relRMS);
          unsigned int lastPoint = m_xsectionRMSGraphs[iproc]->GetN() - 1;
          m_xsectionRMSGraphs[iproc]->SetPointError(lastPoint, 1.e-6);
          for (unsigned int igen = 0; igen < m_generatorsList.size(); igen++) {
            // new index for the deltagraphs
            unsigned int indexDelta = igen + iproc * m_generatorsList.size();
            double relDelta = 0.;
            // we need to get the data from the generator graph, make sure the data is there
            if (int(isqrts) < m_xsectionGraphs[indexDelta]->GetN()) {
              relDelta = (m_xsectionGraphs[indexDelta]->GetPointY(isqrts) - m_xsectionMean4Process[index]) /
                         m_xsectionMean4Process[index];
              m_xsectionDeltaGraphs[indexDelta]->AddPoint(m_sqrtsList[isqrts], relDelta);
              // set the error on the delta to 0
              lastPoint = m_xsectionDeltaGraphs[indexDelta]->GetN() - 1;
              m_xsectionDeltaGraphs[indexDelta]->SetPointError(lastPoint, 1.e-6);
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
  // the canvas is prepared we can now
  for (unsigned int proc = 0; proc < m_processesList.size(); proc++) {
    // top pad
    topPad->cd();
    topPad->SetBottomMargin(0);
    // the cross sections with the graph
    TMultiGraph* mg = new TMultiGraph();
    for (unsigned int gen = 0; gen < m_generatorsList.size(); gen++) {
      unsigned int index = gen + proc * m_generatorsList.size();
      name << m_processesList[proc] << " " << m_generatorsList[gen];
      m_xsectionGraphs[index]->SetName(name.str().c_str());
      m_xsectionGraphs[index]->SetStats(kFALSE);
      m_xsectionGraphs[index]->SetMarkerStyle(20 + gen);
      m_xsectionGraphs[index]->SetMarkerColor(2 + gen);
      m_xsectionGraphs[index]->SetMarkerSize(1.25);
      mg->Add(m_xsectionGraphs[index], "AP");
      name.clear();
      name.str("");
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
    m_xsectionRMSGraphs[proc]->SetStats(kFALSE);
    m_xsectionRMSGraphs[proc]->SetMarkerStyle(20);
    m_xsectionRMSGraphs[proc]->SetMarkerColor(kBlack);
    m_xsectionRMSGraphs[proc]->SetMarkerSize(1.25);

    // now the graph
    TMultiGraph* mgRMS = new TMultiGraph();
    mgRMS->Add(m_xsectionRMSGraphs[proc], "AP");
    mgRMS->Draw("AP");

    // graph drawn we can work on the axes
    mgRMS->GetXaxis()->SetTitle("#sqrt{s} [GeV]");
    mgRMS->GetXaxis()->SetTitleSize(0.12);
    mgRMS->GetXaxis()->SetTitleOffset(0.8);
    mgRMS->GetXaxis()->SetLabelSize(0.1);
    mgRMS->GetYaxis()->SetTitle("RMS/<#sigma>");
    mgRMS->GetYaxis()->SetTitleSize(0.12);
    mgRMS->GetYaxis()->SetTitleOffset(0.4);
    mgRMS->GetYaxis()->SetLabelSize(0.1);

    // generate a name and write a png
    name << m_processesList[proc] << "wRMS.png";
    c1->Print(name.str().c_str());
    name.clear();
    name.str("");

    // now we do a second figure where we update only the bottom
    bottomPad->cd();
    bottomPad->Clear();

    // the multigraph
    TMultiGraph* mgDelta = new TMultiGraph();
    for (unsigned int gen = 0; gen < m_generatorsList.size(); gen++) {
      unsigned int index = gen + proc * m_generatorsList.size();
      name << m_processesList[proc] << " " << m_generatorsList[gen];
      m_xsectionDeltaGraphs[index]->SetName(name.str().c_str());
      m_xsectionDeltaGraphs[index]->SetStats(kFALSE);
      m_xsectionDeltaGraphs[index]->SetMarkerStyle(20 + gen);
      m_xsectionDeltaGraphs[index]->SetMarkerColor(2 + gen);
      m_xsectionDeltaGraphs[index]->SetMarkerSize(1.25);
      mgDelta->Add(m_xsectionDeltaGraphs[index], "AP");
      name.clear();
      name.str("");
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
    mgDelta->GetYaxis()->SetLabelSize(0.1);

    // generate a name and write a png
    name << m_processesList[proc] << "wDelta.png";
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
  analysisHistosAverage.resize(m_processesSqrtsList.size());
  for (unsigned int proc = 0; proc < m_processesSqrtsList.size(); proc++) {
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
	  if ( generatorAverageHisto == nullptr ){
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
  for (unsigned int proc = 0; proc < m_processesSqrtsList.size(); proc++) {
    // check that it's the correct process
    for (unsigned int ihisto = 0; ihisto < m_cnvAnalysisHistos[proc].size(); ihisto++) {
      name << m_processesSqrtsList[proc] << m_cnvAnalysisHistosNames[proc][ihisto] << ".png";
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
          // check the compatibility of the histo compared to average
          calculateChi2(m_processesSqrtsList[proc], theDelta, analysisHistosAverage[proc][ihisto]);
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
          theDelta->GetYaxis()->SetLabelSize(0.1);
        }
      }
      // done, save the canvas
      m_cnvAnalysisHistos[proc][ihisto]->Print(name.str().c_str());
      name.clear();
      name.str("");
    }
  }
}
void k4GeneratorsConfig::eventGenerationCollections2Root::writeTree() { m_tree->Write(); }
void k4GeneratorsConfig::eventGenerationCollections2Root::calculateChi2(std::string procName, TH1D* histo,
                                                                        TH1D* refHisto) {

  if (histo->GetNbinsX() != refHisto->GetNbinsX()) {
    std::cout << "Process " << procName << " chi2 test impossible: number of bins incompatible " << histo->GetNbinsX()
              << " != " << refHisto->GetNbinsX() << std::endl;
  }
  double chi2 = 0.;
  unsigned int nbOfPoints = 0;
  for (int i = 0; i < histo->GetNbinsX() + 2; i++) {
    if (histo->GetBinError(i) != 0. || refHisto->GetBinError(i) != 0.) {
      double deltaChi2 = histo->GetBinContent(i) - refHisto->GetBinContent(i);
      deltaChi2 *= deltaChi2;
      // to be checked whether we say "ref" has not error?
      deltaChi2 /= (histo->GetBinError(i) * histo->GetBinError(i) + refHisto->GetBinError(i) * refHisto->GetBinError(i));
      chi2 += deltaChi2;
      nbOfPoints++;
    }
  }

  // divide by the number of measurements
  chi2 /= nbOfPoints;
  std::cout << "Proc " << procName << " Generator " << histo->GetTitle() << " Type " << refHisto->GetXaxis()->GetTitle()
            << " chi2 = " << chi2 << std::endl;
}
