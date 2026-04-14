import ROOT
#modified so it ca plot relevant infos for each selection
# global parameters
intLumi        = 5.0e+06 #in pb-1
ana_tex        = 'e^{+}e^{-} #rightarrow ZH #rightarrow l^{+}l^{-} + X'
delphesVersion = '3.4.2'
energy         = 240.0
collider       = 'FCC-ee'
BES            = False
inputDir       = '/eos/user/g/gmarchio/fcc-new/ZllHqq/analysis/root/IDEA/finalsel/'
formats        = ['pdf']
yaxis          = ['lin']
stacksig       = ['nostack','stack']
fillsig        = False
scaleSig       = 1.0
outdir         = '/eos/user/g/gmarchio/fcc-new/ZllHqq/analysis/plots/IDEA/'
xleg           = 0.67

#variables = ['N_elec','N_muon','leptons_p','leptons_pt','jets_p','jets_pt','N_jets','N_btag_jets','N_ctag_jets','cos_theta_Z', 'missing_e', 'dilepton_mass', 'hadronic_mass', 'leptonic_recoil_mass', 'leptonic_recoil_mass_2']
#variables = ['leptonic_recoil_mass','leptonic_recoil_mass_2']
variables = ['m_recoil','m_recoil_2']

#variables = ['N_jets', 'N_ctag_jets', 'N_btag_jets', 'leptonic_recoil_mass']
#variables = ['leptonic_recoil_mass']

### Dictionary with the analysis name as a key, and the list of
### selections to be plotted for this analysis. The name of the
### selections should be the same than in the final selection
selections = {}
#selections['ZH']   = ['Nosel','finalsel']
selections['ZH']   = [
    'Nosel',
    'selN_Z',
    'selN_mZ',
    'selN_cos',
    'selN_H',
    'selN_mhad',
    'selN_miss',
    'selN_lepveto',
    'selN_nn',
    ]
#selections['ZH']   = ['Nosel','selN','selN_p','selN_jet','selN_Z','selN_cos','selN_miss']
#selections['ZH']   = ['selN_2c0b','selN_2c0b_final','selN_2c1b','selN_2c1b_final','selN_1c0b_final','selN_1c0b_final', 'selN_1c1b_final', 'selN_1c1b']
#selections['ZH']   = ['Nosel', 'finalsel', 'selN_2b', 'selN_2c0b','selN_2c1b', 'selN_1c1b','selN_1c0b','selN_0c0b0g','selN_0c0b1g','selN_0c0b2g']
#selections['ZH']   = ['selN_0c0b', 'selN_0c0b_final']
#selections['ZH']   = ['selN_glu']
#selections['ZH']   = ['Nosel']
#selections['ZH']   = ['selN_2b']
#selections['ZH']   = ['selN_1c1b_final']

extralabel = {}
extralabel['Nosel'] = 'No selection'
extralabel['selN_Z'] = '1 Z(ll) candidate (2 SFOS l, 25<p_{l}<80GeV)'
extralabel['selN_mZ'] = '81<m_{ll}<101 GeV'
extralabel['selN_cos'] = '81<m_{ll}<101 GeV, |cos#theta_{ll}|<0.8'
extralabel['selN_H'] = '81<m_{ll}<101 GeV, |cos#theta_{ll}|<0.8, 120<m_{recoil}<140 GeV'
extralabel['selN_mhad'] = '81<m_{ll}<101 GeV, |cos#theta_{ll}|<0.8, 120<m_{recoil}<140 GeV, 100<m_{jets}<140 GeV'
extralabel['selN_miss'] = '81<m_{ll}<101 GeV, |cos#theta_{ll}|<0.8, 120<m_{recoil}<140 GeV, 100<m_{jets}<140 GeV, E_{miss}<30 GeV'
extralabel['selN_lepveto'] = 'Z(ll), m_{ll}, |cos#theta_{ll}|, m_{recoil}, m_{jets}, E_{miss}, lep. veto'
extralabel['selN_nn'] = 'Z(ll), m_{ll}, |cos#theta_{ll}|, m_{recoil}, m_{jets}, E_{miss}, lep. veto'
extralabel['selN_2b'] = '2b-tags'
#extralabel['selN_ctagged'] = 'Selec: 2 c-tagged jets and < 2 b-tagged jets'
#extralabel['selN_ctagged_final'] = 'Selec: 2 c-tagged jets and < 2 b-tagged jets, cuts on ETmiss and dijets mass'
extralabel['selN_0c0b'] = '0b, 0c-tags'
extralabel['selN_0c0b0g'] = '0b, 0c, 0g-tags'
extralabel['selN_0c0b1g'] = '0b, 0c, 1g-tags'
extralabel['selN_0c0b2g'] = '0b, 0c, 2g-tags'
extralabel['selN_glu'] = '0b, 0c-tags'
extralabel['selN_2c0b'] = '0b, 2c-tags'
extralabel['selN_2c0b_final'] = '0b, 2c-tags'
extralabel['selN_2c1b'] = '1b, 2c-tags'
extralabel['selN_1c0b'] = '0b, 1c-tags'
#extralabel['selN_2c0b_final'] = 'Selec: 2 c-tagged jets and 0 b-tagged jets, cuts on ETmiss and dijets mass'
extralabel['selN_2c1b_final'] = '1b, 2c-tags, cuts on E_{miss} and dijets mass'
extralabel['selN_1c0b_final'] = '0b, 1c-tags cuts on E_{miss} and dijets mass'
extralabel['selN_0c0b_final'] = '0b, 0c-tags, cuts on E_{miss} and dijets mass'
extralabel['selN_1c1b'] = '1b, 1c-tags'
extralabel['selN_1c1b_final'] = '1b, 1c-tags, cuts on E_{miss} and dijets mass'


