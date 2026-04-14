# do plots of histograms produced by fccanalysis final

# import common definitions
import os, sys
configdir = os.getenv('FCCANACONFS')
sys.path.append(configdir)
from analysis_config import *
from analysis_plots import *

# import ROOT and other libraries
import ROOT
from ROOT import kRed, kPink, kOrange, kCyan, kBlue, kGreen, kViolet, kBlack
from ROOT import kDashed, gPad
from ROOT import TCanvas, THStack, TLegend, TFile, TLine, TH1D
import math
import argparse

splitZHother = True
#splitZHother = False

showFirstGen = False
showFV = False

def plotvars(signalOnly = False):

    from analysis_config import basedir
    print(basedir)
    
    # vars: varname, preselection, cutmin, cutmax, axis title, legend position, plot type
    # could be replaced with dictionary
    # list of cuts could be taken from config files
    vars = [
        # momentum of all leptons (selNone)
        ('all_leptons_p', 'selNone', 25., 80., 'p(l_{rec}) [GeV]', 0.7, 'lin'),
        
        # type or reconstructed Z candidate (0=none, 1=Zee, 2=Zmm) (selNone)
        ('zed_flavour',   'selNone', 0.5,    -9999., 'Z type', 0.7, 'lin'),
        
        # momentum of Z leptons (sel_Z)
        ('zed_leptons_p', 'sel_Z', 9999., -9999., 'p(l_{Z}) [GeV]', 0.7, 'lin'),
        
        # zed candidate mass (sel_Z)
        ('dilepton_mass_2', 'sel_Z', 81., 101.,   'm_{ll} [GeV]', 0.15, 'lin'),
        
        # zed candidate direction (sel_mZ)
        ('cos_theta_Z', 'sel_mZ', 9999., 0.8,   '|cos#theta_{ll}|', 0.15, 'lin'),
        
        # leptonic recoil mass (sel_cosThetaZ)
        ('m_recoil_2', 'sel_cosThetaZ', 120., 140.,   'm_{recoil} [GeV]', 0.15, 'lin'),
        
        # jets momenta (sel_mrecoil)
        ('all_jets_p', 'sel_mrecoil', 15., 100.,   'p^{j} [GeV]', 0.7, 'lin'),
        ('jets_p', 'sel_mrecoil', 9999., -9999.,   'p^{j} [GeV]', 0.7, 'lin'),
        
        # invariant mass of the jets (sel_mrecoil)
        # ('hadronic_mass_zoom', 'sel_mrecoil', 100., 140.,  'm_{jets} [GeV]', 0.15, 'lin'),
        # no cut
        ('hadronic_mass_zoom', 'sel_mrecoil', 9999., -9999.,  'm_{jets} [GeV]', 0.15, 'lin'),        
        
        # missing energy (selN_mhad)
        # ('missing_e',       'sel_mjj', 9999.,  30.,   'p_{miss} [GeV]', 0.7, 'lin'),
        ('missing_e',       'sel_mrecoil', 9999.,  -9999.,   'p_{miss} [GeV]', 0.7, 'lin'),
        
        # number of additional high-p electrons and muons (selN_miss)
        # ('N_extra_leptons', 'sel_emiss', 0.5, -9999., 'N(l^{high p,extra})', 0.7, 'lin'),
        ('N_extra_leptons', 'sel_mrecoil', 0.5, -9999., 'N(l^{high p,extra})', 0.7, 'lin'),
        
        # dmerge (selN_miss)
        # ('jets_d23',       'sel_emiss', 2.0,  -9999.,  'd_{23}', 0.7, 'log'),
        # ('jets_d34',       'sel_emiss', 1.5,  -9999.,  'd_{34}', 0.7, 'log'),
        # ('jets_d45',       'sel_emiss', 1.0,  -9999.,  'd_{45}', 0.7, 'log'),
        ('jets_d23',       'sel_leptonveto', 0.0,  -9999.,  'd_{23}', 0.7, 'log'),
        ('jets_d34',       'sel_leptonveto', 0.5,  -9999.,  'd_{34}', 0.7, 'log'),
        ('jets_d45',       'sel_leptonveto', 0.0,  -9999.,  'd_{45}', 0.7, 'log'),
        
        # tagger score
        # 'trainNN'
        ('jet1_isB',       'finalsel', 9999., -9999.,  'isB(j1)', 0.7, 'log'),
        ('jet2_isB',       'finalsel', 9999., -9999.,  'isB(j2)', 0.7, 'log'),
        ('jet1_isC',       'finalsel', 9999., -9999.,  'isC(j1)', 0.7, 'log'),
        ('jet2_isC',       'finalsel', 9999., -9999.,  'isC(j2)', 0.7, 'log'),
        ('jet1_isG',       'finalsel', 9999., -9999.,  'isG(j1)', 0.7, 'log'),
        ('jet2_isG',       'finalsel', 9999., -9999.,  'isG(j2)', 0.7, 'log'),
        ('jet1_isS',       'finalsel', 9999., -9999.,  'isS(j1)', 0.7, 'log'),
        ('jet2_isS',       'finalsel', 9999., -9999.,  'isS(j2)', 0.7, 'log'),
        ('jet1_isU',       'finalsel', 9999., -9999.,  'isU(j1)', 0.7, 'log'),
        ('jet2_isU',       'finalsel', 9999., -9999.,  'isU(j2)', 0.7, 'log'),
        ('jet1_isD',       'finalsel', 9999., -9999.,  'isD(j1)', 0.7, 'log'),
        ('jet2_isD',       'finalsel', 9999., -9999.,  'isD(j2)', 0.7, 'log'),
        ('jet1_isTAU',     'finalsel', 9999., -9999.,  'isTAU(j1)', 0.7, 'log'),
        ('jet2_isTAU',     'finalsel', 9999., -9999.,  'isTAU(j2)', 0.7, 'log'),

         # the other 4 vars used in the NN
        ('hadronic_mass',  'finalsel', 9999., -9999.,  'm_{jets} [GeV]', 0.7, 'lin'),
        ('missing_e',      'finalsel', 9999., -9999.,  'p_{miss} [GeV]', 0.7, 'lin'),

        ('jets_d23',       'finalsel', 9999., -9999.,  'd_{23}', 0.7, 'lin'),
        ('jets_d34',       'finalsel', 9999., -9999.,  'd_{34}', 0.7, 'lin'),

        # subleading jet energy
        ('jet2_E',         'finalsel', 9999., -9999.,  'E_{j2} [GeV]', 0.7, 'lin'),
    ]

    # list of processes to draw (and how to group them)
    processes = {
        'ZHbb' : ['wzp6_ee_eeH_Hbb_ecm365',    'wzp6_ee_mumuH_Hbb_ecm365'],
        'ZHcc' : ['wzp6_ee_eeH_Hcc_ecm365',    'wzp6_ee_mumuH_Hcc_ecm365'],
        'ZHgg' : ['wzp6_ee_eeH_Hss_ecm365',    'wzp6_ee_mumuH_Hss_ecm365'],
        'ZHgg' : ['wzp6_ee_eeH_Hgg_ecm365',    'wzp6_ee_mumuH_Hgg_ecm365'],
    }
    if splitZHother:
        if showFirstGen:
            processes.update({
                'ZHuu'     : ['wzp6_ee_eeH_Huu_ecm365', 'wzp6_ee_mumuH_Huu_ecm365'],
                'ZHdd'     : ['wzp6_ee_eeH_Hdd_ecm365', 'wzp6_ee_mumuH_Hdd_ecm365'],
                'ZHtautau' : ['wzp6_ee_eeH_Htautau_ecm365','wzp6_ee_mumuH_Htautau_ecm365'],
                'ZHWW'     : ['wzp6_ee_eeH_HWW_ecm365',    'wzp6_ee_mumuH_HWW_ecm365'],
                'ZHZZ'     : ['wzp6_ee_eeH_HZZ_ecm365',    'wzp6_ee_mumuH_HZZ_ecm365']
            })
        else:
            processes.update({
                'ZHtautau' : ['wzp6_ee_eeH_Htautau_ecm365','wzp6_ee_mumuH_Htautau_ecm365'],
                'ZHWW'     : ['wzp6_ee_eeH_HWW_ecm365',    'wzp6_ee_mumuH_HWW_ecm365'],
                'ZHZZ'     : ['wzp6_ee_eeH_HZZ_ecm365',    'wzp6_ee_mumuH_HZZ_ecm365']
        })
    else:
        if showFirstGen:
            processes.update({
                'ZHother' : [
                    'wzp6_ee_eeH_Huu_ecm365', 'wzp6_ee_mumuH_Huu_ecm365',
                    'wzp6_ee_eeH_Hdd_ecm365', 'wzp6_ee_mumuH_Hdd_ecm365',
                    'wzp6_ee_eeH_Htautau_ecm365','wzp6_ee_mumuH_Htautau_ecm365',
                    'wzp6_ee_eeH_HWW_ecm365',    'wzp6_ee_mumuH_HWW_ecm365',
                    'wzp6_ee_eeH_HZZ_ecm365',    'wzp6_ee_mumuH_HZZ_ecm365'
                ]
            })
        else:
            processes.update({
                'ZHother' : [
                    'wzp6_ee_eeH_Htautau_ecm365','wzp6_ee_mumuH_Htautau_ecm365',
                    'wzp6_ee_eeH_HWW_ecm365',    'wzp6_ee_mumuH_HWW_ecm365',
                    'wzp6_ee_eeH_HZZ_ecm365',    'wzp6_ee_mumuH_HZZ_ecm365'
                ]
            })
    if showFV:
        processes.update({
            'ZHcu'     : ['wzp6_ee_eeH_Hcu_ecm365', 'wzp6_ee_mumuH_Hcu_ecm365'],
            'ZHbd'     : ['wzp6_ee_eeH_Hbd_ecm365', 'wzp6_ee_mumuH_Hbd_ecm365'],
            'ZHbs'     : ['wzp6_ee_eeH_Hbs_ecm365', 'wzp6_ee_mumuH_Hbs_ecm365'],
            'ZHsd'     : ['wzp6_ee_eeH_Hsd_ecm365', 'wzp6_ee_mumuH_Hsd_ecm365'],
        })
    processes.update({
        'ZZ'    : ['p8_ee_ZZ_ecm365'],
        'WW'    : ['p8_ee_WW_ecm365'],
        'ttbar' : ['p8_ee_tt_ecm365'],
        'Zqq'   : ['p8_ee_Zqq_ecm365'],
        'Zll'   : ['wzp6_ee_ee_Mee_30_150_ecm365', 'wzp6_ee_mumu_ecm365']
    })

    # directory containing the cutflow files
    basedir += 'analysis-final/hists/'
    plotpath = basedir.replace('hists','plots') + '/nostack'
    if not os.path.isdir(plotpath):
        os.makedirs(plotpath)

    #Draw histos
    c = TCanvas('c', 'c', 800, 600)

    # loop over variables
    for iVar in range(len(vars)):
        var, sel, cutMin, cutMax, title, legPos, plotStyle = vars[iVar]
        print('Plotting variable ', var)
        
        # initialize stack and legend
        hs = THStack(var, '')
        leg = TLegend(legPos, 0.6, legPos+0.18, 0.88, '', 'brNDC')
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        
        # loop over the processes
        hist = {}
        for process, sampleList in processes.items():

            procLabel = processLabels[process]
            hist[process] = TH1D()
            first = True
            for proc in sampleList:
                if (signalOnly and not 'wzp6_ee_eeH' in proc and not 'wzp6_ee_mumuH' in proc): continue

                # open file with histos
                fileName = '{:s}/{:s}_{:s}_histo.root'.format(basedir,proc,sel)
                print('Opening file ', fileName)
                f = TFile.Open(fileName, 'READ')

                # read histo
                print('Getting histogram ', var)
                h = f.Get(var)
                if first:
                    hist[process] = h.Clone(procLabel)
                    first = False
                    hist[process].SetLineColor(colors[process])
                    hist[process].SetLineWidth(3)
                    hist[process].SetDirectory(0)                  
                else:
                    hist[process].Add(h)

            # normalize histo to 1
            if hist[process].Integral()!=0.0:
                hist[process].Scale(1./hist[process].Integral(), 'nosw2')

            # add histos to stack and legend
            # do not draw histograms with too few entries otherwise plot will have large spikes
            if hist[process].GetEntries()>300.:
                hs.Add(hist[process])
                leg.AddEntry(hist[process], procLabel, 'L')


        # draw the histo stack and legend
        c.Clear()
        hs.Draw('hist nostack')    
        hs.GetXaxis().SetTitle(title)
        leg.Draw()
        c.SetLogy(plotStyle=='log')
        gPad.Update()

        # draw the cuts
        print('Drawing cuts')
        yMax = c.GetUymax()
        yMin = c.GetUymin()
        if plotStyle=='log':
            yMax = math.pow(10,yMax)
            yMin = math.pow(10,yMin)
        if cutMin>-9999. :
            l1 = TLine(cutMin, yMin, cutMin, yMax)
            l1.SetLineStyle(kDashed)
            l1.SetLineColor(kBlack)
            l1.SetLineWidth(3)
            l1.Draw()
        if cutMax<9999. :
            l2 = TLine(cutMax, yMin, cutMax, yMax)
            l2.SetLineStyle(kDashed)
            l2.SetLineColor(kBlack)
            l2.SetLineWidth(3)
            l2.Draw()

        if signalOnly:
            c.Print('{:s}/{:s}_{:s}_signal.pdf'.format(plotpath,var,sel))
        else:
            c.Print('{:s}/{:s}_{:s}_sigbkg.pdf'.format(plotpath,var,sel))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--signalOnly", action="store_true")  # default is false
    args = parser.parse_args()
    plotvars(args.signalOnly)
