#include "analysisHistos.h"
#include <iostream>
#include <memory>

#include "TFile.h"
#include "TKey.h"
#include "TROOT.h"

k4GeneratorsConfig::analysisHistos::analysisHistos()
    : m_sqrts(0.), m_generator(""), m_process(""), m_file(""), m_isValid(false) {}
k4GeneratorsConfig::analysisHistos::analysisHistos(const analysisHistos& theOriginal) {
  if (this != &theOriginal) {
    m_sqrts = theOriginal.m_sqrts;
    m_generator = theOriginal.m_generator;
    m_process = theOriginal.m_process;
    m_file = theOriginal.m_file;
    m_isValid = theOriginal.m_isValid;
    for (auto histo : theOriginal.m_listOfHists) {
      m_listOfHists.push_back(new TH1D(*histo));
    }
  }
}
k4GeneratorsConfig::analysisHistos& k4GeneratorsConfig::analysisHistos::operator=(const analysisHistos& theOriginal) {
  if (this != &theOriginal) {
    m_sqrts = theOriginal.m_sqrts;
    m_generator = theOriginal.m_generator;
    m_process = theOriginal.m_process;
    m_file = theOriginal.m_file;
    m_isValid = theOriginal.m_isValid;
    for (auto hist : m_listOfHists) {
      delete hist;
    }
    m_listOfHists.clear();
    for (auto hist : theOriginal.m_listOfHists) {
      m_listOfHists.push_back(new TH1D(*hist));
    }
  }

  return *this;
}
k4GeneratorsConfig::analysisHistos::~analysisHistos() {}
bool k4GeneratorsConfig::analysisHistos::processFile() {

  // open the root file
  std::unique_ptr<TFile> theFile(TFile::Open(m_file.c_str()));
  if (!theFile || theFile->IsZombie())
    return false;

  // retrieve the RunInfo for the weight names, there should only be 1 entry per Run
  TIter keyList(theFile->GetListOfKeys());
  TKey* key;
  while ((key = (TKey*)keyList())) {
    TClass* cl = gROOT->GetClass(key->GetClassName());
    if (cl->InheritsFrom("TH1")) {
      m_listOfHists.push_back(new TH1D(*(TH1D*)key->ReadObj()));
      // turn ownership over to analysisHistos:
      m_listOfHists[m_listOfHists.size() - 1]->SetDirectory(0);
    }
  }

  return true;
}
void k4GeneratorsConfig::analysisHistos::setSQRTS(double sqrts) { m_sqrts = sqrts; }
void k4GeneratorsConfig::analysisHistos::setGenerator(std::string gen) { m_generator = gen; }
void k4GeneratorsConfig::analysisHistos::setProcess(std::string proc) { m_process = proc; }
void k4GeneratorsConfig::analysisHistos::setFile(std::string file) {
  m_file = file;
  m_isValid = processFile();
}
double k4GeneratorsConfig::analysisHistos::SQRTS() { return m_sqrts; }
std::string k4GeneratorsConfig::analysisHistos::Generator() { return m_generator; }
std::string k4GeneratorsConfig::analysisHistos::Process() { return m_process; }
std::string k4GeneratorsConfig::analysisHistos::File() { return m_file; }
bool k4GeneratorsConfig::analysisHistos::isValid() { return m_isValid; }
TH1D* k4GeneratorsConfig::analysisHistos::TH1DHisto(unsigned int iHisto) {
  return m_listOfHists.size() > 0 ? m_listOfHists[iHisto] : 0;
}
unsigned int k4GeneratorsConfig::analysisHistos::NbOf1DHistos() { return m_listOfHists.size(); }
void k4GeneratorsConfig::analysisHistos::Print() {
  std::cout << std::endl;
  std::cout << "AnalysisHistos object summary:" << std::endl;
  std::cout << "File                : " << m_file << std::endl;
  std::cout << "Process             : " << m_process << std::endl;
  std::cout << "SQRTS               : " << m_sqrts << std::endl;
  std::cout << "Generator           : " << m_generator << std::endl;
  std::cout << "analysisHistos valid: " << m_isValid << std::endl;
  std::cout << std::endl;
}
