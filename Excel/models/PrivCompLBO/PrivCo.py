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

#Assumptions

purchaseMultiple = 5 #float

debtToEquity = '60:40' #string
interestRate = 10 / 100 #float ~ must be a percent

revenueStart = 100 000 000#float and 000s indicator
revenueGrowth = 10 / 100 #float ~ must be a percent

EBITDAMargin = 40 / 100 #float ~ must be a percent

CAPEX = 15 / 100 #float ~ must be a percent of revenue

WCGrowth = 5 000 000 #float and 000s indicator

taxRate = 40 / 100 #float ~ must be a percent

timeFrame = 5 #int years

debtPaydownAtCompletion = True #boolean toggle


#computations

EBITDA = EBITDAMargin * revenueStart
purchasePrice = multiple * EBITDA

debtRequired = (int(debtToEquity.split(':')[0])/100) * purchasePrice
equityRequired = (int(debtToEquity.split(':')[1])/100) * purchasePrice


#classes
class incomeStatement:

	def __init__(self, purchaseMultiple, debtPaydownAtCompletion):
		self.purchaseMultiple = purchaseMultiple
		self.debtToEquity = debtToEquity

	def purchasePrice(self.multiple, self.EBITDA):
		
		return self.purchasePrice = multiple*EBITDA

class balanceSheet:

	def __init__(self, purchaseMultiple, debtPaydownAtCompletion):
		self.purchaseMultiple = purchaseMultiple
		self.debtToEquity = debtToEquity

	def purchasePrice(self.multiple, self.EBITDA):
		
		return self.purchasePrice = multiple*EBITDA

#classes
class cashFlowStatement:

	def __init__(self, purchaseMultiple, debtPaydownAtCompletion):
		self.purchaseMultiple = purchaseMultiple
		self.debtToEquity = debtToEquity

	def purchasePrice(self.multiple, self.EBITDA):
		
		return self.purchasePrice = multiple*EBITDA
	

