---
weight: 140
title: "Contours géographiques - IGN Admin Express"
description: ""
icon: "location_on"
date: "2024-07-19T11:27:41+02:00"
lastmod: "2024-07-19T11:27:41+02:00"
draft: false
toc: true
---

<hr>

On souhaite pouvoir **créer des visualisations de données spatiales** à partir des données d'offres d'emploi. Par exemple, représenter sur une carte la répartition géographiques des offres d'emploi pour un métier donné. Nous utiliserons deux types de visualisation spatiale:

- **Choroplèthe** ou **Area Map**: une couleur est attribuée à chaque aire géographique en fonction de la valeur de la variable numérique que l'on souhaire représenter.

Ex: répartition des offres de Data Engineer en Ile de france

![area_map](/images/area_map.png)

- **Carte à bulle** ou **Bubble Map**: le diamètre de chaque bulle varie en fonction de la valeur de la variable numérique que l'on souhaire représenter. En combinant des aires géographiques et des bulles, on pourra alors représenter plusieurs variables sur une même carte. Ce type de visualisation nécessite de fournir la coordonnée géographique (latitude, longitude) de chaque bulle afin de les positionner sur la carte.

![base_map](/images/base_map.png)

Pour réaliser ce type de visualisation, il est nécessaire de disposer des contours géographiques des territoires pour lesquels on souhaite représenter les données.
Nous utiliserons le jeu de données **ADMIN-EXPRESS-COG-CARTO édition 2024 France entière** disponible [ici](https://geoservices.ign.fr/adminexpress#telechargement) mis à disposition par l'IGN.

- Format: ShapeFile
- Précision: Entre 15 et 50 m

Les niveaux de territoires représentés seront les suivants:

- Région
- Département
- Commune
- Arrondissement municipal

{{< alert context="info" text="Note: les métadonnées des fichiers ShapeFile des niveaux commune et arrondissement municipal contiennent la <strong>population</strong>." />}}
