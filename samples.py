from dataclasses import dataclass

@dataclass
class Sample:
    name: str
    title: str = ''
    year: int = 2018

samples = [
    Sample('ZMumu_M2300', r'Z$\rightarrow\mu\mu$ (M > 2300 GeV)'),
    Sample('GToHH2B2Tau3000', 'GToHH2B2Tau3000'),
    Sample('BBAToZhToLLTauTau', 'BBAToZhToLLTauTau'),
    Sample('GJet', '$Gamma$+jet'),
    Sample('HINV', r'H$\rightarrow$invisible'),
    Sample('TTTT', 'tttt'),
    Sample('TTTT_UL17', 'tttt'),
    Sample('TTTT_UL16postVFP', 'tttt'),
    Sample('TTTT_UL16preVFP', 'tttt'),
    Sample('TTTT_2022', 'tttt', 2022),
    Sample('DY_2016_preUL_early', 'DY', 2016),
    Sample('DY_2016_preUL', 'DY', 2016),
    Sample('DY_2018_preUL', 'DY', 2016),
    Sample('DY_2016_postvfp', 'DY', 2016),
    Sample('DY_2018', 'DY'),
    Sample('DY_2016_prevfp', 'DY', 2016),
    Sample('DY_2022', 'DY', 2022),
    Sample('TTdilepton', 'tt dilepton'),
    Sample('TTdilep_2022', 'tt dilepton', 2022),
    Sample('TTdilep_2023', 'tt dilepton', 2023),
    Sample('QCD', 'QCD'),
    Sample('SMS-T5qqqqHg', 'SMS T5qqqqHG'),
    Sample('SMS-T2tt-4bd', 'SMS T2tt-4bd'),
    Sample('SMS-TChiZZ', 'SMS TChiZZ'),
    Sample('HHBBTT', r'HH$\rightarrow$bb$\tau\tau$'),
    Sample('TTHmumu', r'ttH (H$\rightarrow\mu\mu$)'),
    Sample('TTHbbdilep', r'ttH (H$\rightarrow$bb) dilepton'),
]

samples_d = {s.name: s for s in samples}