# Running tests:
You can test the creation of the input files and the event generation step:
```
bash
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
cd build
ctest --verbose
```
⚠️ **Warning**: Always run this scheme as cmake and make set up the environment variables correctly for the execution of the generation step

## Running with local modifications of the code:
Setting up with
```bash
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
cd build
cmake ../CMakeLists.txt -DCMAKE_INSTALL_PREFIX=../install
make install
k4_local_repo
```
will extract the global paths and set the executables to the local install directory instead of the release. The runscripts therefore will run automatically with the executables
you have modified

