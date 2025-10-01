# [ Projet NEXUS ]
# Suite Médicale d'Aide à la Décision
de Sidoine B.

![Nexus Logo](Nexus.jpg)
## .: OBJECTIFS :.

NEXUS est une suite complète d'outils médicaux et paramédicaux développée pour accompagner les professionnels de santé dans leurs prises de décision cliniques quotidiennes. L'application offre une interface moderne et intuitive avec des calculateurs médicaux avancés, des valeurs normales biologiques et des outils de gestion patient.

## .: LICENSE :.

Le programme NEXUS est un projet sous license libre GNU GPL (https://www.gnu.org).

## .: UTILISATION :.

En premier lieu, une version console de NEXUS est proposée comme solution basique aux différents outils.
Une version avec interface graphique est mise en place pour les différents dispositifs de secours (ex: PMA, PC, etc...) 
Enfin, cette suite d'ouils sera porté sur une application mobile, afin d'aider les IS et paramédics sur le terrain, dans leurs bilans et autres prises de décisions.
Dans sa finalité, cet outils pourra être stocké sur le web, sur un hebergeur http classique (style OVH), mais il est possible d'envisager une version local wifi (sur RaspberryPi Zero) à embarquer dans les VPSP, PMA, etc.


## .: Installation :.

### Prérequis

- **Python 3.8+** (3.9+ recommandé)
- **Système d'exploitation** : Windows, macOS, Linux
- **Mémoire** : 512 Mo RAM minimum
- **Espace disque** : 100 Mo

### Installation rapide

```bash
# 1. Cloner le repository
git clone https://github.com/votre-username/nexus-medical.git
cd nexus-medical

# 2. Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer NEXUS
python Nexus.py
```

### Installation alternative

```bash
# Installation directe des dépendances
pip install numpy pandas matplotlib python-dateutil tkinter
python Nexus.py
```

### **Historique des versions**
- **v2.0** : Interface graphique moderne, calculateurs avancés [upgrade en Vibe Coding par [Claude](https://claude.ai/chat)]
- **v1.0** : Version console originale
- **v0.1** : Prototype initial

## Roadmap

### **Version 2.1** (Q1 2024)
- [ ] Algorithme décisionnel collier cervical
- [ ] Calculateur de posologies pédiatriques
- [ ] Export PDF des rapports
- [ ] Mode sombre/clair

### **Version 2.5** (Q2 2024)
- [ ] Base de données médicamenteuse
- [ ] Alertes et rappels
- [ ] Synchronisation cloud
- [ ] Application mobile companion

### **Version 3.0** (Q4 2024)
- [ ] Intelligence artificielle diagnostique
- [ ] Interface web complète
- [ ] Multi-utilisateurs
- [ ] Intégration dossier médical
