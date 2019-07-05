#!/bin/sh
source /cvmfs/cms.cern.ch/cmsset_default.sh
x509userproxy=/tmp/x509up_u94005
#The build architecture of CMSSW version
export SCRAM_ARCH=slc6_amd64_gcc630
CMSSWBaseDir=/afs/cern.ch/user/w/wiwong/work/TagAndProbe/CMSSW_9_4_0_pre3/src
cd ${CMSSWBaseDir}
#cd /afs/cern.ch/user/w/wiwong/work/TagAndProbe/CMSSW_9_4_0_pre3/src/test_condor

# This is equivalent to doing "cmsenv"
eval `scramv1 runtime -sh`
cd -

cp ${CMSSWBaseDir}/fitMuon2_newselector2.py .

iteration=miniLoose_Loose_abseta_fit_test
input_type=DATA

if [ "${input_type}" == "MC" ]; then
   file=mc2017
   mode=mc_all
elif [ "${input_type}" == "DATA" ]; then
   #file=dataidF
   file=dataidC
   mode=data_all
else
   echo "Unknown parameter"
fi

outputDir=Efficiency20_${iteration}
outputSubDir=${input_type}_${file}

cmsRun fitMuon2_newselector2.py ${iteration} looseiso looseid ${mode} ${file} pt_eta default

if [ ! -d ${CMSSWBaseDir}/${outputDir} ]; then
  mkdir ${CMSSWBaseDir}/${outputDir}
fi

if [ ! -d ${CMSSWBaseDir}/${outputDir}/${outputSubDir} ]; then
  mkdir ${CMSSWBaseDir}/${outputDir}/${outputSubDir}
fi

cp -r ${outputDir}/${outputSubDir}/* ${CMSSWBaseDir}/${outputDir}/${outputSubDir}/
