import pandas as pd
import numpy as np
import math
from collections import defaultdict
import json
import argparse
import os

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

directory = 'data/2023/'

def getRate(bank, period):
	global CEO
	global tax
	global directory

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
	
	#print(cashData)
	# for column in balanceData.columns:
	# 	if("Vay ngắn hạn" in balanceData.iloc[73,0]):
	# 		for year in years:
	# 			if year in column:
	# 				print(year)
	# 				shortLoan = np.abs(balanceData.loc[73,column])
	# 				print(shortLoan)
	#print(balanceData.loc[75][0])
	#print(balanceData.loc[75][0],"\n", balanceData.loc[88][0],"\n", balanceData.loc[95][0],"\n", balanceData.loc[1][0],"\n", balanceData.loc[65][0]\
	#	,"\n", cashData.loc[22][0],"\n", cashData.loc[23][0],"\n", cashData.loc[3][0])

	# print(cashData)

	# balanceData = financial_report (symbol= bank, report_type='BalanceSheet', frequency='yearly')
	# cashData = financial_report (symbol= bank, report_type='cashflow', frequency='yearly')

	#print(incomeData.loc[7][0],incomeData.loc[16][0], incomeData.loc[20][0])

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

	for column in balanceData.columns:
		if("Vay ngắn hạn" in balanceData.loc[75][0] and "Vay dài hạn" in balanceData.loc[88][0] and "VỐN CHỦ SỞ HỮU" in balanceData.loc[95][0]\
				and "TÀI SẢN NGẮN HẠN" in balanceData.loc[1][0] and "Nợ ngắn hạn" in balanceData.loc[65][0] and "Tiền mua tài sản cố định và các tài sản dài hạn khác" in cashData.loc[22][0]\
				 and "Tiền thu được từ thanh lý tài sản cố định" in cashData.loc[23][0] and "Khấu hao TSCĐ" in cashData.loc[3][0]):
			for year in years:
				if year in column:
					# Co cau Von
					shortLoan = np.abs(balanceData.loc[75,column])
					shortLoanYears[year]= shortLoan

					longloan = np.abs(balanceData.loc[88,column])
					totalLoan = shortLoan + longloan
					totalDebt[year] = totalLoan

					equity = np.abs(balanceData.loc[95,column])
					totalEquity[year] = equity

					shortAsset = np.abs(balanceData.loc[1,column])
					shortAssetYears[year] = shortAsset

					shortDebt = np.abs(balanceData.loc[65,column])
					shortDebtYears[year] = shortDebt

					buyAsset = np.abs(cashData.loc[22,column])
					buyAssetYears[year] = buyAsset

					liqAsset = np.abs(cashData.loc[23,column])
					liqAssetYears[year] = liqAsset

					depreData = np.abs(cashData.loc[3, column])
					depreDataYears[year] = depreData


					
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
			perdiod = str(list(bankEbitDict.keys())[ebit]) + "-" + str(list(bankEbitDict.keys())[ebit+1])
			result = ceil(ebit1t * 100, 2)
			rateYearly[perdiod] = result
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
	print(roaeYearly)
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
																for bworkingcap, vworkingcap in bankWorkingCapitalChangedYears.items():
																	for breinvest, vreinvest in bankReinvestFixedAsset.items():
																		for btotalreinvest, vtotalreinvest in bankTotalReInvestDict.items():
																			for bfreecash, vfreecash in freeProfitCashDict.items():
																				for bproinvest, vproinvest in proReinvestYearlyDict.items():
																					if name == x == i == a == c == e == p == l == o == bwacc == bwaccav == broce == bworkingcap == btotalreinvest == bproinvest:
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
									

	#allClasses[bank] = classA
	result = json.dumps(classA, indent=4)
	print(result)



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--code', type=str, help='a company code')
	parser.add_argument('--type', type=str, help='Yearly/Quarterly')
	try:
		args = parser.parse_args()
	except argparse.ArgumentError as e:
		print("Error:", e.message)
		sys.exit(1)
	
	code = args.code
	period = args.type
	getRate(code,period)
	#getFile("DGW")




