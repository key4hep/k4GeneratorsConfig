import os
import sys
import shutil
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'Tools')))
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), 'Generators')))

import argparse
import Input
import Particles as particles
import Process
import Generators as Gen


parser = argparse.ArgumentParser(description='')

parser.add_argument(
  "-f",
  nargs="*",
  type=str,  # any type/callable can be used here
  default=[],
  help="Input yaml file"
)
args = parser.parse_args()
FILES = (args.f)

def MakeOutDir(gens, OUTDIR):
  # Overright directory if exisit
  if not os.path.exists(OUTDIR):
    # shutil.rmtree(OUTDIR)
    os.mkdir(OUTDIR)
  for g in gens:
    if not os.path.exists(OUTDIR+"/{}".format(g)):
      os.mkdir(OUTDIR+"/{}".format(g))


def main():
  for files in FILES:
    settings=Input.Input(files)
    settings.Generators()
    procs = settings.GetProcesses()
    sqrts = settings.GetSqrtS()
    model = settings.GetModel()
    events = settings.GetEventNumber()
    pdata = settings.GetParticleData()
    gens = Gen.generators(settings.Generators())
    
    try:
      outdir = settings.get("OutDir")
    except:
    # If not dir set in input use default
      outdir= "Run-Cards"

    MakeOutDir(settings.Generators(),outdir)
    proc = {}
    for key, value in procs.items():
      initial = value["Initial"]
      final   = value["Final"]
      order   = value["Order"]
      param = Process.ProcessParameters(settings)
      proc[key] = Process.Process(initial, final, sqrts, 
                                  order, key, param, OutDir=outdir 
                                  )
    for p in proc.values():
      p.ProcessInfo()
      p.SetParticleData(pdata)
      gens.SetProcessInfo(p)
      gens.InitalizeGenerators()



if __name__ == '__main__':
	main()

    
