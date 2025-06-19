export WHIZARDLIB=`whizard-config --libdir`/../
echo EXTENDING LD_LIBRARY_PATH with $WHIZARDLIB >> whizardDEBUG.log
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$WHIZARDLIB
export MYWHIZARD=`which whizard`
echo whizard is: $MYWHIZARD >> whizardDEBUG.log
echo ldd whizard >> whizardDEBUG.log
ldd $MYWHIZARD >> whizardDEBUG.log
export MYLIB=`whizard-config --libdir`
echo lib dir is $MYLIB >> whizardDEBUG.log
echo ldd $MYLIB/../libomega.so.0 >> whizardDEBUG.log
ldd $MYLIB/../libomega.so.0 >> whizardDEBUG.log
whizard ref-results/Whizard/Muon350/Muon350_ISR.sin
echo LIBTOOL in makefile is: >> whizardDEBUG.log
grep libtool default_lib.makefile >> whizardDEBUG.log
echo LOOKING INTO .libs >> whizardDEBUG.log
ls -l .libs/* >> whizardDEBUG.log
echo ldd of .libs/default_lib.so  >> whizardDEBUG.log
ldd .libs/default_lib.so  >> whizardDEBUG.log
echo ldd of .libs/default_lib.so.0  >> whizardDEBUG.log
ldd .libs/default_lib.so.0  >> whizardDEBUG.log
echo ldd of .libs/default_lib.so.0.0.0  >> whizardDEBUG.log
ldd .libs/default_lib.so.0.0.0  >> whizardDEBUG.log
echo ldd of .libs/default_lib.so.0.0.0  >> whizardDEBUG.log
echo cat default_lib.la >> whizardDEBUG.log
cat default_lib.la >> whizardDEBUG.log
echo cat default_lib.lo >> whizardDEBUG.log
cat default_lib.lo >> whizardDEBUG.log
echo ls -l /cvmfs/sw-nightlies.hsf.org/key4hep/releases/2025-06-07/x86_64-almalinux9-gcc14.2.0-opt/whizard/3.1.5-3v5fcx/lib >> whizardDEBUG.log
ls -l /cvmfs/sw-nightlies.hsf.org/key4hep/releases/2025-06-07/x86_64-almalinux9-gcc14.2.0-opt/whizard/3.1.5-3v5fcx/lib >> whizardDEBUG.log
echo readelf -d .libs/default_lib.so  >> whizardDEBUG.log
readelf -d .libs/default_lib.so  >> whizardDEBUG.log
echo LD_LIBRARY_PATH  >> whizardDEBUG.log
echo $LD_LIBRARY_PATH  >> whizardDEBUG.log

