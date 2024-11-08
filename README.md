# README - Green Spaces Dashboard

Green Spaces Dashboard
======================

Green Spaces Dashboard est une application web interactive qui permet de visualiser et de filtrer les espaces verts à Paris. L'application utilise Mapbox GL pour afficher les données GeoJSON sur une carte et Chart.js pour afficher les statistiques sous forme de graphiques.

Configuration du projet
-----------------------

### Installation des dépendances

Pour installer les dépendances du projet, exécutez la commande suivante :

    npm install

### Compilation et rechargement à chaud pour le développement

Pour compiler le projet et lancer un serveur de développement avec rechargement à chaud, exécutez la commande suivante :

    npm run serve

### Compilation et minification pour la production

Pour compiler le projet en vue de sa mise en production, exécutez la commande suivante :

    npm run build

### Linting et correction des fichiers

Pour analyser et corriger les fichiers du projet, exécutez la commande suivante :

    npm run lint

Structure du projet
-------------------

Voici la structure des principaux fichiers et répertoires du projet :

    
    ├── .gitignore
    ├── babel.config.js
    ├── jsconfig.json
    ├── package.json
    ├── public/
    │   ├── geojson/
    │   │   ├── green_spaces_paris.geojson
    │   │   └── trees_paris.geojson
    │   └── public/index.html
    ├── README.md
    ├── src/
    │   ├── src/App.vue
    │   ├── assets/
    │   ├── components/
    │   │   ├── src/components/FilterComponent.vue
    │   │   ├── src/components/NavBar.vue
    │   │   ├── src/components/StatisticCard.vue
    │   │   └── src/components/StatisticsChart.vue
    │   ├── src/config.js
    │   ├── src/main.js
    │   ├── router/
    │   │   └── src/router/index.js
    │   └── views/
    │       ├── src/views/Home.vue
    │       └── src/views/Statistics.vue
    └── vue.config.js
        

Utilisation
-----------

### Filtrage des données sur la carte

L'application permet de filtrer les différents types d'espaces verts à Paris en utilisant les composants de filtre situés en haut à gauche de la carte. Les filtres disponibles sont :

*   Parcs
*   Jardins
*   Terrains de jeux
*   Emplacements
*   Forêts
*   Bois
*   Arbres (avec sous-filtres pour les arbres à feuilles caduques, larges et d'aiguilles)

### Affichage des statistiques

La page des statistiques affiche des cartes et des graphiques représentant la répartition des différents types d'espaces verts. Les données sont mises à jour en temps réel en fonction des filtres appliqués.

Personnalisation de la configuration
------------------------------------

Pour personnaliser la configuration du projet, consultez la [documentation de Vue CLI](https://cli.vuejs.org/config/).

Auteurs
-------

Philip Léo

Licence
-------