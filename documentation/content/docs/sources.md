---
weight: 200
title: "Sources de données"
description: "Description des sources de données utilisées."
icon: "dataset"
date: "2024-07-19T11:25:58+02:00"
lastmod: "2024-07-19T11:25:58+02:00"
draft: false
toc: true
---

<hr>

## France Travail.io

La plateforme [francetravail.io](https://francetravail.io) met à disposition un certain nombre d'API en lien avec le marché de l'emploi.
<p>Ce projet utilise les API suivantes:</p>

- **Offres d'emploi v2**: mise à disposition en temps réel des offres d'emploi de France Travail
- **ROME 4.0 - Métiers v1**: nomenclature des métiers ROME

### Offres d'emploi

L'API Offres d’emploi restitue en temps réel les offres d'emploi actives collectées par France Travail, et la sélection de partenaires ayant consenti à la diffusion de leurs offres via l'API.

Les données d'offres d'emploi sont mises à disposition sous [licence Etalab Licence Ouverte / Open License](https://www.etalab.gouv.fr/licence-ouverte-open-licence/) du gouvernement, permettant la réutilisation des données publiques mises à disposition gratuitement. Voir également la [documentation de la base de données des offres d’emploi de France Travail](https://francetravail.io/data/api/offres-emploi?tabgroup-api=documentation).

L'API permet de recupérer une offre donnée par son identifiant, ou un ensemble d'offres selon des critères. Pour ce projet, nous collectons quotidiennement l'ensemble des offres créées au cours de la journée (env. 40 000 nouvelles offres par jour en semaine).

### Nomenclature des métiers ROME

La nomenclature des métiers ROME (Répertoire Opérationnel des Métiers et des Emplois) est un système de classification des métiers géré par France Travail (anciennement Pôle emploi). Elle a pour but de fournir une description standardisée des différents métiers et emplois.

Cette nomenclature est organisée en 3 niveaux hierarchiques. 

- Un métier ROME est identifié par un code ROME. Il est composé d’une lettre et quatre chiffres, exemple **M1811 - Data engineer**.
- Les métiers sont regroupés en grands domaines d'activités économiques. Le domaine est identifié par les 3 premiers caractères du code ROME, exemple **M18 - Systèmes d'information et de télécommunication**
- Chaque domaine est subdivisé en familles professionnelles. La famille est identifiée par la 1ère lettre (de A à N), exemple : **M – Support à l'entreprise**.

<u>Exemple de codification d'un métier ROME</u>: 

{{< table >}}
| Niveau | Code | Intitulé |
|---------|--------|-----|
| `Métier` | M1811 | Data engineer |
| `Grand domaine` | M18 | Systèmes d'information et de télécommunication |
| `Famille professionnelle` | M | Support à l'entreprise |
{{< /table >}}

{{< alert context="info" text="Le code ROME est systèmatiquement renseignés dans les offres d'emploi de France Travail.io. La nomenclature ROME à 3 niveaux nous permettra de pouvoir **effectuer des calculs d'agrégation sur un niveau ou un autre en fonction du besoin**. En effet on pourra par exemple observer un métier donnée (ex Data Engineer), ou bien observer les offres d'emploi plus largement sur une famille d'emploi (ex K - Services à la personne et à la collectivité)" />}}


## Limites géographiques COG Carto

On souhaite pouvoir **créer des visualisations de données spatiales** à partir des données d'offres d'emploi. Par exemple, représenter sur une carte la répartition géographiques des offres d'emploi pour un métier donné. Nous utiliserons deux types de visualisation spatiale:

- **Choroplèthe** ou **Area Map**: une couleur est attribuée à chaque aire géographique en fonction de la valeur de la variable numérique que l'on souhaite observer.

<u>Ex: répartition des offres de Data Engineer par département en Ile-de-France</u>

![area_map](/images/area_map.png)

- **Carte à bulle** ou **Bubble Map**: le diamètre de chaque bulle varie en fonction de la valeur de la variable numérique que l'on souhaire représenter. En combinant des aires géographiques et des bulles, on pourra alors observer plusieurs variables sur une même carte afin de matérialiser des corrélations spatiales entre ces variables. Ce type de visualisation nécessite de fournir la coordonnée géographique (latitude, longitude) de chaque bulle afin de les positionner sur la carte.

![base_map](/images/base_map.png)

Pour réaliser ce type de visualisation, il est nécessaire de disposer des contours géographiques des territoires pour lesquels on souhaite représenter les données.
Nous utiliserons le jeu de données **ADMIN-EXPRESS-COG-CARTO édition 2024 France entière** disponible [ici](https://geoservices.ign.fr/adminexpress#telechargement) mis à disposition par l'IGN.

- Format: Shapefile
- Précision: Entre 15 et 50 m

Les niveaux de territoires représentés seront les suivants:

- Région
- Département
- Commune
- Arrondissement municipal

### Le format Shapefile

Le format Shapefile est un format de fichier numérique utilisé en géomatique pour le stockage de données géospatiales vectorielles. Développé par la société Esri (Environmental Systems Research Institute), il est largement utilisé dans les systèmes d'information géographique (SIG) pour représenter des entités géographiques sous forme de points, de lignes et de polygones.

{{< alert context="primary" text="Les jeux de données au format Shapefile seront convertis au format **GeoJSON**, qui est le **format standard des outils de visualisation de données spatiales**." />}}

#### Composition d'un Shapefile

Un Shapefile est en réalité un ensemble de plusieurs fichiers distincts qui, ensemble, contiennent toutes les informations nécessaires à la représentation et à l'attribution des données géospatiales. Les principaux fichiers composant un Shapefile sont :

- .shp (Shapefile) : Contient la géométrie des entités géographiques (points, lignes ou polygones).
- .shx (Shape Index File) : Contient un index de la géométrie pour un accès rapide.
- .dbf (Database File) : Contient les attributs (ou métadonnées) des entités géographiques sous forme de table.

{{< alert context="info" text="Note: les métadonnées des fichiers Shapefile des niveaux Commune et Arrondissement Municipal comportent la <strong>population</strong>. Cet attribut nous sera utile, par exemple pour pondérer une observation sur un territoire donné en fonction de la population." />}}

## Nomenclature des Activités Françaises NAF

La nomenclature NAF (Nomenclature des Activités Françaises) est un système de classification des activités économiques utilisé en France. Elle est gérée par l'**Institut National de la Statistique et des Etudes Economiques (INSEE)**. La NAF permet de classer les entreprises et les établissements selon leur activité principale.

La nomenclature NAF est structurée hierarchiquement sur 5 niveaux: sections, divisions, groupes, classes et sous-classes. Le code NAF, également connu sous le terme code APE, est attribué par l'INSEE lors de l'immatriculation d'une entreprise, il correspond à la sous-classe, le niveau le plus fin.

<u>Exemple de codification d'un code NAF (ou code APE)</u>: 

{{< table >}}
| Niveau | Code | Intitulé |
|---------|--------|-----|
| `Section` | J | Information et communication |
| `Division` | 62 | Programmation, conseil et autres activités informatiques |
| `Groupe` | 62.0 | Programmation, conseil et autres activités informatiques |
| `Classe` | 62.01 | Programmation informatique |
| `Sous-classe (code NAF)` | 62.01Z | Programmation informatique |
{{< /table >}}

{{< alert context="primary" text="Le schéma d'une offre d'emploi comporte un attribut code NAF, correspondant à l'activité de l'entreprise à l'origine de l'offre d'emploi. La nomenclature NAF nous permettra d'étudier la répartition d'un métier donné en fonction de l'activité. On pourra par exemple répondre à la question suivante: le métier de **`Data Engineer`** est il principalement exercé au sein d'entreprises qui exercent une activité dans le domaine **`Programmation, conseil et autres activités informatiques`** ou non." />}}

- Source: [Page NAF de l'INSEE](https://www.insee.fr/fr/information/2120875)
- Format: Excel (xls). 1 fichier par niveau + 1 fichier de jointure des différents niveaux.

## Base Sirene des entreprises et de leurs établissements (SIREN, SIRET)

- La base de données SIRENE d'immatriculation des entreprises est mise à disposition sur [data.gouv](https://www.data.gouv.fr/fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/).

- Les données sont mises à disposition sous formes de deux fichiers CSV compactés et **mises à jour tous les 1er de chaque mois**.

  - **Fichier StockUniteLegale**: ensemble des entreprises (identifiées par un **SIREN**) inscrites actives ou ayant cessé leur activité

  - **Fichier StockEtablissement**: ensemble des établissements (identifiées par un **SIRET**) d'entreprises (une entreprise comprend 1 à n établissements) actifs ou ayant cessé leur activité.

- Pour ce projet, nous récupérons le fichier StockEtablissement. Ce jeu de données contient notamment le code INSEE de la commune de localisation de l'établissement, ainsi que le code INSEE de l'activé NAF de l'établissement

- Taille du fichier compacté (08/2024): 2.4G / Taille du fichier du fichier CSV décompacté: 8.0G / env. 38 millions de lignes