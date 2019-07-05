#include "TTree.h"
#include "TFile.h"
#include "TStopwatch.h"
#include <math.h>

using namespace std;


void addVariables() {
    TTree *tIn  = (TTree *) gFile->Get("tpTree/fitter_tree");

    cout << "Loaded tree" << endl;
    // ================================================
    // ===== Write here the variables you need to merge

    // Merging Loose                       // For Loose Definition (although it is exactly the same as the PF --- i checked in 2012A --- it saves some variables)

    // New High PT ID

    //Merging Triggers
    Int_t IsoMu24, IsoTkMu24, Mu50;
    tIn->SetBranchAddress("IsoMu24", &IsoMu24);
    tIn->SetBranchAddress("IsoTkMu24", &IsoTkMu24);
    tIn->SetBranchAddress("Mu50", &Mu50);

    Float_t miniIsoCharged, miniIsoPhotons, miniIsoNeutrals, combRelIsoPF04dBeta, fixedGridRhoFastjetCentralNeutral;
    Float_t pt, eta;
    tIn->SetBranchAddress("miniIsoCharged",&miniIsoCharged);
    tIn->SetBranchAddress("miniIsoPhotons",&miniIsoPhotons);
    tIn->SetBranchAddress("miniIsoNeutrals",&miniIsoNeutrals);
    tIn->SetBranchAddress("combRelIsoPF04dBeta", &combRelIsoPF04dBeta);
    tIn->SetBranchAddress("fixedGridRhoFastjetCentralNeutral",&fixedGridRhoFastjetCentralNeutral);
    tIn->SetBranchAddress("pt",&pt);
    tIn->SetBranchAddress("eta",&eta);

    // Making tag_abseta
    // // Merging Triggers

    cout << "SetBranchAddress done" << endl;
    // ===============================================
    // ===== Write here the variables you want to save

    //TFile *fOut = new TFile("/lustre/cms/store/user/schhibra/tnpZ_withVars.root", "RECREATE");// To run batch jobs
    TFile *fOut = new TFile("/eos/user/w/wiwong/TagAndProbe/addVar_out/fullF_ss.root", "RECREATE");
//    TFile *fOut = new TFile("fullDY_iso.root", "RECREATE");
    fOut->mkdir("tpTree")->cd();
    TTree *tOut = tIn->CloneTree(0);

    cout << "Made output file and tree" << endl;
    Int_t miniisotight;
    Int_t miniisoloose;
    Int_t pfisotight;
    Int_t pfisoloose;
    Int_t IsoMu24Mu50OR;
    Float_t abseta;

    tOut->Branch("miniIsoTight",   &miniisotight,      "miniIsoTight/I");
    tOut->Branch("miniIsoLoose",   &miniisoloose,      "miniIsoLoose/I");
    tOut->Branch("PFIsoTight",   &pfisotight,      "PFIsoTight/I");
    tOut->Branch("PFIsoLoose",   &pfisoloose,      "PFIsoLoose/I");
    tOut->Branch("IsoMu24Mu50OR",         &IsoMu24Mu50OR,         "IsoMu24Mu50OR/I");
//    tOut->Branch("abseta", &abseta, "abseta/F");

    cout << "Output branches defined" << endl;
    // =====================================
    // ===== Compute your new variables here

//    double Aeff_Fall15Anal[2][7] = {{ 0.1752, 0.1862, 0.1411, 0.1534, 0.1903 , 0.2243, 0.2687 },{ 0.0735, 0.0619, 0.0465, 0.0433, 0.0577 , 0.0,0.0}};
    double Aeff_Fall17Anal[2][7] = {{ 0.1566, 0.1626, 0.1073, 0.0854, 0.1051, 0.1204, 0.1524 },{ 0.0735, 0.0619, 0.0465, 0.0433, 0.0577 , 0.0,0.0}};

    int step = tIn->GetEntries()/100;
    double evDenom = 100.0/double(tIn->GetEntries());
    TStopwatch timer; timer.Start();
    for (int i = 0, n = tIn->GetEntries(); i < n; ++i) {
        tIn->GetEntry(i);
   
        // Here Do what you want
   	// ---------------------
    	// loose2012 = pf && (glb || tma);
    	// tag_loose2012 = tag_pf && (tag_glb || tag_tma);
    	// highptid = glb && (glbvalidmuhits > 0) && (numberofmatchedstations > 1) && (dxy < 0.2) && (dz < 0.5) && (tkvalidpixelhits > 0) && (tktrackerlay > 5) && (pair_newtunep_sigmaptoverpt < 0.3);

        // make combined miniIso
        double r_iso = std::max(0.05,std::min(0.2, 10.0/pt));
        double CorrectedTerm=0.0;
        double riso2 = r_iso*r_iso;
        double rho = fixedGridRhoFastjetCentralNeutral;

        if( TMath::Abs( eta ) < 0.8 ) CorrectedTerm = rho * Aeff_Fall17Anal[1][ 0 ]*(riso2/0.09);
        else if( TMath::Abs( eta ) > 0.8 && TMath::Abs( eta ) < 1.3 )   CorrectedTerm = rho * Aeff_Fall17Anal[1][ 1 ]*(riso2/0.09);
        else if( TMath::Abs( eta ) > 1.3 && TMath::Abs( eta ) < 2.0 )   CorrectedTerm = rho * Aeff_Fall17Anal[1][ 2 ]*(riso2/0.09);
        else if( TMath::Abs( eta ) > 2.0 && TMath::Abs( eta ) < 2.2 )   CorrectedTerm = rho * Aeff_Fall17Anal[1][ 3 ]*(riso2/0.09);
        else if( TMath::Abs( eta ) > 2.2 && TMath::Abs( eta ) < 2.5 )   CorrectedTerm = rho * Aeff_Fall17Anal[1][ 4 ]*(riso2/0.09);
        double miniiso = (miniIsoCharged + TMath::Max(0.0, miniIsoPhotons + miniIsoNeutrals - CorrectedTerm ))/pt;
        miniisotight = (miniiso < 0.1);
        miniisoloose = (miniiso < 0.4);
        pfisotight = (combRelIsoPF04dBeta<0.15);
        pfisoloose = (combRelIsoPF04dBeta<0.25);
        IsoMu24Mu50OR = IsoMu24 || IsoTkMu24 || Mu50;
//        abseta=TMath::Abs( eta );
        // End Do what you want
        // --------------------
        tOut->Fill();
        if ((i+1) % step == 0) {
            double totalTime = timer.RealTime()/60.; timer.Continue();
            double fraction = double(i+1)/double(n+1), remaining = totalTime*(1-fraction)/fraction;
            printf("Done %9d/%9d   %5.1f%%   (elapsed %5.1f min, remaining %5.1f min)\n", i, n, i*evDenom, totalTime, remaining);
            fflush(stdout);
        }
    }

    tOut->AutoSave(); // according to root tutorial this is the right thing to do
    fOut->Close();
}
