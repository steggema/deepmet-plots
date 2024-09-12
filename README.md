# DeepMET simulation performance plots

Make plots of missing ET resolution directly from official CMS NanoAOD:
- Input: CMS NanoAOD input files
- Output: DeepMET performance plots (resolution as function of some variable), comparing with Puppi and PF MET
- Requirements (install via conda or pip):
  * python3 (any python > 3.7 should work)
  * uproot 
  * matplotlib
  * mplhep (for plot style)
  * scipy, numpy, awkward: should come with the former three]

## Example

`python plot.py --samples DY_2018 TTTT --algos std central68 --dir /Users/jan/cernbox`

where
* samples: list of ROOT files to analyse (stripped off the `.root` extension); label is extracted from `samples.py`
* algos: list of algorithms with which to conclude the resolution, where
  * std: standard deviation
  * central[68/95/99]: central 68, 95, or 99% quantile
  * sqrt_mse: root mean square
* dir: the NanoAOD ROOT files need to reside in the given directory