colors = {}
colors['ZH'] = ROOT.kBlack
colors['ZHbb'] = ROOT.kRed-2
colors['ZHcc'] = ROOT.kPink+1
colors['ZHgg'] = ROOT.kOrange
colors['ZHss'] = ROOT.kRed+4
colors['WW'] = ROOT.kBlue+1
colors['ZZ'] = ROOT.kGreen+2
colors['ZHnonhad'] = ROOT.kCyan-6
colors['Zgamma'] = ROOT.kViolet

plots = {}

plots['ZH'] = {
    'signal':
    {
#                         'ZHbb':['wzp6_ee_ZllHbb_ecm240'],
#                         'ZHcc':['wzp6_ee_ZllHcc_ecm240'],
#                         'ZHss':['wzp6_ee_ZllHss_ecm240'],
#                         'ZHgg':['wzp6_ee_ZllHgg_ecm240']
        'ZHbb':['wzp6_ee_eeH_Hbb_ecm240', 'wzp6_ee_mumuH_Hbb_ecm240'],
        'ZHgg':['wzp6_ee_eeH_Hgg_ecm240', 'wzp6_ee_mumuH_Hgg_ecm240'],
        'ZHcc':['wzp6_ee_eeH_Hcc_ecm240', 'wzp6_ee_mumuH_Hcc_ecm240'],
        'ZHss':['wzp6_ee_eeH_Hss_ecm240', 'wzp6_ee_mumuH_Hss_ecm240']
    },
    'backgrounds':
    {
        'WW':['p8_ee_WW_ecm240'],
        'ZZ':['p8_ee_ZZ_ecm240'],
        #'Zgamma': ['p8_ee_Zll_ecm240', 'p8_ee_Zqq_ecm240'],                              
        'Zgamma': ['wzp6_ee_mumu_ecm240', 'wzp6_ee_ee_Mee_30_150_ecm240', 'p8_ee_Zqq_ecm240'],
        'ZHnonhad': [
            'wzp6_ee_eeH_Htautau_ecm240', 'wzp6_ee_mumuH_Htautau_ecm240',
            'wzp6_ee_eeH_HWW_ecm240', 'wzp6_ee_mumuH_HWW_ecm240',
            'wzp6_ee_eeH_HZZ_ecm240', 'wzp6_ee_mumuH_HZZ_ecm240'
        ]
    }
}

legend = {}
#legend['ZH'] = 'Total'
legend['ZHbb'] = 'llH(b#bar{b})'
legend['ZHcc'] = 'llH(c#bar{c})'
legend['ZHgg'] = 'llH(gg)'
legend['ZHss'] = 'llH(s#bar{s})'
legend['ZHnonhad'] = 'llH(other)'
legend['ZZ'] = 'ZZ'
legend['WW'] = 'WW'
legend['Zgamma'] = 'Z/#gamma*'
#legend['VV'] = 'VV boson'




