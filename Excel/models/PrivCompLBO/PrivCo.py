'''

Starting simple with: http://www.streetofwalls.com/finance-training-courses/private-equity-training/paper-lbo-model-example/

To be determined: Class / Function Structure
Can this be done start to finish

This is the LBO CLass -

Structure:

LBO
	Income
		Line Items
	Balance
		Line Items
	Cash
		Line Items

The idea is that the final line items should always interact in the same way and the
LBO assumptions should be "standard" to a degree but we can build these out later

'''

import pandas as pd
import math

def IRR(MOI, years):
	return MOI**(1/(years-1))

def listOp(list1, list2, op):
	if op == '+':
		sum_list = [a + b for a, b in zip(list1, list2)]
		return sum_list

	elif op == '*':
		prod_list = [a * b for a, b in zip(list1, list2)]
		return prod_list

	elif op == '/':
		div_list = [a / b for a, b in zip(list1, list2)]
		return div_list

	else:
		print('Check your function definition.')

def Less(a):
	return [-1*i for i in a]

class Revenue:

	def __init__(self, initial, growthRate, years):
		self.Projection = [initial * (1+growthRate)**i for i in range(0,years)]

class EBITDA:
	def __init__(self, rev, margin): #margin needs to be a list in the end
		self.Projection = listOp(rev,[margin]*len(rev),'*')

class DaA:
	def __init__(self, depr, amort, rev): #these need to be lists in the end
		self.Projection = [depr + amort]*len(rev)

class EBIT:
	def __init__(self, EBITDA, DaA):
		self.Projection = listOp(EBITDA, Less(DaA) ,'+')

class debtInterest:
	def __init__(self, amount, interestRate, rev): #interestRate needs to be a list in the end
		self.Projection = listOp([amount]*len(rev), [interestRate]*len(rev) ,'*')

class EBT:
	def __init__(self, EBIT, debtInterest):
		self.Projection = listOp(EBIT, Less(debtInterest) ,'+')

class taxCalc:
	def __init__(self, ebt, taxRate): #interestRate needs to be a list in the end
		self.Projection = listOp(ebt, [taxRate]*len(ebt) ,'*')

class netIncome:
	def __init__(self, EBT, taxCalc):
		self.Projection = listOp(EBT, Less(taxCalc) ,'+')

class capEx:
	def __init__(self, rev, margin): #interestRate needs to be a list in the end
		self.Projection = listOp(rev, [margin]*len(rev) ,'*')

class FCF:
	def __init__(self, netincome, daa, capex, nwc):

		Plus = daa

		lessCapEx = Less(capex.Projection)
		lessNWC = Less(nwc)
		Lesses = listOp(lessCapEx, lessNWC, '+')

		adjustments = listOp(Plus, Lesses, '+')

		self.Projection = listOp(netincome, adjustments, '+') #will need some generalization work



#statements
class incomeStatement:

	kind = 'Income Statement'
	def __init__(self,
				 purchaseMultiple,
				 debtToEquity,
				 interestRate,
				 revenueStart,
				 revenueGrowth,
				 EBITDAMargin,
				 depreciation,
				 amortization,
				 taxRate,
				 timeFrame
				 ):
		self.purchaseMultiple = purchaseMultiple
		self.debtToEquity = debtToEquity
		self.interestRate = interestRate
		self.revenueStart = revenueStart
		self.revenueGrowth = revenueGrowth
		self.EBITDAMargin = EBITDAMargin
		self.depreciation = depreciation
		self.amortization = amortization
		self.taxRate = taxRate
		self.timeFrame = timeFrame

	def calculate(self):
		self.EBITDAStart = self.revenueStart * self.EBITDAMargin
		self.purchasePrice = self.purchaseMultiple * self.EBITDAStart

		self.debtRequired = (int(self.debtToEquity.split(':')[0])/100) * self.purchasePrice
		self.equityRequired = (int(self.debtToEquity.split(':')[1])/100) * self.purchasePrice

		self.revenue = Revenue(self.revenueStart, self.revenueGrowth, self.timeFrame)

		self.ebitda = EBITDA(self.revenue.Projection, self.EBITDAMargin)
		self.daa = DaA(self.depreciation, self.amortization, self.revenue.Projection)

		self.ebit = EBIT(self.ebitda.Projection, self.daa.Projection)
		self.debtinterest = debtInterest(self.debtRequired, self.interestRate, self.revenue.Projection)

		self.ebt = EBT(self.ebit.Projection, self.debtinterest.Projection)
		self.taxcalc = taxCalc(self.ebt.Projection, self.taxRate)

		self.netincome = netIncome(self.ebt.Projection, self.taxcalc.Projection)

		self.incomeStatementRaw = pd.DataFrame({
					'Revenue':self.revenue.Projection,
					'EBITDA':self.ebitda.Projection,
					'D&A':self.daa.Projection,
					'EBIT':self.ebit.Projection,
					'Debt Interest':self.debtinterest.Projection,
					'EBT':self.ebt.Projection,
					'Tax Expense':self.taxcalc.Projection,
					'Next Income':self.netincome.Projection})
		self.cleanIncomeStatement = self.incomeStatementRaw.T.round(2)

	def getStatement(self):
		self.calculate()
		return self.cleanIncomeStatement

class cashFlowStament:

	def __init__(self,
				 incomestatement,
				 capexMargin,
				 nwc ):

		self.incomestatement = incomestatement
		self.capexMargin = capexMargin
		self.nwc = nwc

	def calculate(self): #needs some generalization work
		self.netincome = self.incomestatement.netincome.Projection
		self.daa = self.incomestatement.daa.Projection
		self.capex =  capEx(self.incomestatement.revenue.Projection, self.capexMargin)#this will be changed and generalized
		self.nwc = [self.nwc]*len(self.daa) #this will be changed and generalized

		self.fcf = FCF(self.netincome, self.daa, self.capex, self.nwc).Projection[:-1] #needs ssome generalization work


#Assumptions ~ each of these will become a class

purchaseMultiple = 5 #float
exitMultiple = 5 #float

debtToEquity = '60:40' #string
interestRate = 10/100 #float ~ must be a percent

revenueStart = 100#float and 000s indicator
revenueGrowth = 10/100 #float ~ must be a percent

EBITDAMargin = 40/100 #float ~ must be a percent

depreciation = 20 #float and 000s indicator
amortization = 0 #float and 000s indicator

CAPEX = 15/100 #float ~ must be a percent of revenue

WCGrowth = 5 #float and 000s indicator

taxRate = 40/100 #float ~ must be a percent

timeFrame = 5 + 1 #int years

debtPaydownAtCompletion = True #boolean toggle


IS = incomeStatement(purchaseMultiple,
				 debtToEquity,
				 interestRate,
				 revenueStart,
				 revenueGrowth,
				 EBITDAMargin,
				 depreciation,
				 amortization,
				 taxRate,
				 timeFrame)
IS.calculate()


CFS = cashFlowStament(IS,
					  CAPEX,
					  WCGrowth)
CFS.calculate()

cummulativeCashFlow = sum(CFS.fcf) #be careful about the length of fcf
exitEBITDA = IS.ebitda.Projection[-1] #be careful with year, this is the "last year"
TEV = exitMultiple * exitEBITDA
netDebtAtExit = IS.debtRequired - cummulativeCashFlow
ev = TEV - netDebtAtExit
moi = EV / IS.equityRequired
irr = IRR(MOI, timeFrame)
