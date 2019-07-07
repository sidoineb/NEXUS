"""
Projet Nexus écrit par Sidoine B.
"""

print("############################################")
print("##           .: Nexus v0.1 :.             ##")
print("############################################\n")

print("  1) Conversion glycémie capillaire")
print("  2) Algo décision pose de collier cervical")
print("  3) Calcul NIH")
print("  4) Calcul score de Glasgow")
print("  5) Fiche d'intervention\n")

# Variables des choix

choix = [1,2,3,4]

choix = input("Tapez votre choix :")

# Choix de la glycémie capillaire

if choix == 1:
	print("Conversion valeurs Glycémie capillaire\n")
	print("1) Convertir g/L -> mmol/L")
	print("2) Convertir mmol/L -> g/L\n")

		choixGly = input("Tapez votre choix :\n")
          
		if choixGly == 1:
			ValeurGly1 = input("Entrez votre valeur en g/L :\n")
			try:
				ValeurGly1 = float(ValeurGly1)
				Valeurmmol = float(ValeurGly1) * 5.5
			except:
				print("Valeur incorrecte")
			else:
				print("Votre dosage de glycémie en mmol/L est de", Valeurmmol)

		if choixGly == 2:
			ValeurGly2 = input("Entrez votre valeur en mmol/L\n :")
			try:
				ValeurGly2 = float(ValeurGly2)
				Valeurgl = float(ValeurGly2) * 0.18
			except:
				print("Valeur incorrecte\n")
			else:
				print("Votre dosage de glycémie en g/L est de", Valeurgl)

# Choix algorithme collier cervical
          
if choix == 2:
	print("AlgoCC")

# Choix calcul NIH

if choix == 3:
	print("NIH")

# Choix du calcul du score de Glasgow

if choix == 4:
	print("Score de Glasgow\n")

	print("1) Ouverture des yeux\n")
	print("Spontanée : 4")
	print("A la demande : 3")
	print("A la douleur : 2")
	print("nulle : 1\n")
	eyes = input("Votre choix:\n")

	try:
		eyes = [1,2,3,4]
		eyes = int(eyes)
	except:
		print("Valeur incorrecte\n")
	else:
		print("Votre réponse enregistrèe est", eyes)


	print("2) Reponse Verbale\n")
	print("Normale : 5")
	print("Confuse : 4")
	print("Inappropriee : 3")
	print("Incomprehensive : 2")
	print("Nulle : 1\n")
	verb = input("Votre choix :\n")
	
	try:
		verb = [1,2,3,4,5)
		verb = int(verb)
	except:
		print("Valeur incorrecte\n")
	else:
		print("Votre réponse enregistrèe est", verb)

	print("3) Reponse Motrice\n")
	print("Aux ordres : 6")
	print("Oriente : 5")
	print("Evitement : 4")
	print("Flexion stereotypee : 3")
	print("Extension stereotypee : 2")
	print("Nulle : 1\n")
	motr = input("Votre choix :\n")
	
	try:
		motr = [1,2,3,4,5,6]
		motr = int(motr)
	except:
		print("Valeur incorrecte\n")
	else:
		print("Votre réponse enregistrèe est", motr)

	calculG = eyes + verb + motr
	calculG = int(calculG)

	print("Calcul du score de Glasgow à", calculG)
	

# Choix de la fiche d'intervention

if choix == 5:
	print("Work In Progress")


