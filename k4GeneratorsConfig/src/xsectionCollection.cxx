#include "xsectionCollection.h"
#include <filesystem>
#include <algorithm>
#include <iostream>
#include <sys/stat.h>

k4GeneratorsConfig::xsectionCollection::xsectionCollection()
{

}
k4GeneratorsConfig::xsectionCollection::xsectionCollection(const xsectionCollection& theOriginal)
{
  if ( this != &theOriginal ){
    m_xsectionCollection = theOriginal.m_xsectionCollection;
  }
}
k4GeneratorsConfig::xsectionCollection& k4GeneratorsConfig::xsectionCollection::operator=(const xsectionCollection& theOriginal)
{
  if ( this != &theOriginal ){
    m_xsectionCollection = theOriginal.m_xsectionCollection;
  }

  return *this;
}
k4GeneratorsConfig::xsectionCollection::~xsectionCollection(){
}
void k4GeneratorsConfig::xsectionCollection::Execute(){

  // first make the collection
  makeCollection();

  // second order the collection according to the process
  orderCollection();

  // third print the final results
  Print();
}
void k4GeneratorsConfig::xsectionCollection::makeCollection(){

  for (const auto& yamls : std::filesystem::directory_iterator(".")) {
    std::filesystem::path yamlsPath = yamls.path();
    if ( yamlsPath.extension() == ".yaml" ) continue;
    for (const auto& generators : std::filesystem::directory_iterator(yamlsPath.string()+"/Run-Cards")) {
      std::filesystem::path generatorsPath = generators.path();
      for (const auto& procs : std::filesystem::directory_iterator(generatorsPath.string())) {
	std::filesystem::path processPath = procs.path();
	for (const auto& files : std::filesystem::directory_iterator(processPath.string())) {
	  std::filesystem::path filenamePath = files.path();
	  if ( filenamePath.extension() == ".edm4hep" ){
	    k4GeneratorsConfig::xsection *xsec = new k4GeneratorsConfig::xsection();
	    xsec->setProcess(processPath.filename().string());
	    xsec->setGenerator(generatorsPath.filename().string());
	    xsec->setFile(filenamePath.string());
	    m_xsectionCollection.push_back(*xsec);
	    delete xsec;
	  }
	}
      }
    }
  }

}
void k4GeneratorsConfig::xsectionCollection::orderCollection(){

  std::sort(m_xsectionCollection.begin(),m_xsectionCollection.end(),[this](xsection A, xsection B){ return this->compareAB(A,B);});

}
bool k4GeneratorsConfig::xsectionCollection::compareAB(xsection A, xsection B){

  // retrieve the process as ordering variable
  std::string processA = A.Process();
  std::string processB = B.Process();
  
  if ( processA.size() < processB.size() ) return true;
  if ( processA.size() > processB.size() ) return true;
  // now only strings of equal size remain
  return !processA.compare(processB);
}
void k4GeneratorsConfig::xsectionCollection::Print(bool onlyOK){
  
  for (auto xsec: m_xsectionCollection){
    if ( !onlyOK ){
      xsec.Print();
    }
    else {
      if ( xsec.isValid() ){
      xsec.Print();
      }
    }

  }
}
void k4GeneratorsConfig::xsectionCollection::PrintSummary(std::ostream &output) const {

  std::string previousProcess= "XXXX";
  for (auto xsec: m_xsectionCollection){
    // only print valid cross sections
    if ( !xsec.isValid() ) continue;
    // if it's a new process print a new line
    std::string proc = xsec.Process();
    if ( proc.compare(previousProcess) != 0 ){
      if ( previousProcess.compare("XXXX")!= 0 ) output << std::endl;
      output << proc << ":" << std::endl;
      previousProcess = proc;
    }
    // print the generator name and cross section with its error
    output << xsec.Generator() << " " << xsec.Xsection() << " +- " << xsec.XsectionError() << " pb" << std::endl;
  }

}
