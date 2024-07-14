#include <sstream>
#include "xsection2Root.h"

#include "TCanvas.h"
#include "TMultiGraph.h"

k4GeneratorsConfig::xsection2Root::xsection2Root()
{
  m_file = new TFile("xsection2RootSummary.root","RECREATE");
  Init();
}
k4GeneratorsConfig::xsection2Root::xsection2Root(std::string file)
{
  m_file = new TFile(file.c_str(),"RECREATE");
  Init();
}
void k4GeneratorsConfig::xsection2Root::Init(){
  m_tree = new TTree("CrossSections","cross sections");
  m_tree->Branch("process",&m_process);
  m_tree->Branch("iprocess",&m_processCode,"iprocess/I");
  m_tree->Branch("xsec",&m_crossSection,"xsec/D");
  m_tree->Branch("dxsec",&m_crossSectionError,"dxsec/D");
  m_tree->Branch("sqrts",&m_sqrts,"sqrts/D");
  m_tree->Branch("generator",&m_generator);
  m_tree->Branch("igenerator",&m_generatorCode,"igenerator/I");
}
k4GeneratorsConfig::xsection2Root::~xsection2Root(){
}
void k4GeneratorsConfig::xsection2Root::add2Tree(xsection &xsec){

  // do things
  m_crossSection      = xsec.Xsection();
  m_crossSectionError = xsec.XsectionError();
  m_sqrts             = xsec.SQRTS();
  m_generator         = xsec.Generator();

  //need to remove - from the names
  if ( m_generator.find("-") != std::string::npos ){
    m_generator.erase(m_generator.find("-"),1);
  }
  if ( m_generator.find("@") != std::string::npos ){
    m_generator.erase(m_generator.find("@"),1);
  }
  if ( m_generator.find("_") != std::string::npos ){
    m_generator.erase(m_generator.find("_"),1);
  }
  
  // assign a code for each generator
  if ( std::find(m_generatorsList.begin(),m_generatorsList.end(),m_generator)== m_generatorsList.end() ) {
    m_generatorsList.push_back(m_generator);
  }
  
  m_generatorCode     = std::find(m_generatorsList.begin(),m_generatorsList.end(),m_generator) - m_generatorsList.begin();

  // process needs to be processed to removeeveything form the subscript on:
  m_process           = xsec.Process();
  if ( m_process.find_last_of("_") != std::string::npos ){
    m_process.erase(m_process.find_last_of("_"));
  }
  // assign a code for each generator
  if ( std::find(m_processesList.begin(),m_processesList.end(),m_process)== m_processesList.end() ) {
    m_processesList.push_back(m_process);
  }
  
  m_processCode     = std::find(m_processesList.begin(),m_processesList.end(),m_process) - m_processesList.begin();

  // write to the tree
  m_tree->Fill();
  
}
void k4GeneratorsConfig::xsection2Root::Finalize(){
  m_file->cd();
  writeHistos();
  writeTree();
  m_file->Close();

}
void k4GeneratorsConfig::xsection2Root::writeHistos(){

  std::stringstream name, desc;
  for (auto proc: m_processesList){
    for (auto gen: m_generatorsList){
      name << gen << proc;
      desc << gen << "::Process: " << proc << ": CrossSection vs Sqrts";
      m_histos.push_back(new TH2D(name.str().c_str(),desc.str().c_str(),600,0.,600.,1000,0.,10000.));
      name << "Graph";
      m_graphs.push_back(new TGraphErrors());
      m_graphs[m_graphs.size()-1]->SetName(name.str().c_str());
      name.clear(); name.str(""); desc.clear(); desc.str("");
    }
  }

  //access the data and write to the histo via the index of the generatorList
  for (unsigned int entry=0; entry < m_tree->GetEntries(); entry++){
    // a tree for root analysis
    m_tree->GetEntry(entry);
    // calculate the index of histos and graphs
    unsigned int index = m_generatorCode+m_processCode*m_generatorsList.size();
    // histos as benchmark
    m_histos[index]->Fill(m_sqrts,m_crossSection,1.);
    // graphs for pecise drawing
    m_graphs[index]->AddPoint(m_sqrts,m_crossSection);
    unsigned int lastPoint = m_graphs[m_generatorCode+m_processCode*m_generatorsList.size()]->GetN()-1;
    m_graphs[index]->SetPointError(lastPoint,m_sqrts*1e-4,m_crossSectionError);
  }
  // write the histos out
  for (auto histo: m_histos){
    histo->Write();
  }
  for (auto graph: m_graphs){
    graph->Write();
  }
  // produce a png
  TCanvas *c1 = new TCanvas("c1","CrossSectionsCanvas");
  for (unsigned int proc=0; proc<m_processesList.size(); proc++){
    TMultiGraph *mg = new TMultiGraph();
    for (unsigned int gen=0; gen<m_generatorsList.size(); gen++){
      unsigned int index = gen+proc*m_generatorsList.size();
      m_graphs[index]->SetStats(kFALSE);
      m_graphs[index]->SetMarkerStyle(20+gen);
      m_graphs[index]->SetMarkerColor(gen);
      m_graphs[index]->SetMarkerSize(1.5);
      mg->Add(m_graphs[index],"AP");
    }
    // draw and set the stuff for the multigraphs
    mg->Draw("AP");
    mg->GetXaxis()->SetTitle("#sqrt{s} [GeV");
    mg->GetYaxis()->SetTitle("#sigma [pb]");

    name << m_processesList[proc] << ".png";
    c1->BuildLegend(0.55,0.55,0.9,0.9);
    c1->Print(name.str().c_str());

    // clear and delete
    name.clear(); name.str("");
    delete mg; mg=0;
  }

  delete c1; 
}
void k4GeneratorsConfig::xsection2Root::writeTree(){
  m_tree->Write();
}
