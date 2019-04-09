# Muon_TagAndProbe
A (nearly) step-by-step description for 2018 Muon SF, combining instructions from:
- https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonTagAndProbeTreesRun2
- https://github.com/cms-MuonPOG/TnPUtils/blob/80X/README.md

## Set-Up (https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonTagAndProbeTreesRun2#Current_working_recipe_102X)
~~~~
cmsrel CMSSW_10_2_5
cd CMSSW_10_2_5/src
cmsenv

git cms-merge-topic HuguesBrun:updateL3MuonCollectionsToMatch
git clone git@github.com:sscruz/Tnp94.git MuonAnalysis/TagAndProbe -b 94_newSelector
git cms-addpkg PhysicsTools/PatAlgos

cmsenv
scramv1 b -j 5

cmsenv
git cms-addpkg PhysicsTools/PatAlgos
git clone https://github.com/cms-MuonPOG/TnPUtils.git
scramv1 b -j 5
git clone https://gitlab.cern.ch/cms-muonPOG/TnPfromZ.git -b 80X 
mv TnPfromZ/SFsExtractor plotsAndSFsExtractor
~~~~

### 0. Check https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonTagAndProbeTreesRun2#Tree_production_versions for available TnPTrees. (If not already available, work on tree production using MuonAnalysis/TagAndProbe/test/zmumu/{tp_from_aod_Data/MC}.py)

### 1. Calculate weight (ratio of tag_nVertices in data to that in MC) and store as a branch in MC tree using `TnPUtils/addNVtxWeight`
- To save computing time, find the upper edge of bins and and use it in to set `--histogramRange` option. GetMaxBin.py can be used directly for 2018 Data and DY trees (default). One can update the list of files `--file "filepath/1.root filepath/2.root` , tree name `--treename`, branch (of which max bin is wanted) `--branch`.
~~~~
python GetMaxBin.py
~~~~
- Max bin value will be printed in command line (rounded up to nearest 0.5). Use it to define `--histogramRange (nbins, -0.5, maxbin)` where maxbin is the  output value of GetMaxBin.py and nbins = (maxbin+0.5). For 2018 (as of date 19 Mar 2018) :
~~~~
nohup ./TnPUtils/addNVtxWeight "/eos/cms/store/group/phys_muon/TagAndProbe/Run2018/102X/TnPTreeZ_17Sep2018_SingleMuon_Run2018Av2_GoldenJSON.root /eos/cms/store/group/phys_muon/TagAndProbe/Run2018/102X/TnPTreeZ_17Sep2018_SingleMuon_Run2018Bv1_GoldenJSON.root /eos/cms/store/group/phys_muon/TagAndProbe/Run2018/102X/TnPTreeZ_17Sep2018_SingleMuon_Run2018Cv1_GoldenJSON.root /eos/cms/store/group/phys_muon/TagAndProbe/Run2018/102X/TnPTreeZ_SingleMuon_Run2018Dv2_GoldenJSON.root" "/eos/cms/store/group/phys_muon/TagAndProbe/Run2018/102X/TnPTreeZ_102XAutumn18_DYJetsToLL_M50_MadgraphMLM.root" /eos/user/w/wiwong/TagAndProbe/add_PUweight/TnPTree_DY2018_weighted.root --histogramRange "149,-0.5,148.5" > addweight.log 2>&1 &
~~~~
- note: nohup mode is recommanded since it takes quite long to run this command. You can also use other kind of batch mode.

