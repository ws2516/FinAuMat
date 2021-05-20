from operator import add

class financingAssumptions:

	kind = 'Financing Assumptions'

	def __init__(self, EBITDA, years):

		self.EBITDA = EBITDA
		self.years = years + 2

		self.bankDebtLev = self.assumptions('Bank Debt leverage?')
		self.subDebtLev = self.assumptions('Sub Debt leverage?')
		self.pikSubDebtLev = self.assumptions('PIK Sub Debt leverage?')

		self.bankDebt = self.bankDebtLev * self.EBITDA
		self.subDebt = self.subDebtLev * self.EBITDA
		self.pikSubDebt = self.pikSubDebtLev * self.EBITDA

		self.totalLeverage = self.bankDebt + self.subDebt + self.pikSubDebt

		self.bankDebtFee = self.assumptions('Bank Debt Fee (as Decimal)?')
		self.subDebtFee = self.assumptions('Sub Debt Fee (as Decimal)?')
		self.pikSubDebtFee = self.assumptions('PIK Sub Debt Fee (as Decimal)?')

		self.bankDebtFeeDol = self.bankDebtFee * self.bankDebt
		self.subDebtFeeDol = self.subDebtFee * self.subDebt
		self.pikSubDebtFeeDol = self.pikSubDebtFee * self.pikSubDebt

		self.totalDebtFees = self.bankDebtFeeDol + self.subDebtFeeDol + self.pikSubDebtFeeDol

		self.bankDebtpYear, self.subDebtpYear, self.pikDebtpYear = self.bankDebtFeeDol/self.years, self.subDebtFeeDol/self.years, self.pikSubDebtFeeDol/self.years

		self.totalLevCost = self.bankDebtpYear + self.subDebtpYear + self.pikDebtpYear


	def assumptions(self,  string ):
		return float(input('What is the input for ' + string + ' '))

class Revenue:

	kind = 'Revenue'

	def __init__(self, years, named):
		self.rev = self.assumptions('starting ' + str(named) + '?')
		self.revGrowthInitial = self.assumptions('initial '+ str(named) + ' growth rate (as % per year)?')
		self.revGrowthEnding = self.assumptions('final '+ str(named) + ' growth rate (as % per year)?')
		self.revGrowthStep = self.stepCalc(self.revGrowthInitial, self.revGrowthEnding, years)
		self.revGrowth = [self.revGrowthInitial + i*self.revGrowthStep for i in range(0,int(years))]
		self.revProjection = self.project(self.rev, self.revGrowth)


	def project(self, initial, rateList):
		temp = [initial]
		for i in rateList:
			temp.append( round( temp[-1]*(1+i) , 5 ) )
		return temp

	def stepCalc(self, initial, ending, steps):
		return round( (ending - initial)/steps , 5 )

	def assumptions(self,  string ):
		return float(input('What is the input for ' + string + ' '))

class COGs:

	kind = 'COGS'

	def __init__(self, years, revProjection, named):
		self.cogs = self.assumptions('starting ' + str(named) + '?')
		self.cogsGrowthInitial = self.assumptions('initial '+ str(named) + ' margin (as % of Rev)?')
		self.cogsGrowthEnding = self.assumptions('final '+ str(named) + ' margin (as % of Rev)?')
		self.cogsGrowthStep = self.stepCalc(self.cogsGrowthInitial, self.cogsGrowthEnding, years)
		self.cogsGrowth = [self.cogsGrowthInitial + i*self.cogsGrowthStep for i in range(0,int(years)+1)]
		self.cogsProjection = [revProjection[i] * self.cogsGrowth[i] for i in range(len(revProjection))]

	def stepCalc(self, initial, ending, steps):
		return round( (ending - initial)/steps , 5 )

	def assumptions(self,  string ):
		return float(input('What is the input for ' + string + ' '))

class OpEx:

	kind = 'OpEx'

	def __init__(self, years, revProjection, named):
		self.opex = self.assumptions('starting ' + str(named) + '?')
		self.opexGrowthInitial = self.assumptions('initial '+ str(named) + ' margin (as % of Rev)?')
		self.opexGrowthEnding = self.assumptions('final '+ str(named) + ' margin (as % of Rev)?')
		self.opexGrowthStep = self.stepCalc(self.opexGrowthInitial, self.opexGrowthEnding, years)
		self.opexGrowth = [self.opexGrowthInitial + i*self.opexGrowthStep for i in range(0,int(years)+1)]
		self.opexProjection = [revProjection[i] * self.opexGrowth[i] for i in range(len(revProjection))]

	def stepCalc(self, initial, ending, steps):
		return round( (ending - initial)/steps , 5 )

	def assumptions(self,  string ):
		return float(input('What is the input for ' + string + ' '))

class Depreciation:

	kind = 'Depreciation'

	def __init__(self, years, revProjection, named):
		self.depr = self.assumptions('starting ' + str(named) + '?')
		self.deprGrowthInitial = self.assumptions('initial '+ str(named) + ' margin (as % of Rev)?')
		self.deprGrowthEnding = self.assumptions('final '+ str(named) + ' margin (as % of Rev)?')
		self.deprGrowthStep = self.stepCalc(self.deprGrowthInitial, self.deprGrowthEnding, years)
		self.deprGrowth = [self.deprGrowthInitial + i*self.deprGrowthStep for i in range(0,int(years)+1)]
		self.deprProjection = [revProjection[i] * self.deprGrowth[i] for i in range(len(revProjection))]

	def stepCalc(self, initial, ending, steps):
		return round( (ending - initial)/steps , 5 )

	def assumptions(self,  string ):
		return float(input('What is the input for ' + string + ' '))

