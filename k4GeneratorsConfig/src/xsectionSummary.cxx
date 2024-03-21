// File to read EDM4HEP output and extract the cross sections
#include <iostream>
#include <fstream>
#include "xsectionCollection.h"

//
int main(int argc, char** argv)
{

  // instantiate the collection as pointer
  k4GeneratorsConfig::xsectionCollection *xsecColl = new k4GeneratorsConfig::xsectionCollection();
  // execute the gathering of information including detailed output
  xsecColl->Execute();
  // print the summary on screen
  xsecColl->PrintSummary(std::cout);
  // save the summary in a file
  std::ofstream outFile("XsectionSummary.dat");
  std::ostream &output = outFile;
  xsecColl->PrintSummary(output);
  // delete the pointer
  delete xsecColl; xsecColl=0;
}
