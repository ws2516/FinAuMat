'''

Getting a bit more complex with: http://www.streetofwalls.com/finance-training-courses/private-equity-training/lbo-modeling-test-example/

Here the focus will be on sources and uses and debt schedule as well as building out a 
clear integrated financial statement system

	Income 
		Line Items
	Balance
		Line Items
	Cash
		Line Items

implementing now
use an int to define how many instances of line items you have (let this drive the loop constructor)

ideas
use a checkbox to define which items are to be counted in the Balance sheet, this abotuu hwoyou can make this an indicator for the future

'''

import pandas as pd
import math
import numpy as np


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

class projectionPass:
	def __init__(self, list1, list2, op):
		self.Projection = listOp(list1,list2, op)

class itemized:
	
	def __init__(self, initial, growthRate, lineItems, years):
		for i in range(len(lineItems)):
			setattr(self, lineItems[i].upper()+'PROJECTION', self.project(initial[i],growthRate[i], years)) #we use upper so we have to keep this for now
		self.Projection = self.sumAll() #listOp(self.all()[0],self.all()[1], '+')
	
	def project(self, initial, growthRate, years):
		return [initial * (1+growthRate)**i for i in range(0,years)]
	
	def sumAll(cls): # I dont like this but it works
		returnAll = [value for name, value in vars(cls).items() if name.isupper()]
		sums = np.zeros(len(returnAll[0]))
		for i in returnAll:
			sums += i
		return sums

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

class totalDebt:

	def __init__(self, leverageSource, leverageMultiple, leverageFees, years, startingEBITDA):
		for i in range(len(leverageSource)):
			setattr(self, leverageSource[i].upper()+'DEBT', leverageMultiple[i]*startingEBITDA) #we use upper so we have to keep this for now
			setattr(self, leverageSource[i].lower()+'debtfeesperyear', leverageFees[i]*leverageMultiple[i]*startingEBITDA/years)
		self.TotalLeverage = self.sumAllTotals() #listOp(self.all()[0],self.all()[1], '+')
		self.TotalLeverageFees = self.sumAllFees()
	
	def sumAllTotals(cls): # I dont like this but it works
		returnAll = [value for name, value in vars(cls).items() if name.isupper()]
		sums = 0
		for i in returnAll:
			sums += i
		return sums
	
	def sumAllFees(cls): # I dont like this but it works
		returnAll = [value for name, value in vars(cls).items() if name.islower()]
		sums = 0
		for i in returnAll:
			sums += i
		return sums
		
class valuationTable:
	
	def __init__(self, IS, debt, cash):
		self.transactionValue = IS.purchasePrice
		
		self.debt = Less(debt)[0] #will need to come from BS
		self.cash = cash[0] #will need to come from BS
		
		self.offerValue = self.transactionValue + self.debt + self.cash
		
class Uses:
	
	def __init__(self, purchase, existingDebt, financingFees, transactionCosts):
		self.purchase = purchase
		self.existingDebt = existingDebt
		self.financingFees = financingFees
		self.transactionCosts = transactionCosts
		self.totalUses = purchase + existingDebt + financingFees + transactionCosts

class Sources:
	
	def __init__(self, totalDebt, cashOnHand, sponsorEquity, uses):
		debtNames = [name for name, value in vars(totalDebt).items() if name.islower()]
		debtValues = [value for name, value in vars(totalDebt).items() if name.islower()]
		for i in range(len(debtNames)):
			setattr(self, debtNames[i], debtValues[i])
		self.totalSources = uses.totalUses
		self.cashOnHand = cashOnHand
		self.sponsorEquity = self.totalSources - np.sum(debtValues) - self.cashOnHand
		
		


