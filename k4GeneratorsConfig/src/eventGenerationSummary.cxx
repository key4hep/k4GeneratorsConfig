// File to read EDM4HEP output and extract the cross sections
#include "eventGenerationCollections.h"
#include <fstream>
#include <iostream>
#include <unistd.h>

//
int main(int argc, char** argv) {

  std::string topDir = "Run-Cards";
  std::string filename = "GenerationSummary.dat";
  std::string dirRoot = ".";
  std::string fileRoot = "eventGenerationSummary.root";
  int c;
  while ((c = getopt(argc, argv, "hw:f:d:r:")) != -1)
    switch (c) {
    case 'w':
      topDir = optarg;
      break;
    case 'f':
      filename = optarg;
      break;
    case 'd':
      dirRoot = optarg;
      break;
    case 'r':
      fileRoot = optarg;
      break;
    case 'h':
      std::cout << "Usage: xsectionSummary -h -w workdir -f filename -d rootdir -r rootfile" << std::endl;
      std::cout << "-h: print this help" << std::endl;
      std::cout << "-w dirname: top directory to start the search for generators and processes (default: Run-Cards)"
                << std::endl;
      std::cout << "-f filename: print the summary information to this file (default: GenerationSummary.dat)"
                << std::endl;
      std::cout << "-d rootdir: write the RootTree and figures to this directory (default: .)" << std::endl;
      std::cout << "-r footfile: write the RootTree to this file (default: eventGenerationSummary.root)" << std::endl;
      exit(0);
    default:
      exit(0);
    }

  // instantiate the collection as pointer
  k4GeneratorsConfig::eventGenerationCollections* evgenColls = new k4GeneratorsConfig::eventGenerationCollections();
  // execute the gathering of information including detailed output
  evgenColls->Execute(topDir);
  // do the root analysis
  evgenColls->Write2Root(dirRoot, fileRoot);
  // print the summary on screen
  evgenColls->PrintSummary(std::cout);
  // save the summary in a file (call after root to fill the log
  std::ofstream outFile(filename);
  std::ostream& output = outFile;
  evgenColls->PrintSummary(output);
  // if there is a failure:
  bool failure = false;
  if (evgenColls->NbOfFailures() != 0) {
    std::cout << evgenColls->NbOfFailures() << "/" << evgenColls->NbOfFailures() + evgenColls->NbOfSuccesses()
              << " Runs failed" << std::endl;
    failure = true;
  }
  // delete the pointer
  delete evgenColls;
  evgenColls = nullptr;

  // fallure exit non zero
  if (failure) {
    exit(1);
  }
}