### 2. Skim trees using `TnPUtils/skimTree`. Customize option `-k` to keep branches you need and `-c` to apply simple cuts so as to slim the file.
- For 2018 (as of date 19 Mar 2018) MiniIsolation v.s. CutBasedIDs (Tight and Loose), e.g.
~~~~
nohup TnPUtils/skimTree /eos/cms/store/group/phys_muon/TagAndProbe/Run2018/102X/TnPTreeZ_17Sep2018_SingleMuon_Run2018Av2_GoldenJSON.root /eos/user/w/wiwong/TagAndProbe/skimtree_out/skimmed_20_RunA2018.root -r "all" -k "pt abseta dB dzPV eta mass pair_newTuneP_mass pair_newTuneP_probe_pt pair_probeMultiplicity pair_deltaR run IsoMu24 IsoTkMu24 Mu50 fixedGridRhoFastjetCentralNeutral miniIsoCharged miniIsoNeutrals miniIsoPhotons combRelIsoPF04dBeta CutBasedIdTight CutBasedIdMedium CutBasedIdLoose tag_nVertices" -c "((pt > 20 || pair_newTuneP_probe_pt > 20) && mass > 69.5 && mass < 130.1 && tag_combRelIsoPF04dBeta < 0.2 && tag_combRelIsoPF04dBeta > -0.5 && tag_pt > 30 && tag_IsoMu27 == 1 && abseta < 2.401 && pair_probeMultiplicity == 1)" > /eos/user/w/wiwong/TagAndProbe/skimtree_out/skimmer18A.log 2>&1 &

nohup TnPUtils/skimTree /eos/user/w/wiwong/TagAndProbe/add_PUweight/TnPTree_DY2018_weighted.root /eos/user/w/wiwong/TagAndProbe/skimtree_out/skimmed_20_DY2018.root -r "all" -k "pt abseta dB dzPV eta mass pair_newTuneP_mass pair_newTuneP_probe_pt pair_probeMultiplicity pair_deltaR run IsoMu24 IsoTkMu24 Mu50 fixedGridRhoFastjetCentralNeutral miniIsoCharged miniIsoNeutrals miniIsoPhotons combRelIsoPF04dBeta CutBasedIdTight CutBasedIdMedium CutBasedIdLoose tag_nVertices weight" -c "((pt > 20 || pair_newTuneP_probe_pt > 20) && mass > 69.5 && mass < 130.1 && tag_combRelIsoPF04dBeta < 0.2 && tag_combRelIsoPF04dBeta > -0.5 && tag_pt > 30 && tag_IsoMu27 == 1 && abseta < 2.401 && pair_probeMultiplicity == 1)" > /eos/user/w/wiwong/TagAndProbe/skimtree_out/skimmer18DY.log 2>&1 &
~~~~
- Take the above example and run for each data and MC TnPTrees (note use MC tree from output of addNVtxWeight). Check `skims.sh`.

