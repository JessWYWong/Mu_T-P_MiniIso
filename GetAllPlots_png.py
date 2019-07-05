from ROOT import *
import sys

gROOT.SetBatch(True)
gStyle.SetPaintTextFormat("6.5f")

print 'Running' + str(sys.argv[0])

Directory = str(sys.argv[1])
Filename = str(sys.argv[2])

print 'Get TFile: '+ Directory+Filename
f = TFile.Open(Directory+Filename,"READ")

def FindDir(f, fpaths, Directory,prefix):
  SubDirfpath = []
  ThereIsSubDir = False
  for fpath in fpaths:
    TDir = f.Get(fpath)
    TDirName = TDir.GetName()
    for key in TDir.GetListOfKeys():
      keyName = key.GetName()
      obj = TDir.Get(keyName)
      print keyName
      if "Canvas" in obj.ClassName() or "canvas" in obj.ClassName():
        gStyle.SetPaintTextFormat("5.4f")
        obj.SaveAs(Directory+prefix +"_"+TDirName+"_"+ keyName+".png")
      elif "TH2" in obj.ClassName() or "TH1" in obj.ClassName():
        obj.SetDirectory(0)
        canvas = TCanvas('canvas')
        obj.Draw()
        #obj.SetAxisRange(0.9, 1.1, "Z")
        if "abseta_pt" in keyName:
          canvas.SetLogy()
          obj.SetAxisRange(0.98, 1.08, "Z")
          obj.SetAxisRange(20.0,299.9, "Y")
        elif "pt_abseta" in keyName:
          #canvas.SetLogx()
          obj.SetAxisRange(0.98, 1.0, "Z")
          obj.SetAxisRange(20.0,119.9, "X")
        obj.GetZaxis().SetLabelSize(0.035)
        obj.GetYaxis().SetLabelSize(0.035)
        obj.GetXaxis().SetLabelSize(0.035)
        obj.GetZaxis().SetTitleSize(0.035)
        obj.GetYaxis().SetTitleSize(0.035)
        obj.GetXaxis().SetTitleSize(0.035)
        gStyle.SetPaintTextFormat("5.4f")
        gPad.Modified()
        gPad.Update()
        canvas.SaveAs(Directory+prefix +'_'+TDirName+"_"+ keyName+".png")
        del canvas
      if obj.IsFolder():
        ThereIsSubDir = True
        SubDirfpath.append(fpath+"/"+keyName)
  if ThereIsSubDir:
    return FindDir(f, SubDirfpath, Directory,prefix)
  else:
    return 0

fpath = []
prefix = Filename[11:-5]
if "DATA" in Directory :
  prefix = "Run"+Directory[-2:-1]+"_"+Filename[:3]
if "MC" in Directory :
  prefix = "MC_"+Filename[:3]
for key in f.GetListOfKeys():
  keyName = key.GetName()
  obj = f.Get(keyName)
  if "Canvas" in obj.ClassName() or "canvas" in obj.ClassName():
    #obj.SetDirectory(0)
    gStyle.SetPaintTextFormat("5.4f")
    obj.SaveAs(Directory+prefix+"_"+keyName+".png")
  elif "TH2" in obj.ClassName() or "TH1" in obj.ClassName():
    obj.SetDirectory(0)
    canvas = TCanvas("canvas")
    obj.Draw()
    #obj.SetAxisRange(0.9, 1.1, "Z")
    if "abseta_pt" in keyName:
      canvas.SetLogy()
      obj.SetAxisRange(0.98, 1.08, "Z")
      obj.SetAxisRange(20,299.9, "Y")
    elif "pt_abseta" in keyName:
      #canvas.SetLogx()
      obj.SetAxisRange(0.98, 1.0, "Z")
      obj.SetAxisRange(20.,119.9, "X")
    obj.GetZaxis().SetLabelSize(0.035)
    obj.GetYaxis().SetLabelSize(0.035)
    obj.GetXaxis().SetLabelSize(0.035)
    obj.GetZaxis().SetTitleSize(0.035)
    obj.GetYaxis().SetTitleSize(0.035)
    obj.GetXaxis().SetTitleSize(0.035)
    gStyle.SetPaintTextFormat("5.4f")
    gPad.Modified()
    gPad.Update()
    canvas.SaveAs(Directory+prefix+"_"+keyName+".png")
    del canvas
  if obj.IsFolder():
    fpath.append(keyName)
FindDir(f, fpath, Directory,prefix)

exit(0)


