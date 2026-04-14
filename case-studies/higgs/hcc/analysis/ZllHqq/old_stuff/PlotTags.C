#include <TH1D.h>
#include <TCanvas.h>
#include <TFile.h>
#include <THStack.h>
#include <TLegend.h>
#include <TColor.h>
#include <TLine.h>
#include <TTree.h>
#include <vector>
#include <string>
#include <iostream>


void PlotTags(const std::string & process) {

  const std::vector<std::string> tags = {
    "isB",
    "isC",
    "isG",
    "isS",
    "isQ"
  };

  const std::vector<int> tagColors = {
    kRed-2,
    kPink+1,
    kOrange,
    kCyan-6,
    kBlue+1,
  };


  // Open input file
  TString baseDir = "/eos/user/g/gmarchio/fcc-new/ZllHqq/analysis/root/IDEA";
  std::string fileName = Form("%s/%s.root",baseDir.Data(),process.c_str());
  std::cout << "Opening file " << fileName << std::endl;
  TFile* f = TFile::Open(fileName.c_str(),"READ");
  TTree* T = (TTree*) f->Get("events");

  // Fill and draw histos
  TCanvas c("c", "c", 800, 600);
  THStack hs("hs", process.c_str());
  TLegend leg(0.5,0.6,0.8,0.9,"","brNDC");
  leg.SetBorderSize(0);
  leg.SetFillStyle(0);
  for (unsigned int iTag=0; iTag<tags.size(); iTag++) {
    const std::string tag = tags[iTag];
    TH1D* h = new TH1D(Form("h_%s",tag.c_str()),Form("h_%s",tag.c_str()),50,0.,1.);
    T->Draw(Form("jet_%s>>h_%s",tag.c_str(),tag.c_str()));
    h->SetDirectory(0);
    h->SetLineColor(tagColors[iTag]);
    h->SetLineWidth(3);
    //h->Scale(1./h->Integral(), "nosw2");
    hs.Add(h);
    leg.AddEntry(h,tag.c_str(),"L");
  }
  c.Clear();
  hs.Draw("hist nostack");
  hs.GetXaxis()->SetTitle("isX");
  leg.Draw();

  TString plotpath = baseDir;
  plotpath.ReplaceAll("root","plots");
  plotpath+="/nostack";
  c.Print(Form("%s/%s_tags.pdf",plotpath.Data(),process.c_str()));
  c.SetLogy();
  c.Print(Form("%s/%s_tags_log.pdf",plotpath.Data(),process.c_str()));
}

