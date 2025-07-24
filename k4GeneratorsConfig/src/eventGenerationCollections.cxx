#include "eventGenerationCollections.h"
#include "eventGenerationCollections2Root.h"
#include <algorithm>
#include <filesystem>
#include <iostream>
#include <sys/stat.h>

k4GeneratorsConfig::eventGenerationCollections::eventGenerationCollections() : m_validCounter(0), m_invalidCounter(0) {}
k4GeneratorsConfig::eventGenerationCollections::eventGenerationCollections(
    const eventGenerationCollections& theOriginal) {
  if (this != &theOriginal) {
    m_xsectionCollection = theOriginal.m_xsectionCollection;
    m_analysisHistosCollection = theOriginal.m_analysisHistosCollection;
    m_validCounter = theOriginal.m_validCounter;
    m_invalidCounter = theOriginal.m_invalidCounter;
    m_log = theOriginal.m_log;
  }
}
k4GeneratorsConfig::eventGenerationCollections&
k4GeneratorsConfig::eventGenerationCollections::operator=(const eventGenerationCollections& theOriginal) {
  if (this != &theOriginal) {
    m_xsectionCollection = theOriginal.m_xsectionCollection;
    m_analysisHistosCollection = theOriginal.m_analysisHistosCollection;
    m_validCounter = theOriginal.m_validCounter;
    m_invalidCounter = theOriginal.m_invalidCounter;
    m_log = theOriginal.m_log;
  }

  return *this;
}
k4GeneratorsConfig::eventGenerationCollections::~eventGenerationCollections() {}
void k4GeneratorsConfig::eventGenerationCollections::Execute() {

  // first make the collection
  makeCollections();

  // second order the collection according to the process
  orderCollections();
}
void k4GeneratorsConfig::eventGenerationCollections::makeCollections() {

  for (const auto& generators : std::filesystem::directory_iterator("Run-Cards")) {
    std::filesystem::path generatorsPath = generators.path();
    if (!std::filesystem::is_directory(generatorsPath))
      continue;

    for (const auto& procs : std::filesystem::directory_iterator(generatorsPath.string())) {
      std::filesystem::path processPath = procs.path();
      if (!std::filesystem::is_directory(processPath))
        continue;

      k4GeneratorsConfig::xsection* xsec = new k4GeneratorsConfig::xsection();
      for (const auto& files : std::filesystem::directory_iterator(processPath.string())) {
        std::filesystem::path filenamePath = files.path();
        if (!std::filesystem::is_regular_file(filenamePath))
          continue;
        // take care of the total cross section extracted from the EDM4HEP file
        if (filenamePath.extension() == ".edm4hep") {
          std::cout << "eventGenerationCollections::Process: " << processPath.filename().string()
                    << " File:" << filenamePath.filename().string() << std::endl;
          xsec->setProcess(processPath.filename().string());
          xsec->setFile(filenamePath.string());
          // in some cases the generator name is not available, therefore derive from the filename
          xsec->setGenerator(generatorsPath.filename().string());
          std::cout << "Generator " << xsec->Generator() << " has been processed" << std::endl;
          m_xsectionCollection.push_back(*xsec);
          if (xsec->isValid())
            m_validCounter++;
          if (!xsec->isValid())
            m_invalidCounter++;
        }
      }
      // we need to keep xsec alive for the analysisHistos distributions
      for (const auto& files : std::filesystem::directory_iterator(processPath.string())) {
        std::filesystem::path filenamePath = files.path();
        if (!std::filesystem::is_regular_file(filenamePath))
          continue;
        // take care of the analysisHistos distributions extracted from the .root (analysis output) file
        if (filenamePath.extension() == ".root") {
          std::cout << "eventGenerationCollections::Process: " << processPath.filename().string()
                    << " File: " << filenamePath.filename().string() << std::endl;
          k4GeneratorsConfig::analysisHistos* diffDist = new k4GeneratorsConfig::analysisHistos();
          diffDist->setProcess(processPath.filename().string());
          diffDist->setFile(filenamePath.string());
          diffDist->setSQRTS(xsec->SQRTS());
          // in some cases the generator name is not available, therefore derive from the filename
          diffDist->setGenerator(generatorsPath.filename().string());
          std::cout << "Generator " << diffDist->Generator() << " has been processed for analysisHistos distributions"
                    << std::endl;
          m_analysisHistosCollection.push_back(*diffDist);
          delete diffDist;
        }
      }
      delete xsec;
    }
  }
}
void k4GeneratorsConfig::eventGenerationCollections::orderCollections() {

  // order by content
  std::sort(m_xsectionCollection.begin(), m_xsectionCollection.end(),
            [this](xsection A, xsection B) { return this->compareLexical(A, B); });

  // order by content
  std::sort(m_analysisHistosCollection.begin(), m_analysisHistosCollection.end(),
            [this](analysisHistos A, analysisHistos B) { return this->compareLexical(A, B); });
}
bool k4GeneratorsConfig::eventGenerationCollections::compareLength(xsection A, xsection B) {

  // retrieve the process as ordering variable
  std::string processA = A.Process();
  std::string processB = B.Process();

  return processA.size() < processB.size();
}
bool k4GeneratorsConfig::eventGenerationCollections::compareLexical(xsection A, xsection B) {

  // retrieve the process as ordering variable
  std::string processNgenA = A.Process() + A.Generator();
  std::string processNgenB = B.Process() + B.Generator();

  std::vector<std::string> listOf2;
  listOf2.push_back(processNgenA);
  listOf2.push_back(processNgenB);
  sort(listOf2.begin(), listOf2.end());

  // if the order is changed return true otherwise false
  if (processNgenA.compare(listOf2[0]) == 0)
    return true;

  return false;
}
bool k4GeneratorsConfig::eventGenerationCollections::compareLexical(analysisHistos A, analysisHistos B) {

  // retrieve the process as ordering variable
  std::string processNgenA = A.Process() + A.Generator();
  std::string processNgenB = B.Process() + B.Generator();

  std::vector<std::string> listOf2;
  listOf2.push_back(processNgenA);
  listOf2.push_back(processNgenB);
  sort(listOf2.begin(), listOf2.end());

  // if the order is changed return true otherwise false
  if (processNgenA.compare(listOf2[0]) == 0)
    return true;

  return false;
}
unsigned int k4GeneratorsConfig::eventGenerationCollections::NbOfSuccesses() { return m_validCounter; }
unsigned int k4GeneratorsConfig::eventGenerationCollections::NbOfFailures() { return m_invalidCounter; }
void k4GeneratorsConfig::eventGenerationCollections::Write2Root(std::string dirname, std::string filename) {

  eventGenerationCollections2Root out(dirname, filename);

  for (auto xsec : m_xsectionCollection) {
    if (xsec.isValid()) {
      out.Execute(xsec);
    }
  }
  // diffhists uses the matrix calculated before for the xsectionCollection
  for (auto diffHists : m_analysisHistosCollection) {
    if (diffHists.isValid()) {
      out.Execute(diffHists);
    }
  }
  out.Finalize();

  // now we save the log to the log :)
  std::vector<std::string> logRoot;
  logRoot = out.getLog();
  m_log.insert(m_log.end(), logRoot.begin(), logRoot.end());
}
void k4GeneratorsConfig::eventGenerationCollections::Print(bool onlyOK, std::ostream& output) const {

  for (auto xsec : m_xsectionCollection) {
    if (!onlyOK) {
      xsec.Print(output);
    } else {
      if (xsec.isValid()) {
        xsec.Print(output);
      }
    }
  }
}
void k4GeneratorsConfig::eventGenerationCollections::PrintRootLog(std::ostream& output) const {

  for (auto line : m_log) {
    output << line << std::endl;
  }
}
void k4GeneratorsConfig::eventGenerationCollections::PrintSummary(std::ostream& output) const {

  // print the root messages (chi2)
  PrintRootLog(output);

  // print all details for each run
  Print(false, output);

  // and now the summary
  std::string previousProcess = "XXXX";
  for (auto xsec : m_xsectionCollection) {
    // only print valid cross sections
    if (!xsec.isValid())
      continue;
    // if it's a new process print a new line
    std::string proc = xsec.Process();
    std::string filename = xsec.File();
    if (proc.compare(previousProcess) != 0) {
      if (previousProcess.compare("XXXX") != 0)
        output << std::endl;
      output << proc << " sqrts= " << xsec.SQRTS();
      if (filename.find("ISR") != std::string::npos) {
        output << " with ISR ";
        if (filename.find("BST") != std::string::npos) {
          output << " with Beamstrahlung ";
        }
      }
      output << ":" << std::endl;
      previousProcess = proc;
    }
    // print the generator name and cross section with its error
    output << std::setw(20) << std::left << xsec.Generator() << " " << std::setw(8) << std::left << xsec.Xsection()
           << " +- " << std::setw(8) << std::left << xsec.XsectionError() << " pb" << std::endl;
  }
  output << std::endl;
  // last thing the invalids
  output << "Number of runs           : " << m_invalidCounter + m_validCounter << std::endl;
  output << "Number of failed runs    : " << m_invalidCounter << std::endl;
  output << "Number of successful runs: " << m_validCounter << std::endl;
}
