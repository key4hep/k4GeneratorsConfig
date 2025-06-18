export MYWHIZARD=`which whizard`
echo whizard is: $MYWHIZARD >> whizard.log
echo ldd whizard >> whizard.log
ldd $MYWHIZARD >> whizard.log
export MYLIB=`whizard-config --libdir`
echo lib dir is $MYLIB >> whizard.log
echo ldd $MYLIB/libomega.so.0 >> whizard.log
ldd $MYLIB/libomega.so.0 >> whizard.log
whizard ref-results/Whizard/Muon350/Muon350_ISR.sin
ls -alt >> whizard.log

