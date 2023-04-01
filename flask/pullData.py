from vnstock import *
import pandas as pd
import numpy as np
import math
from collections import defaultdict
import json
import argparse
import os



#NOT AVAILABLE

#VVS,XDC,HSV,CST,BVL,SGI,TOS,VTZ,SSH,BCA,FUCTVGF3,FUEIP100,GMH,BIG,CMM,CNA,FUEKIV30,ODE,HMR,PCH,DSD,NO1,MGR,PPT,CVP,CAR,GPC,FUCTVGF4,FUEDCMID,FUEKIVFS,FUEMAVND,GCF,LPT,ACS,ACV,AFX,CKA,AGP,CAG,LTG,AGG,AGX,AG1,AGE,ACG,ANT,APH,APL,HII,A32,ASG,ATG,AVC,BAF,BAL,BCV,BNA,BRR,CBC,BLW,VLB,BBH,BBT,BCB,BCP,MVC,BFC,BDG,BSA,PRT,BEL,NBT,BGW,BHK,BHP,BCM,BLT,DBD,BHG,BIO,BWE,BKG,BLI,MH3,DTB,BMD,BMG,BMS,MBN,BNW,VTG,BSP,BSR,BTN,BTD,BTV,BLN,BVN,TNH,BWA,BWS,HNB,C69,C22,C71,TS3,CPA,CFV,CCT,CCA,HFB,CMW,KCB,CBS,VSM,CDH,CDG,CRE,STK,TW3,CFM,CH5,CHC,CLX,CI5,CE1,CEG,C4G,C12,CKG,CIP,CBI,CK8,CMK,ADG,CMF,TVH,TIN,CMD,CAT,CC1,CDP,TCK,CMN,ICN,CNN,DP1,DTP,CPH,CIA,CRC,SGP,CT3,GTS,ICT,TTS,AUM,DCR,DCG,DRG,DRI,UDL,DWC,DHB,ADS,DAN,DNE,DAP,DAS,DPG,TDB,VBG,DCF,DM7,DC1,TTE,DLM,DUS,NSS,DNW,DND,CDN,DSC,DNT,DOC,MCD,BSD,DMN,DOP,CDR,DWS,DPP,DP2,DSV,BDT,DTN,DTV,MTV,MGG,DVC,DSG,DVW,DXS,FUESSV50,E1VFVN30,E29,EME,EMG,EMS,EPC,FUESSVFL,EVG,EVF,EIC,LEC,FHS,ROS,FBA,FIC,FIR,FSO,ART,FOC,FBC,FCS,FRM,DP3,FTM,FRT,FTS,FRC,FT1,FOX,FTI,FUEMAV30,FUESSV30,FUEVFVND,FUEVN100,GAB,M10,BVB,GEX,GEE,PGV,FGL,GLW,GEG,GIC,C36,DDH,GTH,H11,PHN,HC1,HCB,HC3,HDP,HPX,HID,HNR,HLB,HLT,HAM,HHV,AAS,BBM,HAN,HD6,HNP,HSM,HTM,HES,GH3,HAV,HGW,HTW,HBH,XDH,HCD,HCI,HTE,DHD,HDW,HEC,HEJ,HEM,HEP,HFC,HFX,HGT,HHN,HHP,HHR,TCH,HSL,HPI,HKP,HLR,HLS,HMS,BKH,DCH,HAF,HNA,DHN,HRT,TSJ,HJC,HAC,CCP,HPH,HPM,HPP,DPH,HPT,TUG,HPW,HRB,HSP,HTN,HTR,HD2,HU6,HD8,HWS,HNI,HUG,HNF,HVH,L40,ICC,ILB,ICI,CC4,IDC,MCI,IME,IBD,DDG,IRC,ILS,IPA,ISG,ITS,KTC,KHG,KHW,KGM,KHS,KLM,GKM,KOS,KHD,LMC,L45,L63,LMI,DKC,LSG,LBC,LCC,LQN,LWS,LDG,LDW,LGM,LIC,L12,LG9,LLM,LAI,AMS,LKW,LNC,LPB,MA1,MCM,MDA,MEF,MEL,MRF,MES,JOS,MIE,MIG,MTA,MLS,MLC,MML,MPY,MCH,MSR,MTC,MTH,MTL,NAU,MTP,NDP,NJC,NAC,FHN,NTF,BAB,NAS,VET,NAW,NBE,NDC,MND,HND,NDW,NED,NRC,MNB,VCE,VHM,NHT,NHV,NLS,NNT,NVL,PMB,PSH,NTT,NUE,NTW,NWT,NXT,EVS,TOW,ONW,PAI,PAP,PC1,PCC,CSI,PDV,PEC,PEQ,PCF,PEG,PTV,PLX,PLP,PBC,PIA,PIC,PIS,EIN,PJS,PLA,PLO,PLE,PMG,PMJ,PMP,PMW,PNG,PNT,POB,DNA,PPH,BT1,PSL,GCB,PTE,PTO,KSF,PTG,PTN,PTP,POS,PSN,PTX,PTT,DSP,DTD,DAT,PBK,PBT,PCE,PVM,PXC,PVH,PCN,PSW,RGC,PRE,OIL,PPY,POW,PVY,PVP,PWA,PX1,PWS,BQB,MQN,QSP,CQN,PQN,QNS,QNT,QTP,QNU,QNW,NQN,RAT,RCD,TBR,DS3,RBC,S72,BSH,BSQ,SGN,SAL,SKV,SKH,APT,CHS,BSL,SAC,VNB,SAB,SBD,SBH,SBM,SID,SCS,XLV,SDV,SSB,SEA,SPV,SEP,BSG,NSG,SRT,SIP,TPS,NSH,MSH,SHX,SBV,SZC,SIV,SKN,SNC,SMN,SIG,SNZ,SZG,SJG,SHE,SBR,NSL,SPB,SPH,SP2,ISH,TSG,S4A,SSF,STW,SUM,SZB,TA3,TA6,TA9,TKA,AST,TB8,TBH,RTB,TBT,FUCVREIT,TCI,G36,TCW,VCP,GTD,TDG,TTD,TDM,NTH,TDT,CET,TED,TEL,TGG,TGP,MTB,TLP,TDI,THN,BTB,DTH,THI,TQN,THU,TAN,TTH,TID,DTG,TLD,TTL,TLI,MBS,TMW,STH,BAX,TNS,TNI,TNM,TNP,TCJ,BCF,THP,TR1,TCD,TVW,TRS,TAR,TDF,TVB,TSD,TTT,TTG,HUB,TRT,GND,TQW,TV6,TVA,TVG,TVP,TNW,UCT,UEM,FCC,UMC,UPC,UPH,USC,USD,PAT,CCV,VIH,CLM,VCI,VDB,VDN,VDT,VEA,VEC,VFS,VUA,NDT,TVT,SB1,PVO,MBG,VDP,MVB,VJC,DVM,VTD,VTR,VLC,VIM,TVM,TMG,DTK,VIF,VHE,VHD,VVN,KIP,VGT,VMT,VGL,GVT,VPS,VGR,VLP,VIR,VSN,VWS,VIW,VMS,ABC,MGC,VMA,MTS,AIC,HVN,VGV,CGV,TMB,E12,BMV,VSF,VNZ,MVN,VLG,VPD,DVN,VNP,GVR,TVN,VXT,VNY,VNX,VOC,VSA,VPR,VPA,VPI,VPW,NVP,VRE,VSE,VGG,VGI,VTI,VTK,VTM,VTP,VTQ,VBB,DLT,CAB,CLH,VLW,VW3,VCW,WTC,X26,EPH,DFC,CQT,XHC,XMP,YBM,YEG,YTC


