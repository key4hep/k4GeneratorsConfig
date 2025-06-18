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
ls .libs/* >> whizardDEBUG.log
echo ldd of .libs/default_lib.so
ldd .libs/default_lib.so
echo ldd of .libs/default_lib.so.0
ldd .libs/default_lib.so.0
echo ldd of .libs/default_lib.so.0.0.0
ldd .libs/default_lib.so.0.0.0

