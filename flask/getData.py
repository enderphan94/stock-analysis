#THIS VERSION IS NOT USING VNSTOCK

import pandas as pd
import numpy as np
import math
from collections import defaultdict
import json
import argparse
import os
import locale

locale.setlocale(locale.LC_ALL, '')

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)

def ceil(number, digits) -> float: return math.ceil((10.0 ** digits) * number) / (10.0 ** digits)
def div(n, d):
    return n / d if d else 0
#DO NOT CHANGE THE FIRST ELEMENT
bank_code = ["CTG","BID","VCB","VIB","MBB","TCB","HDB","STB","EIB","ACB","VPB","MSB","NAB","PGB","ABB","KLB","SHB","SGB", "STB", "VPB"]
retail_code = ["AAT","BSC","ABR","AMD","BTT","DGW","MWG","PET","PIV","PIT","IBC","PSD","CPH","ST8","HTC","KLF","FPTR","TASECOAIRS","PTBD","PNCO","SCID"]
# N/A: "IMH","HEX","SEC","T12"

avaiCode= ["AAA","AAM","AAT","AAV","ABB","ABI","ABR","ABS","ABT","ACB","ACC","ACE","ACL","ACM","ADC","ADP","AGF","AGM","AGR","ALT","ALV","AMC","AMD","AME","AMP","AMV","ANV","APC","APF","APG","API","APL","APP","APS","ARM","ASA","ASM","ASP","ATA","ATB","ATS","AVF","B82","BBC","BBH","BBS","BBT","BCB","BCC","BCE","BCG","BCP","BDB","BDW","BED","BHA","BHC","BHK","BHN","BHP","BHT","BIC","BID","BII","BKC","BLF","BMC","BMD","BMF","BMI","BMJ","BMN","BMP","BOT","BPC","BRC","BRS","BSC","BSI","BST","BT6","BTG","BTH","BTN","BTP","BTS","BTT","BTU","BTW","BVG","BVH","BVN","BVS","BWA","BXH","C21","C22","C32","C47","C92","CAD","CAN","CAP","CAV","CCI","CCL","CCM","CCR","CDC","CDH","CDO","CEN","CEO","CFM","CH5","CHP","CI5","CID","CIG","CII","CJC","CKD","CKV","CLC","CLG","CLL","CLW","CMC","CMG","CMI","CMP","CMS","CMT","CMV","CMX","CNC","CNG","CNT","COM","CPC","CPH","CPI","CSC","CSM","CSV","CT3","CT6","CTA","CTB","CTC","CTD","CTF","CTG","CTI","CTN","CTP","CTR","CTS","CTT","CTW","CTX","CVN","CVT","CX8","CYC","D11","D2D","DAC","DAD","DAE","DAG","DAH","DAP","DAS","DBC","DBM","DBT","DC2","DC4","DCL","DCM","DCS","DCT","DDM","DDN","DDV","DFF","DGC","DGT","DGW","DHA","DHC","DHG","DHM","DHP","DHT","DIC","DID","DIG","DIH","DL1","DLD","DLG","DLR","DMC","DNC","DNH","DNL","DNM","DNN","DNP","DNT","DPC","DPM","DPP","DPR","DPS","DQC","DRC","DRH","DRL","DSN","DST","DSV","DTA","DTC","DTE","DTI","DTL","DTN","DTT","DTV","DVC","DVG","DVP","DVW","DXG","DXL","DXP","DXV","DZM","E1VFVN30","EBS","ECI","EFI","EIB","EID","ELC","EMC","EVE","FBA","FCM","FCN","FDC","FID","FIT","FLC","FMC","FPT","FRC","FT1","FTI","FUEMAV30","FUESSV30","FUEVFVND","FUEVN100","G20","GAS","GDT","GDW","GER","GGG","GHC","GIL","GLC","GLT","GMA","GMC","GMD","GMX","GSM","GSP","GTA","GTH","GTT","H11","HAD","HAG","HAH","HAI","HAP","HAR","HAS","HAT","HAV","HAX","HBC","HBD","HBS","HCC","HCI","HCM","HCT","HDA","HDB","HDC","HDG","HDM","HDO","HEJ","HEP","HEV","HFC","HFX","HGM","HHC","HHG","HHN","HHS","HIG","HJS","HKB","HKP","HKT","HLA","HLC","HLD","HLG","HLR","HLY","HMC","HMG","HMH","HNG","HNM","HOM","HOT","HPB","HPD","HPG","HPH","HPP","HPT","HQC","HRB","HRC","HSA","HSG","HSI","HT1","HTC","HTG","HTI","HTL","HTP","HTT","HTV","HU1","HU3","HU4","HUT","HVA","HVG","HVT","HVX","IBC","ICC","ICF","ICG","ICI","IDI","IDJ","IDP","IDV","IFS","IHK","IJC","ILA","ILC","IME","IMP","IN4","INC","INN","IST","ITA","ITC","ITD","ITQ","IVS","JVC","KAC","KBC","KCE","KDC","KDH","KDM","KHA","KHL","KHP","KKC","KLB","KLF","KMR","KMT","KPF","KSB","KSD","KSH","KSQ","KSS","KST","KSV","KTL","KTS","KTT","KVC","L10","L14","L18","L35","L43","L44","L61","L62","LAF","LAS","LAW","LBC","LBE","LBM","LCC","LCD","LCG","LCM","LCS","LCW","LDP","LGC","LGL","LHC","LHG","LIG","LIX","LKW","LM3","LM7","LM8","LMH","LO5","LSS","LTC","LUT","MAC","MAS","MBB","MCC","MCF","MCG","MCO","MCP","MDA","MDC","MDF","MDG","MEC","MED","MEF","MFS","MHC","MHL","MIC","MIM","MKP","MKV","MLC","MPC","MPT","MPY","MQB","MSB","MSN","MST","MTC","MTG","MTH","MTL","MTP","MWG","NAB","NAF","NAG","NAP","NAV","NBB","NBC","NBP","NBW","NCS","NCT","ND2","NDC","NDF","NDN","NDX","NET","NFC","NGC","NHA","NHC","NHH","NHP","NKG","NLG","NLS","NNC","NNG","NNT","NOS","NQB","NQT","NS2","NSC","NST","NT2","NTB","NTC","NTL","NTP","NTW","NVB","NVT","NWT","NXT","OCB","OCH","OGC","ONE","ONW","OPC","ORS","PAC","PAN","PAS","PBP","PCG","PCM","PCT","PDB","PDC","PDN","PDR","PEC","PEN","PET","PFL","PGB","PGC","PGD","PGI","PGN","PGS","PGT","PHC","PHH","PHP","PHR","PHS","PIC","PID","PIT","PIV","PJC","PJS","PJT","PLC","PLE","PMC","PMJ","PMS","PMT","PNC","PND","PNJ","PNP","POB","POM","POT","POV","PPC","PPE","PPI","PPP","PPS","PRC","PRO","PSB","PSC","PSD","PSE","PSG","PSI","PSL","PSP","PTB","PTC","PTD","PTG","PTH","PTI","PTL","PTP","PTS","PTT","PV2","PVA","PVB","PVC","PVD","PVE","PVG","PVI","PVL","PVR","PVS","PVT","PVV","PVX","PX1","PXA","PXI","PXL","PXM","PXS","PXT","QBS","QCC","QCG","QHD","QHW","QNC","QNT","QNU","QPH","QST","QTC","RAL","RCC","RCD","RCL","RDP","REE","RIC","S12","S27","S55","S74","S96","S99","SAF","SAL","SAM","SAP","SAS","SAV","SBA","SBL","SBS","SBT","SC5","SCC","SCD","SCG","SCI","SCJ","SCL","SCO","SCR","SCY","SD1","SD2","SD3","SD4","SD5","SD6","SD7","SD8","SD9","SDA","SDB","SDC","SDD","SDG","SDJ","SDK","SDN","SDP","SDT","SDU","SDV","SDX","SDY","SEB","SED","SEP","SFC","SFG","SFI","SFN","SGB","SGC","SGD","SGH","SGO","SGR","SGS","SGT","SHA","SHB","SHC","SHG","SHI","SHN","SHP","SHS","SHX","SIC","SII","SJ1","SJC","SJD","SJE","SJF","SJM","SJS","SKG","SKN","SLS","SMA","SMB","SMC","SMT","SNC","SPB","SPC","SPD","SPH","SPI","SPM","SQC","SRA","SRB","SRC","SRF","SSC","SSF","SSG","SSI","SSM","SSN","ST8","STB","STC","STG","STL","STP","STS","STT","SUM","SVC","SVD","SVG","SVH","SVI","SVN","SVT","SWC","SZE","SZL","TA3","TA6","TAW","TB8","TBC","TBD","TBT","TBX","TC6","TCB","TCL","TCM","TCO","TCR","TCT","TDC","TDH","TDN","TDP","TDS","TDW","TEG","TET","TFC","TGP","TH1","THB","THD","THG","THS","THT","THU","THW","TIE","TIG","TIP","TIS","TIX","TJC","TKC","TKG","TKU","TL4","TLG","TLH","TLT","TMC","TMP","TMS","TMT","TMW","TMX","TN1","TNA","TNB","TNC","TNG","TNM","TNT","TOP","TOT","TPB","TPC","TPH","TPP","TRA","TRC","TRS","TS4","TSB","TSC","TST","TTA","TTB","TTC","TTF","TTG","TTN","TTP","TTZ","TV1","TV2","TV3","TV4","TV6","TVA","TVC","TVD","TVG","TVS","TXM","TYA","UCT","UDC","UDJ","UIC","UMC","UNI","UPC","USC","USD","V11","V12","V15","V21","VAB","VAF","VAT","VAV","VBC","VBH","VC1","VC2","VC3","VC5","VC6","VC7","VC9","VCA","VCB","VCC","VCF","VCG","VCM","VCR","VCS","VCT","VCX","VDB","VDL","VDN","VDS","VDT","VE1","VE2","VE3","VE4","VE8","VE9","VEF","VES","VFC","VFG","VFR","VGC","VGP","VGS","VHC","VHF","VHG","VHH","VHL","VIB","VIC","VID","VIE","VIG","VIN","VIP","VIR","VIT","VIX","VKC","VKP","VLA","VLF","VMC","VMD","VMG","VNA","VNC","VND","VNE","VNF","VNG","VNH","VNI","VNL","VNM","VNR","VNS","VNT","VNX","VOS","VPB","VPC","VPG","VPH","VPR","VPW","VQC","VRC","VRG","VSC","VSE","VSG","VSH","VSI","VST","VTA","VTB","VTC","VTE","VTH","VTI","VTJ","VTK","VTL","VTM","VTO","VTS","VTV","VTX","VXB","VXP","WCS","WSB","WSS","WTC","X20","X26","X77","XMC","XMD","XPH","YBC"]
yearList = ["2013","2014","2015","2016","2017","2018","2019","2020","2021","2022"]

