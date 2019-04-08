from ROOT import *
from array import *
import math
gStyle.SetPaintTextFormat("1.3f")

################# needs to be updated #####################
era = ["A", "B", "C", "D"]
Lumi = [14.00,7.10,6.94,31.93]
bin_pt = array('d',[2.0, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.5, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 120.0, 200.0, 300.0, 500.0, 700.0, 1200.0])
bin_abseta = array('d',[0., 0.9, 1.2, 2.1, 2.4])
FolderName = "Tight_PtEtaBins"
Prefix = "EfficienciesAndSF_Run"
Suffix = "_TightCutPFiso_NUM_tightPFiso_DEN_TightIDandIPCut_PAR_pt_eta.root"
###########################################################

nbin_pt = len(bin_pt)-1
nbin_abseta = len(bin_abseta)-1
scale = {}
abseta_pt_DATA = {}
pt_abseta_DATA = {}

for ind,i in enumerate(era):
  scale[i] = Lumi[ind]/sum(Lumi)
  file= TFile.Open(Prefix+i+Suffix)
  abseta_pt_DATA[i] = file.Get(FolderName).Get("efficienciesDATA").Get("abseta_pt_DATA")
  abseta_pt_DATA[i].SetDirectory(0)
  pt_abseta_DATA[i] = file.Get(FolderName).Get("efficienciesDATA").Get("pt_abseta_DATA")
  pt_abseta_DATA[i].SetDirectory(0)
  file.Close()

file= TFile.Open(Prefix+era[0]+Suffix)
h1_MC = file.Get(FolderName).Get("efficienciesMC").Get("abseta_pt_MC")
h1_MC.SetDirectory(0)
h2_MC = file.Get(FolderName).Get("efficienciesMC").Get("pt_abseta_MC")
h2_MC.SetDirectory(0)
file.Close()

h_abseta_pt = TH2F("abseta_pt_DATA_scaled", "abseta_pt_DATA_scaled", nbin_abseta, bin_abseta, nbin_pt, bin_pt)
h_pt_abseta = TH2F("pt_abseta_DATA_scaled", "pt_abseta_DATA_scaled", nbin_pt, bin_pt, nbin_abseta, bin_abseta)
h_abseta_pt_totWeight = TH2F("abseta_pt_DATA_Weight", "abseta_pt_DATA_Weight", nbin_abseta, bin_abseta, nbin_pt, bin_pt)
h_pt_abseta_totWeight = TH2F("pt_abseta_DATA_Weight", "pt_abseta_DATA_Weight", nbin_pt, bin_pt, nbin_abseta, bin_abseta)

for ind,i in enumerate(era):
  h1 = abseta_pt_DATA[i].Clone()
  h2 = pt_abseta_DATA[i].Clone()
  if ind == 0 :
    print 'first clone'
    h1_weight = h1.Clone()
    h1_weight.Divide(h1_weight)
    h1_weight.Scale(Lumi[ind])
    h1.Scale(Lumi[ind])
    h_abseta_pt_totWeight = h1_weight.Clone()
    h_abseta_pt = h1.Clone()
    #
    h2_weight = h2.Clone()
    h2_weight.Divide(h2_weight)
    h2_weight.Scale(Lumi[ind])
    h2.Scale(Lumi[ind])
    h_pt_abseta_totWeight = h2_weight.Clone()
    h_pt_abseta = h2.Clone()
  else:
    print 'adding with weight'
    h1_weight = h1.Clone()
    h1_weight.Divide(h1_weight)
    h1_weight.Scale(Lumi[ind])
    h_abseta_pt_totWeight.Add(h1_weight)
    h_abseta_pt.Add(h1, Lumi[ind])
    #
    h2_weight = h2.Clone()
    h2_weight.Divide(h2_weight)
    h2_weight.Scale(Lumi[ind])
    h_pt_abseta_totWeight.Add(h2_weight)
    h_pt_abseta.Add(h2, Lumi[ind])

h_abseta_pt.Divide(h_abseta_pt_totWeight)
h_pt_abseta.Divide(h_pt_abseta_totWeight)

ratio_abseta_pt = TH2F("ratio_abseta_pt", "ratio_abseta_pt", nbin_abseta, bin_abseta, nbin_pt, bin_pt)
ratio_abseta_pt = h_abseta_pt.Clone()
ratio_abseta_pt.Divide(ratio_abseta_pt, h1_MC)

ratio_pt_abseta = TH2F("ratio_pt_abseta", "ratio_pt_abseta", nbin_pt, bin_pt, nbin_abseta, bin_abseta)
ratio_pt_abseta = h_pt_abseta.Clone()
ratio_pt_abseta.Divide(ratio_pt_abseta, h2_MC)

file_out = TFile("ScaledRuns_EfficienciesAndSF.root", "RECREATE")
file_out.mkdir(FolderName)
file_out.cd(FolderName)
ratio_abseta_pt.Write("abseta_pt_ratio")
ratio_pt_abseta.Write("pt_abseta_ratio")

gDirectory.mkdir("efficienciesDATA")
gDirectory.mkdir("efficienciesMC")
gDirectory.mkdir("efficienciesRUN")

gDirectory.cd("efficienciesMC")
h1_MC.Write("abseta_pt_MC")
h2_MC.Write("pt_abseta_MC")

gDirectory.cd("../efficienciesDATA")
h_abseta_pt.Write("abseta_pt_DATA_scaled")
h_pt_abseta.Write("pt_abseta_DATA_scaled")
gDirectory.cd("../efficienciesRUN")
for ind,i in enumerate(era):
  name1 = "abseta_pt_DATA_Run"+i
  h1 = abseta_pt_DATA[i]
  h1.Write(name1)
  name2 = "pt_abseta_DATA_Run"+i
  h2 = pt_abseta_DATA[i]
  h2.Write(name2)

gDirectory.cd("../../")

file_out.Close()
