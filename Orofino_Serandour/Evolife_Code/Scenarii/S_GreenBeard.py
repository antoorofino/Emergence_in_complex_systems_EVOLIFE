#!/usr/bin/env python3
##############################################################################
# EVOLIFE  http://evolife.telecom-paris.fr             Jean-Louis Dessalles  #
# Telecom Paris  2021                                      www.dessalles.fr  #
# -------------------------------------------------------------------------- #
# License:  Creative Commons BY-NC-SA                                        #
##############################################################################



##############################################################################
#  S_GreenBeard                                                              #
##############################################################################

import random
						
""" EVOLIFE: GreenBeard Scenario:
	This small experiment was proposed in Richard Dawkins's book
	*The selfish gene*. It shows how some interesting coupling
	between genes may emerge in a population.
	Suppose a given gene has two effects on its carriers:
	(1) they get a conspicuous characteristic, like a green beard;
	(2) they tend to behave altruistically toward green-bearded individuals.
	Such a gene is expected to invade the population, whereas its supposed
	allele (no green beard + no altruism) tends to disappear. 
	However, as soon as the gene gets split in two genes with their own alleles
	(green beard vs. no green beard, and altruism toward green beard vs.
	no altruism) then altruism disappears. 
"""
	#=============================================================#
	#  HOW TO MODIFY A SCENARIO: read Default_Scenario.py		 #
	#=============================================================#


import sys
if __name__ == '__main__':  sys.path.append('../..')  # for tests


######################################
# specific variables and functions   #
######################################

from Evolife.Scenarii.Default_Scenario import Default_Scenario

from Evolife.Tools.Tools import percent

class Scenario(Default_Scenario):

	######################################
	# Most functions below overload some #
	# functions of Default_Scenario	  #
	######################################

	def genemap(self):
		""" Defines the name of genes and their position on the DNA.
		Accepted syntax:
		['genename1', 'genename2',...]:   lengths and coding are retrieved from configuration
		[('genename1', 8), ('genename2', 4),...]:   numbers give lengths in bits; coding is retrieved from configuration
		[('genename1', 8, 'Weighted'), ('genename2', 4, 'Unweighted'),...]:	coding can be 'Weighted', 'Unweighted', 'Gray', 'NoCoding'
		"""
		return [('GreenBeard',1),('Nasty',1)]

	def start_game(self,members):
		""" defines what to be done at the group level before interactions
			occur - Used in 'life_game'
		"""
		for indiv in members:
			#Don't forget that scores MUST REMAIN POSITIVE
			# So include a line such as:
			indiv.score(30, FlagSet=True) # or whatever appropriate value to set scores to some initial value each year
		Default_Scenario.start_game(self, members)


	def interaction(self, indiv, partner):
		""" Genes control the behaviour of 'indiv' toward 'partner'
		"""
		if (not indiv.gene_value('GreenBeard')) and indiv.gene_value('Nasty') and partner.gene_value('GreenBeard'):
			indiv.score(self.Parameter('N_Payback'))
			partner.score(-self.Parameter('N_Attack'))
		elif indiv.gene_value('GreenBeard') and (not indiv.gene_value('Nasty')) and partner.gene_value('GreenBeard'):
			indiv.score(-self.Parameter('GB_Cost'))
			partner.score(self.Parameter('GB_Gift'))
		elif indiv.gene_value('GreenBeard') and indiv.gene_value('Nasty') and partner.gene_value('GreenBeard'):
			indiv.score(self.Parameter('N_Payback'))
			indiv.score(-self.Parameter('GB_N_Penalty'))
			partner.score(-self.Parameter('N_Attack'))
		if indiv.gene_value('Nasty'):
			indiv.score(-self.Parameter('N_Penalty'))

	def parents(self, candidates):
		"""
		If it is set to True, then GreenBeard carriers will not reproduce with nasty carriers.
		"""
		if not self.Parameter('N_Segregation'):
			return super().parents(candidates)
		try:	
			for i in range(10):
				m = random.choice(candidates)
				f = random.choice(candidates)
				if m[0].gene_value('Nasty') and f[0].gene_value('GreenBeard'):
					continue
				if f[0].gene_value('Nasty') and m[0].gene_value('GreenBeard'):
					continue
				return (m,f)
			return None
		except	IndexError:	return None
		
	def display_(self):
		""" Defines the name of genes and their position on the DNA.
		Accepted syntax:
		['genename1', 'genename2',...]:   lengths and coding are retrieved from configuration.
		[('genename1', 8), ('genename2', 4),...]:   numbers give lengths in bits; coding is retrieved from configuration.
		[('genename1', 8, 'Weighted'), ('genename2', 4, 'Unweighted'),...]:	coding can be 'Weighted', 'Unweighted', 'Gray', 'NoCoding'.
		Note that 'Unweighted' is unsuitable to explore large space.
		"""
		return [('green1','GreenBeard'),('red','Nasty')]





###############################
# Local Test                  #
###############################

if __name__ == "__main__":
	print(__doc__ + '\n')
	input('[Return]')
	
