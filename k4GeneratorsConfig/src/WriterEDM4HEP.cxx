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

  // add the event_scale
  std::string name = "event_scale";
  eventFrame.putParameter(name,retrieveAttribute(evt,name));

  // add the alphaQED
  name = "alphaQED";
  eventFrame.putParameter(name,retrieveAttribute(evt,name));

  // add alphaQCD
  name = "alphaQCD";
  eventFrame.putParameter(name,retrieveAttribute(evt,name));

  // write the frame to the Writer:
  m_edm4hepWriter.writeFrame(eventFrame, podio::Category::Event);

}
double WriterEDM4HEP::retrieveAttribute(const GenEvent &evt, std::string name) {

  shared_ptr<HepMC3::DoubleAttribute> hepmcPtr = evt.attribute<HepMC3::DoubleAttribute>(name);
  double result = hepmcPtr?(hepmcPtr->value()):0.0;

  return result;
}


void WriterEDM4HEP::write_run_info() {

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

  // add the SQRTS to the runFrame
  double sqrts= 4711.;
  runFrame.putParameter("SQRTS",sqrts);

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
	std::cout << "k4GeneratorsConfig::WriterEDM4HEP::ERROR the vector has size " << colorFlowPtr->value().size() 
		  << " greater then 2 as foreseen by EDM4HEP" << std::endl
		  << "Stopping Execution" << std::endl;
	exit(1);
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

  // try something
  /*  HepMC3::GenEvent *mutableEvent = new GenEvent();  
  std::shared_ptr<HepMC3::GenParticle> mutableHepMCparticle= std::make_shared<HepMC3::GenParticle>();  
  HepMC3::FourVector myVec(10.,20.,30.,1000.);
  mutableHepMCparticle->set_momentum(myVec);
  mutableEvent->add_particle(mutableHepMCparticle);

  std::vector<int> val;
  val.push_back(4711);
  val.push_back(4712);
  mutableHepMCparticle->add_attribute("flows",std::make_shared<VectorIntAttribute>(val));  
  std::cout << "Retrieving the attribute " << mutableHepMCparticle->attribute_as_string("flows") << std::endl;
  std::cout << "Attribute names " << mutableHepMCparticle->attribute_names().size() << std::endl;
  std::shared_ptr<HepMC3::VectorIntAttribute> colorFlowPtrM = mutableHepMCparticle->attribute<HepMC3::VectorIntAttribute>("flows");
  std::cout << "Retrieval Pointer " << colorFlowPtrM << std::endl;
  std::cout << "Retrieval Size " << colorFlowPtrM->value().size() << std::endl;
  std::cout << "Retrieval val0 " << colorFlowPtrM->value()[0] << std::endl;
  std::cout << "Retrieval val1 " << colorFlowPtrM->value()[1] << std::endl;*/

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
