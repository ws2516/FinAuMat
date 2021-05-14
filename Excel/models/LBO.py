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

	def __init__(self, years):
		self.rev = self.assumptions('starting revenue?')
		self.revGrowthInitial = self.assumptions('initial revenue growth rate?')
		self.revGrowthEnding = self.assumptions('final revenue growth rate?')
		self.revGrowthStep = self.stepCalc(self.revGrowthInitial, self.revGrowthEnding, years)
		self.revGrowth = [self.revGrowthInitial + i*self.revGrowthStep for i in range(1,int(years)+1)]
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
	
	def __init__(self, years, revProjection):
		self.cogs = self.assumptions('starting COGs?')
		self.cogsGrowthInitial = self.assumptions('initial COGs margin (as % of Rev)?')
		self.cogsGrowthEnding = self.assumptions('final COGs margin (as % of Rev)?')
		self.cogsGrowthStep = self.stepCalc(self.cogsGrowthInitial, self.cogsGrowthEnding, years)
		self.cogsGrowth = [self.cogsGrowthInitial + i*self.cogsGrowthStep for i in range(0,int(years)+1)]
		self.cogsProjection = [revProjection[i] * self.cogsGrowth[i] for i in range(len(revProjection))]
		print(self.cogsProjection, self.cogsGrowth, self.cogsGrowthStep)

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
		print(self.opexProjection)
	
	def stepCalc(self, initial, ending, steps):
		return round( (ending - initial)/steps , 5 )
			
	def assumptions(self,  string ):
		return float(input('What is the input for ' + string + ' '))
		
		
class OpExs:

	kind = 'OpEx'
	
	def __init__(self, nameList, projection):
		for i in nameList:
			setattr(self, i, projection)


class incomeStatement:
	
	kind = 'Income Statement'
	
	def __init__(self):
		
		self.years = self.assumptions('modeled years?')
		
		#Make these subclasses? These go into EBITDA
		Revenues = Revenue(self.years)
		self.revProjection = Revenues.revProjection
		self.revGrowth = Revenues.revGrowth
		
		COGS = COGs(self.years, self.revProjection)
		self.cogsProjection = COGS.cogsProjection
		self.cogsGrowth = COGS.cogsGrowth
		
		self.grossProfit = [self.revProjection[i]-self.cogsProjection[i] for i in range(0,int(self.years)+1)]
		self.grossProfitMargin = [self.grossProfit[i]/self.revProjection[i] for i in range(0,int(self.years)+1)]
		
		
		#make this a function
		OpExNames = input('What are the OpEx Expenses, input in a list like the following: SGA, Sales and Marketing, ... (Please ensure you use a comma)')
		OpExProjectionList, OpExMarginList = [], []
		for i in OpExNames.split(','):
			temp = OpEx(self.years, self.revProjection, i)
			OpExProjectionList += [temp.opexProjection]
			OpExMarginList  += [temp.opexGrowth]
		
			setattr(self, i+'Margin', temp.opexGrowth)
			setattr(self, i+'Projection', temp.opexProjection)
			
		self.totalOpExProjection = [sum(x) for x in zip(*OpExProjectionList)]
		self.totalOpExMargin = [sum(x) for x in zip(*OpExMarginList)]
		print(self.totalOpExProjection, self.totalOpExMargin)
		
		self.EBITDA = [self.revProjection[i]-self.cogsProjection[i]-self.totalOpExProjection[i] for i in range(0,int(self.years)+1)]
		self.EBITDAMargin = [self.EBITDA[i]/self.revProjection[i] for i in range(0,int(self.years)+1)]
		print(self.EBITDA, self.EBITDAMargin)
		
		fA = financingAssumptions(self.EBITDA[0], self.years)
		
		self.depr = self.assumptions('starting Depreciation?')
		self.deprGrowthInitial = self.assumptions('initial Depreciation margin (as % of Rev)?')
		self.deprGrowthEnding = self.assumptions('final Depreciation margin (as % of Rev)?')
		self.deprGrowthStep = self.stepCalc(self.deprGrowthInitial, self.deprGrowthEnding, self.years)
		self.deprGrowth = [self.deprGrowthInitial + i*self.deprGrowthStep for i in range(0,int(self.years)+1)]
		self.deprProjection = [self.revProjection[i] * self.deprGrowth[i] for i in range(len(self.revProjection))]
		print(self.deprProjection)

		self.amort = self.assumptions('starting Amortization?')
		self.amortProjection = [self.amort]+[self.amort + fA.totalLevCost]*(len(self.revProjection)-1)
		print(self.amortProjection)		
		
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