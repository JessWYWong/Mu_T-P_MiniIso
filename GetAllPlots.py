from ROOT import *
import sys

gROOT.SetBatch(True)
gStyle.SetPaintTextFormat("1.3f")

print 'Running' + str(sys.argv[0])

Directory = str(sys.argv[1])
Filename = str(sys.argv[2])

print 'Get TFile: '+ Directory+Filename
f = TFile.Open(Directory+Filename)

def FindDir(f, fpaths, Directory):
  SubDirfpath = []
  ThereIsSubDir = False
  for fpath in fpaths:
    TDir = f.Get(fpath)
    prefix = TDir.GetName()
    for key in TDir.GetListOfKeys():
      keyName = key.GetName()
      obj = TDir.Get(keyName)
      print keyName
      if "Canvas" in obj.ClassName() or "canvas" in obj.ClassName():
        obj.SaveAs(Directory+prefix +"_"+ keyName+".pdf")
      elif "TH2" in obj.ClassName() or "TH1" in obj.ClassName():
        canvas = TCanvas('canvas')
        obj.Draw()
        p = obj.GetListOfFunctions().FindObject("palette")
        p.SetX1NDC(0.905)
        p.SetX2NDC(0.95)
        if "abseta_pt" in keyName:
          canvas.SetLogy()
          obj.SetAxisRange(20,1200, "Y")
        elif "pt_abseta" in keyName:
          canvas.SetLogx()
          obj.SetAxisRange(20,1200, "X")
        gStyle.SetPaintTextFormat("1.3f")
        canvas.Modified()
        canvas.Update()
        canvas.SaveAs(Directory+prefix +'_'+ keyName+'.pdf')
        del canvas
      if obj.IsFolder():
        ThereIsSubDir = True
        SubDirfpath.append(fpath+"/"+keyName)
  if ThereIsSubDir:
    return FindDir(f, SubDirfpath, Directory)
  else:
    return 0

fpath = []
prefix = Filename[:-5]
for key in f.GetListOfKeys():
  keyName = key.GetName()
  obj = f.Get(keyName)
  if "Canvas" in obj.ClassName() or "canvas" in obj.ClassName():
    obj.SaveAs(Directory+prefix+keyName+".pdf")
  elif "TH2" in obj.ClassName() or "TH1" in obj.ClassName():
    canvas = TCanvas("canvas")
    obj.Draw()
    p = obj.GetListOfFunctions().FindObject("palette")
    p.SetX1NDC(0.905)
    p.SetX2NDC(0.95)
    if "abseta_pt" in keyName:
      canvas.SetLogy()
      obj.SetAxisRange(20,1200, "Y")
    elif "pt_abseta" in keyName:
      canvas.SetLogx()
      obj.SetAxisRange(20,1200, "X")
    canvas.Modified()
    canvas.Update()
    canvas.SaveAs(Directory+prefix+"_"+keyName+".pdf")
    del canvas
  if obj.IsFolder():
    fpath.append(keyName)
FindDir(f, fpath, Directory)

exit(0)

