// File to read EDM4HEP output and extract the cross sections
#include <fstream>
#include <iostream>
#include <unistd.h>

#include "TFile.h"
#include "TH1D.h"

#include "edm4hep/Constants.h"
#include "edm4hep/GeneratorEventParametersCollection.h"
#include "edm4hep/GeneratorToolInfo.h"
#include "edm4hep/MCParticleCollection.h"
#include "podio/Frame.h"
#include "podio/ROOTReader.h"

#include "edm4hep/utils/kinematics.h"

std::string translatePDG2Name(int);

//
int main(int argc, char** argv) {

  std::string inFileName = "events.edm4hep";
  std::string outFileName = "histograms.root";
  std::string particles = "11,-11";
  int c;
  while ((c = getopt(argc, argv, "hp:i:o:")) != -1)
    switch (c) {
    case 'o':
      outFileName = optarg;
      break;
    case 'i':
      inFileName = optarg;
      break;
    case 'p':
      particles = optarg;
      break;
    case 'h':
      std::cout << "Usage: key4HEPAnlysis -h -i filename -o filename -p pdgID1,pdgID2,...." << std::endl;
      std::cout << "-h: print this help" << std::endl;
      std::cout << "-i filename: input filename" << std::endl;
      std::cout << "-o filename: output filename" << std::endl;
      std::cout << "-p pdgID1,pddID2,....: comma separated list of the pdg ids in the finalstate to be analyzed"
                << std::endl;
      exit(0);
    default:
      exit(0);
    }

  // decode and store in the vector
  std::vector<int> particlesList;
  std::vector<std::string> particlesNamesList;
  std::stringstream ss(particles);
  int pdg;
  while (ss >> pdg) {
    particlesList.push_back(pdg);
    particlesNamesList.push_back(translatePDG2Name(pdg));
    ss.ignore(1);
  }

  std::cout << "key4HEPAnalysis:" << std::endl
            << "Input  file         " << inFileName << std::endl
            << "Output file        : " << outFileName << std::endl;
  for (unsigned int i = 0; i < particlesList.size(); i++) {
    std::cout << "pdg particle " << i << " : " << particlesList[i] << std::endl;
  }

  // open the edm4hep file
  podio::ROOTReader* reader;
  reader = new podio::ROOTReader();
  reader->openFile(inFileName);

  // retrieve the RunInfo for the weight names, there should only be 1 entry per Run
  if (reader->getEntries(podio::Category::Run) == 0) {
    exit(0);
  }

  // decode the tool infor from Run
  auto runinfo = podio::Frame(reader->readNextEntry(podio::Category::Run));
  auto toolInfos = edm4hep::utils::getGenToolInfos(runinfo);
  if (toolInfos.size() > 0) {
    std::cout << "analyze2f the tool " << toolInfos[0].name << std::endl;
  } else {
    std::cout << "k4GeneratorsConfig::Warning: ToolInfos not available" << std::endl;
  }
  
  // retrieve the cross section for the last event if not possible it's not valid
  if (reader->getEntries(podio::Category::Event) == 0) {
    exit(0);
  }
  
  // get the frame parameters
  auto event = podio::Frame(reader->readNextEntry(podio::Category::Event));
  const edm4hep::GeneratorEventParametersCollection& genParametersCollection =
      event.get<edm4hep::GeneratorEventParametersCollection>(edm4hep::labels::GeneratorEventParameters);
  if (genParametersCollection.size() == 0)
    exit(0);
  edm4hep::GeneratorEventParameters genParameters = genParametersCollection[0];

  // decode sqrts
  double sqrts = genParameters.getSqrts();
  
  // histogram reservations
  // prepare some histograms
  std::stringstream name, desc;
  std::vector<TH1D *> costhetaHistos;
  std::vector<TH1D *> massHistos;
  std::vector<TH1D *> pTHistos;
  std::vector<TH1D *> pZHistos;

  unsigned int i=0;
  for (auto part:particlesList){
    name.clear(); name.str(""); desc.clear(); desc.str("");
    name << "pdgcostheta" << particlesNamesList[i];
    desc << "Particle PDGID = " << part << " cos(theta)";
    costhetaHistos.push_back(new TH1D(name.str().c_str(),desc.str().c_str(),100, -1.,1.));
    i++;
  }

  for (unsigned int part1=0; part1 < particlesList.size(); part1++){
    for (unsigned int part2=part1+1; part2 < particlesList.size(); part2++){

      name.clear(); name.str(""); desc.clear(); desc.str("");
      name << "mass" << particlesNamesList[part1] << particlesNamesList[part2];
      desc << "Invariant Mass(" << particlesList[part1] << "," << particlesList[part2] << ")";
      massHistos.push_back(new TH1D(name.str().c_str(),desc.str().c_str(),1000, 0., sqrts));
      
      name.clear(); name.str(""); desc.clear(); desc.str("");
      name << "pt" << particlesNamesList[part1] << particlesNamesList[part2];
      desc << "pT(" << particlesList[part1] << "," << particlesList[part2] << ")";
      pTHistos.push_back(new TH1D(name.str().c_str(),desc.str().c_str(),1000, 0., sqrts));

      name.clear(); name.str(""); desc.clear(); desc.str("");
      name << "pz" << particlesNamesList[part1] << particlesNamesList[part2];
      desc << "pZ(" << particlesList[part1] << "," << particlesList[part2] << ")";
      pZHistos.push_back(new TH1D(name.str().c_str(),desc.str().c_str(),1000, 0., sqrts));
    }
  }

  //  loop over the events
  std::vector<edm4hep::LorentzVectorM *> selectedParticles;
  selectedParticles.resize(particlesList.size());
  for (size_t iEntry = 0; iEntry < reader->getEntries(podio::Category::Event); ++iEntry) {
    if (iEntry)
      event = podio::Frame(reader->readNextEntry(podio::Category::Event));
    
    // loop over the particles of the event:
    auto& mcParticles = event.get<edm4hep::MCParticleCollection>(edm4hep::labels::MCParticles);
    for (unsigned int ipart=0; ipart<particlesList.size(); ipart++){
      for (auto part: mcParticles){
	if ( part.getPDG() == particlesList[ipart]){
	  if ( part.getGeneratorStatus() > 0 && !selectedParticles[ipart]){
	    auto momentumA = part.getMomentum();
	    selectedParticles[ipart] = new edm4hep::LorentzVectorM(momentumA.x, momentumA.y, momentumA.z, part.getMass());
	  }
	}
      }
    }
    // fill the histograms:
    for (unsigned int ipart=0; ipart<particlesList.size(); ipart++){
      if (selectedParticles[ipart]){
	double costheta = cos(selectedParticles[ipart]->Theta());
	costhetaHistos[ipart]->Fill(costheta);
      }
    }

    unsigned counter = 0;
    for (unsigned int ipart1=0; ipart1<particlesList.size(); ipart1++){
      for (unsigned int ipart2=ipart1+1; ipart2<particlesList.size(); ipart2++){
	if (selectedParticles[ipart1] && selectedParticles[ipart2] ){
	  edm4hep::LorentzVectorM combParticle = *selectedParticles[ipart1] + *selectedParticles[ipart2];
	  massHistos[counter]->Fill(combParticle.mass());
	  pTHistos[counter]->Fill(combParticle.pt());
	  pZHistos[counter]->Fill(combParticle.pz());
	}
	counter++;
      }
    }

    // release memory after an event
    for (unsigned int ipart=0; ipart<selectedParticles.size(); ipart++){
      if ( selectedParticles[ipart] ) {
	delete selectedParticles[ipart];
	selectedParticles[ipart]=nullptr;
      }
    }
  }
  // instantiate the collection as pointer
  std::unique_ptr<TFile> outputFilePtr(TFile::Open(outFileName.c_str(), "RECREATE"));
  outputFilePtr->cd();

  for (auto histo:costhetaHistos){
    histo->Write();
  }
  for (auto histo:massHistos){
    histo->Write();
  }
  for (auto histo:pTHistos){
    histo->Write();
  }
  for (auto histo:pZHistos){
    histo->Write();
  }

  outputFilePtr->Write();
  outputFilePtr->Close();
}
std::string translatePDG2Name(int pdg){

  if (pdg == 1)
    return "d";
  else if (pdg == -1)
    return "dbar";
  else if (pdg == 2)
    return "u";
  else if (pdg == -2)
    return "ubar";
  else if (pdg == 3)
    return "s";
  else if (pdg == -3)
    return "sbar";
  else if (pdg == 4)
    return "c";
  else if (pdg == -4)
    return "cbar";
  else if (pdg == 5)
    return "b";
  else if (pdg == -5)
    return "bbar";
  else if (pdg == 6)
    return "t";
  else if (pdg == -6)
    return "tbar";
  else if (pdg == 11)
    return "electron";
  else if (pdg == -11)
    return "positron";
  else if (pdg == 12)
    return "neutrinoe";
  else if (pdg == -12)
    return "antineutrinoe";
  else if (pdg == 13)
    return "muon";
  else if (pdg == -13)
    return "antimuon";
  else if (pdg == 14)
    return "neutrinomuon";
  else if (pdg == -14)
    return "antineutrinomuon";
  else if (pdg == 15)
    return "tau";
  else if (pdg == -15)
    return "antitau";
  else if (pdg == 16)
    return "neutrinotau";
  else if (pdg == -16)
    return "antineutrinotau";
  else if (pdg == 21)
    return "gluon";
  else if (pdg == 22)
    return "photon";
  else if (pdg == 23)
    return "Z";
  else if (pdg == 24)
    return "wplus";
  else if (pdg == -24)
    return "wminus";
  else if (pdg == 25)
    return "higgs";

  // if it's not that:
  return "unknown";
}
