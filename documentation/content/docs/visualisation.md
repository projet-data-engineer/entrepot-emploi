---
weight: 700
title: "Visualisation des données"
description: "Documentation des tableaux de bord de visualisation des données."
icon: "finance"
date: "2024-07-30T11:54:48+02:00"
lastmod: "2024-07-30T11:54:48+02:00"
draft: false
toc: true
---


# Visualisation

## Evidence.dev

Nous avons utilisé le framework d'Evidence.dev [Evidence.dev](https://evidence.dev) pour la partie de visualisation. C’est un framework open source permettant de créer des produits de données avec SQL, tels que des rapports, des outils d'aide à la décision et des tableaux de bord intégrés. Il s'agit d'une alternative low code aux outils de BI par copier-coller.

Evidence restitue un site Web BI à partir de fichiers markdown:

- Les sources de données peuvent inclure des entrepôts de données, des fichiers flat et des sources de données non SQL.
- Les instructions SQL dans les fichiers markdown exécutent des requêtes sur les sources de données.
- Les graphiques et les composants sont rendus à l'aide de ces résultats de requête.
- Les pages modélisées génèrent de nombreuses pages à partir d'un seul modèle de markdown.
- Les boucles et les instructions If/Else permettent de contrôler ce qui est affiché aux utilisateurs.

## Sections du Projet

Nous avons segmenté notre présentation en quatre parties principales :

**Introduction** générale au projet et au contexte.

**Présentation et Analyse de la Qualité de la Donnée**

**Compréhension des Nomenclatures et Informations Théoriques**

**Partie Interactive d'Exploration de la Donnée**

### 1. Introduction

La page d’accueil contextualise le projet Job Market pour l’utilisateur final. On donne un aperçu des différentes tables et données mises à disposition.

### 2. Qualité de la Donnée

Cette section comprend la structure de la base de données et les référentiels associés. Elle présente les critères de qualité et la stratégie pour s’assurer de la qualité de la donnée. On y fait une analyse de la complétude des offres d’emplois, des valeurs nécessaires et des valeurs manquantes, de la cohérence de la donnée et de la présence d’incohérence.

### 3. Exploration des Données Théoriques

Cette section fait référence aux différentes tables de dimension de notre schéma en étoile. Elle propose notamment :
- Une partie interactive d’exploration du code NAF et du nombre de postes associés sur un territoire donné.
- Une partie interactive d’exploration du code ROME et du nombre de postes associés sur un territoire donné.
- Une exploration des métiers les plus demandés dans les offres d'emplois et des activités les plus présentes dans les départements et régions sélectionnés.

### 4. Exploration

Cette section offre une vue d'ensemble détaillée et interactive des offres d'emploi, des activités d'entreprise et des demandes d'emploi par localisation et métier.

#### 4.1 Contrats et Qualifications

Présentation détaillée des différents types de contrat (CDI, CDD, intérim, etc.), des natures de contrat ainsi que des qualifications demandées dans nos offres d'emploi. Cette section aide à comprendre les exigences courantes et les options disponibles dans le cadre des offres d'emploi de FranceTravail.

#### 4.2 Ranking

Page présentant divers classements basés sur l'analyse des offres d'emploi et des entreprises :
- **Activités d'entreprise** : Classement des secteurs d'activité les plus représentés.
- **Domaines d'activité** : Hiérarchisation des domaines d'activité en fonction de leur demande.
- **Expérience demandée** : Classement selon les niveaux d'expérience les plus recherchés.
- **Régions les plus demandeuses d'emploi** : Identification des régions avec la plus forte demande en termes d'offres d'emploi.

#### 4.3 Activité

Page interactive permettant de sélectionner une activité spécifique pour découvrir les régions, départements et villes ayant le plus grand nombre d'entreprises correspondant à cette activité. Exploration de la répartition géographique des entreprises par activité.

#### 4.4 Métiers

Page interactive permettant de sélectionner un métier pour visualiser les régions, départements et villes avec le plus grand nombre de demandes d'emploi pour ce métier. Exploration géographique de la demande pour un métier spécifique.

#### 4.5 Recherche Géographique

Page interactive combinant des critères géographiques et professionnels pour une analyse approfondie. En sélectionnant un métier et une région, vous obtiendrez :
- **Carte démographique** : Affiche la population de chaque département de la région sélectionnée ainsi que la répartition du nombre de métiers sélectionnés dans chaque département.
- **Carte des activités d'entreprise** : Montre les activités des entreprises ayant publié des offres d’emploi pour le métier sélectionné dans la région.

#### 4.6 Code NAF associé à un métier

Outil d'association entre le code NAF des entreprises et le code ROME des postes proposés dans les offres d'emploi de Pôle Emploi. Cet outil permet de :
- Faciliter la recherche d'emploi en associant ces deux codes.
- Améliorer l'analyse du marché du travail pour les analystes.
- Identifier les offres correspondant à leur secteur d'activité et à leurs compétences spécifiques.

En utilisant les données empiriques rassemblées, nous dégageons des tendances sur les activités des entreprises demandant un métier spécifique.

## Méthode

Nous avons utilisé :
- Des fichiers markdown pour la structure des pages.
- Des requêtes SQL pour la récupération des données.
- Des composants de sélection tels que des menus déroulants.
- Des représentations géographiques :
  - **AreaMaps** : Cartes de zone permettant de visualiser des régions géographiques spécifiques et leurs caractéristiques.
  - **Bubble Map** : Cartes avec des bulles représentant la taille et l'importance relative des données sur différentes zones géographiques.
  - **Point Map** : Cartes avec des points marquant des emplacements spécifiques et des données associées.
  - **Base Map** : Carte pouvant associer plusieurs éléments (AreaMap combinée à une Bubble Map par exemple).
- Des graphiques statistiques classiques (Bar, histogramme, Tableau de données)
- Des composants de données sélectionnantes avec la **Dimension Grid** qui est une grille dimensionnelle permettant la sélection et le filtrage des données sur un tableau précis.

## Exemples

#### Code NAF associé à un métier

Actuellement, il n’existe pas de dispositif efficace pour associer le code NAF au code ROME dans les offres d’emploi, ce qui complique l’analyse et la recherche d’opportunités de carrière. L’objectif est de créer un outil d’association entre ces deux codes pour faciliter la recherche d’emploi et améliorer l’analyse du marché du travail. En rassemblant les offres d’emploi et en analysant les données empiriques, nous pouvons identifier des tendances actuelles. Une solution future serait d'améliorer la précision des correspondances avec des algorithmes de machine learning.

Nous sélectionnons dans la dernière page de notre rapport une catégorie de Métier, une sous-catégorie ou un métier précis. Nous obtenons alors les données suivantes

![evidence_code_NAF_metier](/images/evidence_code_NAF_metier.png)


#### Recherche géographique

Dans cette page, nous sélectionnons un métier et une région pour obtenir deux cartes:
- Une première qui met en avant la densité de population par département de la région sélectionnée et la répartition géographique du métier sélectionné.
- Une seconde qui met en avant le dynamisme des entrprise pour les activités associées au métier sélectionné par département de la région sélectionnée et la répartition géographique du métier sélectionné.

Cela permet de visualiser à la fois la concentration démographique et l’activité économique liée au métier dans la région.

![evidence_recherche_geographique](/images/evidence_recherche_geographique.png)
