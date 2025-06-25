#!/usr/bin/tcsh


# Automatically get the directory where this script is located
#K4GeneratorsConfigLocalBuildDir=$(cd -- "$(dirname -- "${(%):-%x}")" && pwd)
# check that we are sourcing
if ("$0" != "-tcsh" && "$0" != "tcsh") then
    echo Please use source setup.csh to set up the project
    exit
endif
# it's clumsy, but that's C-SHELL which does not allow nested commands
set theCommand=($_)
set thePath=`dirname "$theCommand[2]"`
set K4GeneratorsConfigDir=`cd "$thePath"; pwd`
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
       setenv PYTHONPATH ${K4GeneratorsConfigDir}/python/${dir}:$PYTHONPATH
   else
       setenv PYTHONPATH ${K4GeneratorsConfigDir}/python/${dir}
   endif
end

# Check if the directory exists
if (! -d "${K4GeneratorsConfigDir}/install/") then
    echo Install directory not found!
    echo After: 
    echo cmake ../CMakeLists.txt -DCMAKE_INSTALL_PREFIX=../install
    echo Please run:
    echo make install
    exit 1
endif

setenv K4GENERATORSCONFIG  "${K4GeneratorsConfigDir}/install/bin"

# Set executable
alias k4GeneratorsConfig "python3 ${K4GeneratorsConfigDir}/python/main.py"
