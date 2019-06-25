[ Projet NEXUS ]
================
de Sidoine B.


.: OBJECTIFS :.

NEXUS est un programme à destination des équipes de prompt secours et paramedicales.
L'idée de ce projet est de fournir une suite d'outils, facilement consultable durant une prise en charge de patients, afin de faciliter certaines decisions.
Cette boite à outils contiendra un algorithme d'immobilisation dans le cas de traumatisme du rachis, calcul de différents scores (Glasgow, APGAR, NIH, etc.).

.: LICENSE :.

Le programme NEXUS est un projet sous license libre GNU GPL (https://www.gnu.org).

.: UTILISATION :.

En premier lieu, une version console de NEXUS est propoposée comme solution basique des différents outils.
Une version avec interface graphique est mis en place pour les différents dispositifs de secours (ex: PMA, PC, etc...) 
Enfin, cette suite d'ouils sera porté sur une application mobile, afin d'aider les IS et paramédics sur le terrain, dans leurs bilans et autres prises de décisions.
Dans sa finalité, cet outils pourra être stocké sur le web, sur un hebergeur http classique (style OVH), mais il est possible d'envisager une version local wifi (sur RaspberryPi Zero) à embarquer dans les VPSP, PMA, etc.


.: TECHNIQUE :.

Le langage utiliser pour créer ce programme sera Python (console, puis grpahique), puis ce script sera integré à des page HTML/CSS3 (via Gpython, que je vais apprendre à connaitre), pour être, après test en local, transféré sur un hebergeur "classique" (OVH, etc...)
En paralléle, une éventuelle solution nomade sera à évalué en fonction de la necessité de celle-ci. L'idée sera de remplacer la solution de l'hebergeur par un systéme de Raspberry Zero, module Wifi, batterie, etc. (style PirateBox https://daviddarts.com/piratebox ) à embarqué dans un VPSP, PMA, etc...

.: DEVELOPPEMENT :.

+ Phase 1: Création du programme sous Python (console, puis graphique)
+ Phase 2: Transfert et mise en page sur HTML/CSS3 via Gpython
* Phase 3: Migration du local vers un hebergeur
+ Phase 4: Beta-test auprès d'un noyau de testeurs pour feedback