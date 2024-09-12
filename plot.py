import os
import argparse

import uproot
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import mplhep as hep

from samples import Sample, samples_d
from vars import var_d

hep.style.use("CMS")


def make_plot(sample, error_alg='std', var='HT', f_dir='/Users/jan/cernbox/'):
    if sample not in samples_d:
        print(f'Warning, sample {sample} not in sample metadata, will use defaults')
        samples_d[sample] = Sample(sample)

    title = samples_d[sample].title
    year = samples_d[sample].year

    fig = plt.figure(num=1, clear=True)
    ax = fig.add_subplot()
    print('Analysing sample', sample)

    hep.cms.label('', data=False, lumi=None, year=year)

    f = uproot.open(os.path.join(f_dir, f'{sample}.root'))
    t = f['Events']

    # Get the missing ET
    genmet = t['GenMET_pt'].array()
    genmetphi = t['GenMET_phi'].array()

    algos = [('MET', 'PF'), ('PuppiMET', 'PUPPI'), ('DeepMETResolutionTune', 'DeepMET'), ('RawPuppiMET', 'PUPPI raw'), ('RawMET', 'PF raw') ] #, ('DeepMETResolutionTuneDiv2', 'DeepMET/2')]
    if 'preUL' in sample:
        algos = [('MET', 'PF'), ('PuppiMET', 'PUPPI'), ('RawMET', 'PF raw')]

    ht = var_d[var].func(t)
    label = f'{var_d[var].title} [{var_d[var].unit}]'

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
            subres = res[(ht > ht_bins[i]) & (ht < ht_bins[i+1])]
            if len(subres) == 0: continue
            if error_alg == 'std':
                std[i] = np.std(subres)
            elif error_alg == 'central68':
                std[i] = (np.percentile(subres, 84) - np.percentile(subres, 16))/2.
            elif error_alg == 'central95':
                std[i] = (np.percentile(subres, 97.5) - np.percentile(subres, 2.5))/2.
            elif error_alg == 'central99':
                std[i] = (np.percentile(subres, 99.5) - np.percentile(subres, 0.5))/2.
            elif error_alg == 'sqrt_mse':
                std[i] = np.mean(subres**2)**0.5
            else:
                print(f'Warning, no known error algo {error_alg}')

        plt.errorbar(ht_centers, std, xerr=(ht_bins[1:] - ht_bins[:-1]) / 2, fmt='o', label=algo_title)
        if var == 'nvtx' and error_alg == 'std':
            print(f'{algo} 5-10 bin {std[0]:.2f} 35-40 bin {std[6]:.2f} Delta {std[6]-std[0]:.1f}')
    plt.xlabel(f'{label}')
    plt.ylabel('p$_T^{miss}$ resolution [GeV]')
    plt.legend(title=title, alignment='left')
    fig.savefig(f"{sample}_{error_alg}.pdf", format="pdf")
    fig.savefig(f"{sample}_{error_alg}.png", format="png")
    # plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Make MET resolution plots')
    parser.add_argument('--samples', nargs='+', type=str, default=['TTTT'], help='Samples to plot')
    parser.add_argument('--algos', nargs='+', type=str, default=['std'], help='Algorithm to determine resolution (choose from std, central68, central95, central99, sqrt_mse)')
    parser.add_argument('--vars', nargs='+', type=str, default=['HT'], help='x-axis variable (choose from photon, tau, muon, electron, jet, nvtx, HT)')
    parser.add_argument('--dir', type=str, default='/Users/jan/cernbox/', help='Location of input root files')
    args = parser.parse_args()

    for sample in args.samples:
        for algo in args.algos:
            for var in args.vars:
                make_plot(sample, algo, var, args.dir)