def getDataYearly(code):

    incomeData = financial_report (symbol= code, report_type='IncomeStatement', frequency='yearly')
    balanceData = financial_report (symbol= code, report_type='BalanceSheet', frequency='yearly')
    cashData = financial_report (symbol= code, report_type='cashflow', frequency='yearly')

    dfIncomeData = pd.DataFrame(incomeData)
    dfBalanceData = pd.DataFrame(balanceData)
    dfCashData = pd.DataFrame(cashData)

    incomeName = code + '_IncomeData_Yearly' +'.csv'
    balanceName = code + '_BalanceData_Yearly' +'.csv'
    cashName = code + '_CashData_Yearly' +'.csv'

    # create the directory if it does not exist
    directory = 'data/2023/'+code+"/"

    if not os.path.exists(directory):
        os.makedirs(directory)

    # save the files to the directory
    file_path_income = directory + incomeName
    file_path_balance = directory + balanceName
    file_path_cash = directory + cashName

    dfIncomeData.to_csv(file_path_income, index=True)
    dfBalanceData.to_csv(file_path_balance, index=True)
    dfCashData.to_csv(file_path_cash, index=True)



def getDataQuarterly(code):
    incomeData = financial_report (symbol= code, report_type='IncomeStatement', frequency='Quarterly')
    balanceData = financial_report (symbol= code, report_type='BalanceSheet', frequency='Quarterly')
    cashData = financial_report (symbol= code, report_type='cashflow', frequency='Quarterly')

    dfIncomeData = pd.DataFrame(incomeData)
    dfBalanceData = pd.DataFrame(balanceData)
    dfCashData = pd.DataFrame(cashData)

    incomeName = code + '_IncomeData_Quarterly' +'.csv'
    balanceName = code + '_BalanceData_Quarterly' +'.csv'
    cashName = code + '_CashData_Quarterly' +'.csv'

    # create the directory if it does not exist
    directory = 'data/2023/'+code+"/"

    if not os.path.exists(directory):
        os.makedirs(directory)

    # save the files to the directory
    file_path_income = directory + incomeName
    file_path_balance = directory + balanceName
    file_path_cash = directory + cashName

    dfIncomeData.to_csv(file_path_income, index=True)
    dfBalanceData.to_csv(file_path_balance, index=True)
    dfCashData.to_csv(file_path_cash, index=True)

companyCode = listing_companies()

companyCodeList = []
#print(companyCode.loc[0][0])
for line in range(len(companyCode)):
	#print(np.abs(companyCode.loc[0,line]))
	#try:
	companyCodeList.append(companyCode.loc[line][0])

print(companyCodeList)

for code in companyCodeList:
	try: 
		getDataYearly(code)
		getDataQuarterly(code)
	except KeyError:
		continue

	except Exception as e:
        # Handle other exceptions as needed
		print(code)