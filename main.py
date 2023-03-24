from vnstock import *
import pandas as pd
import numpy as np
import math
from collections import defaultdict
import json

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)

def ceil(number, digits) -> float: return math.ceil((10.0 ** digits) * number) / (10.0 ** digits)

#DO NOT CHANGE THE FIRST ELEMENT
bank_code = ["CTG","BID","VCB","VIB","MBB","TCB","HDB","STB","EIB","ACB","VPB","MSB","NAB","PGB","ABB","KLB","SHB","SGB", "STB", "VPB"]
#retail_code = ["AAT","BSC","ABR","AMD","AST","BTT","FRT","DGW","GCB","IMH","MWG","PET","PIV","PIT","HEX","IBC","SEC","PNG","PSD","T12","SID","CPH","ST8","HTC","KLF"]
#bank_code = ["CTG","BID","VCB","VIB","MBB","TCB","HDB","STB"]
retail_code = ["AAT","MWG"]
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

def getRate(code):
	classA = defaultdict(list)
	classB = defaultdict(list)
	bankRate = defaultdict(list)
	ebitData = defaultdict(list)
	profitData = defaultdict(list)
	bankPropoEquityPerYears=defaultdict(list)
	bankPropoEquityPerYearsAv=defaultdict(list)
	bankCapExpendPerYears=defaultdict(list)
	bankCexpendPerY3ears=defaultdict(list)

	for bank in code:
		incomeData = financial_report (symbol= bank, report_type='IncomeStatement', frequency='yearly')
		balanceData = financial_report (symbol= bank, report_type='BalanceSheet', frequency='yearly')

		totalEquity={}
		totalEquityAv={}
		propoEquityPerYears={}
		capExpendPerYears={}
		totalDebt={}
		totalDebtAv={}
		bankEbit=[]
		bankEbitDict={}
		netProfitDict={}
		#print(balanceData.iloc[91,0])
		for column in balanceData.columns:
			if(code[0] =="AAT" and "Vay ngắn hạn" in balanceData.iloc[73,0] and "Vay dài hạn" in balanceData.iloc[86,0] and "VỐN CHỦ SỞ HỮU" in balanceData.iloc[91,0]):
				for year in years:
					if year in column:
						# Co cau Von
						shortLoan = np.abs(balanceData.loc[75,column])
						longloan = np.abs(balanceData.loc[88,column])
						totalLoan = shortLoan + longloan
						totalDebt[year] = totalLoan

						equity = np.abs(balanceData.loc[95,column])
						totalEquity[year] = equity

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
				#print(debt, bank, list(totalDebt.keys())[debt], rs)
				totalEquityAv[list(totalEquity.keys())[ed]] = rs


		# Tỷ trọng vốn chủ sổ hữu trên Tổng Vốn = E/(D+E) từng năm
		for y, ed in totalEquityAv.items():
			for yr, debt in totalDebtAv.items():
				if y == yr:
					propoEquityPerYear = ed/(ed+debt)
					propoEquityPerYears[y] = ceil(propoEquityPerYear*100,2)
					#print(y, ceil(propoEquityPerYear*100,2))

		bankPropoEquityPerYears[bank].append(propoEquityPerYears)

		# Tỷ trọng vốn chủ sổ hữu trên Tổng Vốn - Bình quân
		bankPropoEquity = sum(totalEquity.values()) / (sum(totalEquity.values()) + sum(totalDebt.values()))
		bankPropoEquityPerYearsAv[bank].append(ceil(bankPropoEquity*100,2))

		interestYearly={}
		for column in incomeData.columns:
			#note that the colum 15 and 16 of the retail is fucked up
			#print(incomeData.iloc[21,0])
			if (code[0] =="AAT" and "Chi phí lãi vay" in incomeData.iloc[7,0] and "ròng trước thuế" in incomeData.iloc[15,0] and "thuần sau thuế" in incomeData.iloc[19,0]):
				for year in years:
					if year in column:
						income = np.abs(incomeData.loc[16,column])
						netProfit = np.abs(incomeData.loc[20,column])
						interest = np.abs(incomeData.loc[7,column])
						ebit = income + interest
						tax = 0.2
						res = ebit*(1-tax)
						bankEbitDict[year]=res
						bankEbit.append(res)
						netProfitDict[year] = netProfit
						interestYearly[year] = interest
						#print(bank,year, income,interest, res)
							

			if (code[0] =="CTG" and "Chi phí lãi" in incomeData.iloc[1,0] and "Tổng lợi nhuận trước thuế" in incomeData.iloc[17,0] and "Lợi nhuận sau thuế" in incomeData.iloc[21,0]):
				for year in years:
					if year in column:
						income = np.abs(incomeData.loc[17,column])
						netProfit = np.abs(incomeData.loc[21,column])
						interest = np.abs(incomeData.loc[1,column])
						ebit = income + interest
						tax = 0.2
						res = ebit*(1-tax)
						bankEbitDict[year]=res
						bankEbit.append(res)
						netProfitDict[year] = netProfit



		rateYearly={}
		#print(bankEbitDict)
		if all(res is not None for res in bankEbitDict.values()) and all(net is not None for net in netProfitDict.values()):
			ebitData[bank] = (((list(bankEbitDict.values())[-1]/list(bankEbitDict.values())[0])**(1/5))-1)*100
			profitData[bank] = (((list(netProfitDict.values())[-1]/list(netProfitDict.values())[0])**(1/5))-1)*100
			#print(bank,list(netProfitDict.values())[-1],list(netProfitDict.values())[0])
			for ebit in range(len(bankEbitDict)):
				if(ebit+1 >= len(bankEbitDict)):
					break
				ebit1t = (list(bankEbitDict.values())[ebit+1] - list(bankEbitDict.values())[ebit])/list(bankEbitDict.values())[ebit]
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
						capExpendPerYears[year] = ceil((interest/debt)*100,2)
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
		
		expendPerY3ears = ceil((totalIn3/totalDebt3)*100,2)
		bankCexpendPerY3ears[bank].append(expendPerY3ears)


		#ROAE - Tỷ suất lợi nhuận trên bình quân VCSH
		



		
	for name, rate in ebitData.items():
		for x,y in bankRate.items():
			for i,j in profitData.items():
				for a,b in bankPropoEquityPerYears.items():
					for c,d in bankPropoEquityPerYearsAv.items():
						for e,f in bankCapExpendPerYears.items():
							for p,k in bankCexpendPerY3ears.items():
								if rate >= 15 and name == x and name == i == a == c == e == p :
									classA[x] ="Tang truong tung nam: %s" %y,"Tang truong TB / nam (LN truoc lai vay sau thue): %s" % ceil(rate,2), "LN rong TB / nam: %s" % ceil(j,2),"Ty trong VCSH tren Tong Von tung nam: %s" % b \
									, "Ty trong VCSH/ Tong Von (Binh quan): %s" % d[0], "Ty trong von vay / Tong von (binh quan): %s" % str(ceil(100-d[0],2)) \
									, "Chi phi no vay tung nam: %s" % f, "Binh quan chi phi no vay (3 nam): %s" % k[0]
								elif rate < 15 and name == x and name == i == a == c == e == p:
									classB[x] ="Tang truong tung nam: %s" %y,"Tang truong TB/  nam (LN truoc lai vay sau thue): %s" % ceil(rate,2), "LN rong / nam: %s" % ceil(j,2), "Ty trong VCSH tren Tong Von tung nam: %s" % b \
									, "Ty trong VCSH/ Tong Von (Binh quan): %s" % d[0], "Ty trong von vay / Tong von (binh quan): %s" % str(ceil(100-d[0],2)) \
									, "Chi phi no vay tung nam: %s" % f, "Binh quan chi phi no vay (3 nam): %s" % k[0]
	
	allClasses["A"] = classA
	allClasses["B"] = classB

	print('all :', json.dumps(allClasses, indent=4))


vcb = financial_report (symbol= "MFS", report_type='BalanceSheet', frequency='yearly')
mwg = financial_report (symbol= "MWG", report_type='BalanceSheet', frequency='yearly')

#print(mwg)
#print(mwg.loc[0][9],mwg.loc[75][9])


getRate(retail_code)




