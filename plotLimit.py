import ROOT as r
import pandas as pd
from collections import defaultdict
from array import array
import numpy as np

df = pd.read_csv("muonSV_limits.csv",index_col=False)


massList = []
ctauList =[]
perMass = defaultdict(list)
perMassPlus1 = defaultdict(list)
perMassMinus1 = defaultdict(list)
perLifetime = defaultdict(list)
perLifetimePlus1 = defaultdict(list)
perLifetimeMinus1 = defaultdict(list)
for irow in df.iterrows():
    row = irow[1]
    perMass[row.mass].append([row.lifetime,row["Expected 50.0%"]*0.01])
    perMassPlus1[row.mass].append([row.lifetime,row["Expected 16.0%"]*0.01])
    perMassMinus1[row.mass].append([row.lifetime,row["Expected 84.0%"]*0.01])
    perLifetime[row.lifetime].append([row.mass,row["Expected 50.0%"]*0.01])
    perLifetimePlus1[row.lifetime].append([row.mass,row["Expected 16.0%"]*0.01])
    perLifetimeMinus1[row.lifetime].append([row.mass,row["Expected 84.0%"]*0.01])
outGraphs = []
outGraphsPlus1 = []
outGraphsMinus1 = []

colors = {2:r.kMagenta,5:r.kYellow,10:r.kBlack,15:r.kRed,20:r.kBlue}
oC = r.TCanvas()
outputHist = r.TH1D("dummy",";c#tau [mm];95% CL on BR(H#rightarrow#psi#psi)",100,1,1000)
outputHist.Draw()
outputHist.SetMaximum(10)
outputHist.SetMinimum(1E-5)
r.gStyle.SetOptStat(0)
leg = r.TLegend(0.6,0.6,0.89,0.89)
leg.SetBorderSize(0)
for mass in perMass:
    perMass[mass] = np.array(perMass[mass])
    perMassPlus1[mass] = np.array(perMassPlus1[mass])
    perMassMinus1[mass] = np.array(perMassMinus1[mass])

    X = array("d",perMass[mass][:,0])
    Y = array("d",perMass[mass][:,1])
    YPlus1 = array("d",perMassPlus1[mass][:,1])
    YMinus1 = array("d",perMassMinus1[mass][:,1])

    outGraphs.append(r.TGraph(len(perMass[mass]),X,Y))
    outGraphsPlus1.append(r.TGraph(len(perMassPlus1[mass]),X,YPlus1))
    outGraphsMinus1.append(r.TGraph(len(perMassMinus1[mass]),X,YMinus1))
    outGraphs[-1].SetLineColor(colors[mass])
    outGraphsPlus1[-1].SetLineColor(colors[mass])
    outGraphsMinus1[-1].SetLineColor(colors[mass])
    outGraphs[-1].SetLineWidth(2)
    outGraphsPlus1[-1].SetLineStyle(2)
    outGraphsMinus1[-1].SetLineStyle(2)
    outGraphs[-1].Draw("same")
    outGraphsPlus1[-1].Draw("same")
    outGraphsMinus1[-1].Draw("same")
    leg.AddEntry(outGraphs[-1],"m_{s} = "+str(int(mass))+" GeV")
leg.Draw()
oC.SetLogy()
oC.SetLogx()
oC.SaveAs("limitsPerMass.pdf")

outputHistPerL = r.TH1D("dummy2",";m_{s} [GeV];95% CL on BR(H#rightarrow#psi#psi)",100,1,30)
outputHistPerL.Draw()
outputHistPerL.SetMaximum(10)
outputHistPerL.SetMinimum(1E-5)
colors = {1:r.kMagenta,10:r.kYellow,50:r.kBlack,100:r.kRed,500:r.kBlue}
leg = r.TLegend(0.6,0.6,0.89,0.89)
leg.SetBorderSize(0)
for lifetime in perLifetime:
    perLifetime[lifetime] = np.array(perLifetime[lifetime])
    perLifetimePlus1[lifetime] = np.array(perLifetimePlus1[lifetime])
    perLifetimeMinus1[lifetime] = np.array(perLifetimeMinus1[lifetime])

    X = array("d",perLifetime[lifetime][:,0])
    Y = array("d",perLifetime[lifetime][:,1])
    YPlus1 = array("d",perLifetimePlus1[lifetime][:,1])
    YMinus1 = array("d",perLifetimeMinus1[lifetime][:,1])

    outGraphs.append(r.TGraph(len(perLifetime[lifetime]),X,Y))
    outGraphsPlus1.append(r.TGraph(len(perLifetimePlus1[lifetime]),X,YPlus1))
    outGraphsMinus1.append(r.TGraph(len(perLifetimeMinus1[lifetime]),X,YMinus1))
    outGraphs[-1].SetLineColor(colors[lifetime])
    outGraphsPlus1[-1].SetLineColor(colors[lifetime])
    outGraphsMinus1[-1].SetLineColor(colors[lifetime])
    outGraphs[-1].SetLineWidth(2)
    outGraphsPlus1[-1].SetLineStyle(2)
    outGraphsMinus1[-1].SetLineStyle(2)
    outGraphs[-1].Draw("same")
    outGraphsPlus1[-1].Draw("same")
    outGraphsMinus1[-1].Draw("same")
    leg.AddEntry(outGraphs[-1],"c#tau = "+str(int(lifetime))+" mm")
leg.Draw()
oC.SetLogy()
oC.SetLogx(0)
oC.SaveAs("limitsPerLifetime.pdf")
