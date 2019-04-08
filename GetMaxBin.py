import argparse
import sys
import os

from ROOT import *
gROOT.SetBatch(True)

files_2018_RunA2D_DY = "/eos/cms/store/group/phys_muon/TagAndProbe/Run2018/102X/TnPTreeZ_17Sep2018_SingleMuon_Run2018Av2_GoldenJSON.root /eos/cms/store/group/phys_muon/TagAndProbe/Run2018/102X/TnPTreeZ_17Sep2018_SingleMuon_Run2018Bv1_GoldenJSON.root /eos/cms/store/group/phys_muon/TagAndProbe/Run2018/102X/TnPTreeZ_17Sep2018_SingleMuon_Run2018Cv1_GoldenJSON.root /eos/cms/store/group/phys_muon/TagAndProbe/Run2018/102X/TnPTreeZ_SingleMuon_Run2018Dv2_GoldenJSON.root /eos/cms/store/group/phys_muon/TagAndProbe/Run2018/102X/TnPTreeZ_102XAutumn18_DYJetsToLL_M50_MadgraphMLM.root"

"""
Setup argument parser
"""
parser = argparse.ArgumentParser(description="Taking list of files in argument")
parser.add_argument("-f", "--files", default=files_2018_RunA2D_DY , help="List of input files (full file path).")
parser.add_argument("-t", "--treename", default="fitter_tree", help="Tree name in root files.")
parser.add_argument("-b", "--branch", default="tag_nVertices", help="Branch of which upper edge is desired.")
args = parser.parse_args()

"""
initialize counter for largest 
"""
max_n = 0

"""
Loop over files
"""
for fpath in args.files.split(' '):
  f = TFile.Open(fpath)
  t = f.tpTree.Get(args.treename)
  h = TH1F()
  t.Draw(args.branch)
  h = c1.GetPrimitive("htemp") #default histogram name when draw from tree directly
  h.SetDirectory(0) #detach the histogram from root file so one can close file and manipulate the histogram freely
  f.Close()
  max_h = h.GetXaxis().GetBinUpEdge(h.FindLastBinAbove()) #upper edge of the histogram bins
  if max_h > max_n:
    max_n = max_h #store the maximum value in counter
print max_n 

