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
from ROOT import kYellow, kDashed, gPad
from ROOT import TCanvas, THStack, TLegend, TFile, TLine, TH1D
import math
import argparse

splitZHother = True
#splitZHother = False

showFirstGen = True
showFV = True

def plotvars(signalOnly = False):

    from analysis_config import basedir
    # vars: varname, preselection, cutmin, cutmax, axis title, legend position, plot type
    vars = [
        # momentum of all leptons (SelNone)
        ('leptons_p'                          , 'selNone',           9999.,     20., 'p(leptons) [GeV]'            , 0.7, 'lin'),
        # missing mass
        ('mmiss'                              , 'selNone',           9999.,  -9999., 'm_{miss} [GeV]'              , 0.7, 'lin'),
        # number of high momentum leptons
        ('n_selected_leptons'                 , 'selNone',           9999.,     1.0, 'N(high-p leptons)'           , 0.7, 'lin'),
        # energy of leading and subleading jets
        ('jet1_E'                             , 'sel_nolep',           15.,    105., 'E_{j1} [GeV]'                , 0.15, 'lin'),   
        ('jet2_E'                             , 'sel_nolep',           10.,     70., 'E_{j2} [GeV]'                , 0.7, 'lin'),
        # number of constituents of leading and subleading jet
        # ('jet1_nconst'                        , 'sel_jetE',          10.,  -9999., 'N^{const}_{j1}'              , 0.7, 'lin'),
        # ('jet2_nconst'                        , 'sel_jetE',           6.,  -9999., 'N^{const}_{j2}'              , 0.7, 'lin')
        # needless now that we have tau-ID
        ('jet1_nconst'                        , 'sel_jetE',          9999.,  -9999., 'N^{const}_{j1}'              , 0.7, 'lin'),
        ('jet2_nconst'                        , 'sel_jetE',          9999.,  -9999., 'N^{const}_{j2}'              , 0.7, 'lin'),
        # cosine of polar angle of dijet system
        # ('higgs_hadronic_cos_theta'           , 'sel_pmiss',       9999.,     0.9, 'cos(#theta_{jj})'            , 0.15, 'log'),
        # ('higgs_hadronic_cos_theta'           , 'sel_nconst',      9999.,     0.9, 'cos(#theta_{jj})'            , 0.15, 'log'),
        ('higgs_hadronic_cos_theta'           , 'sel_jetE',          9999.,     0.9, 'cos(#theta_{jj})'            , 0.15, 'log'),        
        # are two jets back-to-back in theta?
        ('higgs_hadronic_cosSumThetaJJ'       , 'sel_cosThetaJJ',      0.5,   9999., 'cos(#theta_{j1}+#theta_{j2})', 0.15, 'log'),  
        # are two jets back-to-back in phi?        
        ('higgs_hadronic_cosDeltaPhiJJ_zoom'  , 'sel_cosSumThetaJJ', 9999.,   0.999, 'cos(#phi_{j1}-#phi_{j2})'    , 0.15, 'log'),
        # missing momentum
        ('pmiss'                              , 'sel_cosDPhiJJ',     9999.,  -9999., 'p_{miss} [GeV]'              , 0.15, 'lin'),
        # missing mass
        ('mmiss'                              , 'sel_cosDPhiJJ',       50.,    140., 'm_{miss} [GeV]'              , 0.7, 'lin'),
        # visible mass
        ('mvis'                               , 'sel_cosDPhiJJ',       70.,    150., 'm_{vis} [GeV]'               , 0.7, 'lin'),
        # missing mass, zoomed
        ('higgs_hadronic_recoil_mass_zoom'    , 'sel_cosDPhiJJ',     9999.,  -9999., 'm_{miss} [GeV]'              , 0.7, 'lin'),
        # visible mass, zoomed
        ('mvis_zoom'                          , 'sel_cosDPhiJJ',     9999.,  -9999., 'm_{vis} [GeV]'               , 0.7, 'lin'),
        # tagging score for leading and subleading jets
        ('jet1_isB'                           , 'finalsel',         9999.,  -9999., 'isB(j1)'                     , 0.7, 'log'), 
        ('jet2_isB'                           , 'finalsel',         9999.,  -9999., 'isB(j2)'                     , 0.7, 'log'), 
        ('jet1_isC'                           , 'finalsel',         9999.,  -9999., 'isC(j1)'                     , 0.7, 'log'), 
        ('jet2_isC'                           , 'finalsel',         9999.,  -9999., 'isC(j2)'                     , 0.7, 'log'), 
        ('jet1_isG'                           , 'finalsel',         9999.,  -9999., 'isG(j1)'                     , 0.7, 'log'), 
        ('jet2_isG'                           , 'finalsel',         9999.,  -9999., 'isG(j2)'                     , 0.7, 'log'), 
        ('jet1_isS'                           , 'finalsel',         9999.,  -9999., 'isS(j1)'                     , 0.7, 'log'), 
        ('jet2_isS'                           , 'finalsel',         9999.,  -9999., 'isS(j2)'                     , 0.7, 'log'), 
        ('jet1_isU'                           , 'finalsel',         9999.,  -9999., 'isU(j1)'                     , 0.7, 'log'), 
        ('jet2_isU'                           , 'finalsel',         9999.,  -9999., 'isU(j2)'                     , 0.7, 'log'),
        ('jet1_isD'                           , 'finalsel',         9999.,  -9999., 'isD(j1)'                     , 0.7, 'log'), 
        ('jet2_isD'                           , 'finalsel',         9999.,  -9999., 'isD(j2)'                     , 0.7, 'log'),
        ('jet1_isTAU'                         , 'finalsel',         9999.,  -9999., 'isTAU(j1)'                   , 0.7, 'log'), 
        ('jet2_isTAU'                         , 'finalsel',         9999.,  -9999., 'isTAU(j2)'                   , 0.7, 'log'),
        # dmerge for 3->2 and 4->3 steps
        ('jets_d23'                           , 'finalsel',         9999.,  -9999., 'd_{23}'                      , 0.7, 'lin'),
        ('jets_d34'                           , 'finalsel',         9999.,  -9999., 'd_{34}'                      , 0.7, 'lin'),
#        ('higgs_hadronic_mass'                , 'finalsel',         9999.,  -9999., 'm_{jj} [GeV]'                , 0.7, 'lin'),         
    ]
    
    processes = {
        'ZHbb' : ['wzp6_ee_nunuH_Hbb_ecm365'],
        'ZHcc' : ['wzp6_ee_nunuH_Hcc_ecm365'],
        'ZHss' : ['wzp6_ee_nunuH_Hss_ecm365'],
        'ZHgg' : ['wzp6_ee_nunuH_Hgg_ecm365']
    }
    if splitZHother:
        if showFirstGen:
            processes.update({
                'ZHuu'     : ['wzp6_ee_nunuH_Huu_ecm365'],
                'ZHdd'     : ['wzp6_ee_nunuH_Hdd_ecm365'],
                'ZHtautau' : ['wzp6_ee_nunuH_Htautau_ecm365'],
                'ZHWW'     : ['wzp6_ee_nunuH_HWW_ecm365'],
                'ZHZZ'     : ['wzp6_ee_nunuH_HZZ_ecm365'],
            })
        else:
            processes.update({
                'ZHtautau' : ['wzp6_ee_nunuH_Htautau_ecm365'],
                'ZHWW'     : ['wzp6_ee_nunuH_HWW_ecm365'],
                'ZHZZ'     : ['wzp6_ee_nunuH_HZZ_ecm365'],
            })            
    else:
        if showFirstGen:
            processes.update({
                'ZHother' : [
                    'wzp6_ee_nunuH_Huu_ecm365',
                    'wzp6_ee_nunuH_Hdd_ecm365',
                    'wzp6_ee_nunuH_Htautau_ecm365',
                    'wzp6_ee_nunuH_HWW_ecm365',
                    'wzp6_ee_nunuH_HZZ_ecm365'
                ]
            })
        else:
            processes.update({
                'ZHother' : [
                    'wzp6_ee_nunuH_Htautau_ecm365',
                    'wzp6_ee_nunuH_HWW_ecm365',
                    'wzp6_ee_nunuH_HZZ_ecm365'
                ]
            })
    if showFV:
        processes.update({
            'ZHcu'     : ['wzp6_ee_nunuH_Hcu_ecm365'],
            'ZHbd'     : ['wzp6_ee_nunuH_Hbd_ecm365'],
            'ZHbs'     : ['wzp6_ee_nunuH_Hbs_ecm365'],
            'ZHsd'     : ['wzp6_ee_nunuH_Hsd_ecm365'],
        })
    processes.update({
        'ZZ'      : [ 'p8_ee_ZZ_ecm365' ],
        'WW'      : [ 'p8_ee_WW_ecm365' ],
        'Zqq'     : [ 'p8_ee_Zqq_ecm365' ],
        'nuenueZ' : [ 'wzp6_ee_nuenueZ_ecm365' ],
    })

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
                if (signalOnly and not 'wzp6_ee_nunuH' in proc): continue

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
                #h.SetDirectory(0)

                # set graphic attributes of histo
                #h.SetLineColor(processColors[process])
                #h.SetLineWidth(3)

            # normalize histo to 1
            if hist[process].Integral()!=0.0:
                hist[process].Scale(1./hist[process].Integral(), 'nosw2')

            # add histos to stack and legend
            # do not draw histograms with too few entries otherwise plot will have large spikes
            if hist[process].GetEntries()>300.:
                hs.Add(hist[process])
                leg.AddEntry(hist[process],procLabel,'L')


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
