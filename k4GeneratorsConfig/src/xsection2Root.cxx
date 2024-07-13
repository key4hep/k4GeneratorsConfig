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

  if ( std::find(m_generatorsList.begin(),m_generatorsList.end(),m_generator)== m_generatorsList.end() ) {
    m_generatorsList.push_back(m_generator);
  }
  
  m_generatorCode     = std::find(m_generatorsList.begin(),m_generatorsList.end(),m_generator) - m_generatorsList.begin();  
  // write to the tree
  m_tree->Fill();
  
}
void k4GeneratorsConfig::xsection2Root::writeTree(){

  m_file->cd();
  m_tree->Write();
  m_file->Close();
}
