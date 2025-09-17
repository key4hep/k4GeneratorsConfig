# Identified Issues in inverse chronological order

- $${\color{green}&check;}$$  means that the problem has been solved
- $${\color{red}&cross;}$$  means that the problem is under investigation

## Generator Configuration in Key4hep

- $${\color{green}&check;}$$ [Issue](https://github.com/key4hep/key4hep-spack/pull/763): Configuration of WHIZARD missing environment variable on ALMA in Key4hep.  CI failed on ALMA, not on UBUNTU. The WHIZARD environment was not set up consistently in Key4hep.

- $${\color{green}&check;}$$ [Issue](https://github.com/key4hep/key4hep-spack/issues/721): Configuration of MADGRAPH incomplete in key4hep. The MADGRAPH model file for the standard EW scheme is not shipped with the distribution, it has to be installed in addition.

## Generator Issues

- $${\color{red}&cross;}$$  [Issue](https://github.com/key4hep/k4GeneratorsConfig/issues/33): Inconsistent kinematics with ISR in MADGRAPH. The system detected a decreased cross section with ISR due to event rejection. An adhoc fix was applied in MADGRAPH.

- $${\color{green}&check;}$$ [Issue](https://gitlab.com/sherpa-team/sherpa/-/issues/655): Inconsistent cross-section from Sherpa. Our automated
   test discovered that Sherpa was underestimating the total cross-section. The bug was found and fixed in a subsequent [merge request](https://gitlab.com/sherpa-team/sherpa/-/merge_requests/1086).

- $${\color{red}&cross;}$$ [Issue](https://github.com/key4hep/k4GeneratorsConfig/issues/47): ISR/boost inconsistencies in SHERPA identified by cross section comparisons due to the rejection of events at the
   parton shower/hardronisation stage. A bugfix was applied in SHERPA and propagated to Key4hep.