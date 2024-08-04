---
title: Projet Job market
---

Dans ce projet, nous avons regroupé des informations sur les offres d’emplois et les compagnies qui les proposent. Notre objectif est de développer une meilleure vision du marché de l’emploi : quels secteurs recrutent le plus, quelles compétences sont requises, quelles sont les villes les plus actives.

Le projet s'est déroulé en 5 étapes: 
- **Récolte des données**: Nous avons cherché plusieurs sources de données parmis lesquelles on retrouve LinkedIn, HelloWork, France Travail ou encore Welcome to the Jungle. Nous avons finalement utilisé comme source unique l'API de France Travail pour les données d'emploi. Nous avons également récolté des données géographiques, ainsi que des informations précises sur les entreprises avec l'open data de l'INSEE
- **Architecture des données**: Après plusieurs modifications dans l'architecture des données, nous pouvons retrouver l'architecture définitive sur le lien suivant https://projet-data-engineer.github.io/entrepot-emploi/docs/objectifs/#description-fonctionnelle-du-projet 
- **Consommation de la donnée**: Nous avons fait le choix d'evidence.dev pour consommer et mettre à disposition la donnée pour les utilisateurs finaux. La transparence dans le requêtage de nos bases de données, l'intéractivité et la qualité des représentations ont été des arguments forts pour notre sélection.
- **Déploiement**: Une API a été créé pour mettre à disposition la donnée. Tous les composants du projet ont été mis sous Docker
- **Automatisation des flux**: La récupération de la donnée se fait quotidiennement grâce à une automatisation sur Airflow

Voyons ensemble un aperçu de nos données

# Aperçu des données

```sql tables
SELECT 
    table_name,
    COUNT(column_name) AS "Nombre de colonnes"
FROM 
    information_schema.columns
GROUP BY 
    table_name
ORDER BY 
    "Nombre de colonnes" DESC;
```
<DataTable data={tables}/>


## Table region

### Schéma

```sql schema_region

SELECT 
  column_name, 
  data_type
FROM 
  information_schema.columns
WHERE 
  table_name = 'region';
```

<DataTable data={schema_region}/>

### Aperçu

```sql head_region

SELECT 
  *
FROM 
  region
LIMIT 3
```

<DataTable data={head_region}/>


## Table departement


### Schéma

```sql schema_departement

SELECT 
  column_name, 
  data_type
FROM 
  information_schema.columns
WHERE 
  table_name = 'departement';
```

<DataTable data={schema_departement}/>

### Aperçu

```sql head_departement

SELECT 
  *
FROM 
  departement
LIMIT 3
```

<DataTable data={head_departement}/>

## Table dim_lieu_activite

### Schéma

```sql schema_dim_lieu_activite

SELECT 
  column_name, 
  data_type
FROM 
  information_schema.columns
WHERE 
  table_name = 'dim_lieu_activite';
```

### Aperçu

```sql head_dim_lieu_activite

SELECT 
  *
FROM 
  dim_lieu_activite
LIMIT 3
```

<DataTable data={head_dim_lieu_activite}/>

## Table dim_lieu

### Schéma

```sql schema_dim_lieu

SELECT 
  column_name, 
  data_type
FROM 
  information_schema.columns
WHERE 
  table_name = 'dim_lieu';
```

### Aperçu

```sql head_dim_lieu

SELECT 
  *
FROM 
  dim_lieu
LIMIT 3
```

<DataTable data={head_dim_lieu}/>

## Table dim_naf

### Schéma

```sql schema_dim_naf

SELECT 
  column_name, 
  data_type
FROM 
  information_schema.columns
WHERE 
  table_name = 'dim_naf';
```

### Aperçu

```sql head_dim_naf

SELECT 
  *
FROM 
  dim_naf
LIMIT 3
```

<DataTable data={head_dim_naf}/>

## Table dim_rome

### Schéma

```sql schema_dim_rome

SELECT 
  column_name, 
  data_type
FROM 
  information_schema.columns
WHERE 
  table_name = 'dim_rome';
```

### Aperçu

```sql head_dim_rome

SELECT 
  *
FROM 
  dim_rome
LIMIT 3
```

<DataTable data={head_dim_rome}/>

## Table fait_offre_emploi

### Schéma

```sql schema_fait_offre_emploi

SELECT 
  column_name, 
  data_type
FROM 
  information_schema.columns
WHERE 
  table_name = 'fait_offre_emploi';
```

### Aperçu

```sql head_fait_offre_emploi

SELECT 
  *
FROM 
  fait_offre_emploi
LIMIT 3
```

<DataTable data={head_fait_offre_emploi}/>