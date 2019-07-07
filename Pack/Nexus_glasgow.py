# Code score de Glasgow

def algo_glasgow():

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

		print("Votre réponse enregistrèe est", eyes)

	except:
		print("Valeur incorrecte\n")


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

		print("Votre réponse enregistrèe est", verb)

	except:
		print("Valeur incorrecte\n")


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

		print("Votre réponse enregistrèe est", motr)

	except:
		print("Valeur incorrecte\n")
		

	calculG = eyes + verb + motr
	calculG = int(calculG)

	print("Calcul du score de Glasgow à", calculG)

	exit()