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
  std::unordered_map<unsigned int, int> mapOID2PODIO;

  std::map<unsigned int, edm4hep::MutableMCParticle> mapIDPart;
  for (auto hepmcParticle:evt.particles()) {
    //    std::cout << "Converting hepmc particle with Pdg_ID " << hepmcParticle->pdg_id() << "and id " <<  hepmcParticle->id() << std::endl;
    if (mapIDPart.find(hepmcParticle->id()) == mapIDPart.end()) {
      edm4hep::MutableMCParticle edm_particle = write_particle(hepmcParticle);
      mapIDPart.insert({hepmcParticle->id(), edm_particle});
    }
    // mother/daughter links
    auto prodvertex = hepmcParticle->production_vertex();
    if (nullptr != prodvertex) {
      for (auto particle_mother: prodvertex->particles_in()) {
        if (mapIDPart.find(particle_mother->id()) == mapIDPart.end()) {
          edm4hep::MutableMCParticle edm_particle = write_particle(particle_mother);
          mapIDPart.insert({particle_mother->id(), edm_particle});
        }
        mapIDPart[hepmcParticle->id()].addToParents(mapIDPart[particle_mother->id()]);
      }
    }
    auto endvertex = hepmcParticle->end_vertex();
    if (nullptr != endvertex) {
      for (auto particle_daughter: endvertex->particles_out()) {
        if (mapIDPart.find(particle_daughter->id()) == mapIDPart.end()) {
          auto edm_particle = write_particle(particle_daughter);
          mapIDPart.insert({particle_daughter->id(), edm_particle});
        }
        mapIDPart[hepmcParticle->id()].addToDaughters(mapIDPart[particle_daughter->id()]);
      }
    }
  }
  // insert the edm4hepParticles into a collection
  // keep a link between HepMC and EDM4HEP for further processing
  for (auto particle_pair: mapIDPart) {
    particleCollection.push_back(particle_pair.second);
    mapOID2PODIO.insert({particle_pair.first,particle_pair.second.getObjectID().index});
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
  eventFrame.put(std::move(evtHeaderCollection), "EventHeaders");

  // add the cross sections as parameter vector to the Frame
  eventFrame.putParameter("CrossSections",evt.cross_section()->xsecs());

  // add the cross section errors as parameter vector to the Frame
  eventFrame.putParameter("CrossSectionErrors",evt.cross_section()->xsec_errs());

  // add the event_scale
  std::string name = "event_scale";
  eventFrame.putParameter(name,retrieveDoubleAttribute(evt,name));

  // add SQRTS
  name = "SQRTS";
  double sqrts = 0.; 
  if ( evt.beams().size()==2 ) {
    ConstGenParticlePtr beam1 = evt.beams()[0];
    ConstGenParticlePtr beam2 = evt.beams()[1];
    sqrts = (beam1->momentum()+beam2->momentum()).m();
  }
  eventFrame.putParameter(name,sqrts);

  // signal process ID
  name = "signal_process_id";
  eventFrame.putParameter(name,retrieveIntAttribute(evt,name));

  // signal vertex ID
  name = "signal_vertex_id";
  int signalVertexID = write_signal_vertex_id(evt,retrieveIntAttribute(evt,name),mapOID2PODIO);
  // inconsistent use of attributes, fallback for SHERPA
  if ( signalVertexID == 0 ){
    name = "signal_process_vertex";
    int signalVertexID = write_signal_vertex_id(evt,retrieveIntAttribute(evt,name),mapOID2PODIO);
  }
  eventFrame.putParameter(name,signalVertexID);

  // now the PDFs: define the variables
  std::vector<int> partonID; 
  std::vector<double> x; 
  std::vector<double> xf; 
  std::vector<int> pdf_id; 
  // retrieve the pdf information
  HepMC3::ConstGenPdfInfoPtr pdfinfo = evt.pdf_info();
  if ( pdfinfo ){
    // store for transfer
    for (unsigned int i=0; i<2; i++){
      partonID.push_back(pdfinfo->parton_id[i]);
      x.push_back(pdfinfo->x[i]);
      xf.push_back(pdfinfo->xf[i]);
      pdf_id.push_back(pdfinfo->pdf_id[i]);
    }
    // now write them to EDM4HEP
    eventFrame.putParameter("PDF_parton_id",partonID);
    eventFrame.putParameter("PDF_x",x);
    eventFrame.putParameter("PDF_scale",pdfinfo->scale);
    eventFrame.putParameter("PDF_xf",xf);
    eventFrame.putParameter("PDF_pdf_id",pdf_id);
  }

  // add the alphaQED
  name = "alphaQED";
  eventFrame.putParameter(name,retrieveDoubleAttribute(evt,name));

  // add alphaQCD
  name = "alphaQCD";
  eventFrame.putParameter(name,retrieveDoubleAttribute(evt,name));

  // LAST ITEM: write the collection of MCParticles to the frame mv empties the collection which we need for processing!!
  eventFrame.put(std::move(particleCollection), "MCParticles");

  // write the frame to the Writer:
  m_edm4hepWriter.writeFrame(eventFrame, podio::Category::Event);

}
  int WriterEDM4HEP::write_signal_vertex_id(const GenEvent& evt, int hepmcVertexID, std::unordered_map<unsigned int, int>&mapHEPMC2PODIO){

  int result = 0;
  int particleOID = 0;
  for (auto vtx: evt.vertices() ){
    if ( vtx->id() == hepmcVertexID && vtx->particles_in_size() > 0 ){
      unsigned int hepmcParticleID = vtx->particles_in()[0]->id();
      if ( mapHEPMC2PODIO.find(hepmcParticleID) != mapHEPMC2PODIO.end() ) {
	return mapHEPMC2PODIO[hepmcParticleID];
      }
    }
  }

  return result;
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
  std::vector<std::string> listOfNames;
  std::vector<std::string> listOfVersions;
  std::vector<std::string> listOfDescriptions;
  for ( auto tool: listOfTools ){
    listOfNames.push_back(tool.name);
    listOfVersions.push_back(tool.version);
    listOfDescriptions.push_back(tool.description);
  }

  // add the three versions to EDM4HEP but only if there is at least one name
  if ( listOfNames.size() > 0 ){
    runFrame.putParameter("name",listOfNames);
    runFrame.putParameter("version",listOfVersions);
    runFrame.putParameter("description",listOfDescriptions);
  }

  // weight names
  std::vector<std::string> weights = run_info()->weight_names();
  std::cout << "WriterEDM4HEP found " << weights.size() << " weight names for conversion" << std::endl;
  for ( unsigned int i=0; i< weights.size() ; i++){
    std::cout << "Weight index " << i << " name " << weights[i] << std::endl;
  }

  if ( weights.size() == 0 ){
    std::cout << "No weight names found, writing a single name to the frame" << std::endl;
    weights.push_back("reference");
  }

  // add the weights as parameters to the frame
  runFrame.putParameter("WeightNames", weights);

  // write the frame to the Writer:
  m_edm4hepWriter.writeFrame(runFrame, podio::Category::Run);

}

