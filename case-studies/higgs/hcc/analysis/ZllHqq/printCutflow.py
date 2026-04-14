# import common definitions
import os, sys
configdir = os.getenv('FCCANACONFS')
sys.path.append(configdir)
from analysis_config import *

import subprocess
import math
import argparse

# directory containing the cutflow files
basedir += 'analysis-final/hists/'

# populate the cut list
cutList = {}
#for cut in cutList_histOnly:
#    cutList[cut] = cutDict[cut]['label']
for cut in sel:
    cutList[cut] = cutDict[cut]['label']
cutList['finalsel'] = 'All cuts'
cutList['finalsel_e'] = 'l=e'
cutList['finalsel_mu'] = 'l=mu'


def main():

    parser = argparse.ArgumentParser(description='Print the event-level cutflow')
#    parser.add_argument('input_file', type=str, help='Path to the input file')
#    parser.add_argument('--output', '-o', type=str, help='Path to the output file')
    parser.add_argument('--sig', '-s', action='store_true', help='Print significance instead of efficiency')
    parser.add_argument('--debug', '-d', action='store_true', help='Enable debug mode')
    parser.add_argument('--nobkg', action='store_true', help='Do not show the cutflow for the bkg')
    parser.add_argument('--nosplitZHnonhad', action='store_true', help='Split ZH(nonhad) into WW/ZZ/tautau')
    parser.add_argument('--showZHfirstgen', action='store_true', help='Show ZH(uu) and ZH(dd)')
    parser.add_argument('--showZHfv', action='store_true', help='Show ZH(cu/bs/bd/sd)')
    parser.add_argument('--nosplitZll', action='store_true', help='Do not split Z(ll) by flavour')

    args = parser.parse_args()
    
    # debug
    # debug = False
    debug = args.debug

    # show bkg or not
    # showBkg = False
    showBkg = not args.nobkg

    # In the tables, split ZHnonhad into WW/ZZ/tautau or not
    # splitZHother = True
    splitZHother = not args.nosplitZHnonhad

    # show uu and dd decays or not
    # showFirstGen = False
    showFirstGen = args.showZHfirstgen

    # show FV decays or not
    # showFV = True
    showFV = args.showZHfv

    # Z(ll)+jets sample is Pythia8 Z(ll) (False) or WzPy6 ee+mumu (True)
    # splitZllByFlavour = True
    splitZllByFlavour = not args.nosplitZll
    
    # print significance or efficiency
    printSig = args.sig
    if printSig and not showBkg:
        print("\nWARNING: significance without background not meaningful!\n")
    
    processes = {
        'ZHbb'      : ['wzp6_ee_eeH_Hbb_ecm240',     'wzp6_ee_mumuH_Hbb_ecm240'],
        'ZHcc'      : ['wzp6_ee_eeH_Hcc_ecm240',     'wzp6_ee_mumuH_Hcc_ecm240'],
        'ZHgg'      : ['wzp6_ee_eeH_Hgg_ecm240',     'wzp6_ee_mumuH_Hgg_ecm240'],
        'ZHss'      : ['wzp6_ee_eeH_Hss_ecm240',     'wzp6_ee_mumuH_Hss_ecm240'],
    }
    if splitZHother:
        processes.update({
            'ZHWW'    : ['wzp6_ee_eeH_HWW_ecm240',     'wzp6_ee_mumuH_HWW_ecm240'],
            'ZHZZ'    : ['wzp6_ee_eeH_HZZ_ecm240',     'wzp6_ee_mumuH_HZZ_ecm240'],
            'ZHtautau': ['wzp6_ee_eeH_Htautau_ecm240', 'wzp6_ee_mumuH_Htautau_ecm240']})
    else:
        processes.update({
            'ZHnonhad': ['wzp6_ee_eeH_Htautau_ecm240', 'wzp6_ee_mumuH_Htautau_ecm240',
                         'wzp6_ee_eeH_HWW_ecm240',     'wzp6_ee_mumuH_HWW_ecm240',
                         'wzp6_ee_eeH_HZZ_ecm240',     'wzp6_ee_mumuH_HZZ_ecm240']})
    if showFirstGen:
        processes.update({
            'ZHuu'    : ['wzp6_ee_eeH_Huu_ecm240', 'wzp6_ee_mumuH_Huu_ecm240'],
            'ZHdd'    : ['wzp6_ee_eeH_Hdd_ecm240', 'wzp6_ee_mumuH_Hdd_ecm240'],
        })
    if showFV:
        processes.update({
            'ZHcu'    : ['wzp6_ee_eeH_Hcu_ecm240', 'wzp6_ee_mumuH_Hcu_ecm240'],
            'ZHbd'    : ['wzp6_ee_eeH_Hbd_ecm240', 'wzp6_ee_mumuH_Hbd_ecm240'],
            'ZHbs'    : ['wzp6_ee_eeH_Hbs_ecm240', 'wzp6_ee_mumuH_Hbs_ecm240'],
            'ZHsd'    : ['wzp6_ee_eeH_Hsd_ecm240', 'wzp6_ee_mumuH_Hsd_ecm240'],
        })
    if showBkg:
        processes.update({
            'ZZ'        : ['p8_ee_ZZ_ecm240'],
            'WW'        : ['p8_ee_WW_ecm240'],
        })
        if splitZllByFlavour:
            processes.update({'Zll': ['wzp6_ee_ee_Mee_30_150_ecm240', 'wzp6_ee_mumu_ecm240']})
        else:
            processes.update({'Zll': ['p8_ee_Zll_ecm240']})
        processes.update({
            'Zqq'       : ['p8_ee_Zqq_ecm240']
        })

    yieldsInitial = {}
    yieldsFinal = {}
    yieldsFinal_e = {}
    yieldsFinal_mu = {}
    yieldsPrevious = {}
    
    # print title of table
    print('')
    if printSig:
        print('{:25s} '.format('Cut'), end='')
        for proc in processes:
            if 'ZH' in proc:
                print('{:>10s} {:>5s} '.format(proc, ''), end='')
            else:
                print('{:>10s} '.format(proc), end='')
        print('')
        print('{:25s} '.format(''), end='')
        for proc in processes:
            if 'ZH' in proc:
                print('{:>10s} {:>5s} '.format('Yield', 'Sig'), end='')
            else:
                print('{:>10s} '.format('Yield'), end='')
        print('')              
    else:
        print('{:25s} '.format('Cut'), end='')
        for proc in processes:
            print('{:>10s} {:>5s} '.format(proc, ''), end='')
        print('')
        print('{:25s} '.format(''), end='')
        for proc in processes:
            print('{:>10s} {:>5s} '.format('Yield', 'Eff'), end='')
        print('')               

    # loop over the cuts and populate table rows
    for cut in cutList:
        if debug: print(cut)
        yields = {}
        sumYields = 0.0
        for proc in processes:
            yields[proc] = 0.
            for subproc in processes[proc]:
                filename = basedir+'/'+subproc+'_cutflow_weighted.txt'
                if os.path.isfile(filename):
                    cmd = "grep \ " + cut + "\  " + basedir + "/"+subproc+"_cutflow_weighted.txt | awk '{print $5}'"
                    if debug: print(cmd)
                    subproc_return = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
                    if debug: print(subproc_return)
                    yields[proc] += float(subproc_return.split('\n')[-2])
            else:
                yields[proc] += 0.0
            sumYields += yields[proc]
        if (cut=='selNone'): yieldsInitial=dict(yields)
        if (cut=='finalsel'): yieldsFinal=dict(yields)
        #if (cut=='selN_nn'): yieldsFinal=dict(yields)
        #if (cut=='selN_lepveto'): yieldsFinal=dict(yields)
        if (cut=='finalsel_e'): yieldsFinal_e=dict(yields)
        if (cut=='finalsel_mu'): yieldsFinal_mu = dict(yields)
        print('{:25s} '.format(cutList[cut]), end='')
        if printSig:
            sig = {}
            for proc in processes:
                if 'ZH' in proc:
                    sig[proc] = yields[proc]/math.sqrt(sumYields)
                    print('{:10.0f} {:5.0f} '.format(yields[proc],sig[proc]), end='')
                else:
                    print('{:10.0f} '.format(yields[proc]), end='')
            print('')
        else:
            eff = {}        
            if cut!='selNone' and cut!='finalsel_e' and cut!='finalsel_mu':
                for proc in processes:
                    eff[proc] = 100.*yields[proc]/yieldsPrevious[proc]
                    print('{:10.0f} {:5.0f} '.format(yields[proc], eff[proc]), end='')
            else:
                for proc in processes:
                    print('{:10.0f} {:>5s} '.format(yields[proc], '-'), end= '')
            print('')
            yieldsPrevious = dict(yields)  
    print('\n')

    str = '{:25s}'.format('Efficiency (%)')
    for proc in processes: str+='{:>10s}'.format(proc)
    print(str)
    str = '{:25s}'.format('')
    for proc in processes:
        if (yieldsInitial[proc]!=0.):
            str+='{:10.2f}'.format(yieldsFinal[proc]*100./yieldsInitial[proc])
        else:
            str+='{:10s}'.format('')
    print(str)
    print('')


    # Print efficiency separately for ee and mumu channels
    str = '{:25s}'.format('Eff. in e channel (%)')
    for process in processes: str+='{:>10s}'.format(process)
    print(str)
    str = '{:25s}'.format('')
    for proc in processes:
        if (yieldsInitial[proc]!=0.):
            str+='{:10.2f}'.format(yieldsFinal_e[proc]*200./yieldsInitial[proc])
        else:
            str+='{:10s}'.format('')
    print(str)
    print('')

    str = '{:25s}'.format('Eff. in mu channel (%)')
    for process in processes: str+='{:>10s}'.format(process)
    print(str)
    str = '{:25s}'.format('')
    for proc in processes: 
        if (yieldsInitial[proc]!=0.):
            str+='{:10.2f}'.format(yieldsFinal_mu[proc]*200./yieldsInitial[proc])
        else:
            str+='{:10s}'.format('')
    print(str)
    print('')


    # Print efficiency for HWW/ZZ/tautau normalised taking into account hadronic BRs
    # Not correct because some events pass selection even if they are not fully had
    # For instance Z(nunu)Z(qq)
    if splitZHother:
        BRhad = {
            'WW': 0.454,
            'ZZ': 0.489,
            'tautau': 0.42
        }
        # calculated from mumuH_HWW/ZZ/tautau after finalsel
        fracHad = {
            'WW': 0.62539938,
            'ZZ': 0.53700247,
            'tautau': 0.56990203
            }
        str = '{:50s}'.format('Eff. in ZH(other) channels wrt had decays (%)')
        for decay in BRhad:
            str+='{:>10s}'.format(decay)
        print(str)
        str = '{:50s}'.format('')
        for decay in BRhad:
            str+='{:10.2f}'.format(yieldsFinal['ZH'+decay]*100./yieldsInitial['ZH'+decay]*fracHad[decay]/BRhad[decay])  
        print(str)
        print('')


if __name__ == '__main__':
    main()
