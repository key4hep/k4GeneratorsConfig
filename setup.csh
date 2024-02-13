#!/usr/bin/tcsh


# Automatically get the directory where this script is located
#K4GenDir=$(cd -- "$(dirname -- "${(%):-%x}")" && pwd)
# check that we are sourcing
if ("$0" != "-tcsh" && "$0" != "tcsh") then
    echo Please use source setup.csh to set up the project
    exit
endif
# it's clumsy, but that's C-SHELL which does not allow nested commands
set theCommand=($_)
set thePath=`dirname "$theCommand[2]"`
set K4GenDir=`cd "$thePath"; pwd`
unset thePath
unset theCommand

set PYTHON3=`where python3`x
if ( "$PYTHON3" == "x" ) then
    echo "Python3 is required, but not found!"
    exit
endif

set SrcDir=( Generators )

foreach dir ( $SrcDir )
   if ( $?PYTHONPATH ) then
       setenv PYTHONPATH ${K4GenDir}/python/${dir}:$PYTHONPATH
   else 
       setenv PYTHONPATH ${K4GenDir}/python/${dir}
   endif
end

# Set executable
alias k4gen "python3 ${K4GenDir}/python/main.py"
