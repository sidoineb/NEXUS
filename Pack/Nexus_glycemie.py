# Code conversion glycemie

def algo_glycemie():

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
