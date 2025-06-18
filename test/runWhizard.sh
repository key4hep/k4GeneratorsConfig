export MYWHIZARD=`which whizard`
echo whizard is: $MYWHIZARD >> whizardDEBUG.log
echo ldd whizard >> whizardDEBUG.log
ldd $MYWHIZARD >> whizardDEBUG.log
export MYLIB=`whizard-config --libdir`
echo lib dir is $MYLIB >> whizardDEBUG.log
echo ldd $MYLIB/libomega.so.0 >> whizardDEBUG.log
ldd $MYLIB/libomega.so.0 >> whizardDEBUG.log
whizard ref-results/Whizard/Muon350/Muon350_ISR.sin
ls -alt >> whizardDEBUG.log

