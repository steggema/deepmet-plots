from dataclasses import dataclass
from typing import Callable
import awkward as ak

@dataclass
class Var:
    name: str
    func: Callable
    title: str = ''
    unit: str = ''

vars = [
    Var('photon', lambda t: ak.max(t['Photon_pt'].array(), axis=1), 'Leading photon p$_T$', 'GeV'),
    Var('tau', lambda t: ak.max(t['Tau_pt'].array(), axis=1), 'Leading tau p$_T$', 'GeV'),
    Var('muon', lambda t: ak.max(t['Muon_pt'].array(), axis=1), 'Leading muon p$_T$', 'GeV'),
    Var('electron', lambda t: ak.max(t['Electron_pt'].array(), axis=1), 'Leading electron p$_T$', 'GeV'),
    Var('jet', lambda t: ak.max(t['Jet_pt'].array(), axis=1), 'Leading jet p$_T$', 'GeV'),
    Var('nvtx', lambda t: t['PV_npvs'].array(), '$N_{vertex}$', ''),
    Var('HT', lambda t: ak.sum(t['GenJet_pt'].array(), axis=1), 'H$_T$ (generator jets)', 'GeV'),
]

var_d = {v.name: v for v in vars}
