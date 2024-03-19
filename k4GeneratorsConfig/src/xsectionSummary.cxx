// File to read EDM4HEP output and extract the cross sections
#include <filesystem>
#include <iostream>
#include <sys/stat.h>
// KEY4HEP specific stuff
#include "podio/ROOTFrameReader.h"
#include "podio/Frame.h"
#include "edm4hep/MCParticleCollection.h"

// function prototypes
std::vector<std::string> getListOfFiles();
double getXsection(std::string);
//
int main(int argc, char** argv)
{
  std::vector<std::string> theList = getListOfFiles();

  // loop over file list
  double xsection = 0.;
  for (unsigned int i=0; i<theList.size();i++){
    xsection = getXsection(theList[i]);
  }

}
std::vector<std::string> getListOfFiles(){

  std::vector<std::string> list;

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
	    std::cout << "Adding " << filenamePath.string() << " to list" << std::endl;
	    list.push_back(filenamePath.string());
	  }
	}
      }
    }
  }
  return list;
}
// open the file and retrieve the cross section
double getXsection(std::string filename){

  // instantiate reader
  auto reader = podio::ROOTFrameReader();
  // open the edm4hep file
  reader.openFile(filename);
  
  // Loop over all events
  double xsection = 0.;
  for (size_t i = 0; i < reader.getEntries("events"); ++i) {
    auto event = podio::Frame(reader.readNextEntry("events"));
    auto& mcParticles = event.get<edm4hep::MCParticleCollection>("MCParticles");
    // retrieve the cross section (once we know how to store it....)
    xsection = 1.;
  }
  std::cout << "Number of Events " << reader.getEntries("events") << std::endl;
  
  std::cout << "cross section for " << filename << " is " << xsection << " pb" << std::endl;
  return xsection;
}
