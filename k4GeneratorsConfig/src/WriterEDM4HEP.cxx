// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014-2023 The HepMC collaboration (see AUTHORS for details)
//
///
/// @file WriterEDM4HEP.cc
/// @brief Implementation of \b class WriterEDM4HEP
///
#include <cstring>


#include "HepMC3/GenEvent.h"
#include "HepMC3/GenParticle.h"
#include "HepMC3/GenVertex.h"
#include "HepMC3/Units.h"
#include "HepMC3/Version.h"

#include "WriterEDM4HEP.h"

#include "edm4hep/Constants.h"
#include "edm4hep/GeneratorToolInfo.h"
#include "edm4hep/GeneratorEventParametersCollection.h"
#include "edm4hep/GeneratorPdfInfoCollection.h"

#include "edm4hep/MCParticleCollection.h"
#include "edm4hep/EventHeaderCollection.h"

#include "HepPDT/ParticleID.hh"
#include "HepMC3/Attribute.h"

#include "podio/Frame.h"

namespace HepMC3
{


WriterEDM4HEP::WriterEDM4HEP(const std::string &filename, std::shared_ptr<GenRunInfo> run)
    : m_file(filename),
      m_stream(&m_file),
      m_particle_counter(0),
      m_edm4hepWriterClosed(false),
      m_edm4hepWriter(filename)
{
    HEPMC3_WARNING("WriterEDM4HEP::WriterEDM4HEP: the conversion to EDM4HEP is still being developed")
    set_run_info(run);
    if ( !run_info() ) set_run_info(std::make_shared<GenRunInfo>());
    if ( !m_file.is_open() )
    {
        HEPMC3_ERROR("WriterEDM4HEP: could not open output file: " << filename )
    }
}

WriterEDM4HEP::WriterEDM4HEP(std::ostream &stream, std::shared_ptr<GenRunInfo> run)
    : m_stream(&stream),
      m_particle_counter(0),
      m_edm4hepWriterClosed(false),
      m_edm4hepWriter("")
{
    HEPMC3_WARNING("WriterEDM4HEP::WriterEDM4HEP: HepMC2 IO_GenEvent format is outdated. Please use HepMC3 Asciiv3 format instead.")
    set_run_info(run);
    if ( !run_info() ) set_run_info(std::make_shared<GenRunInfo>());
    const std::string header = "HepMC::Version " + version() + "\nHepMC::IO_GenEvent-START_EVENT_LISTING\n";
    m_stream->write(header.data(), header.length());
}

WriterEDM4HEP::WriterEDM4HEP(std::shared_ptr<std::ostream> s_stream, std::shared_ptr<GenRunInfo> run)
    : m_shared_stream(s_stream),
      m_stream(s_stream.get()),
      m_particle_counter(0),
      m_edm4hepWriterClosed(false),
      m_edm4hepWriter("")
{
    HEPMC3_WARNING("WriterEDM4HEP::WriterEDM4HEP: HepMC2 IO_GenEvent format is outdated. Please use HepMC3 Asciiv3 format instead.")
    set_run_info(run);
    if ( !run_info() ) set_run_info(std::make_shared<GenRunInfo>());
    const std::string header = "HepMC::Version " + version() + "\nHepMC::IO_GenEvent-START_EVENT_LISTING\n";
    m_stream->write(header.data(), header.length());
}


WriterEDM4HEP::~WriterEDM4HEP()
{
  if ( !m_edm4hepWriterClosed )
    close();
}


void WriterEDM4HEP::write_event(const GenEvent &evt) 
{

  // make sure run_info is up to date
  if ( !run_info() ) {
    set_run_info(evt.run_info());
    write_run_info();
  }
  if ( evt.run_info() && run_info() != evt.run_info() ) {
    set_run_info(evt.run_info());
    write_run_info();
  }
  // now deal with the event
  auto eventFrame = podio::Frame();

  // here is the collection
  edm4hep::MCParticleCollection particleCollection;

  std::map<unsigned int, edm4hep::MutableMCParticle> mapIDPart;
  for (auto hepmcParticle:evt.particles()) {
    //    std::cout << "Converting hepmc particle with Pdg_ID " << hepmcParticle->pdg_id() << "and id " <<  hepmcParticle->id() << std::endl;
    if (mapIDPart.find(hepmcParticle->id()) == mapIDPart.end()) {
      edm4hep::MutableMCParticle edm_particle = transformParticle(hepmcParticle);
      mapIDPart.insert({hepmcParticle->id(), edm_particle});
    }
    // mother/daughter links
    auto prodvertex = hepmcParticle->production_vertex();
    if (nullptr != prodvertex) {
      for (auto particle_mother: prodvertex->particles_in()) {
        if (mapIDPart.find(particle_mother->id()) == mapIDPart.end()) {
          edm4hep::MutableMCParticle edm_particle = transformParticle(particle_mother);
          mapIDPart.insert({particle_mother->id(), edm_particle});
        }
        mapIDPart[hepmcParticle->id()].addToParents(mapIDPart[particle_mother->id()]);
      }
    }
    auto endvertex = hepmcParticle->end_vertex();
    if (nullptr != endvertex) {
      for (auto particle_daughter: endvertex->particles_out()) {
        if (mapIDPart.find(particle_daughter->id()) == mapIDPart.end()) {
          auto edm_particle = transformParticle(particle_daughter);
          mapIDPart.insert({particle_daughter->id(), edm_particle});
        }
        mapIDPart[hepmcParticle->id()].addToDaughters(mapIDPart[particle_daughter->id()]);
      }
    }
  }

  for (auto particle_pair: mapIDPart){
    particleCollection.push_back(particle_pair.second);
  }

  // now we need the event header
  edm4hep::EventHeaderCollection evtHeaderCollection;
  edm4hep::MutableEventHeader evtHeader;

  // add eventNumber
  evtHeader.setEventNumber(evt.event_number());

  // add the weights
  for (auto weight: evt.weights()){
    evtHeader.addToWeights(weight);
  }  

  // push to collection
  evtHeaderCollection.push_back(evtHeader);

  // write the EventHeader collection to the frame
  eventFrame.put(std::move(evtHeaderCollection), edm4hep::labels::EventHeader);

  // first the GeneratorEventParameters
  edm4hep::GeneratorEventParametersCollection generatorParametersCollection;
  edm4hep::MutableGeneratorEventParameters generatorParameters;

  // add the cross sections and its errors as parameter vector to the Frame
  if ( evt.cross_section() ) {
    for (auto xsec: evt.cross_section()->xsecs()){
      generatorParameters.addToCrossSections(xsec);
    }
    for (auto xsecErr: evt.cross_section()->xsec_errs()){
      generatorParameters.addToCrossSectionErrors(xsecErr);
    }
  }

  // add the event_scale
  std::string name = "event_scale";
  generatorParameters.setEventScale(retrieveDoubleAttribute(evt,name));

  // add SQRTS
  double sqrts = 0.; 
  if ( evt.beams().size()==2 ) {
    ConstGenParticlePtr beam1 = evt.beams()[0];
    ConstGenParticlePtr beam2 = evt.beams()[1];
    sqrts = (beam1->momentum()+beam2->momentum()).m();
  }
  // special treatement for MADGRAPH: overwrite beams to get the SQRTS correctly
  if ( run_info()->tools().size() > 0 ) {
    if ( run_info()->tools()[0].name.find("MadGraph") != std::string::npos){
      sqrts = retrieveDoubleAttribute(evt,"EBMUP1") + retrieveDoubleAttribute(evt,"EBMUP2");
    }
  }
  // now we write to the structure:
  generatorParameters.setSqrts(sqrts);

  //signal process ID
  name = "signal_process_id";
  generatorParameters.setSignalProcessId(retrieveIntAttribute(evt,name));

  //signal vertex ID
  name = "signal_vertex_id";
  bool convertOK = writeSignalVertex(evt,retrieveIntAttribute(evt,name),mapIDPart,generatorParameters);
  // inconsistent use of attributes, fallback for SHERPA
  if ( !convertOK ){
    name = "signal_process_vertex";
    writeSignalVertex(evt,retrieveIntAttribute(evt,name),mapIDPart,generatorParameters);
  }

  // add the alphaQED
  name = "alphaQED";
  generatorParameters.setAlphaQED(retrieveDoubleAttribute(evt,name));

  // add alphaQCD
  name = "alphaQCD";
  generatorParameters.setAlphaQCD(retrieveDoubleAttribute(evt,name));

  // add the object to the collection:
  generatorParametersCollection.push_back(generatorParameters);
  // write the GeneratorEventParameters collection to the frame 
  eventFrame.put(std::move(generatorParametersCollection), edm4hep::labels::GeneratorEventParameters);

  // now the PDFs:
  edm4hep::GeneratorPdfInfoCollection pdfCollection;
  edm4hep::MutableGeneratorPdfInfo pdfEDM4HEP;
  //
  // retrieve the pdf information
  HepMC3::ConstGenPdfInfoPtr pdfinfo = evt.pdf_info();
  if ( pdfinfo ){
    // store for transfer
    pdfEDM4HEP.setPartonId({pdfinfo->parton_id[0],pdfinfo->parton_id[1]});
    pdfEDM4HEP.setX({pdfinfo->x[0],pdfinfo->x[1]});
    pdfEDM4HEP.setXf({pdfinfo->xf[0],pdfinfo->xf[1]});
    pdfEDM4HEP.setLhapdfId({pdfinfo->pdf_id[0],pdfinfo->pdf_id[1]});
    pdfEDM4HEP.setScale(pdfinfo->scale);
  }
  //
  pdfCollection.push_back(pdfEDM4HEP);
  eventFrame.put(std::move(pdfCollection), edm4hep::labels::GeneratorPdfInfo);

  // LAST ITEM: write the collection of MCParticles to the frame mv empties the collection which we need for processing!!
  eventFrame.put(std::move(particleCollection), edm4hep::labels::MCParticles);

  // write the frame to the Writer:
  m_edm4hepWriter.writeFrame(eventFrame, podio::Category::Event);

}
bool WriterEDM4HEP::writeSignalVertex(const GenEvent& evt, int hepmcVertexID, std::map<unsigned int, edm4hep::MutableMCParticle> &mapHEPMC2EDM4HEP, edm4hep::MutableGeneratorEventParameters& generatorParameters){

  bool convertOK = false;
  // retrieve the vertices
  for (auto vtx: evt.vertices() ){
    // identify the signalvertex via its hepmcID
    if ( vtx->id() == hepmcVertexID ) {
      convertOK = true;
      // now insert all incoming particles to the generatorParameters
      for ( auto part : vtx->particles_in() ){
	unsigned int hepmcParticleID = part->id();
	if ( mapHEPMC2EDM4HEP.find(hepmcParticleID) != mapHEPMC2EDM4HEP.end() ) {
	  generatorParameters.addToSignalVertex(mapHEPMC2EDM4HEP[hepmcParticleID]);
	}
      }
    }
  }

  return convertOK;
}

double WriterEDM4HEP::retrieveDoubleAttribute(const GenEvent &evt, std::string name) {

  shared_ptr<HepMC3::DoubleAttribute> hepmcPtr = evt.attribute<HepMC3::DoubleAttribute>(name);
  double result = hepmcPtr?(hepmcPtr->value()):0.0;

  return result;
}

double WriterEDM4HEP::retrieveIntAttribute(const GenEvent &evt, std::string name) {

  shared_ptr<HepMC3::IntAttribute> hepmcPtr = evt.attribute<HepMC3::IntAttribute>(name);
  int result = hepmcPtr?(hepmcPtr->value()):0.0;

  return result;
}

void WriterEDM4HEP::write_run_info() {

  // create the frame
  auto runFrame = podio::Frame();

  // start with the generator information 
  const std::vector<GenRunInfo::ToolInfo> listOfTools = run_info()->tools();
  if ( listOfTools.size() == 0 ) {
    std::cout << "WARNING: no tools found, hepmc run_info incomplete" << std::endl;
  }

  // the EDM4HEP structure
  std::vector<edm4hep::GeneratorToolInfo> toolInfosVectEDM4HEP;
  for ( auto hepmcTool:listOfTools){
    edm4hep::GeneratorToolInfo edm4hepTool;
    edm4hepTool.name    = hepmcTool.name;
    edm4hepTool.version = hepmcTool.version;
    edm4hepTool.description = hepmcTool.description;
    toolInfosVectEDM4HEP.push_back(edm4hepTool);
  }
  edm4hep::utils::putGenToolInfos(runFrame, toolInfosVectEDM4HEP);
  
  // weight names
  std::vector<std::string> weights = run_info()->weight_names();

  // add the weights as parameters to the frame
  runFrame.putParameter(edm4hep::labels::GeneratorWeightNames, weights);

  // write the frame to the Writer:
  m_edm4hepWriter.writeFrame(runFrame, podio::Category::Run);

}

edm4hep::MutableMCParticle WriterEDM4HEP::transformParticle(const ConstGenParticlePtr& hepmcParticle)
{
  edm4hep::MutableMCParticle edm_particle;
  edm_particle.setPDG(hepmcParticle->pdg_id());
  edm_particle.setGeneratorStatus(hepmcParticle->status());
  // look up charge from pdg_id
  HepPDT::ParticleID particleID(hepmcParticle->pdg_id());
  edm_particle.setCharge(particleID.charge());

  // convert momentum
  auto p = hepmcParticle->momentum();
  edm_particle.setMomentum(edm4hep::Vector3d(p.px(), p.py(), p.pz()));

  // set the mass (energy is deduced in EDM4HEP
  edm_particle.setMass(p.m());

  // add spin (particle helicity) information if available
  //  std::shared_ptr<HepMC3::VectorFloatAttribute> spin = hepmcParticle->attribute<HepMC3::VectorFloatAttribute>("spin");
  //if (spin) {
  //   edm4hep::Vector3f hel(spin->value()[0], spin->value()[1], spin->value()[2]);
  //   edm_particle.setSpin(hel);
  //}
  std::shared_ptr<HepMC3::DoubleAttribute> thetaPtr = hepmcParticle->attribute<HepMC3::DoubleAttribute>("theta");
  std::shared_ptr<HepMC3::DoubleAttribute> phiPtr   = hepmcParticle->attribute<HepMC3::DoubleAttribute>("phi");
  if ( thetaPtr && phiPtr ){
    float theta = static_cast<float>(thetaPtr->value());
    float phi   = static_cast<float>(phiPtr->value());
    edm4hep::Vector3f hel(cos(phi)*cos(theta), sin(phi)*cos(theta), sin(theta));
    edm_particle.setSpin(hel);
  }

  // convert production vertex info and time info:
  auto prodVtx = hepmcParticle->production_vertex();
  if ( prodVtx!=nullptr ) {
    auto& pos = prodVtx->position();
    edm_particle.setVertex(edm4hep::Vector3d(pos.x(), pos.y(), pos.z()));
    edm_particle.setTime(pos.t());
  }

  // convert the decay vertex (if present) 
  auto endpointVtx = hepmcParticle->end_vertex();
  if ( endpointVtx!=nullptr ) {
    auto& pos = endpointVtx->position();
    edm_particle.setEndpoint(edm4hep::Vector3d(pos.x(), pos.y(), pos.z()));
  }

  // retrieve the color flow:
  std::shared_ptr<HepMC3::IntAttribute> flow1Ptr = hepmcParticle->attribute<HepMC3::IntAttribute>("flow1");
  std::shared_ptr<HepMC3::IntAttribute> flow2Ptr = hepmcParticle->attribute<HepMC3::IntAttribute>("flow2");
  std::shared_ptr<HepMC3::VectorIntAttribute> colorFlowPtr = hepmcParticle->attribute<HepMC3::VectorIntAttribute>("flows");

  // if one of the pointers is present we should fill the color flow object
  if ( colorFlowPtr || flow1Ptr || flow2Ptr) {
    int flow0 = 0;
    int flow1 = 0;

    // first try whether the new (HepMC3.2 and higher) implmentation was used
    if ( colorFlowPtr ){
      switch ( colorFlowPtr->value().size() ){
      case 1:
	flow0 = colorFlowPtr->value()[0];
	break;
      case 2:
	flow0 = colorFlowPtr->value()[0];
	flow1 = colorFlowPtr->value()[1];
	break;
      default:
	std::cout << "k4GeneratorsConfig::WriterEDM4HEP::WARNING the vector has size " << colorFlowPtr->value().size() 
		  << " greater then 2 as foreseen by EDM4HEP, undefined behaviour, colorflow not written to EDM4HEP" << std::endl;
	break;
      }
    }
    else {
      if ( flow1Ptr ) flow0 = flow1Ptr->value();
      if ( flow2Ptr ) flow1 = flow2Ptr->value();
    }
    //    std::cout << "Writing COLORFLOW " << flow0 << " " << flow1 << std::endl; 
    edm_particle.setColorFlow(edm4hep::Vector2i(flow0, flow1));
  }

  return edm_particle;
}

bool WriterEDM4HEP::failed()
{
  return false;
}
void WriterEDM4HEP::close()
{
  m_edm4hepWriter.finish();
  m_edm4hepWriterClosed = true;
}
}
