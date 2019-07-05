import json
import sys
import argparse
from ROOT import *
from array import *

"""
Setup argument parser
"""
parser = argparse.ArgumentParser(description="Taking list of files in argument")
parser.add_argument("-pf", "--privatefiles" , help="List of JSON files privately produced.")
parser.add_argument("-rf", "--referencefiles", default="RunBCDEF_SF_ISO_syst.json" , help="JSON produced by MuonPOG. Downloaded from https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonReferenceEffs2017")
args = parser.parse_args()

refSFs = {}
for fpath in args.referencefiles.split(' '):
  f = open(fpath)
  data = eval(json.dumps(json.load(f)).replace("null", "-999"))
  refSFs.update(data)
  f.close()

privSFs = {}
for fpath in args.privatefiles.split(' '):
  f = open(fpath)
  data = eval(json.dumps(json.load(f)).replace("null", "-999"))
  privSFs.update(data)
  f.close()

TextStyle = TStyle("TextStyle","TextStyle")
TextStyle.SetPaintTextFormat("4.3e")
TextStyle.SetOptStat(0)
gROOT.SetStyle("TextStyle")
#ouputfile = open("JsonDiff.txt","w")
fileout= TFile.Open("JsonDiff.root", "RECREATE")
gFile = fileout
gROOT.SetStyle("TextStyle")
gROOT.ForceStyle()


