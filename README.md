TP stats
========

This is a webapp written with Django in order to record some measures and compute
simple statistical informations.

The standard application concerns the investigations of chemical glasswares
accuracy.

## TODO et questions

### Isoler les expériences

* Comment faire pour isoler les expériences et faire en sorte que les
glasswares ou n'importe quel item sur lequel on enregistre des statistiques soit
interne à une expérience.

* Il faudrait que l'auteur d'une expérience ne puisse pas modifier celles qui ne
lui appartiennent pas.

### Nombre dynamique d'item/glassware

* Actuellement les glasswares sur lesquels on accumule des statistiques sont définis
à l'avance. Il faudrait pouvoir définir leur nombre et leurs noms lors de la
création de l'expériences.

* Dans un modèle (Experiment) comment avoir un champ dynamique ? Les glasswares.

### Enregistrer les plots et statistiques

* Ajouter un champ Image au modèle Experiment pour stocker les images
* Raffraichir l'image à la demande au lieu de la reconstruire à chaque affichage de la page
* Idem pour le calcul des moyennes, std, quartiles ...
