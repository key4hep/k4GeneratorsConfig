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
    //    if ( yamlsPath.extension() == ".yaml" ) continue;
    if ( !std::filesystem::is_directory(yamlsPath) ) continue;

    for (const auto& generators : std::filesystem::directory_iterator(yamlsPath.string()+"/Run-Cards")) {
      std::filesystem::path generatorsPath = generators.path();
      if ( !std::filesystem::is_directory(generatorsPath) ) continue;

      for (const auto& procs : std::filesystem::directory_iterator(generatorsPath.string())) {
	std::filesystem::path processPath = procs.path();
	if ( !std::filesystem::is_directory(processPath) ) continue;

	for (const auto& files : std::filesystem::directory_iterator(processPath.string())) {
	  std::filesystem::path filenamePath = files.path();
	  if ( !std::filesystem::is_regular_file(filenamePath) ) continue;
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

  // order by length
  //std::sort(m_xsectionCollection.begin(),m_xsectionCollection.end(),[this](xsection A, xsection B){ return this->compareLength(A,B);});

  // order by content
  std::sort(m_xsectionCollection.begin(),m_xsectionCollection.end(),[this](xsection A, xsection B){ return this->compareLexical(A,B);});

}
bool k4GeneratorsConfig::xsectionCollection::compareLength(xsection A, xsection B){

  // retrieve the process as ordering variable
  std::string processA = A.Process();
  std::string processB = B.Process();
  
  return processA.size() < processB.size();
}
bool k4GeneratorsConfig::xsectionCollection::compareLexical(xsection A, xsection B){

  // retrieve the process as ordering variable
  std::string processA = A.Process();
  std::string processB = B.Process();
  std::vector<std::string> listOf2;
  listOf2.push_back(processA);
  listOf2.push_back(processB);
  sort(listOf2.begin(),listOf2.end());

  // if the order is changed return true otherwise false
  if ( processA.compare(listOf2[0]) == 0 ) return true;
  
  return false;
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
      output << proc << " sqrts= " << xsec.SQRTS() << ":" << std::endl;
      previousProcess = proc;
    }
    // print the generator name and cross section with its error
    output << std::setw(15) << std::left << xsec.Generator() << " " 
	   << std::setw(8 ) << std::left << xsec.Xsection() << " +- " 
	   << std::setw(8)  << std::left << xsec.XsectionError() << " pb" << std::endl;
  }
  output << std::endl;

}