/*
void PlotTagsAll() {

  const std::vector<std::string> tags = {
    "isB",
    "isC",
    "isG",
    "isS",
    "isQ"
  };
 
  std::vector<string> processes = {
    "wzp6_ee_nunuH_Hbb_ecm240", "wzp6_ee_nunuH_Hcc_ecm240", "wzp6_ee_nunuH_Hss_ecm240", "wzp6_ee_nunuH_Hgg_ecm240", "wzp6_ee_nunuH_Huu_ecm240",
    "p8_ee_ZH_Znunu_Hbb_ecm240", "p8_ee_ZH_Znunu_Hcc_ecm240", "p8_ee_ZH_Znunu_Hss_ecm240", "p8_ee_ZH_Znunu_Hgg_ecm240", "p8_ee_ZH_Znunu_Huu_ecm240"
  };


  TCanvas c("c", "c", 800, 600);
 // Open input file
  TString baseDir = "/eos/user/g/gmarchio/fcc-new/ZllHqq/analysis/root/IDEA";
  std::string fileName = Form("%s/%s.root",baseDir.Data(),process.c_str());
  std::cout << "Opening file " << fileName << std::endl;
  TFile* f = TFile::Open(fileName.c_str(),"READ");
  TTree* T = (TTree*) f->Get("events");

  // Fill and draw histos
  TCanvas c("c", "c", 800, 600);
  THStack hs("hs", process.c_str());
  TLegend leg(0.5,0.6,0.8,0.9,"","brNDC");
  leg.SetBorderSize(0);
  for (unsigned int iTag=0; iTag<tags.size(); iTag++) {

  const std::vector<int> processColors = {
    kRed-2,
    kPink+1,
    kOrange,
    kCyan-6,
    kBlue+1,
    kRed-2,
    kPink+1,
    kOrange,
    kCyan-6,
    kBlue+1,
  };

  const std::vector<int> processStyle = {
    kSolid,
    kSolid,
    kSolid,
    kSolid,
    kSolid,
    kDashed,
    kDashed,
    kDashed,
    kDashed,
    kDashed
  };

  TString baseDir = "/eos/user/g/gmarchio/fcc-new/ZllHqq/analysis/root/IDEA";
  TString plotpath = baseDir;
  plotpath.ReplaceAll("root","plots");
  plotpath+="/nostack";

  //Draw histos
  TCanvas c("c", "c", 800, 600);

  for (unsigned int iVar=0; iVar<vars.size(); iVar++) {
    const std::string var = vars[iVar];
    const std::string sel = selections[iVar];
    std::cout << "Plotting variable " << var << std::endl;
      
    THStack hs(var.c_str(),"");
    TLegend leg(legPos[iVar],0.6,legPos[iVar]+0.2,0.9,"","brNDC");
    leg.SetBorderSize(0);
    leg.SetFillStyle(0);
    
    for (unsigned int iProcess=0; iProcess<processes.size(); iProcess++) {

      const std::string proc = processes[iProcess];
      const std::string procLabel = processLabels[iProcess];
      
      if (var=="jets_p" && procLabel=="WW") continue;

      std::string fileName = Form("%s/%s_%s_histo.root",baseDir.Data(),proc.c_str(),sel.c_str());
      std::cout << "Opening file " << fileName << std::endl;
      TFile* f = TFile::Open(fileName.c_str(),"READ");
      std::cout << "Getting histogram " << var << std::endl;
      TH1D* h = (TH1D*) f->Get(Form("%s",var.c_str()));
      h->SetDirectory(0);
      h->SetLineColor(processColors[iProcess]);
      h->SetLineWidth(3);
      h->Scale(1./h->Integral(), "nosw2");
      hs.Add(h);
      leg.AddEntry(h,procLabel.c_str(),"L");
    }
    c.Clear();
    hs.Draw("hist nostack");
    hs.GetXaxis()->SetTitle(titles[iVar].c_str());
    leg.Draw();
    if (cutMin[iVar]>-9999.) {
      double yMax = c.GetUymax();
      TLine* l1 = new TLine(cutMin[iVar],0.0,cutMin[iVar],yMax*0.8);
      l1->SetLineStyle(kDashed);
      l1->SetLineColor(kBlack);
      l1->SetLineWidth(3.);
      l1->Draw();
    }
    if (cutMax[iVar]<9999.) {
      double yMax = c.GetUymax();
      TLine* l2 = new TLine(cutMax[iVar],0.0,cutMax[iVar],yMax*0.8);
      l2->SetLineStyle(kDashed);
      l2->SetLineColor(kBlack);
      l2->SetLineWidth(3.);
      l2->Draw();
    }
    c.Print(Form("%s/%s_%s.pdf",plotpath.Data(),var.c_str(),sel.c_str()));
  }
}
*/

int go() {
  std::vector<string> processes = {
    //    "wzp6_ee_nunuH_Hbb_ecm240", "wzp6_ee_nunuH_Hcc_ecm240", "wzp6_ee_nunuH_Hss_ecm240", "wzp6_ee_nunuH_Hgg_ecm240", "wzp6_ee_nunuH_Huu_ecm240",
    //    "p8_ee_ZH_Znunu_Hbb_ecm240", "p8_ee_ZH_Znunu_Hcc_ecm240", "p8_ee_ZH_Znunu_Hss_ecm240", "p8_ee_ZH_Znunu_Hgg_ecm240", "p8_ee_ZH_Znunu_Huu_ecm240",
    "wzp6_ee_ZllHbb_ecm240", "wzp6_ee_ZllHcc_ecm240", "wzp6_ee_ZllHss_ecm240", "wzp6_ee_ZllHgg_ecm240", "wzp6_ee_ZllHnonhad_ecm240",
  };
  for (unsigned int i=0; i<processes.size(); i++) {
    std::cout << "process: " << processes[i] << std::endl;
    PlotTags(processes[i]);
  }
  return 0;
}
