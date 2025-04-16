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
  std::stringstream ss(particles);
  int pdg;
  while (ss >> pdg) {
    particlesList.push_back(pdg);
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
  ss.clear();
  ss.str("");
  ss << "Particle PDGID = " << particlesList[0] << " cos(theta)";
  TH1D* pdgAcostheta = new TH1D("pdgacostheta", ss.str().c_str(), 200, -1., 1.);
  ss.clear();
  ss.str("");
  ss << "Particle PDGID = " << particlesList[1] << " cos(theta)";
  TH1D* pdgBcostheta = new TH1D("pdgbcostheta", ss.str().c_str(), 200, -1., 1.);

  ss.clear();
  ss.str("");
  ss << "Invariant Mass(" << particlesList[0] << "," << particlesList[1] << ")";
  TH1D* mpdgapdgb = new TH1D("mpdgapdgb", ss.str().c_str(), 1000, 0., sqrts);

  ss.clear();
  ss.str("");
  ss << "PT(" << particlesList[0] << "," << particlesList[1] << ")";
  TH1D* ptpdgapdgb = new TH1D("ptpdgapdgb", ss.str().c_str(), 1000, 0., sqrts);

  ss.clear();
  ss.str("");
  ss << "PZ(" << particlesList[0] << "," << particlesList[1] << ")";
  TH1D* pzpdgapdgb = new TH1D("pzpdgapdgb", ss.str().c_str(), 1000, 0., sqrts);

  //  loop over the events
  for (size_t i = 0; i < reader->getEntries(podio::Category::Event); ++i) {
    if (i)
      event = podio::Frame(reader->readNextEntry(podio::Category::Event));
    auto& mcParticles = event.get<edm4hep::MCParticleCollection>(edm4hep::labels::MCParticles);
    // do more stuff with this event
    edm4hep::LorentzVectorM* particleA;
    edm4hep::LorentzVectorM* particleB;
    for (auto part : mcParticles) {
      if (part.getPDG() == particlesList[0] && !particleA) {
        auto momentumA = part.getMomentum();
        particleA = new edm4hep::LorentzVectorM(momentumA.x, momentumA.y, momentumA.z, part.getMass());
        double costheta = cos(particleA->Theta());
        pdgAcostheta->Fill(costheta);
      }
      if (part.getPDG() == particlesList[1] && !particleB) {
        auto momentumB = part.getMomentum();
        particleB = new edm4hep::LorentzVectorM(momentumB.x, momentumB.y, momentumB.z, part.getMass());
        double costheta = cos(particleB->Theta());
        pdgBcostheta->Fill(costheta);
      }
      if (particleA && particleB) {
        edm4hep::LorentzVectorM part = *particleA + *particleB;
        mpdgapdgb->Fill(part.mass());
        ptpdgapdgb->Fill(part.pt());
        pzpdgapdgb->Fill(part.pz());
      }
    }
    // release memory after an event
    if (particleA) {
      delete particleA;
      particleA = 0;
    }
    if (particleB) {
      delete particleB;
      particleB = 0;
    }
  }

  // now analyze the event

  // instantiate the collection as pointer
  std::unique_ptr<TFile> outputFilePtr(TFile::Open(outFileName.c_str(), "RECREATE"));
  outputFilePtr->cd();

  pdgAcostheta->Write();
  pdgBcostheta->Write();
  mpdgapdgb->Write();
  ptpdgapdgb->Write();
  pzpdgapdgb->Write();

  outputFilePtr->Write();
  outputFilePtr->Close();
}