#statements
class incomeStatement:

	kind = 'Income Statement'
	def __init__(self,
				 purchaseMultiple,
				 debtToEquity,
				 interestRate,
				 
				 revenueStart,
				 revenueLineItems,
				 revenueGrowth,
				 
				 cogsStart,
				 cogsLineItems,
				 cogsGrowth,
				 
				 sgaStart,
				 sgaLineItems,
				 sgaGrowth,				 
				 
				 depreciation,
				 amortization,
				 taxRate,
				 timeFrame
				 ):
		self.purchaseMultiple = purchaseMultiple
		self.debtToEquity = debtToEquity
		self.interestRate = interestRate
		
		self.revenueStart = revenueStart
		self.revenueLineItems = revenueLineItems
		self.revenueGrowth = revenueGrowth
		
		self.cogsStart = cogsStart
		self.cogsLineItems = cogsLineItems
		self.cogsGrowth = cogsGrowth
		
		self.sgaStart = sgaStart
		self.sgaLineItems = sgaLineItems
		self.sgaGrowth = sgaGrowth

		self.depreciation = depreciation
		self.amortization = amortization
		self.taxRate = taxRate
		self.timeFrame = timeFrame
	
	def calculate(self):
		
		self.revenue = itemized(self.revenueStart, self.revenueGrowth, self.revenueLineItems, self.timeFrame)
		
		self.cogs = itemized(self.cogsStart, self.cogsGrowth, self.cogsLineItems, self.timeFrame)
		self.grossprofit = projectionPass(self.revenue.Projection, Less(self.cogs.Projection), '+')
		
		self.sga = itemized(self.sgaStart, self.sgaGrowth, self.sgaLineItems, self.timeFrame)
		self.ebitda = projectionPass(self.grossprofit.Projection, Less(self.sga.Projection),'+')

		self.EBITDAStart = self.ebitda.Projection[0]
		
		self.purchasePrice = self.purchaseMultiple * self.EBITDAStart
		
		self.debtRequired = (int(self.debtToEquity.split(':')[0])/100) * self.purchasePrice
		self.equityRequired = (int(self.debtToEquity.split(':')[1])/100) * self.purchasePrice
		
		self.daa = DaA(self.depreciation, self.amortization, self.revenue.Projection)
		
		self.ebit = EBIT(self.ebitda.Projection, self.daa.Projection)
		self.debtinterest = debtInterest(self.debtRequired, self.interestRate, self.revenue.Projection)
		
		self.ebt = EBT(self.ebit.Projection, self.debtinterest.Projection)
		self.taxcalc = taxCalc(self.ebt.Projection, self.taxRate)
		
		self.netincome = netIncome(self.ebt.Projection, self.taxcalc.Projection)
		
		#automate this
		self.incomeStatementRaw = pd.DataFrame({ 
					'Revenue':self.revenue.Projection,
					'COGS':self.cogs.Projection,
					'Gross Profit':self.grossprofit.Projection,
					'SGA':self.sga.Projection,
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

class sourcesAndUses:
	
	def __init__(self, valuation):
		
		self.transactionValue = valuation.offerValue
		print(self.transactionValue)	

#Assumptions ~ each of these will become a class

purchaseMultiple = 5 #float
exitMultiple = 5 #float

#Extraneous Transaction Costs
startingDebt = [0] #this will be in the BS - a placeholder
startingCash = [0] #this will be in the BS - a placeholder
revolverExists = True #boolean to be a revolver
revolverEBITDAMult = 3 #float and x indicator
revolverAvailability = 90977 #float and 000s indicator
minCash = 5 #float and 000s indicator
MaAFee = 1.5 #float and 000s indicator
existingManagementEquity = 10/100 #float ~ must be a percent
managementRollover = 50/100 #float ~ must be a percent

debtTypes = ['bank','sub','PIK']
debtLeverage = [3,2,2]
debtInterestFees = [2/100,3/100,3/100]

debtToEquity = '60:40' # NEEDS TO TAKE INTO ACCOUNT MANAGEMENT ROLLOVER

interestRate = 10/100 #float ~ must be a percent

revenueStart = [10,10] #list 000s indicator
revenueLineItems = ['TShirt', 'Pants'] #strings name of lineitem
revenueGrowth = [10/100, 10/100] #list must be a percent

cogsStart = [4.5,4.5]#float and 000s indicator
cogsLineItems = ['Fake', 'Cogs'] #strings name of lineitem
cogsGrowth = [9/100, 9/100] #list must be a percent

sgaStart = [1.8,1.1]#list 000s indicator
sgaLineItems = ['GA', 'Sales'] #strings name of lineitem
sgaGrowth = [5/100, 5.5/100] #list must be a percent

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
				 revenueLineItems,
				 revenueGrowth,
				 
				 cogsStart,
				 cogsLineItems,
				 cogsGrowth,
				 
				 sgaStart,
				 sgaLineItems,
				 sgaGrowth,
				 
				 depreciation,
				 amortization,
				 taxRate,
				 timeFrame)
IS.calculate()

valuation = valuationTable(IS, startingDebt, startingCash)

CFS = cashFlowStament(IS, 
					  CAPEX, 
					  WCGrowth)
CFS.calculate()


Uses(purchase, existingDebt, financingFees, transactionCosts))
print(Sources(totalDebt(debtTypes, debtLeverage, debtInterestFees, timeFrame+1, IS.EBITDAStart),0,Uses()))


cummulativeCashFlow = sum(CFS.fcf) #be careful about the length of fcf
exitEBITDA = IS.ebitda.Projection[-1] #be careful with year, this is the "last year"
TEV = exitMultiple * exitEBITDA
netDebtAtExit = IS.debtRequired - cummulativeCashFlow
ev = TEV - netDebtAtExit
moi = ev / IS.equityRequired
irr = IRR(moi, timeFrame)


					
