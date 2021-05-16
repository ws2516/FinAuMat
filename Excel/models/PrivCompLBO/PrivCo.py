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
	
#Assumptions ~ each of these will become a class

purchaseMultiple = 5 #float

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


#computations

class incomeStatement:

	def __init__(self):

EBITDAStart = revenueStart * EBITDAMargin
purchasePrice = purchaseMultiple * EBITDAStart

debtRequired = (int(debtToEquity.split(':')[0])/100) * purchasePrice
equityRequired = (int(debtToEquity.split(':')[1])/100) * purchasePrice

revenue = Revenue(revenueStart, revenueGrowth, timeFrame)

ebitda = EBITDA(revenue.Projection, EBITDAMargin)
daa = DaA(depreciation, amortization, revenue.Projection)

ebit = EBIT(ebitda.Projection, daa.Projection)
debtinterest = debtInterest(debtRequired, interestRate, revenue.Projection)

ebt = EBT(ebit.Projection, debtinterest.Projection)
taxcalc = taxCalc(ebt.Projection, taxRate)

netincome = netIncome(ebt.Projection, taxcalc.Projection)

incomeStatement = pd.DataFrame({ 
					'Revenue':revenue.Projection,
					'EBITDA':ebitda.Projection,
					'D&A':daa.Projection,
					'EBIT':ebit.Projection,
					'Debt Interest':debtinterest.Projection,
					'EBT':ebt.Projection,
					'Tax Expense':taxcalc.Projection,
					'Next Income':netincome.Projection})

print(incomeStatement.T.round(2))
					
