#include "xsection.h"
#include <iostream>

#include "edm4hep/Constants.h"
#include "edm4hep/GeneratorEventParametersCollection.h"
#include "edm4hep/GeneratorToolInfo.h"
#include "podio/Frame.h"

k4GeneratorsConfig::xsection::xsection()
    : m_xsection(0.), m_xsectionError(0.), m_sqrts(0.), m_generator(""), m_process(""), m_file(""), m_isValid(false) {
  m_reader = new podio::ROOTReader();
}
k4GeneratorsConfig::xsection::xsection(double xsec, double xsecError, double sqrts, std::string generator,
                                       std::string process, std::string file) {
  m_xsection = xsec;
  m_xsectionError = xsecError;
  m_sqrts = sqrts;
  m_generator = generator;
  m_process = process;
  m_file = file;

  m_reader = new podio::ROOTReader();
  m_isValid = processFile();
}
k4GeneratorsConfig::xsection::xsection(const xsection& theOriginal) {
  if (this != &theOriginal) {
    m_xsection = theOriginal.m_xsection;
    m_xsectionError = theOriginal.m_xsectionError;
    m_sqrts = theOriginal.m_sqrts;
    m_generator = theOriginal.m_generator;
    m_process = theOriginal.m_process;
    m_file = theOriginal.m_file;
    m_isValid = theOriginal.m_isValid;
    m_reader = new podio::ROOTReader();
  }
}
k4GeneratorsConfig::xsection& k4GeneratorsConfig::xsection::operator=(const xsection& theOriginal) {
  if (this != &theOriginal) {
    m_xsection = theOriginal.m_xsection;
    m_xsectionError = theOriginal.m_xsectionError;
    m_sqrts = theOriginal.m_sqrts;
    m_generator = theOriginal.m_generator;
    m_process = theOriginal.m_process;
    m_file = theOriginal.m_file;
    m_isValid = theOriginal.m_isValid;
    if (m_reader != 0)
      delete m_reader;
    m_reader = new podio::ROOTReader();
  }

  return *this;
}
k4GeneratorsConfig::xsection::~xsection() {
  delete m_reader;
  m_reader = 0;
}
bool k4GeneratorsConfig::xsection::processFile() {

  // open the edm4hep file
  m_reader->openFile(m_file);

  // retrieve the RunInfo for the weight names, there should only be 1 entry per Run
  if (m_reader->getEntries(podio::Category::Run) == 0) {
    return false;
  }
  auto runinfo = podio::Frame(m_reader->readNextEntry(podio::Category::Run));
  const auto possibleWeightNames =
      runinfo.getParameter<std::vector<std::string>>(edm4hep::labels::GeneratorWeightNames);
  const auto weightNames = possibleWeightNames.value();
  if (weightNames.size() == 0) {
    std::cout << "k4GeneratorsConfig::Warning: no weight names were found" << std::endl;
  }

  auto toolInfos = edm4hep::utils::getGenToolInfos(runinfo);
  if (toolInfos.size() > 0) {
    m_generator = toolInfos[0].name;
  } else {
    std::cout << "k4GeneratorsConfig::Warning ToolInfos not available" << std::endl;
  }

  // retrieve the cross section for the last event if not possible it's not valid
  if (m_reader->getEntries(podio::Category::Event) == 0) {
    m_xsection = 0.;
    m_xsectionError = 0.;
    return false;
  }
  unsigned int lastEvent = m_reader->getEntries(podio::Category::Event) - 1;
  auto event = podio::Frame(m_reader->readEntry(podio::Category::Event, lastEvent));

  // now get the event parameters there must be at least one entry!
  const edm4hep::GeneratorEventParametersCollection& genParametersCollection =
      event.get<edm4hep::GeneratorEventParametersCollection>(edm4hep::labels::GeneratorEventParameters);
  if (genParametersCollection.size() == 0)
    return false;
  edm4hep::GeneratorEventParameters genParameters = genParametersCollection[0];

  // decode sqrts
  m_sqrts = genParameters.getSqrts();

  // decode the cross sections
  m_xsection = 0.;
  if (genParameters.crossSections_size() > 0) {
    m_xsection = genParameters.getCrossSections()[0];
  }

  // decode the cross section errors
  m_xsectionError = 0.;
  if (genParameters.crossSectionErrors_size() > 0) {
    m_xsectionError = genParameters.getCrossSectionErrors()[0];
  }

  return true;
}
void k4GeneratorsConfig::xsection::setXsection(double xsec) { m_xsection = xsec; }
void k4GeneratorsConfig::xsection::setXsection(double xsec, double err) {
  setXsection(xsec);
  setXsectionError(err);
}
void k4GeneratorsConfig::xsection::setXsectionError(double error) { m_xsectionError = error; }
void k4GeneratorsConfig::xsection::setSQRTS(double sqrts) { m_sqrts = sqrts; }
void k4GeneratorsConfig::xsection::setGenerator(std::string gen) { m_generator = gen; }
void k4GeneratorsConfig::xsection::setProcess(std::string proc) { m_process = proc; }
void k4GeneratorsConfig::xsection::setFile(std::string file) {
  m_file = file;
  m_isValid = processFile();
}
double k4GeneratorsConfig::xsection::Xsection() { return m_xsection; }
double k4GeneratorsConfig::xsection::XsectionError() { return m_xsectionError; }
double k4GeneratorsConfig::xsection::SQRTS() { return m_sqrts; }
std::string k4GeneratorsConfig::xsection::Generator() { return m_generator; }
std::string k4GeneratorsConfig::xsection::Process() { return m_process; }
std::string k4GeneratorsConfig::xsection::File() { return m_file; }
bool k4GeneratorsConfig::xsection::isValid() { return m_isValid; }
void k4GeneratorsConfig::xsection::Print() {
  std::cout << std::endl;
  std::cout << "xsection object summary:" << std::endl;
  std::cout << "File          : " << m_file << std::endl;
  std::cout << "Process       : " << m_process << std::endl;
  std::cout << "SQRTS         : " << m_sqrts << std::endl;
  std::cout << "Generator     : " << m_generator << std::endl;
  std::cout << "xsection valid: " << m_isValid << std::endl;
  std::cout << "xsection      : " << m_xsection << " +- " << m_xsectionError << " pb" << std::endl;
  std::cout << std::endl;
}
