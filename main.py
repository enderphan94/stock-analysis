from vnstock import *
import pandas as pd
import numpy as np
import math
from collections import defaultdict
import json

def ceil(number, digits) -> float: return math.ceil((10.0 ** digits) * number) / (10.0 ** digits)

#DO NOT CHANGE THE FIRST ELEMENT
bank_code = ["CTG","BID","VCB","VIB","MBB","TCB","HDB","STB","EIB","ACB","VPB","MSB","NAB","PGB","ABB","KLB","SHB","SGB", "STB"]
#retail_code = ["AAT","BSC","ABR","AMD","AST","BTT","FRT","DGW","GCB","IMH","MWG","PET","PIV","PIT","HEX","IBC","SEC","PNG","PSD","T12","SID","CPH","ST8","HTC","KLF"]
#bank_code = ["CTG","BID","VCB","VIB","MBB","TCB","HDB","STB"]
retail_code = ["AAT","BSC","ABR","AMD","BTT","DGW","MWG"]
years = ["2016","2017","2018","2019","2020","2021"]

# bank: 17, CPLV: 1
#MWG: 16, CPLV:7

# cong thuc tinh ti suat loi nhuan tung nam
# EBIT(1-t) = (Loi nhuan ke toan truoc thue + chi lai vay) * income tax
# percent = EBIT(1-t)[1] - EBIT(1-t)[0] / EBIT(1-t)[0]
# Tang truong / nam = ((EBIT(1-t)[-1]/EBIT(1-t)[0])^(1/5))-1

allClasses = defaultdict(list)


def getRate(code):
	classA = defaultdict(list)
	classB = defaultdict(list)
	bankRate = defaultdict(list)
	ebitData = defaultdict(list)
	profitData = defaultdict(list)
	for bank in code:
		dataBank = financial_report (symbol= bank, report_type='IncomeStatement', frequency='yearly')
		bankEbit=[]
		bankEbitDict={}
		netProfitDict={}
		for column in dataBank.columns:
			#note that the colum 15 and 16 of the retail is fucked up
			#print(dataBank.iloc[21,0])
			if (code[0] =="AAT" and "Chi phí lãi vay" in dataBank.iloc[7,0] and "ròng trước thuế" in dataBank.iloc[15,0] and "thuần sau thuế" in dataBank.iloc[19,0]):
				for year in years:
					if year in column:
						income = np.abs(dataBank.loc[16,column])
						netProfit = np.abs(dataBank.loc[20,column])
						interest = np.abs(dataBank.loc[7,column])
						ebit = income + interest
						tax = 0.2
						res = ebit*(1-tax)
						bankEbitDict[year]=res
						bankEbit.append(res)
						netProfitDict[year] = netProfit
						#print(bank,year, income,interest, res)
			if (code[0] =="CTG" and "Chi phí lãi" in dataBank.iloc[1,0] and "Tổng lợi nhuận trước thuế" in dataBank.iloc[17,0] and "Lợi nhuận sau thuế" in dataBank.iloc[21,0]):
				for year in years:
					if year in column:
						income = np.abs(dataBank.loc[17,column])
						netProfit = np.abs(dataBank.loc[21,column])
						interest = np.abs(dataBank.loc[1,column])
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
			
	for name, rate in ebitData.items():
		for x,y in bankRate.items():
			for i,j in profitData.items():
				if rate >= 15 and name == x and name == i:
					classA[x] = y,"Tang truong / nam: %s" % ceil(rate,2), "LN rong / nam: %s" % ceil(j,2)
				elif rate < 15 and name == x and name == i:
					classB[x] = y,"Tang truong /  nam: %s" % ceil(rate,2), "LN rong / nam: %s" % ceil(j,2)
	allClasses["A"] = classA
	allClasses["B"] = classB

	print('all :', json.dumps(allClasses, indent=4))

vcb = financial_report (symbol= "VCB", report_type='IncomeStatement', frequency='yearly')
#mwg = financial_report (symbol= "MWG", report_type='IncomeStatement', frequency='yearly')

print(vcb)
#print(mwg)

getRate(bank_code)




