#include <sstream>
#include "xsection2Root.h"

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
      name.clear(); name.str(""); desc.clear(); desc.str("");
    }
  }

  //access the data and write to the histo via the index of the generatorList
  for (unsigned int entry=0; entry < m_tree->GetEntries(); entry++){
    m_tree->GetEntry(entry);
    m_histos[m_generatorCode+m_processCode*m_generatorsList.size()]->Fill(m_sqrts,m_crossSection,1.);
  }

  // write the histos out
  for (auto histo: m_histos){
    histo->Write();
  }
}
void k4GeneratorsConfig::xsection2Root::writeTree(){
  m_tree->Write();
}