edm4hep::MutableMCParticle WriterEDM4HEP::write_particle(const ConstGenParticlePtr& hepmcParticle)
{
  edm4hep::MutableMCParticle edm_particle;
  edm_particle.setPDG(hepmcParticle->pdg_id());
  edm_particle.setGeneratorStatus(hepmcParticle->status());
  // look up charge from pdg_id
  HepPDT::ParticleID particleID(hepmcParticle->pdg_id());
  edm_particle.setCharge(particleID.charge());

  // convert momentum
  auto p = hepmcParticle->momentum();
  edm_particle.setMomentum( {p.px(), p.py(), p.pz()} );

  // set the mass (energy is deduced in EDM4HEP
  edm_particle.setMass(p.m());

  // add spin (particle helicity) information if available
  std::shared_ptr<HepMC3::VectorFloatAttribute> spin = hepmcParticle->attribute<HepMC3::VectorFloatAttribute>("spin");
  if (spin) {
     edm4hep::Vector3f hel(spin->value()[0], spin->value()[1], spin->value()[2]);
     edm_particle.setSpin(hel);
  }

  // convert production vertex info and time info:
  auto prodVtx = hepmcParticle->production_vertex();
  if ( prodVtx!=nullptr ) {
    auto& pos = prodVtx->position();
    edm_particle.setVertex( {pos.x(), pos.y(), pos.z()} );
    edm_particle.setTime(pos.t());
  }

  // convert the decay vertex (if present) 
  auto endpointVtx = hepmcParticle->end_vertex();
  if ( endpointVtx!=nullptr ) {
    auto& pos = endpointVtx->position();
    edm_particle.setEndpoint( {pos.x(), pos.y(), pos.z()} );
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
