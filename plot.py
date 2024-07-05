import uproot
import numpy as np
import awkward as ak
from scipy import stats
import matplotlib.pyplot as plt
import mplhep as hep

hep.style.use("CMS")


def make_plot(sample, error_alg='std', tag=''):
    sample, title, var = sample
    fig = plt.figure(num=1, clear=True)
    ax = fig.add_subplot()
    print('Analysing sample', sample)

    year = 2018
    if '2022' in sample:
        year = 2022
    elif '2023' in sample:  
        year = 2023
    elif '2016' in sample:  
        year = 2016

    hep.cms.label('', data=False, lumi=None, year=year)

    f = uproot.open(f'/Users/jan/cernbox/{sample}.root')
    t = f['Events']

    # Make a plot of the missing ET resolution


    # Get the missing ET
    genmet = t['GenMET_pt'].array()
    genmetphi = t['GenMET_phi'].array()


    algos = [('MET', 'PF'), ('PuppiMET', 'PUPPI'), ('DeepMETResolutionTune', 'DeepMET'), ('RawPuppiMET', 'PUPPI raw'), ('RawMET', 'PF raw') ] #, ('DeepMETResolutionTuneDiv2', 'DeepMET/2')]
    if 'preUL' in sample:
        algos = [('MET', 'PF'), ('PuppiMET', 'PUPPI'), ('RawMET', 'PF raw')]

    # Make a plot of the standard deviation of the MET resolution as a function of the LHE HT
    label = 'LHE HT'

    if var == 'photon':
        ht = ak.max(t['Photon_pt'].array(), axis=1)
        ht = ak.fill_none(ht, 0)
        label = 'Leading photon p$_T$ [GeV]'
    elif var == 'tau':
        ht = ak.max(t['Tau_pt'].array(), axis=1)
        ht = ak.fill_none(ht, 0)
        label = 'Leading tau p$_T$ [GeV]'
    elif var == 'muon':
        ht = ak.max(t['Muon_pt'].array(), axis=1)
        ht = ak.fill_none(ht, 0)
        label = 'Leading muon p$_T$ [GeV]'
    elif var == 'electron':
        ht = ak.max(t['Electron_pt'].array(), axis=1)
        ht = ak.fill_none(ht, 0)
        label = 'Leading electron p$_T$ [GeV]'
    elif var == 'jet':
        ht = ak.max(t['Jet_pt'].array(), axis=1)
        ht = ak.fill_none(ht, 0)
        label = 'Leading jet p$_T$ [GeV]'
    elif var == 'nvtx':
        ht = t['PV_npvs'].array()
        label = '$N_{vertex}$'
    else: # var == 'HT':
        ht = ak.sum(t['GenJet_pt'].array(), axis=1)
        label = 'H$_T$ (generator jets) [GeV]'

    if var != 'nvtx':
        ht_bins = stats.mstats.mquantiles(ht, np.linspace(0, 1, 15))
        ht_bins = ht_bins[:-1]
        ht_centers = (ht_bins[1:] + ht_bins[:-1]) / 2
    else:
        ht_bins = np.arange(5, 55, 5)
        ht_centers = (ht_bins[1:] + ht_bins[:-1]) / 2

    for algo, algo_title in algos:
        if algo == 'DeepMETResolutionTuneDiv2':
            algo = 'DeepMETResolutionTune'
            met = t[algo+'_pt'].array() / 2
        else:
            met = t[algo+'_pt'].array()
            metphi = t[algo+'_phi'].array()
        
        if not 'DY' in sample:
            res = (met - genmet)
        else:
            # print('DY sample, using met px instead of met')
            res = met*np.cos(metphi) - genmet*np.cos(genmetphi)

        if algo == 'DeepMETResolutionTune':
            ht = ht[np.isnan(res)==0]
            res = res[np.isnan(res)==0]

        std = np.zeros(len(ht_centers))

        for i in range(len(ht_centers)):
            if error_alg == 'std':
                std[i] = np.std(res[(ht > ht_bins[i]) & (ht < ht_bins[i+1])])
            elif error_alg == 'central68':
                subres = res[(ht > ht_bins[i]) & (ht < ht_bins[i+1])]
                if len(subres) == 0: continue
                std[i] = (np.percentile(subres, 84) - np.percentile(subres, 16))/2.
            elif error_alg == 'central95':
                subres = res[(ht > ht_bins[i]) & (ht < ht_bins[i+1])]
                if len(subres) == 0: continue
                std[i] = (np.percentile(subres, 97.5) - np.percentile(subres, 2.5))/2.
            elif error_alg == 'central99':
                subres = res[(ht > ht_bins[i]) & (ht < ht_bins[i+1])]
                if len(subres) == 0: continue
                std[i] = (np.percentile(subres, 99.5) - np.percentile(subres, 0.5))/2.
            elif error_alg == 'sqrt_mse':
                subres = res[(ht > ht_bins[i]) & (ht < ht_bins[i+1])]
                if len(subres) == 0: continue
                std[i] = np.mean(subres**2)**0.5
            else:
                print(f'Warning, no known error algo {error_alg}')
        plt.errorbar(ht_centers, std, xerr=(ht_bins[1:] - ht_bins[:-1]) / 2, fmt='o', label=algo_title)
        if var == 'nvtx' and error_alg == 'std':
            print(f'{algo} 5-10 bin {std[0]:.2f} 35-40 bin {std[6]:.2f} Delta {std[6]-std[0]:.1f}')
    plt.xlabel(f'{label}')
    plt.ylabel('p$_T^{miss}$ resolution [GeV]')
    plt.legend(title=title, alignment='left')
    fig.savefig(f"{sample}{tag}.pdf", format="pdf")
    fig.savefig(f"{sample}{tag}.png", format="png")
    # plt.show()