- Cuts applied explained :
  - pT cut value `(pt > 20 || pair_newTuneP_probe_pt > 20)` depends on your need
  - there should be no need to change mass window `mass > 69.5 && mass < 130.1` (Z mass)
  - require a tight muon as tag `tag_combRelIsoPF04dBeta < 0.2 && tag_combRelIsoPF04dBeta > -0.5 && tag_pt > 30 && tag_IsoMu27 == 1` which might change every year (reference for 2018 : https://cds.cern.ch/record/2629364/files/DP2018_042.pdf)
  - useful eta range (limited by detector) `abseta < 2.401`
  - one matched tag-probe pair `pair_probeMultiplicity == 1`
- Keep braches:
  - `pt abseta` for SF binning 
  - `pt eta fixedGridRhoFastjetCentralNeutral miniIsoCharged miniIsoNeutrals miniIsoPhotons` for calculating custom ID `miniiso = (miniIsoCharged + TMath::Max(0.0, miniIsoPhotons + miniIsoNeutrals - CorrectedTerm ))/pt` where `CorrectedTerm = fixedGridRhoFastjetCentralNeutral * Aeff_Fall17Anal[eta_bin]*(riso2/0.09)`, `riso2 = r_iso*r_iso`, `r_iso = std::max(0.05,std::min(0.2, 10.0/pt))`, and `Aeff_Fall17Anal` is the effective area (changes every era => make sure it is updated!)
  - `combRelIsoPF04dBeta` for determining RelIsoTight/Loose
  - `CutBasedIdTight CutBasedIdMedium CutBasedIdLoose` for CutBasedIDs
  - `mass pair_newTuneP_mass pair_newTuneP_probe_pt pair_probeMultiplicity` for cuts
  - `IsoMu24 IsoTkMu24 Mu50` for extra triggers that might be useful (currectly in use in addVariable.cxx)
  - Other branches that might become useful (`dzPV` is neccessary for running fits later)

### 3. Update output file name in addVariables.cxx (line 43), then open skimmed trees in ROOT and execute addVariables.cxx on ROOT command line
~~~~
root -l file_path_to/skimmed_tree.root
root [1] .x addVariables.cxx
~~~~

### 3.5. (optional) Skim tree again after addVariable. For example : 
~~~~
nohup TnPUtils/skimTree /eos/user/w/wiwong/TagAndProbe/addVar_out/fullA2018_PFiso.root /eos/user/w/wiwong/TagAndProbe/IsoA2018_20.root -r "all" -k "pt abseta dzPV eta mass run CutBasedIdTight miniIsoTight PFIsoTight CutBasedIdLoose miniIsoLoose PFIsoLoose" </dev/null > Iso18A_20.log 2>&1 &
nohup TnPUtils/skimTree /eos/user/w/wiwong/TagAndProbe/addVar_out/fullDY2018_PFiso.root /eos/user/w/wiwong/TagAndProbe/IsoDY2018_20.root -r "all" -k "pt abseta dzPV eta mass run CutBasedIdTight miniIsoTight PFIsoTight CutBasedIdLoose miniIsoLoose PFIsoLoose weight" </dev/null > Iso18DY_20.log 2>&1 &
~~~~

### 4. Update fitMuon2_newselector2.py (modified from `TnPUtils/fitMuon2_newselector.py`). Change definition of looseiso to miniIsoLoose == 1 (miniiso<0.4) and tightiso to miniIsoTight == 1 (miniiso<0.1). One can also define new IDs, update binnings etc..

### 5. Run fitMuon2_newselector2.py on each Run and MC file respectively (there is known memory leakage problem so most likely not possible to combine Runs and do fits).
~~~~
nohup cmsRun fitMuon2_newselector2.py miniLoose_Loose_abseta looseiso looseid data_all dataidD pt_eta default > fitLoose_D_20.log 2>&1 &
nohup cmsRun fitMuon2_newselector2.py miniTight_Tight_abseta_test tightiso tightid mc_all mc2018 pt_eta default > fitTight_DY_20.log 2>&1 &
~~~~
#### OR 
- update `run_Tight_DATA.sh` and `condor_fitMuon.sub` (modify for desired IDs, condor setup etc.)
- run on condor by `condor_submit condor_fitMuon.sub`

### 6. Extract efficiency plots of each run individually using (TnPfromZ/SFsExtractor/) `plotsAndSFsExtractor/extractPlotsAndComputeTheSFs.C`
~~~~
root -b -q -l 'plotsAndSFsExtractor/extractPlotsAndComputeTheSFs.C("A","Loose_PtEtaBins","Efficiency20_miniLoose_Loose_abseta/DATA_dataidA/TnP_MC_NUM_LooseIso_DEN_LooseID_PAR_pt_eta.root", "Efficiency20_miniLoose_Loose_abseta/MC_mc2018/TnP_MC_NUM_LooseIso_DEN_LooseID_PAR_pt_eta.root")'
~~~~

### 7. Scale and add the efficiencies using `ScaleAndAdd.py` after updating information (Lumi, Eras, file prefix and suffix, folder name in root, bins) in `needs to be updated` section. You can change the output file name (line 86). If output structure of the fitMuon scripts changed, one might also need to change the histogram names through out the script accordingly.
~~~~
cd FolderStoringOutputFilesOf_extractPlotsAndComputeTheSFs/
python ../ScaleAndAdd.py
~~~~

### 8. (optional) One can extract all the plots and save as pdf using `python GetAllPlots Folder_path/ Filename.root`

### 9. For Muon POG review, dump SFs in json files using `python createJsonFile_CommonFormat.py file_path_to/SFs.root ouputdirectory/prefix.json` (plotsAndSFsExtractor/createJsonFile_CommonFormat.py)

