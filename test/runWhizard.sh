which libtool
export MYLIBTOOL=`/cvmfs/sw-nightlies.hsf.org/key4hep/releases/2025-06-07/x86_64-almalinux9-gcc14.2.0-opt/whizard/3.1.5-3v5fcx/bin/whizard-config --libdir`/libtool
echo libtool is set to $MYLIBTOOL
whizard ref-results/Whizard/Muon350/Muon350_ISR.sin --libtool $MYLIBTOOL
