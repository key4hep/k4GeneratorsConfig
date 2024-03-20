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
    else
    {
      write_run_info();
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

  auto eventFrame = podio::Frame();
  edm4hep::MCParticleCollection particleCollection;
  
  std::unordered_map<unsigned int, edm4hep::MutableMCParticle> _map;
  for (auto _p:evt.particles()) {
    //    std::cout << "Converting hepmc particle with Pdg_ID " << _p->pdg_id() << "and id " <<  _p->id() << std::endl;
    if (_map.find(_p->id()) == _map.end()) {
      edm4hep::MutableMCParticle edm_particle = write_particle(_p);
      _map.insert({_p->id(), edm_particle});
    }
    // mother/daughter links
    auto prodvertex = _p->production_vertex();
    if (nullptr != prodvertex) {
      for (auto particle_mother: prodvertex->particles_in()) {
        if (_map.find(particle_mother->id()) == _map.end()) {
          edm4hep::MutableMCParticle edm_particle = write_particle(particle_mother);
          _map.insert({particle_mother->id(), edm_particle});
        }
        _map[_p->id()].addToParents(_map[particle_mother->id()]);
      }
    }
    auto endvertex = _p->end_vertex();
    if (nullptr != endvertex) {
      for (auto particle_daughter: endvertex->particles_out()) {
        if (_map.find(particle_daughter->id()) == _map.end()) {
          auto edm_particle = write_particle(particle_daughter);
          _map.insert({particle_daughter->id(), edm_particle});
        }
        _map[_p->id()].addToDaughters(_map[particle_daughter->id()]);
      }
    }
  }
  for (auto particle_pair: _map) {
    particleCollection.push_back(particle_pair.second);
  }

  // write the collection of MCParticles to the frame 
  eventFrame.put(std::move(particleCollection), "MCParticles");

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

  // write the frame to the Writer:
  m_edm4hepWriter.writeFrame(eventFrame, "events");

  // a cross section is attached to GenEvent, so we should try to decode it:
  // print the cross section and error every 10000 events
  if ( evt.event_number() % 10000 == 0 ){
    if ( evt.cross_section() ) {
      if ( evt.cross_section()->is_valid() ){
	std::cout << "Xsection is valid" << std::endl;
	double xsection      = evt.cross_section()->xsecs()[0];
	double xsectionError = evt.cross_section()->xsec_errs()[0];
	std::cout << "The cross section is " << xsection << " with error " << xsectionError << std::endl;
      }
      else{
	std::cout << "Xsection is NOT valid" << std::endl;
      }
    }
    else {
	std::cout << "Xsection object not found" << std::endl;
    }
  }

}


void WriterEDM4HEP::write_run_info() {

  std::cout << "Here we should write the header to EDM4HEP" << std::endl;
  std::vector<std::string> weights = run_info()->weight_names();
  std::cout << "WriterEDM4HEP found " << weights.size() << " weight names for conversion" << std::endl;
  for ( unsigned int i=0; i< weights.size() ; i++){
    std::cout << "Weight index " << i << " name " << weights[i] << std::endl;
  }

  if ( weights.size() == 0 ){
    std::cout << "No weight names found, writing a single name to the frame" << std::endl;
    weights.push_back("reference");
  }

  // create the frame
  auto runFrame = podio::Frame();

  // add the weights as parameters to the frame
  runFrame.putParameter("WeightNames", weights);

  // write the frame to the Writer:
  m_edm4hepWriter.writeFrame(runFrame, "RunInfo");

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
  edm_particle.setMomentum( {float(p.px()), float(p.py()), float(p.pz())} );

  // add spin (particle helicity) information if available
  std::shared_ptr<HepMC3::VectorFloatAttribute> spin = hepmcParticle->attribute<HepMC3::VectorFloatAttribute>("spin");
  if (spin) {
     edm4hep::Vector3f hel(spin->value()[0], spin->value()[1], spin->value()[2]);
     edm_particle.setSpin(hel);
  }

  // convert vertex info and time info:
  auto prodVtx = hepmcParticle->production_vertex();

  if ( prodVtx!=nullptr ) {
    auto& pos = prodVtx->position();
    edm_particle.setVertex( {float(pos.x()), float(pos.y()), float(pos.z())} );
    edm_particle.setTime(pos.t());
  }

  //  std::cout << "Colorflow STATUS missing" << std::endl;

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
