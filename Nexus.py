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

choix1 = int(1)
choix2 = int(2)
choix3 = int(3)
choix4 = int(4)
choix5 = int(5)


choix = input("Tapez votre choix :")

# Choix de la glycémie capillaire

if choix == 1:
	print("Conversion valeurs Glycémie capillaire\n")
	print("1) Convertir g/L -> mmol/L")
	print("2) Convertir mmol/L -> g/L\n")

		choixGly = input("Tapez votre choix :\n")
          
		if choixGly == 1:
			ValeurGly1 = input("Entrez votre valeur en g/L :\n")
			ValeurGly1 = float(ValeurGly1)
			Valeurmmol = float(ValeurGly1) * 5.5
			print("Votre dosage de glycémie en mmol/L est de", Valeurmmol)

		if choixGly == 2:
			ValeurGly2 = input("Entrez votre valeur en mmol/L\n :")
			ValeurGly2 = float(ValeurGly2)
			Valeurgl = float(ValeurGly2) * 0.18
			print("Votre dosage de glycémie en g/L est de", Valeurgl)

# Choix algorythme collier cervical
          
if choix == 2:
	print("AlgoCC")

# Choix calcul NIH

if choix == 3:
	print("NIH")

# Choix du calcul du score de Glasgow

if choix == 4:
	print("Score de Glasgow\n")

	eyes = input("L'ouverture des yeux :\n")
	eyes_spon = int(4)
	eyes_dem = int(3)
	eyes_dou = int(2)
	eyes_auc = int(1)

	verb = input("La réponse verbale :\n")
	verb_orien = int(5)
	verb_conf = int(4)
	verb_inap = int(3)
	verb_incom = int(2)
	verb_auc = int(1)

	motr = input("La réponse motrice :\n")
	motr_obdem = int(6)
	motr_ordou = int(5)
	motr_evna =int(4)
	motr_flexdou = int(3)
	motr_extdou = int(2)
	motr_auc = int(1)

	calculG = eyes + verb + motr
	calculG = int(calculG)

	print("Calcul du score de Glasgow à", calculG)
	

# Choix de la fiche d'intervention

if choix == 5:
	print("Work In Progress")