# bank: 17, CPLV: 1
#MWG: 16, CPLV:7

# cong thuc tinh ti suat loi nhuan tung nam
# EBIT(1-t) = (Loi nhuan ke toan truoc thue + chi lai vay) * income tax
# percent = EBIT(1-t)[1] - EBIT(1-t)[0] / EBIT(1-t)[0]
# Tang truong / nam = ((EBIT(1-t)[-1]/EBIT(1-t)[0])^(1/5))-1

allClasses = defaultdict(list)
CEO = 0.15 # chi phí VCSH
tax = 0.2

directory = 'data/2023/'

def getRate(bank,period,types, fr, to, growth):
	global CEO
	global tax
	global directory

	if fr not in yearList and to not in yearList:
		raise ValueError(f"Year {fr} is not in the list of valid years")

	years = yearList[yearList.index(fr): yearList.index(to)+1]
	
	if len(years) != 6:
			raise ValueError("period issue")


	classA = defaultdict(list)
	classB = defaultdict(list)
	bankRate = defaultdict(list)
	ebitData = defaultdict(list)
	profitData = defaultdict(list)
	bankPropoEquityPerYears=defaultdict(list)
	bankPropoEquityPerYearsAv=defaultdict(list)
	bankPropoMarginPerYears=defaultdict(list)
	bankCapExpendPerYears=defaultdict(list)
	bankCexpendPerY3ears=defaultdict(list)
	bankROAEYears=defaultdict(list)
	bankDiffRE=defaultdict(list)
	bankWaccYearly=defaultdict(list)
	bankWaccAv=defaultdict(list)
	bankRoceYearly=defaultdict(list)
	bankRoceYearlyAv=defaultdict(list)
	bankDiffRF=defaultdict(list)
	bankWorkingCapitalYears=defaultdict(list)
	bankWorkingCapitalChangedYears=defaultdict(list)
	bankReinvestFixedAsset=defaultdict(list)
	bankTotalReInvestDict=defaultdict(list)
	freeProfitCashDict=defaultdict(list)
	proReinvestYearlyDict=defaultdict(list)
	totalReinvestAvDict=defaultdict(list)
	fastGrowthRateDict=defaultdict(list)


	incomeDataDir = directory + code + "/" + code + "_IncomeData_" + period + ".csv"
	balanceDataDir = directory + code + "/" + code + "_BalanceData_" + period + ".csv"
	cashDataDir = directory + code + "/" + code + "_CashData_" + period + ".csv"

	incomeData = pd.read_csv(incomeDataDir,index_col=0)
	balanceData = pd.read_csv(balanceDataDir,index_col=0)
	cashData = pd.read_csv(cashDataDir,index_col=0)


	shortLoanYears={}
	shortDebtYears={}
	shortAssetYears={}
	totalEquity={}
	totalEquityAv={}
	propoEquityPerYears={}
	propoMarginPerYears={}
	capExpendPerYears={}
	totalDebt={}
	totalDebtAv={}
	bankEbit=[]
	bankEbitDict={}
	netProfitDict={}
	buyAssetYears={}
	liqAssetYears={}
	depreDataYears={}
	cashYears={}
	uncontrolledEquityYears={}
	commonStockYears={}

	for column in balanceData.columns:
		if("Vay ngắn hạn" in balanceData.loc[75][0] and "Vay dài hạn" in balanceData.loc[88][0] and "VỐN CHỦ SỞ HỮU" in balanceData.loc[95][0]\
				and "TÀI SẢN NGẮN HẠN" in balanceData.loc[1][0] and "Nợ ngắn hạn" in balanceData.loc[65][0] and "Tiền mua tài sản cố định và các tài sản dài hạn khác" in cashData.loc[22][0]\
				 and "Tiền thu được từ thanh lý tài sản cố định" in cashData.loc[23][0] and "Khấu hao TSCĐ" in cashData.loc[3][0] and "Tiền và tương đương tiền cuối kỳ" in cashData.loc[40][0])\
					and "Lợi ích cổ đông không kiểm soát" in balanceData.loc[113][0] and "Cổ phiếu phổ thông" in balanceData.loc[98][0]:
			for year in years:
				if year in column:
					# Co cau Von
					shortLoan = balanceData.loc[75,column]
					shortLoanYears[year]= shortLoan

					longloan = balanceData.loc[88,column]
					totalLoan = shortLoan + longloan
					totalDebt[year] = totalLoan

					equity = balanceData.loc[95,column]
					totalEquity[year] = equity

					shortAsset = balanceData.loc[1,column]
					shortAssetYears[year] = shortAsset

					shortDebt = balanceData.loc[65,column]
					shortDebtYears[year] = shortDebt

					buyAsset = np.abs(cashData.loc[22,column])
					buyAssetYears[year] = buyAsset

					liqAsset = cashData.loc[23,column]
					liqAssetYears[year] = liqAsset

					depreData = cashData.loc[3, column]
					depreDataYears[year] = depreData

					cash = cashData.loc[40,column]
					cashYears[year] = cash

					uncontrolledEquity= balanceData.loc[113,column]
					uncontrolledEquityYears[year] = uncontrolledEquity

					commonStock = balanceData.loc[98,column]
					commonStockYears[year] = commonStock


					
		else:
			print("something wrong happens")
	
	# Tong vay binh quan
	if all(debt is not None for debt in totalDebt.values()):
		for debt in reversed(range(len(totalDebt))):
			#if(debt+1 >= len(totalDebt)):
			#	break
			rs=0
			if(debt == 0):
				rs = list(totalDebt.values())[debt]
			else:
				rs = (list(totalDebt.values())[debt] + list(totalDebt.values())[debt-1])/2
			#print(debt, bank, list(totalDebt.keys())[debt], rs)
			totalDebtAv[list(totalDebt.keys())[debt]] = rs

	# Binh quan Equity
	if all(ed is not None for ed in totalEquity.values()):
		for ed in reversed(range(len(totalEquity))):
			#if(debt+1 >= len(totalDebt)):
			#	break
			rs=0
			if(ed == 0):
				rs = list(totalEquity.values())[ed]
			else:
				rs = (list(totalEquity.values())[ed] + list(totalEquity.values())[ed-1])/2
			totalEquityAv[list(totalEquity.keys())[ed]] = rs


	# Tỷ trọng vốn chủ sổ hữu trên Tổng Vốn = E/(D+E) từng năm
	for y, ed in totalEquityAv.items():
		for yr, debt in totalDebtAv.items():
			if y == yr:
				propoEquityPerYear = div(ed,(ed+debt))
				propoEquityPerYears[y] = ceil(propoEquityPerYear*100,2)
				#print(y, ceil(propoEquityPerYear*100,2))

	bankPropoEquityPerYears[bank].append(propoEquityPerYears)

	# Tỷ trọng vốn vay / Tổng Vốn từng năm
	for y, ed in totalEquityAv.items():
		for yr, debt in totalDebtAv.items():
			if y == yr:
				propoMarginPerYear = div(debt,(ed+debt))
				propoMarginPerYears[y] = ceil(propoMarginPerYear*100,2)

	bankPropoMarginPerYears[bank].append(propoMarginPerYears)

	# Tỷ trọng vốn chủ sổ hữu trên Tổng Vốn - Bình quân
	bankPropoEquity = div(sum(totalEquity.values()), (sum(totalEquity.values()) + sum(totalDebt.values())))
	bankPropoEquityPerYearsAv[bank].append(ceil(bankPropoEquity*100,2))

	interestYearly={}
	netProfitYearly={}

	for column in incomeData.columns:
		#note that the colum 15 and 16 of the retail is fucked up
		#print(incomeData.iloc[21,0])
		if ("Chi phí lãi vay" in incomeData.loc[7][0] and "ròng trước thuế" in incomeData.loc[16][0] and "thuần sau thuế" in incomeData.loc[20][0]):
			for year in years:
				if year in column:
					income = incomeData.loc[16,column]
					netProfit = incomeData.loc[20,column]
					interest = np.abs(incomeData.loc[7,column])
					ebit = income + interest
					res = ebit*(1-tax)
					bankEbitDict[year]=res
					bankEbit.append(res)
					netProfitDict[year] = netProfit
					interestYearly[year] = interest
					netProfitYearly[year] = netProfit
					#print(bank,year, income,interest, res)
						
		else:
			print("something wrong happens")

		# if ("Chi phí lãi" in incomeData.iloc[1,0] and "Tổng lợi nhuận trước thuế" in incomeData.iloc[17,0] and "Lợi nhuận sau thuế" in incomeData.iloc[21,0]):
		# 	for year in years:
		# 		if year in column:
		# 			income = np.abs(incomeData.loc[17,column])
		# 			netProfit = np.abs(incomeData.loc[21,column])
		# 			interest = np.abs(incomeData.loc[1,column])
		# 			ebit = income + interest
		# 			res = ebit*(1-tax)
		# 			bankEbitDict[year]=res
		# 			bankEbit.append(res)
		# 			netProfitDict[year] = netProfit

		# else:
		# 	print("something wrong happens")

	#print(bankEbitDict.values())
	# Tang truong tung nam				
	rateYearly={}
	if all(res is not None for res in bankEbitDict.values()) and all(net is not None for net in netProfitDict.values()):
		ebitData[bank] = ((div(list(bankEbitDict.values())[-1],list(bankEbitDict.values())[0])**(1/5))-1)*100
		profitData[bank] = ((div(list(netProfitDict.values())[-1],list(netProfitDict.values())[0])**(1/5))-1)*100
		#print(bank,list(netProfitDict.values())[-1],list(netProfitDict.values())[0])
		for ebit in range(len(bankEbitDict)):
			if(ebit+1 >= len(bankEbitDict)):
				break
			ebit1t = div((list(bankEbitDict.values())[ebit+1] - list(bankEbitDict.values())[ebit]),list(bankEbitDict.values())[ebit])
			period = str(list(bankEbitDict.keys())[ebit]) + "-" + str(list(bankEbitDict.keys())[ebit+1])
			result = ceil(ebit1t * 100, 2)
			rateYearly[period] = result
			ebit+=1

		#print(rateYearly)
		bankRate[bank].append(rateYearly)
	
	#Chi phí nợ vay từng năm
	for year, interest in reversed(list(interestYearly.items())):
			for y, debt in totalDebtAv.items():
				if year == y:
					res = div(interest,debt)
					capExpendPerYears[year] = ceil(res*100,2)
	bankCapExpendPerYears[bank].append(capExpendPerYears)

	# Chi phí nợ vay, bình quân (3 năm gần nhất)
	totalIn3 = 0
	if all(inter is not None for inter in interestYearly.values()):
		for inter in reversed(range(len(interestYearly))):
			if(inter == 2):
				break
			totalIn3 += list(interestYearly.values())[inter]
			inter = inter - 1
	
	totalDebt3 = 0
	if all(debt is not None for debt in totalDebtAv.values()):
		for debt in range(len(totalDebtAv)):
			if(debt == 3):
				break
			totalDebt3 += list(totalDebtAv.values())[debt]
			debt = debt + 1
	
	expendPerY3ears = ceil(div(totalIn3,totalDebt3)*100,2)
	bankCexpendPerY3ears[bank].append(expendPerY3ears)


	#ROAE - Tỷ suất lợi nhuận trên bình quân VCSH
	roaeYearly={}
	for year, equityAv in totalEquityAv.items():
		for y, netProfit in netProfitYearly.items():
			if year == y:
				res = ceil(div(netProfit,equityAv)*100,2)
				roaeYearly[year] = res

	bankROAEYears[bank].append(roaeYearly)

	#Cách biệt giữa ROE và chi phí vốn Chủ sở hữu
	latestROAE = list(roaeYearly.values())[0]
	diffRE = latestROAE - (CEO*100)
	bankDiffRE[bank].append(ceil(diffRE,2))

	#Chi phí chi phí vốn của doanh nghiệp, WACC từng năm 
	#WACC = (CP vốn VCSH * % vốn CSH) + (CP vốn vay * % vốn vay * (1 – thuế)) 
	#=(B20*B36)+((B24*B28)*(1-$B$6))
	waccYearly={}
	for year, equity in propoEquityPerYears.items():
		for y, margin in propoMarginPerYears.items():
			for yr, cap in capExpendPerYears.items():
				if year == y == yr:
					wacc = ((equity*(CEO*100))/100) + (((margin*cap)/100)*(1-tax))
					waccYearly[year] = ceil(wacc,2)

	bankWaccYearly[bank].append(waccYearly)


	#Chi phí vốn của doanh nghiệp WACC - Bình quân
	#=(B22*B36)+((B25*B29)*(1-B6))

	waccAv=0
	for bank, proproEq in bankPropoEquityPerYearsAv.items():
		for bank, cap in bankCexpendPerY3ears.items():
			if bank == bank:
				B22 = proproEq[0]
				B36 = CEO 
				B25 = ceil(100-B22,2)
				B29 = cap[0]
				waccAv = ((B22*(B36*100))/100)+(((B25*B29)/100)*(1-tax))
	
	bankWaccAv[bank].append(ceil(waccAv,2))
	
	#Tỷ suất sinh lợi ROCE từng năm  
	roceYearly={}
	for y, e, in totalEquityAv.items():
		for year, d in totalDebtAv.items():
			for yr, ebit in bankEbitDict.items():
				if year == y == yr:
					roce = ceil((div(ebit,(e+d))*100),2)
					roaeYearly[year] = roce
	bankRoceYearly[bank].append(roaeYearly)

	#Tỷ suất sinh lợi ROCE -  Bình quân 
	#=SUM(B7:G7)/(SUM(B47:G47)+SUM(B48:G48))
	roceAv = div(sum(bankEbitDict.values()),(sum(totalEquityAv.values())+sum(totalDebtAv.values()))) * 100
	roceAv = ceil(roceAv,2)
	bankRoceYearlyAv[bank].append(roceAv)

	#Cách biệt giữa ROCE và WACC
	diffRW = roceAv-waccAv
	bankDiffRF[bank].append(ceil(diffRW,2))

	# Vốn lưu động = TS ngắn hạn - Nợ Ngắn hạn + Vay ngắn hạn

	workingCapitalYears={}
	for y, debt in shortDebtYears.items():
		for year, loan in shortLoanYears.items():
			for yr, asset in shortAssetYears.items():
				if y == year == yr:
					workingCapital = asset - debt + loan
					workingCapitalYears[year] = workingCapital

	bankWorkingCapitalYears[bank].append(workingCapitalYears)

	# Thay đổi vốn lưu động
	workingCapitalChangedYears={}
	if all(cap is not None for cap in workingCapitalYears.values()):
		for cap in reversed(range(len(workingCapitalYears))):
			#if(debt+1 >= len(totalDebt)):
			#	break
			rs=0
			if(cap == 0):
				rs = list(workingCapitalYears.values())[cap]
			else:
				rs = list(workingCapitalYears.values())[cap] - list(workingCapitalYears.values())[cap-1]
			
			workingCapitalChangedYears[list(workingCapitalYears.keys())[cap]] = rs

	bankWorkingCapitalChangedYears[bank].append(workingCapitalChangedYears)

	
	# Đầu tư TS cố định (Mua tài sản - Thanh lý TS)
	investFixedAsset={}
	for year, buy in reversed(list(buyAssetYears.items())):
		for y, liq in liqAssetYears.items():
			if year == y:
				fixedAsset = buy - liq
				investFixedAsset[year] = fixedAsset 
	
	# Tái đầu tư TS cố định
	reinvestFixedAsset={}
	for year, investFixed in investFixedAsset.items():
		for y, dep in depreDataYears.items():
			if year == y:
				reInvest = investFixed - dep
				reinvestFixedAsset[y] = reInvest

	bankReinvestFixedAsset[bank].append(reinvestFixedAsset) 


	# Tổng tái đầu tư
	totalReInvestDict={}
	for year, workingcap in workingCapitalChangedYears.items():
		for y, reinvest in reinvestFixedAsset.items():
			if year == y:
				totalReInvest = workingcap + reinvest
				totalReInvestDict[year] = totalReInvest

	bankTotalReInvestDict[bank].append(totalReInvestDict)
	
	# Dòng tiền lợi nhuận tự do
	freeProfitCash={}
	for year, ebit in reversed(list(bankEbitDict.items())):
		for y, totalInvest in reversed(list(totalReInvestDict.items())):
			if year == y:
				freeCash = ebit - totalInvest
				freeProfitCash[year] = freeCash

	freeProfitCashDict[bank].append(freeProfitCash)

	# Tỷ lệ tái đầu tư các năm  = Mức Tái đầu tư / EBIT*(1-Tc))
	proReinvestYearly={}

	for year, totalInvest in totalReInvestDict.items():
		for y, ebit in bankEbitDict.items():
			if year == y:
				proRein = (totalInvest/ebit)*100
				proReinvestYearly[year] = ceil(proRein,2)
	
	proReinvestYearlyDict[bank].append(proReinvestYearly)


	# Tỷ lệ tái đầu tư - Bình quân 
	totalReinvestAv = div(sum(totalReInvestDict.values()),sum(bankEbitDict.values()))*100
	totalReinvestAv = ceil(totalReinvestAv,2)
	totalReinvestAvDict[bank].append(totalReinvestAv)

	# Tốc độ tăng trưởng giai đoạn nhanh 
	fastGrowthRate = div(roceAv*totalReinvestAv,100)
	fastGrowthRate = ceil(fastGrowthRate,2)
	fastGrowthRateDict[bank].append(fastGrowthRate)

	
	# Ngân Lưu
	ebitFurure={}
	reinvestFuture={}
	proReinvestFuture={}
	freeCashFuture={}
	pVCashFlowFuture={}

	delimiter = ","
	growthList = growth.split(delimiter)

	if types == "advanced" and len(growthList) != 10:
			raise ValueError("You should enter the growth value for the next 10 years")
	
	futureData=defaultdict(list)
	no = 1
	now = int(to) + 1
	for i in range(len(growthList)):
		futureData[str(now)].append({no:(float(growthList[i])/100)})
		no = no + 1
		now = now + 1


	lastYear = list(futureData.keys())[-1]
	nextYear = int(lastYear) + 1
	finalYear = nextYear +1

	futureData[nextYear].append({11:0.035})
	futureData[finalYear].append({0:0.035})

	# futureData["2023"].append({1:0.15})
	# futureData["2024"].append({2:0.15})
	# futureData["2025"].append({3:0.15})
	# futureData["2026"].append({4:0.15})
	# futureData["2027"].append({5:0.15})
	# futureData["2028"].append({6:0.1308})
	# futureData["2029"].append({7:0.1117})
	# futureData["2030"].append({8:0.0925})
	# futureData["2031"].append({9:0.0733})
	# futureData["2032"].append({10:0.0542})
	# futureData["2033"].append({11:0.035})
	# futureData["2034"].append({0:0.035})

	ebitLatest = bankEbitDict[to]
		#Lợi nhuận trước lãi vay sau thuế, EBIT*(1-Tc)
	for year, growth in futureData.items():
		for dictionary in growth:
			for no, percent in dictionary.items():
				ebit = ebitLatest*(1+percent)
				ebitLatest = ebit
				ebitFurure[year] = ebit

		#Tỷ lệ tái đầu tư
	for year, growth in futureData.items():
		for dictionary in growth:
			for no, percent in dictionary.items():
				proReInvest = ((percent*100)/roceAv)*100
				proReinvestFuture[year] = ceil(proReInvest,2)

		#Tái Đầu Tư
	for year, ebit in ebitFurure.items():
		for y, pro in proReinvestFuture.items():
			if year == y:
				reInvest = ebit * (pro/100)
				reinvestFuture[year]=reInvest

		#Dòng tiền tự do = Lợi nhuận trước lãi vay sau thuế - Tái đầu tư 
	for year, ebit in ebitFurure.items():
		for y, reInvest in reinvestFuture.items():
			if year == y:
				freeCash = ebit - reInvest
				freeCashFuture[year] = freeCash
	
	#print(freeCashFuture)
	#print(waccAv)
	for year, growth in futureData.items():
		for y, cash in freeCashFuture.items():
			if year == y:
				for dictionary in growth:
					for no, percent in dictionary.items():
						#print(year, cash, waccAv/100, no)
						pv = div(cash,(1+(waccAv/100))**no)
						pVCashFlowFuture[year]=pv

	#lastYearItem = list(pVCashFlowFuture.keys())[-1]
	#pVCashFlowFuture.pop(lastYearItem)

	# print(ebitFurure,"\n")
	# print("ti le tai dau tu",proReinvestFuture,"\n")
	# print("tai dau tu",reinvestFuture,"\n")
	# print("dong tien tu do",freeCashFuture,"\n")
	# print("gia tri hien tai",pVCashFlowFuture,"\n")

	# Tổng GTHT của dòng tiền
	terminalValueYearly={}

	totalPV = sum(list(pVCashFlowFuture.values())[:-1]) #sum tat ca tru nam cuoi cung


	data10 = dict(list(futureData.values())[10][0]).keys()
	no10 = list(data10)[0]

	cashFlow11 = list(freeCashFuture.values())[11]

	for year, growth in futureData.items():
		for y, cash in freeCashFuture.items():
			if year == y:
				for dictionary in growth:
					for no, percent in dictionary.items():
						#print(year, cash, waccAv/100, percent)
						tm = div(cash,div((ceil(waccAv,2)-(percent*100)),100))
						terminalValueYearly[year]=tm

	terminalValue = list(terminalValueYearly.values())[11]

	pVTerminalValue = div(terminalValue,(1+(waccAv/100))**no10)



	
	totalAllCashFlow = totalPV + pVTerminalValue
	cashYearLatest = cashYears[to]
	totalDebtLatest = totalDebt[to]
	equityLatest = totalEquity[to]
	uncontrollELatest = uncontrolledEquityYears[to]
	commonStockLatest= commonStockYears[to]

	companyValue = totalAllCashFlow+cashYearLatest

	# Giá trị doanh nghiệp hợp nhất - sau nợ 
	companyValueAfterDebt = companyValue - totalDebtLatest

	#% của cổ đông công ty
	perShares = (1-(div(uncontrollELatest,equityLatest)))*100
	perShares = ceil(perShares,2)

	# Giá trị doanh nghiệp dành cho cổ đông
	companyValueForShares = companyValueAfterDebt * (perShares/100)
	#print(companyValueForShares,commonStockLatest)

	# Giá trị nội tại/1 cổ phần
	instinctValue = companyValueForShares/(commonStockLatest/10)
	instinctValue = ceil(instinctValue,0)
	#print(instinctValue, companyValueForShares,commonStockLatest )
	# print("VCSH",equityLatest)
	# print("VCSH-non",uncontrollELatest)
	# print("perShares",perShares)
	# print("commonStock",commonStockLatest)
	# print("GTHT",pVTerminalValue)
	# print("totalAllCashFlow", totalAllCashFlow)

	# PRINT DATA HERE, I'm lazy to change this, fuck it!
	for name, rate in ebitData.items():
		for x,y in bankRate.items():
			for i,j in profitData.items():
				for a,b in bankPropoEquityPerYears.items():
					for c,d in bankPropoEquityPerYearsAv.items():
						for o,u in bankPropoMarginPerYears.items():
							for e,f in bankCapExpendPerYears.items():
								for p,k in bankCexpendPerY3ears.items():
									for l,h in bankROAEYears.items():
										for n,m in bankDiffRE.items():
											for bwacc, vwacc in bankWaccYearly.items():
												for bwaccav, vwaccav in bankWaccAv.items():	
													for broce, vroce in bankRoceYearly.items():
														for broceav, vroceav in bankRoceYearlyAv.items():
															for brf, vrf in bankDiffRF.items():
																for bworkingcap, vworkingcap in bankWorkingCapitalChangedYears.items():
																	for breinvest, vreinvest in bankReinvestFixedAsset.items():
																		for btotalreinvest, vtotalreinvest in bankTotalReInvestDict.items():
																			for bfreecash, vfreecash in freeProfitCashDict.items():
																				for bproinvest, vproinvest in proReinvestYearlyDict.items():
																					if name == x == i == a == c == e == p == l == o == bwacc == bwaccav == broce == bworkingcap == btotalreinvest == bproinvest:
																						classA["Tăng trưởng từng năm"].append(y)
																						classA["Tăng trưởng TB / năm (Lợi nhuận trước lãi vay sau thuế)"].append(str(ceil(rate,2))+"%")
																						classA["Lợi nhuận ròng TB / năm"].append(str(ceil(j,2))+"%")
																						classA["Tỷ trọng VCSH / Tổng Vốn từng năm"].append(b)
																						classA["Tỷ trọng VCSH / Tổng Vốn (Bình quân)"].append(d[0])
																						classA["Tỷ trọng vốn vay / Tổng Vốn từng năm"].append(u)
																						classA["Tỷ trọng vốn vay / Tổng vốn (Bình quân)"].append(str(ceil(100-d[0],2)))
																						classA["Chi phí nợ vay từng năm"].append(f)
																						classA["Bình quân chi phí nợ vay (3 năm)"].append(k[0])
																						classA["ROAE"].append(h)
																						classA["Cách biệt giữa ROE và chi phí vốn Chủ sở hữu"].append(m)
																						classA["WACC từng năm"].append(vwacc)
																						classA["WACC Bình quân"].append(vwaccav[0])
																						classA["ROCE từng năm"].append(vroce)
																						classA["ROCE bình quân"].append(vroceav[0])
																						classA["Cách biệt giữa ROE và WACC"].append(vrf)
																						classA["Thay đổi Vốn lưu động"].append(vworkingcap)
																						classA["Tái đầu tư TS cố định"].append(vreinvest)
																						classA["Tổng tái đầu tư"].append(vtotalreinvest)
																						classA["Dòng tiền lợi nhuận tự do"].append(vfreecash)
																						classA["Tỷ lệ tái đầu tư các năm"].append(vproinvest)
																								#classA["Tỷ lệ tái đầu tư (Bình quân) "].append(vtotalreinvestav)
																								#classA["Tốc độ tăng trưởng giai đoạn nhanh ((Tỷ lệ tái đầu tư * Tỷ suất sinh lợi trên vốn))"].append(vfastgrowth)


	for btotalreinvestav, vtotalreinvestav in totalReinvestAvDict.items():
		for bfastgrowth, vfastgrowth in fastGrowthRateDict.items():
				if btotalreinvestav == bfastgrowth:
					classA["Tỷ lệ tái đầu tư (Bình quân) "].append(vtotalreinvestav)
					classA["Tốc độ tăng trưởng giai đoạn nhanh (Tỷ lệ tái đầu tư * Tỷ suất sinh lợi trên vốn)"].append(vfastgrowth)												
	
	classA["Giá trị hiện tại của tất cả dòng tiền tự do"].append(locale.format_string("%0.2f", pVTerminalValue, grouping=True))
	classA["Giá trị tiền mặt"].append(locale.format_string("%0.2f", cashYearLatest, grouping=True))
	classA["Giá trị Doanh Nghiệp"].append(locale.format_string("%0.2f", companyValue, grouping=True))
	classA["Giá trị doanh nghiệp hợp nhất - sau nợ"].append(locale.format_string("%0.2f", companyValueAfterDebt, grouping=True))
	classA["\% của cổ đông công ty"].append(str(perShares)+ " %")
	classA["Giá trị doanh nghiệp dành cho cổ đông"].append(locale.format_string("%0.2f", companyValueForShares, grouping=True))
	classA["Giá trị nội tại / 1 cổ phần"].append(str(instinctValue)+" "+"VND")


	#allClasses[bank] = classA
	result = json.dumps(classA, indent=4)
	print(result)



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--code', type=str, help='a company code')
	parser.add_argument('--type', type=str, help='a company code')
	parser.add_argument('--fr', type=str, help='from year')
	parser.add_argument('--to', type=str, help='to year')
	parser.add_argument('--growth', type=str, help='predicted growths in the next 10 years separated by comma')
	try:
		args = parser.parse_args()
	except argparse.ArgumentError as e:
		print("Error:", e.message)
		sys.exit(1)
	
	code = args.code
	types = args.type
	fromYear = args.fr
	toYear = args.to
	growth = args.growth
	if code in bank_code:
		print("Error: The instrinct value is not applied for banks yet")
				
	getRate(code,'Yearly',types,fromYear,toYear, growth)




