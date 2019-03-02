Hash Code 2016, Final Round - Satellites
===========

*Given a set of imaging satellites and a list of image collections ordered by customers, schedule satellite operations so that the total value of delivered image collections is as high as possible.*

Equipe et répartition des tâches(non exhaustive) :

-QUINQUENEL Nicolas:

    -Gestion de la classe Satellite
        -Changement d'orientation
        -Calcul de la trajectoire
        -Gestion des attributs du satellite (orientation, delta, pointage etc.)
        -Prendre une photo
        -Déterminer les photos possibles à prendre actuellement sous le satellite
    -Création de la première version du programme principal
    -Aide au développement de la lecture du fichier
    -Aide à la documentation

-SOYER Mathieu:

    -Documentation DocString
    -Gestion des intervalles de temps pour la prise d'une photo
    -Gestion apres prise photo d'un point d'interet
        -Mettre a jour les collections contenant ce point
        -Mettre a jour les chemins des satellites contenant un point valide pour toutes les collections en prenant en compte leur(s) intervalle(s) requis

-EHRESMANN Nicolas:

    -Interface Graphique
    -Aide à la documentation

-OUTHIER Arthur:

    -Entrées/Sorties
    -Conception et analyse du projet (diagramme de classe)
    -Gestion de la classe Temps
