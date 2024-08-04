## Contexte

Actuellement, il n'existe pas de dispositif efficace pour associer le code NAF (Nomenclature d'Activités Française) au code ROME (Répertoire Opérationnel des Métiers et des Emplois) au sein des offres d'emploi proposées par Pôle Emploi. Le code NAF est un identifiant utilisé pour catégoriser les entreprises en fonction de leur activité principale, tandis que le code ROME sert à classifier les métiers et les emplois. Cette dissociation des codes complique l'analyse et la recherche d'opportunités de carrière adaptées aux compétences et aux domaines d'activité des demandeurs d'emploi.

### Objectifs

L'objectif est d'avoir un premier outil d'association entre le code NAF des entreprises et le code ROME des postes proposés dans les offres d'emploi de Pôle Emploi. Cet outil permettra de **faciliter la Recherche d'Emploi** en associant ces deux codes, les demandeurs d'emploi pourront facilement identifier les offres correspondant à leur secteur d'activité et à leurs compétences spécifiques. Il permettra également d'**améliorer l'Analyse du Marché du Travail** pour les analystes notamment. 

### Méthodologie

Nous avons rassemblé les offres d'emploi disponibles sur francetravail à travers le temps, incluant les codes NAF des entreprises demandeuses d'emploi et les codes ROME des postes. En nous basant sur les données empiriques, nous pouvons dégager des tendances  sur les activités des entreprises demandant un métier spécifique.

Une piste d'amélioration pourrait être l'utilisation d'algorithmes de machine learning pour améliorer la précision de ces correspondances.

En facilitant l'association de ces deux codes, nous pouvons analyser voire préduire les besoins de certaines compétences pour un secteur d'activité donné.

## Sélectionnez un métier

<Dropdown
    data={list_jobs_code_1}
    name=Catégorie_de_métier
    value=jobs
    multiple=True
/>

<Dropdown
    data={list_jobs_code_2}
    name=Précision_sur_la_catégorie
    value=jobs
    multiple=True
/>

<Dropdown
    data={list_jobs_code_3}
    name="Métier"
    value=jobs
    multiple=True
/>


Le métier {inputs.Métier.value} est associé aux codes NAF suivants:
<DataTable
    data={NAF_associated_with_ROME_code_3}
/>

La précision sur la catégorie de métier {inputs.Précision_sur_la_catégorie.value} est associée aux codes NAF suivants:
<DataTable
    data={NAF_associated_with_ROME_code_2}
/>

La catégorie de métier {inputs.Catégorie_de_métier.value} est associée aux codes NAF suivants:
<DataTable
    data={NAF_associated_with_ROME_code_1}
/>


# Queries

```sql list_jobs_code_1
SELECT 
    distinct dr.libelle_1 as jobs, 
FROM 
    dim_rome dr
```
```sql list_jobs_code_2
SELECT DISTINCT 
    dr.libelle_2 AS jobs
FROM 
    dim_rome dr
WHERE
    dr.libelle_1 = ${inputs.Catégorie_de_métier.value}
    OR ${inputs.Catégorie_de_métier.value} IS NULL;
```
```sql list_jobs_code_3
SELECT DISTINCT 
    dr.libelle_3 AS jobs
FROM 
    dim_rome dr
WHERE
    dr.libelle_2 = ${inputs.Précision_sur_la_catégorie.value}
    OR ${inputs.Précision_sur_la_catégorie.value} IS NULL;

```

```sql NAF_associated_with_ROME_code_1
SELECT 
    dn.code_5 as "Code NAF",
    dn.libelle_5 as "Activité",
    count(*) as occurences
FROM 
    dim_naf dn
JOIN
    fait_offre_emploi foe ON dn.code_5 = foe.code_naf
JOIN 
    dim_rome dr ON foe.code_rome = dr.code_3
where
    dr.libelle_1 = ${inputs.Catégorie_de_métier.value}
GROUP BY 
    dn.libelle_5,dn.code_5
ORDER BY
    occurences DESC
```

```sql NAF_associated_with_ROME_code_2
SELECT 
    dn.code_5 as "Code NAF",
    dn.libelle_5 as "Activité",
    count(*) as occurences
FROM 
    dim_naf dn
JOIN
    fait_offre_emploi foe ON dn.code_5 = foe.code_naf
JOIN 
    dim_rome dr ON foe.code_rome = dr.code_3
where
    dr.libelle_2 = ${inputs.Précision_sur_la_catégorie.value}
GROUP BY 
    dn.libelle_5,dn.code_5
ORDER BY
    occurences DESC
```

```sql NAF_associated_with_ROME_code_3
SELECT 
    dn.code_5 as "Code NAF",
    dn.libelle_5 as "Activité",
    count(*) as occurences
FROM 
    dim_naf dn
JOIN
    fait_offre_emploi foe ON dn.code_5 = foe.code_naf
JOIN 
    dim_rome dr ON foe.code_rome = dr.code_3
where
    dr.libelle_3 = ${inputs.Métier.value}
GROUP BY 
    dn.libelle_5,dn.code_5
ORDER BY
    occurences DESC
```