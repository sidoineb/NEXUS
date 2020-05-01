# Calcul du score NIH
# -------------------
# Le score NIHSS (NIH Stroke Scale) permet le suivi évolutif d’un AVC ischémique ou hémorragique.
# Il est côté de 0 à 42 points

# Implications pratiques du score
# ===============================
# – Des signes mineurs / régressifs avec score NIHSS < 5 sont une contre-indication à la thrombolyse IV dans les infarctus cérébraux.
#   Ces infarctus « mineurs » sont souvent traités par bi-antiagrégation (comme pour les AIT).
# – Un score NIHSS > 16 dans un contexte d’infarctus cérébral malin avant 60 ans est une indication à la crâniectomie de décompression

def algo_nih():

    print("Calcul du Score NIH\n")

    print(" *** Vigilance *** ")
    print("0 : vigilance normale, réactions vives")
    print("1 : Tbl léger de la vigilance : obnubilation, éveil ± adapté aux stimulations nociceptives")
    print("2 : Coma, réponse adaptée aux stimulations nociceptives")
    print("3 : Coma grave, réponse stéréotypée ou aucune réponse motrice\n")

    vigilance = input("Votre choix:\n")

    try:
        vigilance = [0,1,2,3]
        vigilance = int(vigilance)

    except:
        print("Valeur incorrecte\n")

    print(" *** Orientation (mois, age) *** ")
    print("0 : 2 réponses exactes")
    print("1 : 1 réponse exacte")
    print("2 : 0 réponse exacte\n")

    orientation = input("Votre choix:\n")

    try:

        orientation = [0,1,2]
        orientation = int(orientation)


    except:
        print("Valeur incorrecte\n")

    print(" *** Commandes (ouverture des yeux, du poing) *** \n")
    print("0 : 2 réponses exactes")
    print("1 : 1 réponse exacte")
    print("2 : 0 réponse exacte\n")

    commandes = input("Votre choix:\n")

    try:
        commandes = [0,1,2]
        commandes = int(commandes)

    except:
        print("Valeur incorrecte\n")

    print(" *** Oculomotricité *** ")
    print("0 : Normale")
    print("1 : Ophtalmoplégie partielle ou déviation réductible du regard")
    print("2 : Ophtalmoplégie horizontale complète ou déviation forcée du regard\n")

    oculomot = input("Votre choix:\n")

    try:
        oculomot = [0,1,2]
        oculomot = int(oculomot)

    except:
        print("Valeur incorrecte\n")

    print(" *** Champ visuel *** \n")
    print("0 : Normal")
    print("1 : Quadranopsie latérale homonyme ou hémianopsie incomplète ou négligence visuelle unilatérale")
    print("2 : HLH franche")
    print("3 : Cécité bilatérale ou coma (vigilance = 3)\n")

    champ_visuel = input("Votre choix:\n")

    try:
        champ_visuel = [0,1,2,3]
        champ_visuel = int(champ_visuel)

    except:
        print("Valeur incorrecte\n")

    print(" *** Paralysie faciale *** \n")
    print("0 : Motricité faciale normale")
    print("1 : Asymétrie faciale modérée (PF unilatérale incomplète)")
    print("2 : PF unilatérale centrale franche")
    print("3 : PF périphérique ou diplégie faciale\n")

    paralysie_fac = input("Votre choix:\n")

    try:
        paralysie_fac = [0,1,2,3]
        paralysie_fac = int(paralysie_fac)

    except:
        print("Valeur incorrecte\n")

    print(" *** Motricité mb supérieur *** \n")
    print("0 : Pas de déficit proximal")
    print("1 : Affaissement dans les 10s sans atteinte le plan du lit")
    print("2 : Effort contre pesanteur, mais chute du mb dans les 10s sur le plan du lit")
    print("3 : Pas d’effort contre la pesanteur")
    print("4 : Absence de mouvement")
    print("X : Cotation impossible (amputation, arthrodèse)\n")

    mot_mb_sup = input("Votre choix:\n")

    try:
        mot_mb_sup = [0,1,2,3,4,X]

    except:
        print("Valeur incorrecte\n")

    print(" *** Motricité mb inférieur *** \n")
    print("0 : Pas de déficit proximal")
    print("1 : Affaissement dans les 5s sans atteinte le plan du lit")
    print("2 : Effort contre pesanteur, mais chute du mb dans les 5s sur le plan du lit")
    print("3 : Pas d’effort contre la pesanteur")
    print("4 : Absence de mouvement")
    print("X : Cotation impossible (amputation, arthrodèse)\n")

    mot_mb_inf = input("Votre choix:\n")

    try:
        mot_mb_sup = [0,1,2,3,4,X]

    except:
        print("Valeur incorrecte\n")

    print(" *** Ataxie *** \n")
    print("0 : Absence")
    print("1 : 1 membre")
    print("2 : ≥ 2 membres")

    ataxie = input("Votre choix:\n")

    try:
        ataxie = [0,1,2]
        ataxie = int(ataxie)

    except:
        print("Valeur incorrecte\n")

    print(" *** Sensibilité *** \n")
    print("0 : Normale")
    print("1 : Hypoesthésie minime à modérée")
    print("2 : Hypoesthésie sévère ou anesthésie\n")

    sensibilite = input("Votre choix:\n")

    try:
        sensibilite = [0,1,2]
        sensibilite = int(sensibilite)

    except:
        print("Valeur incorrecte\n")

    print(" *** langage *** ")
    print("0 : Pas d’aphasie")
    print("1 : Aphasie discrète à modérée")
    print("2 : Aphasie sévèr")
    print("3 : Mutisme, aphasie totale\n")

    langage = input("Votre choix:\n")

    try:
        langage = [0,1,2,3]
        langage = int(langage)

    except:
        print("Valeur incorrecte\n")

    print(" *** Dysarthrie *** \n")
    print("0 : Normal")
    print("1 : Dysarthrie discrète à modérée")
    print("2 : Dysarthrie sévère")
    print("X : Cotation impossible")

    dysarthrie = input("Votre choix:\n")

    try:
        dysarthrie = [0,1,2,X]
        dysarthrie = int(dysarthrie)

    except:
        print("Valeur incorrecte\n")

    print(" *** Extinction, négligence *** \n")
    print("0 : Absence")
    print("1 : Extinction dans 1 seule modalité (visuelle ou sensitive) ou héminégligence partielle (auditive, spatiale ou personnelle)")
    print("2 : Négligence sévère ou anosognosie ou extinction portant sur > 1 modalité sensorielle")

    extinction = input("Votre choix:\n")

    try:
        extinction = [0,1,2]
        extinction = int(extinction)

    except:
        print("Valeur incorrecte\n")

    calcul_nih = vigilance + orientation + commandes + oculomot + champ_visuel + paralysie_fac + mot_mb_sup + mot_mb_inf + ataxie + sensibilite + langage + dysarthrie + extinction
