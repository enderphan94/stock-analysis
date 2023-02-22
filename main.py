from vnstock import *
import pandas as pd
import numpy as np
import math
from collections import defaultdict
import json

def ceil(number, digits) -> float: return math.ceil((10.0 ** digits) * number) / (10.0 ** digits)

bank_code = ["CTG","BID","VCB","VIB","MBB","TCB","HDB","STB","EIB","ACB","VPB","MSB","NAB","PGB","ABB","KLB","SHB","SGB", "STB"]
#retail_code = ["AAT","BSC","ABR","AMD","AST","BTT","FRT","DGW","GCB","IMH","MWG","PET","PIV","PIT","HEX","IBC","SEC","PNG","PSD","T12","SID","CPH","ST8","HTC","KLF"]
#bank_code = ["CTG","BID","VCB","VIB","MBB","TCB","HDB","STB"]
retail_code = ["AAT","BSC","ABR","AMD","BTT","DGW","MWG"]
years = ["2016","2017","2018","2019","2020","2021"]

# bank: 17, CPLV: 1
#MWG: 16, CPLV:7

def getRate(code):
	classA = defaultdict(list)
	classB = defaultdict(list)
	classC = defaultdict(list)
	classD = defaultdict(list)
	classE = defaultdict(list)
	classF = defaultdict(list)
	allClasses = defaultdict(list)
	bankRate = defaultdict(list)
	for bank in code:
		dataBank = financial_report (symbol= bank, report_type='IncomeStatement', frequency='yearly')
		bankEbit=[]
		bankEbitDict={}
		for column in dataBank.columns:
			#note that the colum 15 and 16 of the retail is fucked up
			if (code[0] =="AAT" and "Chi phí lãi vay" in dataBank.iloc[7,0] and "ròng trước thuế" in dataBank.iloc[15,0] ):
				for year in years:
					if year in column:
						income = np.abs(dataBank.loc[16,column])
						interest = np.abs(dataBank.loc[7,column])
						ebit = income + interest
						tax = 0.2
						res = ebit*(1-tax)
						bankEbitDict[year]=res
						bankEbit.append(res)
						#print(bank,year, income,interest, res)
			if (code[0] =="CTG" and "Chi phí lãi" in dataBank.iloc[1,0] and "Tổng lợi nhuận trước thuế" in dataBank.iloc[17,0] ):
				for year in years:
					if year in column:
						income = np.abs(dataBank.loc[17,column])
						interest = np.abs(dataBank.loc[1,column])
						ebit = income + interest
						tax = 0.2
						res = ebit*(1-tax)
						bankEbitDict[year]=res
						bankEbit.append(res)

		rateYearly={}
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
		smaller={}

		if all(value >= 15 for value in rateYearly.values()):
			print("Classs A: ",bank,",".join(str(v) for v in rateYearly.values()),"\n")
			if bank in classA[bank]:
				classA[bank] = bankRate[bank]
			else:
				classA[bank].append(bankRate[bank])
		else:
			for i,j in rateYearly.items():
				if j < 15:
					smaller[i] = j

		if len(smaller) == 1:
			#print("Class B:", bank, "01 year < 15%: ", list(smaller.keys())[0],"\n")
			if bank in classB[bank]:
				classB[bank] = bankRate[bank]
			else:
				classB[bank].append(bankRate[bank])
		elif len(smaller) ==2:
			#print("Class C:", bank, "has %d years < 15: " %len(smaller), ",".join(smaller.keys()),"\n")
			if bank in classC[bank]:
				classC[bank] = bankRate[bank]
			else:
				classC[bank].append(bankRate[bank])
		elif len(smaller) ==3:
			#print("Class D:", bank, "has %d years < 15: " %len(smaller), ",".join(smaller.keys()),"\n")
			if bank in classD[bank]:
				classD[bank] = bankRate[bank]
			else:
				classD[bank].append(bankRate[bank])
		elif len(smaller) ==4:
			#print("Class E:", bank, "has %d years < 15: " %len(smaller), ",".join(smaller.keys()),"\n")
			if bank in classE[bank]:
				classE[bank] = bankRate[bank]
			else:
				classE[bank].append(bankRate[bank])	

	allClasses["A"] = classA
	allClasses["B"] = classB
	allClasses["C"] = classC
	allClasses["D"] = classD
	allClasses["E"] = classE
	print('all :', json.dumps(allClasses, indent=4))

vcb = financial_report (symbol= "MWG", report_type='IncomeStatement', frequency='yearly')
#mwg = financial_report (symbol= "MWG", report_type='IncomeStatement', frequency='yearly')

print(vcb)
#print(mwg)

getRate(bank_code)




