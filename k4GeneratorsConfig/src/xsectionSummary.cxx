// File to read EDM4HEP output and extract the cross sections
#include <iostream>

#include "xsectionCollection.h"

//
int main(int argc, char** argv)
{

  k4GeneratorsConfig::xsectionCollection *xsecColl = new k4GeneratorsConfig::xsectionCollection();
  xsecColl->Execute();
  delete xsecColl; xsecColl=0;
}
