# Standard Tests
You can test the creation of the input files and the event generation step:
```
bash
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
cd build
ctest --verbose
```
⚠️ **Warning**: Always run this scheme as cmake and make set up the environment variables correctly for the execution of the generation step