for ID in privSFs.keys():
  if ID not in refSFs.keys():
    print("ID %s not present in ref." %(ID) )
    continue
  XY = []
  for xy in privSFs[ID].keys():
    if xy in refSFs[ID].keys():
      XY.append(xy)
  if len(XY)==0:
    print("No matching XY label")
    continue
  for xy in XY:
    #ouputfile.write("Comparing ID =  %s ; XY = %s \n" %(ID, xy) )
    #ouputfile.write(" %-12s | %-14s |  d_value  |  d_error  |  value_1  |  value_2  |  error_1  |  error_2  \n" %(xy.split('_')[0], xy.split('_')[1]))
    #ouputfile.write("-"*102+"\n")
    SF1 = privSFs[ID][xy]
    SF2 = refSFs[ID][xy]
    XBin = []
    YBin = []
    SF1_value = {}
    SF2_value = {}
    SF1_error = {}
    SF2_error = {}
    for xBin in SF1.keys():
      if xBin not in SF2.keys():
        #print("!!! Bin Error !!! Missing {\"%s\": {\"%s\" : %s }} in ref" %(ID, xy, xBin))
        #ouputfile.write("%-15s| \n" %(xBin))
        continue  
      if "pt" in xBin and "15.0" in xBin:
        continue
      for yBin in SF1[xBin].keys():
        if yBin not in SF2[xBin].keys():
          #print("!!! Bin Error !!! Missing {\"%s\": {\"%s\" : {\"%s\" : %s }}} in ref" %(ID, xy, xBin, yBin) )
          #ouputfile.write("%-15s|%-15s| \n" %(xBin, yBin))
          continue
        if "pt" in yBin and "15.0" in yBin:
          continue
        #print (ID, xy,xBin, yBin)
        x = eval(xBin[xBin.find(":")+1:])
        y = eval(yBin[yBin.find(":")+1:])
        XBin.extend(x)
        YBin.extend(y)
        SF1_value[(x[1],y[1])] = SF1[xBin][yBin]["value"]
        SF2_value[(x[1],y[1])] = SF2[xBin][yBin]["value"]
        SF1_error[(x[1],y[1])] = SF1[xBin][yBin]["error"]
        SF2_error[(x[1],y[1])] = SF2[xBin][yBin]["stat"]+SF2[xBin][yBin]["syst"]         
        #if abs(SF2_value-SF1_value) > 0.0 or abs(SF2_error-SF1_error) >0.00:
        #ouputfile.write(" %-12s | %-14s | %8.7f | %8.7f | %8.7f | %8.7f | %8.7f | %8.7f \n" %(xBin[xBin.find(":")+1:], yBin[yBin.find(":")+1:], abs(SF2_value-SF1_value), abs(SF2_error-SF1_error), SF1_value, SF2_value, SF1_error, SF2_error))
    print sorted(XBin)
    XBin = sorted(list(set(XBin)))
    print XBin
    XBins = array('d',XBin)
    YBin = sorted(list(set(YBin)))
    print YBin
    YBins = array('d',YBin)
    hist_value = TH2F("Diff_"+ID+"_"+xy, "Diff_"+ID+"_"+xy, len(XBin)-1, XBins, len(YBin)-1, YBins)
    hist_value_ratio = TH2F("Ratio_"+ID+"_"+xy, "Ratio_"+ID+"_"+xy, len(XBin)-1, XBins, len(YBin)-1, YBins)
    hist_error = TH2F("Diff_"+ID+"_"+xy+"_unc", "Diff_"+ID+"_"+xy+"_unc", len(XBin)-1, XBins, len(YBin)-1, YBins)
    hist_error_ratio = TH2F("Ratio_"+ID+"_"+xy+"_unc", "Ratio_"+ID+"_"+xy+"_unc", len(XBin)-1, XBins, len(YBin)-1, YBins)
    hist_value_yx = TH2F("Diff_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")], "Diff_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")], len(YBin)-1, YBins, len(XBin)-1, XBins)
    hist_value_ratio_yx = TH2F("Ratio_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")], "Ratio_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")], len(YBin)-1, YBins, len(XBin)-1, XBins)
    hist_error_yx = TH2F("Diff_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")]+"_unc", "Diff_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")]+"_unc", len(YBin)-1, YBins, len(XBin)-1, XBins)
    hist_error_ratio_yx = TH2F("Ratio_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")]+"_unc", "Ratio_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")]+"_unc", len(YBin)-1, YBins, len(XBin)-1, XBins)
    hist1d_value = TH1F("Dist_Diff_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")],"Dist_Diff_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")],100, -0.01, 0.01)
    hist1d_error = TH1F("Dist_Diff_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")]+"_unc","Dist_Diff_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")]+"_unc",100, -0.01, 0.01)
    #hist_value.UseCurrentStyle()
    hist_value.SetStats(0)
    hist_value_ratio.SetStats(0)
    hist_error.SetStats(0)
    hist_error_ratio.SetStats(0)
    hist_value.SetOption("COLZ, TEXT")
    hist_value_ratio.SetOption("COLZ, TEXT")
    hist_error.SetOption("COLZ, TEXT")
    hist_error_ratio.SetOption("COLZ, TEXT")
    hist_value_yx.SetStats(0)
    hist_value_ratio_yx.SetStats(0)
    hist_error_yx.SetStats(0)
    hist_error_ratio_yx.SetStats(0)
    hist_value_yx.SetOption("COLZ, TEXT")
    hist_value_ratio_yx.SetOption("COLZ, TEXT")
    hist_error_yx.SetOption("COLZ, TEXT")
    hist_error_ratio_yx.SetOption("COLZ, TEXT")
    for (ix,iy) in SF1_value.keys():
      #print ix, iy, Double(SF1_value[(ix,iy)]-SF2_value[(ix,iy)])
      hist_value.SetBinContent(XBin.index(ix), YBin.index(iy), Double(SF1_value[(ix,iy)]-SF2_value[(ix,iy)]))
      hist_error.SetBinContent(XBin.index(ix), YBin.index(iy), Double(SF1_error[(ix,iy)]-SF2_error[(ix,iy)]))
      hist_value_ratio.SetBinContent(XBin.index(ix), YBin.index(iy), Double(SF1_value[(ix,iy)]/SF2_value[(ix,iy)]))
      hist_error_ratio.SetBinContent(XBin.index(ix), YBin.index(iy), Double(SF1_error[(ix,iy)]/SF2_error[(ix,iy)]))
      hist_value_yx.SetBinContent(YBin.index(iy), XBin.index(ix), Double(SF1_value[(ix,iy)]-SF2_value[(ix,iy)]))
      hist_error_yx.SetBinContent(YBin.index(iy), XBin.index(ix), Double(SF1_error[(ix,iy)]-SF2_error[(ix,iy)]))
      hist_value_ratio_yx.SetBinContent(YBin.index(iy), XBin.index(ix), Double(SF1_value[(ix,iy)]/SF2_value[(ix,iy)]))
      hist_error_ratio_yx.SetBinContent(YBin.index(iy), XBin.index(ix), Double(SF1_error[(ix,iy)]/SF2_error[(ix,iy)]))
      hist1d_value.Fill(SF1_value[(ix,iy)]-SF2_value[(ix,iy)],1.)
      hist1d_error.Fill(SF1_error[(ix,iy)]-SF2_error[(ix,iy)],1.)
    gDirectory.WriteObject(hist_value,"Diff_"+ID+"_"+xy)
    gDirectory.WriteObject(hist_value_ratio,"Ratio_"+ID+"_"+xy)
    gDirectory.WriteObject(hist_error, "Diff_"+ID+"_"+xy+"_unc")
    gDirectory.WriteObject(hist_error_ratio, "Ratio_"+ID+"_"+xy+"_unc")
    gDirectory.WriteObject(hist_value_yx,"Diff_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")])
    gDirectory.WriteObject(hist_value_ratio_yx,"Ratio_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")])
    gDirectory.WriteObject(hist_error_yx, "Diff_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")]+"_unc")
    gDirectory.WriteObject(hist_error_ratio_yx, "Ratio_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")]+"_unc")
    gDirectory.WriteObject(hist1d_value,"Dist_Diff_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")])
    gDirectory.WriteObject(hist1d_error,"Dist_Diff_"+ID+"_"+xy[xy.find("_")+1:]+"_"+xy[:xy.find("_")]+"_unc")
fileout.Close()
      
#ouputfile.close()
