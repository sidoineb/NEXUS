# 🏥 NEXUS Medical Suite

## 📋 Description
NEXUS est une suite complète d'outils médicaux et paramédicaux développée pour accompagner les professionnels de santé dans leurs prises de décision cliniques quotidiennes. L'application offre une interface moderne et intuitive avec des calculateurs médicaux avancés, des valeurs normales biologiques et des outils de gestion patient.

## 🎯 Public cible

- 👨‍⚕️ Médecins : Urgentistes, internistes, généralistes
- 👩‍⚕️ Personnel paramédical : Infirmiers, auxiliaires
- 🔬 Techniciens de laboratoire : Analyses biologiques
- 🚑 Secouristes : Premiers secours, SAMU
- 🎓 Étudiants : Médecine, soins infirmiers

## ✨ Fonctionnalités

#### 📊 Calculateurs Médicaux

- Score de Glasgow : Évaluation neurologique
- Score APGAR : Évaluation néonatale
- Score NIH : Échelle d'AVC complet (13 critères)
- Conversion Glycémie : g/L ↔ mmol/L ↔ mg/dL
- Risque Cardiovasculaire : Framingham
- IMC : Indice de masse corporelle
- Clairance Créatinine : Cockcroft-Gault & MDRD

#### 📋 Valeurs Normales

Hématologie : NFS, hémostase, morphologie
Biochimie : Fonctions hépatique, rénale, lipidique
Gazométrie : pH, gaz du sang, lactates
Constantes Vitales : Tous âges (adulte, enfant, bébé)

#### 👤 Gestion Patient

Création de fiches patient complètes
Historique des calculs effectués
Données anthropométriques (IMC automatique)
Antécédents médicaux

#### 📄 Rapports Médicaux

Génération automatique des rapports
Horodatage des interventions
Export en format texte
Sauvegarde locale sécurisée

#### 🔧 Outils Avancés

Algorithme de décision collier cervical (en développement)
Calculateur de posologies (à venir)
Base de données médicamenteuse (planifié)
Analyses de tendances graphiques (futur)

## 🚀 Installation

#### Prérequis

Python 3.8+ (3.9+ recommandé)
Système d'exploitation : Windows, macOS, Linux
Mémoire : 512 Mo RAM minimum
Espace disque : 100 Mo

**Installation rapide**

bash# 1. Cloner le repository
git clone https://github.com/votre-username/nexus-medical.git
cd nexus-medical

#### 2. Créer un environnement virtuel (recommandé)

python -m venv venv
source venv/bin/activate  # Linux/Mac
#### ou
venv\Scripts\activate     # Windows

#### 3. Installer les dépendances

pip install -r requirements.txt

#### 4. Lancer NEXUS

python Nexus.py
Installation alternative
bash# Installation directe des dépendances
pip install numpy pandas matplotlib python-dateutil tkinter
python Nexus.py

## 🎯 Guide de démarrage rapide

**1. Premier lancement**

bashpython Nexus.py
Un écran de démarrage s'affichera avec une barre de progression, puis l'interface principale apparaîtra.

**2. Configuration initiale**

Créer un patient : Menu Fichier → Nouveau Patient
Remplir les informations : nom, âge, poids, taille, antécédents
Sélectionner un calculateur dans l'onglet Calculateurs

**3. Utilisation des calculateurs**

**Score de Glasgow**

Sélectionner les réponses pour chaque critère
Le score total et l'interprétation s'affichent automatiquement
Résultat ajouté au rapport patient

**Conversion Glycémie**

Entrer la valeur et l'unité d'origine
Conversions automatiques vers toutes les unités
Interprétation clinique incluse

**Valeurs Normales**

Consultation rapide par catégorie
Tableaux organisés avec unités
Distinction homme/femme quand applicable

**4. Gestion des rapports**

Nouveau rapport : Efface et initialise
Sauvegarde : Export au format .txt
Consultation : Historique complet des calculs

## 📊 Interface utilisateur

#### Fenêtre principale
┌─────────────────────────────────────────┐
│ 🏥 NEXUS - Suite Médicale     [Patient] │
├─────────────────────────────────────────┤
│ [Calculateurs] [Valeurs] [Outils] [...]│
│                                         │
│  Liste des        │  Zone de calcul    │
│  calculateurs     │  et résultats      │
│                   │                    │
│                   │                    │
└─────────────────────────────────────────┘
#### Onglets disponibles

📊 Calculateurs : Scores et conversions
📋 Valeurs Normales : Références biologiques
🔧 Outils : Fonctionnalités avancées
📄 Rapports : Édition et export

#### 🧮 Détail des calculateurs

**Score de Glasgow** (3-15 points)

CritèreOptions:
PointsOuverture 
yeuxSpontanée → Aucune4 → 1
Réponse verbaleOrientée → Aucune5 → 1
Réponse motriceAux ordres → Aucune6 → 1

Interprétation :

15 : Normal
13-14 : Traumatisme léger
9-12 : Traumatisme modéré
3-8 : Traumatisme sévère

**Score APGAR** (0-10 points)
Critère012Fréquence cardiaqueAbsente< 100> 100RespirationAbsenteIrrégulièreNormaleTonusFlasqueFlexionActifRéflexesAucunGrimaceCriColorationCyanoséExtrémitésRose

**Conversion Glycémie**

