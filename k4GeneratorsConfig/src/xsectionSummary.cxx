// File to read EDM4HEP output and extract the cross sections
#include "xsectionCollection.h"
#include <fstream>
#include <iostream>
#include <unistd.h>

//
int main(int argc, char** argv) {

  std::string filename = "XsectionSummary.dat";
  std::string fileRoot = "XsectionSummary.root";
  int c;
  while ((c = getopt(argc, argv, "hf:r:")) != -1)
    switch (c) {
    case 'f':
      filename = optarg;
      break;
    case 'r':
      fileRoot = optarg;
      break;
    case 'h':
      std::cout << "Usage: xsectionSummary -h -f filename" << std::endl;
      std::cout << "-h: print this help" << std::endl;
      std::cout << "-f filename: print the summary information to this file" << std::endl;
      std::cout << "-r filename: write the RootTree to this file" << std::endl;
      exit(0);
    default:
      exit(0);
    }

  // instantiate the collection as pointer
  k4GeneratorsConfig::xsectionCollection* xsecColl = new k4GeneratorsConfig::xsectionCollection();
  // execute the gathering of information including detailed output
  xsecColl->Execute();
  // print the summary on screen
  xsecColl->PrintSummary(std::cout);
  // save the summary in a file
  std::ofstream outFile(filename);
  std::ostream& output = outFile;
  xsecColl->PrintSummary(output);
  // write to root
  xsecColl->Write2Root(fileRoot);
  // if there is a failure:
  if (xsecColl->NbOfFailures() != 0) {
    std::cout << xsecColl->NbOfFailures() << "/" << xsecColl->NbOfFailures() + xsecColl->NbOfSuccesses()
              << " Runs failed" << std::endl;
    exit(1);
  }
  // delete the pointer
  delete xsecColl;
  xsecColl = 0;
}
