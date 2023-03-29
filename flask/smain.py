from vnstock import *
import pandas as pd
import numpy as np
import math
from collections import defaultdict
import json
import argparse


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
#bank_code = ["CTG","BID","VCB","VIB","MBB","TCB","HDB","STB"]
#retail_code = ["AAT","FRT"]
single_code = ["BSC","AAT"]
years = ["2016","2017","2018","2019","2020","2021"]

# bank: 17, CPLV: 1
#MWG: 16, CPLV:7

# cong thuc tinh ti suat loi nhuan tung nam
# EBIT(1-t) = (Loi nhuan ke toan truoc thue + chi lai vay) * income tax
# percent = EBIT(1-t)[1] - EBIT(1-t)[0] / EBIT(1-t)[0]
# Tang truong / nam = ((EBIT(1-t)[-1]/EBIT(1-t)[0])^(1/5))-1

allClasses = defaultdict(list)
CEO = 0.15 # chi phí VCSH
tax = 0.2

def getRate(bank):
	global CEO
	global tax
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

	incomeData = financial_report (symbol= bank, report_type='IncomeStatement', frequency='yearly')
	balanceData = financial_report (symbol= bank, report_type='BalanceSheet', frequency='yearly')

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
	#print(balanceData.iloc[91,0])
	for column in balanceData.columns:
		if("Vay ngắn hạn" in balanceData.iloc[73,0] and "Vay dài hạn" in balanceData.iloc[86,0] and "VỐN CHỦ SỞ HỮU" in balanceData.iloc[91,0]):
			for year in years:
				if year in column:
					# Co cau Von
					shortLoan = np.abs(balanceData.loc[75,column])
					longloan = np.abs(balanceData.loc[88,column])
					totalLoan = shortLoan + longloan
					totalDebt[year] = totalLoan

					equity = np.abs(balanceData.loc[95,column])
					totalEquity[year] = equity
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
		if ("Chi phí lãi vay" in incomeData.iloc[7,0] and "ròng trước thuế" in incomeData.iloc[15,0] and "thuần sau thuế" in incomeData.iloc[19,0]):
			for year in years:
				if year in column:
					income = np.abs(incomeData.loc[16,column])
					netProfit = np.abs(incomeData.loc[20,column])
					interest = np.abs(incomeData.loc[7,column])
					ebit = income + interest
					res = ebit*(1-tax)
					bankEbitDict[year]=res
					bankEbit.append(res)
					netProfitDict[year] = netProfit
					interestYearly[year] = interest
					netProfitYearly[year] = netProfit
					#print(bank,year, income,interest, res)
						

		if ("Chi phí lãi" in incomeData.iloc[1,0] and "Tổng lợi nhuận trước thuế" in incomeData.iloc[17,0] and "Lợi nhuận sau thuế" in incomeData.iloc[21,0]):
			for year in years:
				if year in column:
					income = np.abs(incomeData.loc[17,column])
					netProfit = np.abs(incomeData.loc[21,column])
					interest = np.abs(incomeData.loc[1,column])
					ebit = income + interest
					res = ebit*(1-tax)
					bankEbitDict[year]=res
					bankEbit.append(res)
					netProfitDict[year] = netProfit



	rateYearly={}
	if all(res is not None for res in bankEbitDict.values()) and all(net is not None for net in netProfitDict.values()):
		ebitData[bank] = ((div(list(bankEbitDict.values())[-1],list(bankEbitDict.values())[0])**(1/5))-1)*100
		profitData[bank] = ((div(list(netProfitDict.values())[-1],list(netProfitDict.values())[0])**(1/5))-1)*100
		#print(bank,list(netProfitDict.values())[-1],list(netProfitDict.values())[0])
		for ebit in range(len(bankEbitDict)):
			if(ebit+1 >= len(bankEbitDict)):
				break
			ebit1t = div((list(bankEbitDict.values())[ebit+1] - list(bankEbitDict.values())[ebit]),list(bankEbitDict.values())[ebit])
			perdiod = str(list(bankEbitDict.keys())[ebit]) + "-" + str(list(bankEbitDict.keys())[ebit+1])
			result = ceil(ebit1t * 100, 2)
			rateYearly[perdiod] = result
			ebit+=1

		#print(rateYearly)
		bankRate[bank].append(rateYearly)
	
	#Chi phí nợ vay từng năm
	for year, interest in interestYearly.items():
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
	bankDiffRE[bank].append(diffRE)

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
	bankRoceYearlyAv[bank].append(ceil(roceAv,2))

	#Cách biệt giữa ROCE và WACC
	
	diffRW = roceAv-waccAv

	bankDiffRF[bank].append(ceil(diffRW,2))

	# PRINT DATA HERE
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
																if name == x == i == a == c == e == p == l == o == bwacc == bwaccav == broce:
																	classA["Tăng trưởng từng năm"].append(y)
																	classA["Tăng trưởng TB / năm (Lợi nhuận trước lãi vay sau thuế)"].append(ceil(rate,2))
																	classA["Lợi nhuận ròng TB / năm"].append(ceil(j,2))
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

													
									

	#allClasses[bank] = classA
	result = json.dumps(classA, indent=4)
	print(result)

#vcb = financial_report (symbol= "MFS", report_type='BalanceSheet', frequency='yearly')
#mwg = financial_report (symbol= "AST", report_type='BalanceSheet', frequency='yearly')

#print(mwg)
#print(mwg.loc[0][9],mwg.loc[75][9])


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--code', type=str, help='an integer argument')
	try:
		args = parser.parse_args()
	except argparse.ArgumentError as e:
		print("Error:", e.message)
		sys.exit(1)
	
	code = args.code
	getRate(code)