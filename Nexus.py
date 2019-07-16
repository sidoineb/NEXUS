"""
Projet Nexus écrit par Sidoine B.
"""

print("############################################")
print("##           .: Nexus v0.1 :.             ##")
print("############################################\n")

print("  1) Conversion glycémie capillaire")
print("  2) Algo décision pose de collier cervical")
print("  3) Calcul du NIH")
print("  4) Calcul score d'APGAR")
print("  5) Calcul score de Glasgow")
print("  6) Fiche d'intervention\n")

# Variables des choix

choix = [1,2,3,4,5,6]

choix = input("Tapez votre choix :")

# Choix de la glycémie capillaire

if choix == "1":
	from PACK.Nexus_glycemie.py import algo_glycemie
	algo_glycemie()
	

# Choix algorithme collier cervical
          
if choix == "2":
	print("AlgoCC")

# Choix calcul NIH

if choix == "3":
	from PACK.Nexus_nih.py import algo_nih
	algo_nih()

# Choix du calcul du score d'APGAR

if choix == "4":
	print("APGAR")


# Choix du calcul du score de Glasgow

if choix == "5":
	from PACK.Nexus_glasgow.py import algo_glasgow
	algo_glasgow()

# Choix de la fiche d'intervention

if choix == "6":
	print("Work In Progress")


