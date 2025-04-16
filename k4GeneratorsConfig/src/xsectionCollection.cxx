#include "xsectionCollection.h"
#include "xsection2Root.h"
#include <filesystem>
#include <algorithm>
#include <iostream>
#include <sys/stat.h>

k4GeneratorsConfig::xsectionCollection::xsectionCollection():
  m_validCounter(0),
  m_invalidCounter(0)
{

}
k4GeneratorsConfig::xsectionCollection::xsectionCollection(const xsectionCollection& theOriginal)
{
  if ( this != &theOriginal ){
    m_xsectionCollection     = theOriginal.m_xsectionCollection;
    m_differentialCollection = theOriginal.m_differentialCollection;
    m_validCounter           = theOriginal.m_validCounter;
    m_invalidCounter         = theOriginal.m_invalidCounter;
  }
}
k4GeneratorsConfig::xsectionCollection& k4GeneratorsConfig::xsectionCollection::operator=(const xsectionCollection& theOriginal)
{
  if ( this != &theOriginal ){
    m_xsectionCollection     = theOriginal.m_xsectionCollection;
    m_differentialCollection = theOriginal.m_differentialCollection;
    m_validCounter           = theOriginal.m_validCounter;
    m_invalidCounter         = theOriginal.m_invalidCounter;
  }

  return *this;
}
k4GeneratorsConfig::xsectionCollection::~xsectionCollection(){
}
void k4GeneratorsConfig::xsectionCollection::Execute(){

  // first make the collection
  makeCollections();

  // second order the collection according to the process
  orderCollections();

  // third print the final results
  Print();
}
void k4GeneratorsConfig::xsectionCollection::makeCollections(){

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
	  // take care of the total cross section extracted from the EDM4HEP file
	  if ( filenamePath.extension() == ".edm4hep" ){
	    std::cout << "xsectionCollection:: processing " << processPath.filename().string() << std::endl;
	    k4GeneratorsConfig::xsection *xsec = new k4GeneratorsConfig::xsection();
	    xsec->setProcess(processPath.filename().string());
	    xsec->setFile(filenamePath.string());
	    // in some cases the generator name is not available, then derive from the filename
	    if ( xsec->Generator().empty() )
	      xsec->setGenerator(generatorsPath.filename().string());
	    std::cout << "Generator " << xsec->Generator() << " has been processed" << std::endl;
	    m_xsectionCollection.push_back(*xsec);
	    if ( xsec->isValid()  ) m_validCounter++;
	    if ( !xsec->isValid() ) m_invalidCounter++;
	    delete xsec;
	  }
	  // take care of the differential distributions extracted from the .root (analysis output) file
	  if ( filenamePath.extension() == ".root" ){
	    std::cout << "xsectionCollection:: processing " << processPath.filename().string() << std::endl;
	    k4GeneratorsConfig::differential *diffDist = new k4GeneratorsConfig::differential();
	    diffDist->setProcess(processPath.filename().string());
	    diffDist->setFile(filenamePath.string());
	    // in some cases the generator name is not available, then derive from the filename
	    if ( diffDist->Generator().empty() )
	      diffDist->setGenerator(generatorsPath.filename().string());
	    std::cout << "Generator " << diffDist->Generator() << " has been processed for differential distributions" << std::endl;
	    m_differentialCollection.push_back(*diffDist);
	    delete diffDist;
	  }
	}
      }
    }
  }

}
void k4GeneratorsConfig::xsectionCollection::orderCollections(){

  // order by content
  std::sort(m_xsectionCollection.begin(),m_xsectionCollection.end(),[this](xsection A, xsection B){ return this->compareLexical(A,B);});

  // order by content
  std::sort(m_differentialCollection.begin(),m_differentialCollection.end(),[this](differential A, differential B){ return this->compareLexical(A,B);});
}
bool k4GeneratorsConfig::xsectionCollection::compareLength(xsection A, xsection B){

  // retrieve the process as ordering variable
  std::string processA = A.Process();
  std::string processB = B.Process();
  
  return processA.size() < processB.size();
}
bool k4GeneratorsConfig::xsectionCollection::compareLexical(xsection A, xsection B){

  // retrieve the process as ordering variable
  std::string processNgenA = A.Process() + A.Generator();
  std::string processNgenB = B.Process() + B.Generator();

  std::vector<std::string> listOf2;
  listOf2.push_back(processNgenA);
  listOf2.push_back(processNgenB);
  sort(listOf2.begin(),listOf2.end());

  // if the order is changed return true otherwise false
  if ( processNgenA.compare(listOf2[0]) == 0 ) return true;
  
  return false;
}
bool k4GeneratorsConfig::xsectionCollection::compareLexical(differential A, differential B){

  // retrieve the process as ordering variable
  std::string processNgenA = A.Process() + A.Generator();
  std::string processNgenB = B.Process() + B.Generator();

  std::vector<std::string> listOf2;
  listOf2.push_back(processNgenA);
  listOf2.push_back(processNgenB);
  sort(listOf2.begin(),listOf2.end());

  // if the order is changed return true otherwise false
  if ( processNgenA.compare(listOf2[0]) == 0 ) return true;
  
  return false;
}
unsigned int k4GeneratorsConfig::xsectionCollection::NbOfSuccesses(){
  return m_validCounter;
}
unsigned int k4GeneratorsConfig::xsectionCollection::NbOfFailures(){
  return m_invalidCounter;
}
void k4GeneratorsConfig::xsectionCollection::Write2Root(std::string filename){

  xsection2Root out(filename); 
  
  for (auto xsec: m_xsectionCollection){
    if ( xsec.isValid() ){
      out.Execute(xsec);
    }
  }
  // diffhists uses the matrix calculated before for the xsectionCollection
  for (auto diffHists: m_differentialCollection){
    if ( diffHists.isValid() ){
      out.Execute(diffHists);
    }
  }
  out.Finalize();
  
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
    std::string proc     = xsec.Process();
    std::string filename = xsec.File();
    if ( proc.compare(previousProcess) != 0 ){
      if ( previousProcess.compare("XXXX")!= 0 ) output << std::endl;
      output << proc << " sqrts= " << xsec.SQRTS();
      if ( filename.find("ISR") != std::string::npos ) {
	output << " with ISR ";
	if ( filename.find("BST") != std::string::npos ) {
	  output << " with Beamstrahlung ";
	}
      } 
      output << ":" << std::endl;
      previousProcess = proc;
    }
    // print the generator name and cross section with its error
    output << std::setw(20) << std::left << xsec.Generator() << " " 
	   << std::setw(8 ) << std::left << xsec.Xsection() << " +- " 
	   << std::setw(8)  << std::left << xsec.XsectionError() << " pb" << std::endl;
  }
  output << std::endl;
  // last thing the invalids
  output << "Number of runs           : " << m_invalidCounter+m_validCounter << std::endl;
  output << "Number of failed runs    : " << m_invalidCounter << std::endl;
  output << "Number of successful runs: " << m_validCounter << std::endl;

}