samples = [
    # ('ZMumu_M2300', r'Z$\rightarrow\mu\mu$ (M > 2300 GeV)', 'muon'),
    
    # ('GToHH2B2Tau3000', 'GToHH2B2Tau3000', 'electron'),
    # ('BBAToZhToLLTauTau', 'BBAToZhToLLTauTau', 'tau'),
    # ('GJet', '$Gamma$+jet', 'photon'),
    # ('HINV', r'H$\rightarrow$invisible', 'nvtx'),
    # ('TTTT', 'tttt', 'HT'),
    # ('TTTT_UL17', 'tttt', 'HT'),
    # ('TTTT_UL16postVFP', 'tttt', 'HT'),
    # ('TTTT_UL16preVFP', 'tttt', 'HT'),
    # ('TTTT_2022', 'tttt', 'HT'),
    ('DY_2016_preUL_early', 'DY', 'nvtx'),
    ('DY_2016_preUL', 'DY', 'nvtx'),
    ('DY_2018_preUL', 'DY', 'nvtx'),
    ('DY_2016_postvfp', 'DY', 'nvtx'),
    ('DY_2018', 'DY', 'nvtx'),
    ('DY_2016_prevfp', 'DY', 'nvtx'),
    ('DY_2022', 'DY', 'nvtx'),
    # ('TTdilepton', 'tt dilepton', 'nvtx'),
    # ('TTdilep_2022', 'tt dilepton', 'nvtx'),
    # ('TTdilep_2023', 'tt dilepton', 'nvtx'),
    # ('QCD', 'QCD', 'jet'),
    # ('SMS-T5qqqqHg', 'SMS T5qqqqHG', 'photon'),
    # ('SMS-T2tt-4bd', 'SMS T2tt-4bd', 'HT'),
    # ('SMS-TChiZZ', 'SMS TChiZZ', 'HT'),
    # ('HHBBTT', r'HH$\rightarrow$bb$\tau\tau$', 'HT'),
    # ('TTHmumu', r'ttH (H$\rightarrow\mu\mu$)', 'HT'),
    # ('TTHbbdilep', r'ttH (H$\rightarrow$bb) dilepton', 'HT')
]
if __name__ == "__main__":
    for sample in samples:
        make_plot(sample)
        # make_plot(sample, 'central68', '_central68')
        # make_plot(sample, 'central95', '_central95')
        # make_plot(sample, 'central99', '_central99')
        # make_plot(sample, 'sqrt_mse', '_mse')
        

