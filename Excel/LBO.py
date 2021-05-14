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



class incomeStatement:
	
	kind = 'Income Statement'
	
	def __init__(self):
		
		self.taxes = self.assumptions('income taxes?')
		self.years = self.assumptions('modeled years?')
		
		#Make these subclasses? These go into EBITDA
		self.rev = self.assumptions('starting revenue?')
		self.revGrowthInitial = self.assumptions('initial revenue growth rate?')
		self.revGrowthEnding = self.assumptions('final revenue growth rate?')
		self.revGrowthStep = self.stepCalc(self.revGrowthInitial, self.revGrowthEnding, self.years)
		self.revGrowth = [self.revGrowthInitial + i*self.revGrowthStep for i in range(1,int(self.years)+1)]
		self.revProjection = self.project(self.rev, self.revGrowth)
		print(self.revProjection)
		
		self.cogs = self.assumptions('starting COGs?')
		self.cogsGrowthInitial = self.assumptions('initial COGs margin (as % of Rev)?')
		self.cogsGrowthEnding = self.assumptions('final COGs margin (as % of Rev)?')
		self.cogsGrowthStep = self.stepCalc(self.cogsGrowthInitial, self.cogsGrowthEnding, self.years)
		self.cogsGrowth = [self.cogsGrowthInitial + i*self.cogsGrowthStep for i in range(0,int(self.years)+1)]
		self.cogsProjection = [self.revProjection[i] * self.cogsGrowth[i] for i in range(len(self.revProjection))]
		print(self.cogsProjection, self.cogsGrowth, self.cogsGrowthStep)
		
		self.ga = self.assumptions('starting SGA?')
		self.gaGrowthInitial = self.assumptions('initial SGA margin (as % of Rev)?')
		self.gaGrowthEnding = self.assumptions('final SGA margin (as % of Rev)?')
		self.gaGrowthStep = self.stepCalc(self.gaGrowthInitial, self.gaGrowthEnding, self.years)
		self.gaGrowth = [self.gaGrowthInitial + i*self.gaGrowthStep for i in range(0,int(self.years)+1)]
		self.gaProjection = [self.revProjection[i] * self.gaGrowth[i] for i in range(len(self.revProjection))]
		print(self.gaProjection)

		self.sm = self.assumptions('starting Sales & Marketing?')
		self.smGrowthInitial = self.assumptions('initial Sales & Marketing margin (as % of Rev)?')
		self.smGrowthEnding = self.assumptions('final Sales & Marketing margin (as % of Rev)?')
		self.smGrowthStep = self.stepCalc(self.smGrowthInitial, self.smGrowthEnding, self.years)
		self.smGrowth = [self.smGrowthInitial + i*self.smGrowthStep for i in range(0,int(self.years)+1)]
		self.smProjection = [self.revProjection[i] * self.smGrowth[i] for i in range(len(self.revProjection))]
		print(self.smProjection)
		
		self.EBITDA = [self.revProjection[i]-self.cogsProjection[i]-self.gaProjection[i]-self.smProjection[i] for i in range(0,int(self.years)+1)]
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