class iterativeBuilder:

	kind = 'Builder'

	def __init__(self, item, years, revProjection):
		Names = input('What are the ' + item + ' Expenses, input in a list like the following: Item A, Item B, Item C, ... (Please ensure you use a comma)')
		if revProjection != 'None':
			ProjectionList, MarginList = [], []
			for i in Names.split(','):
				if item == 'COGS':
					temp = COGs(years, revProjection, i)
					ProjectionList += [temp.cogsProjection]
					MarginList  += [temp.cogsGrowth]
					setattr(self, i+'Margin', temp.cogsGrowth)
					setattr(self, i+'Projection', temp.cogsProjection)

				elif item == 'OpEx':
					temp = OpEx(years, revProjection, i)
					ProjectionList += [temp.opexProjection]
					MarginList  += [temp.opexGrowth]
					setattr(self, i+'Margin', temp.opexGrowth)
					setattr(self, i+'Projection', temp.opexProjection)

				elif item == 'Depreciation':
					temp = Depreciation(years, revProjection, i)
					ProjectionList += [temp.deprProjection]
					MarginList  += [temp.deprGrowth]
					setattr(self, i+'Margin', temp.deprGrowth)
					setattr(self, i+'Projection', temp.deprProjection)
				else:
					print('No appropriate line item for this')
			self.Projection = [sum(x) for x in zip(*ProjectionList)]
			self.Margin = [sum(x) for x in zip(*MarginList)]

		else:
			ProjectionList, MarginList = [], []
			for i in Names.split(','):
				if item == 'Revenue':
					temp = Revenue(years, i)
					ProjectionList += [temp.revProjection]
					MarginList  += [temp.revGrowth]
					setattr(self, i+'Margin', temp.revGrowth)
					setattr(self, i+'Projection', temp.revProjection)

				else:
					print('No appropriate line item for this')

			self.Projection = [sum(x) for x in zip(*ProjectionList)]
			self.Growth = [sum(x) for x in zip(*MarginList)]

class balanceSheet:

	'''
	BS 2003
			Assets
				CA with WC toggle
				PPE
				Other with intangibles/asset top right toggle
			Liabilities
				shoulld be one class, maybe another for WC toggle

			Equity
		Do a A - L = E check

	WC
		Use BS 2003 and IS to get all WC for toggled vars

	BS 2003 Pro Forma Stuff - this needs an explanation

	Cash Flow

	Debt Paydown


	Project BS 2004 Onwards

	Project CFS 2004 Onwards

	Project Debt Paydown 2004 Onwards

	Finish Income Statement'''



class incomeStatement:

	kind = 'Income Statement'

	def __init__(self):

		self.years = self.assumptions('modeled years?')

		Rev = iterativeBuilder('Revenue', self.years, 'None')
		self.revProjection = Rev.Projection
		self.revGrowth = Rev.Growth

		COGS = iterativeBuilder('COGS', self.years, self.revProjection)
		self.totalCOGSProjection = COGS.Projection
		self.totalCOGSMargin = COGS.Margin

		self.grossProfit = [self.revProjection[i]-self.totalCOGSProjection[i] for i in range(0,int(self.years)+1)]
		self.grossProfitMargin = [self.grossProfit[i]/self.revProjection[i] for i in range(0,int(self.years)+1)]

		OpEx = iterativeBuilder('OpEx', self.years, self.revProjection)
		self.totalOpExProjection = OpEx.Projection
		self.totalOpExMargin = OpEx.Margin

		self.EBITDA = [self.revProjection[i]-self.totalCOGSProjection[i]-self.totalOpExProjection[i] for i in range(0,int(self.years)+1)]
		self.EBITDAMargin = [self.EBITDA[i]/self.revProjection[i] for i in range(0,int(self.years)+1)]

		fA = financingAssumptions(self.EBITDA[0], self.years)

		Dep = iterativeBuilder('Depreciation', self.years, self.revProjection)
		self.totalDepreciationProjection = Dep.Projection
		self.totalDepreciationMargin = Dep.Margin

		self.amort = self.assumptions('starting Amortization?')
		self.amortProjection = [self.amort]+[self.amort + fA.totalLevCost]*(len(self.revProjection)-1)

		self.EBIT = [self.EBITDA[i]-self.deprProjection[i]-self.amortProjection[i] for i in range(0,int(self.years)+1)]
		self.EBITMargin = [self.EBIT[i]/self.revProjection[i] for i in range(0,int(self.years)+1)]

		self.taxes = self.assumptions('income taxes?')

	def project(self, initial, rateList):
		temp = [initial]
		for i in rateList:
			temp.append( round( temp[-1]*(1+i) , 5 ) )
		return temp

	def stepCalc(self, initial, ending, steps):
		print(initial, ending, steps, round((ending - initial)/steps,5))
		return round( (ending - initial)/steps , 5 )

	def assumptions(self,  string ):
		return float(input('What is the input for ' + string + ' '))





test = incomeStatement()
print(test.EBIT)
