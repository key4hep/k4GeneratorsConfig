// File to read EDM4HEP output and extract the cross sections
#include <iostream>
#include <fstream>

#include "TFile.h"
#include "TH1D.h"

#include "podio/ROOTReader.h"
#include "podio/Frame.h"
#include "edm4hep/Constants.h"
#include "edm4hep/GeneratorEventParametersCollection.h"
#include "edm4hep/GeneratorToolInfo.h"
#include "edm4hep/MCParticleCollection.h"

//
int main(int argc, char** argv)
{

  std::string inFileName="events.edm4hep";
  std::string outFileName="histograms.root";
  int pdgIDa = 11;
  int pdgIDb = -11;
  int c;
  while ((c = getopt (argc, argv, "ha:b:i:o:")) != -1)
    switch (c){
    case 'o':
      outFileName = optarg;
      break;
    case 'i':
      inFileName = optarg;
      break;
    case 'a':
      pdgIDa = atoi(optarg);
      break;
    case 'b':
      pdgIDb = atoi(optarg);
      break;
    case 'h':
      std::cout << "Usage: analyze-h -i filename -o filename -a pdgID -b pdgIDb" << std::endl;
      std::cout << "-h: print this help" << std::endl;
      std::cout << "-i filename: input filename" << std::endl;
      std::cout << "-o filename: output filename" << std::endl;
      std::cout << "-a pdgIDa: pdg id of the first particle to be analyzed" << std::endl;
      std::cout << "-a pdgIDa: pdg id of the second particle to be analyzed" << std::endl;
      exit(0);
    default:
      exit(0);
    }

  std::cout << "Anlyze2f:" << std::endl
	    << "Input  file         " << inFileName << std::endl
	    << "Output file        : " << outFileName << std::endl
	    << "pdg first  particle: " << pdgIDa << std::endl
	    << "pdg second particle: " << pdgIDb << std::endl;
  //
    // open the edm4hep file
  podio::ROOTReader *reader;
  reader = new podio::ROOTReader();
  reader->openFile(inFileName);

  // retrieve the RunInfo for the weight names, there should only be 1 entry per Run
  if ( reader->getEntries(podio::Category::Run) == 0 ){
    exit(0);
  }
  // decode the tool infor from Run
  auto runinfo = podio::Frame(reader->readNextEntry(podio::Category::Run));
  auto toolInfos = edm4hep::utils::getGenToolInfos(runinfo);
  if ( toolInfos.size() > 0 ){
    std::cout << "analyze2f the tool " << toolInfos[0].name << std::endl;
  }
  else {
    std::cout << "k4GeneratorsConfig::Error: ToolInfos not available" << std::endl;
  }

  // retrieve the cross section for the last event if not possible it's not valid
  if ( reader->getEntries(podio::Category::Event) == 0 ){
    exit(0);
  }

  // prepare some histograms
  TH1D* pdgAcostheta = new TH1D("pdgacostheta","Particle A cos(theta)",1000, -1.,1.);
  TH1D* pdgBcostheta = new TH1D("pdgbcostheta","Particle B cos(theta)",1000, -1.,1.);

  //  loop over the events
  for (size_t i = 0; i < reader->getEntries(podio::Category::Event); ++i) {
    auto event = podio::Frame(reader->readNextEntry(podio::Category::Event));
    auto& mcParticles = event.get<edm4hep::MCParticleCollection>(edm4hep::labels::MCParticles);
    // do more stuff with this event
    for (auto part: mcParticles){
      if ( part.getPDG() == pdgIDa ){
	auto momentum = part.getMomentum();
	double mag = momentum.x*momentum.x
	  + momentum.y*momentum.y
	  + momentum.z*momentum.z;
	if ( mag > 0. )
	  mag = sqrt(mag);
	else
	  mag = 0.;
	double costheta = -9999;
	if ( mag > 0. )
	  costheta = momentum.z/mag;
	pdgAcostheta->Fill(costheta);
      }
      if ( part.getPDG() == pdgIDb ){
	auto momentum = part.getMomentum();
	double mag = momentum.x*momentum.x
	  + momentum.y*momentum.y
	  + momentum.z*momentum.z;
	if ( mag > 0. )
	  mag = sqrt(mag);
	else
	  mag = 0.;
	double costheta = -9999;
	if ( mag > 0. )
	  costheta = momentum.z/mag;
	pdgBcostheta->Fill(costheta);
      }
    }
  }

  // now analyze the event
  
  // instantiate the collection as pointer
  std::unique_ptr<TFile> outputFilePtr(TFile::Open(outFileName.c_str(),"RECREATE"));
  outputFilePtr->cd();
  pdgAcostheta->Write();
  pdgBcostheta->Write();
  outputFilePtr->Write();
  outputFilePtr->Close();
}