g/L ↔ mmol/L : facteur 5.55
g/L ↔ mg/dL : facteur 100
mmol/L ↔ mg/dL : facteur 18.01

Valeurs normales à jeun :

0.7 - 1.1 g/L
3.9 - 6.1 mmol/L
70 - 110 mg/dL

#### 📋 Valeurs normales intégrées
**Hématologie**
Paramètre: HommeFemme
UnitéHémoglobine13-1711.5-15.5g/dL
Hématocrite40-5035-45%
Globules blancs4000-100004000-10000/mm³
Plaquettes150000-400000150000-400000/mm³

**Biochimie**
ParamètreNormalUnité
Créatinine H0.7-1.3mg/dL
Créatinine F0.6-1.1mg/dL
Urée15-45mg/dL
ASAT/ALAT5-45UI/L
Constantes vitales
Paramètre
AdulteEnfantBébé
Fréquence cardiaque60-10080-120100-160
Fréquence respiratoire12-2016-2525-40
Température36.1-37.8°C36.1-37.8°C36.1-37.8°C

## 🔧 Fonctionnalités avancées

#### Gestion des patients

Fiche complète avec données anthropométriques
Calcul automatique de l'IMC
Antécédents médicaux
Historique des consultations

#### Système de rapports

Horodatage automatique des interventions
Compilation des résultats de calculs
Export sécurisé
Format standard médical

#### Interface adaptive

Design responsive
Thème médical professionnel
Navigation intuitive
Raccourcis clavier

## 🐛 Dépannage
#### Problèmes courants
**"ModuleNotFoundError"**
bash# Installer les dépendances manquantes
pip install -r requirements.txt
Interface ne s'affiche pas
bash# Vérifier l'installation de tkinter
python -m tkinter
Erreurs de calcul

Vérifier la saisie des données numériques
S'assurer que les champs obligatoires sont remplis
Consulter les messages d'erreur détaillés

**Sauvegarde impossible**

Vérifier les droits d'écriture dans le répertoire
Choisir un emplacement accessible
Fermer les fichiers ouverts

**Réinitialisation complète**
bash# Supprimer les fichiers temporaires
rm -rf __pycache__/
rm -f *.pyc

## Relancer l'application
python Nexus.py
🔄 Mises à jour
Version actuelle : 2.0
bash# Vérifier les mises à jour
git pull origin main
pip install -r requirements.txt --upgrade
Historique des versions

v2.0 : Interface graphique moderne, calculateurs avancés
v1.0 : Version console originale
v0.1 : Prototype initial

📈 Roadmap
Version 2.1 (Q1 2024)

 Algorithme décisionnel collier cervical
 Calculateur de posologies pédiatriques
 Export PDF des rapports
 Mode sombre/clair

Version 2.5 (Q2 2024)

 Base de données médicamenteuse
 Alertes et rappels
 Synchronisation cloud
 Application mobile companion

Version 3.0 (Q4 2024)

 Intelligence artificielle diagnostique
 Interface web complète
 Multi-utilisateurs
 Intégration dossier médical

## 🤝 Contribution
Les contributions sont vivement encouragées !
Comment contribuer

Fork le projet
Créer une branche feature : git checkout -b feature/nouvelle-fonctionnalite
Développer et tester
Committer : git commit -am 'Ajout de nouvelle fonctionnalité'
Pusher : git push origin feature/nouvelle-fonctionnalite
Ouvrir une Pull Request

**Guidelines de développement**

Respecter le style PEP 8
Ajouter des tests unitaires
Documenter les nouvelles fonctions
Tester sur plusieurs OS

**Domaines d'amélioration**

Nouveaux calculateurs médicaux
Optimisations d'interface
Traductions
Documentation
Tests automatisés

## 🛡️ Sécurité et conformité

#### Protection des données
Aucune transmission de données patient sur Internet
Stockage local uniquement
Chiffrement des rapports (à venir)
Conformité RGPD

#### Responsabilité médicale
⚠️ IMPORTANT : NEXUS est un outil d'aide à la décision uniquement.

**Ne remplace pas le jugement clinique
Toujours confirmer les calculs critiques
Utilisation sous responsabilité du praticien
Destiné aux professionnels formés**

## 📄 Licence
Ce projet est sous licence GNU General Public License v3.0.
Permissions
✅ Utilisation commerciale
✅ Modification
✅ Distribution
✅ Usage privé
Conditions
📋 Inclure la licence
📋 Inclure le copyright
📋 Documenter les changements
📋 Même licence pour les dérivés
Limitations
❌ Aucune garantie
❌ Aucune responsabilité
Voir le fichier LICENSE pour les détails complets.



## 🏆 Contributions

Sidoine B. - Développeur principal
Claude IA - Aide au passage v2.0 par Vibe Coding

#### Références scientifiques

Score de Glasgow : Teasdale & Jennett (1974)
Score APGAR : Virginia Apgar (1953)
NIH Stroke Scale : National Institute of Health
Framingham Risk Score : Framingham Heart Study

#### Technologies utilisées

Python - Langage principal
Tkinter - Interface graphique
NumPy/Pandas - Calculs scientifiques
Matplotlib - Visualisations


💡 NEXUS : L'aide à la décision médicale à portée de clic
bash# Prêt à améliorer vos pratiques médicales ?
python Nexus.py
