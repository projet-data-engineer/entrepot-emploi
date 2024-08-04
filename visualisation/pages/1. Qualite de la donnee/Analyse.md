## Objectif

Nous avons vu que nous disposons d'une donnée exacte, cohérente, uniforme et actualisée. Notre objectif est donc de vérifier que les données récupérées sont complètes.

### Présence de valeurs manquantes :

Nous identifions les colonnes contenant des valeurs nulles :

```sql Nom_des_colonnes
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'fait_offre_emploi'
```


```SQL valeurs_nulles_par_colonnes
SELECT
 'type_contrat' AS colonne,
 COUNT(*) AS Variable_incomplete
FROM fait_offre_emploi
WHERE type_contrat IS NULL
HAVING Variable_incomplete > 0
UNION ALL
SELECT
  'qualification_code' AS colonne,
  COUNT(*) AS Variable_incomplete
FROM fait_offre_emploi
WHERE qualification_code IS NULL
HAVING Variable_incomplete > 0
UNION ALL
SELECT
 'nombre_postes' AS colonne,
 COUNT(*) AS Variable_incomplete
FROM fait_offre_emploi
WHERE nombre_postes IS NULL
HAVING Variable_incomplete > 0
UNION ALL
SELECT
 'nature_contrat' AS colonne,
 COUNT(*) AS Variable_incomplete
FROM fait_offre_emploi
WHERE nature_contrat IS NULL
HAVING Variable_incomplete > 0
UNION ALL
SELECT
 'lieu_travail_code' AS colonne,
 COUNT(*) AS Variable_incomplete
FROM fait_offre_emploi
WHERE lieu_travail_code IS NULL
HAVING Variable_incomplete > 0
UNION ALL
SELECT
 'id' AS colonne,
 COUNT(*) AS Variable_incomplete
FROM fait_offre_emploi
WHERE id IS NULL
HAVING Variable_incomplete > 0
UNION ALL
SELECT
 'experience_exige' AS colonne,
 COUNT(*) AS Variable_incomplete
FROM fait_offre_emploi
WHERE experience_exige IS NULL
HAVING Variable_incomplete > 0
UNION ALL
SELECT
  'entreprise_adaptee' AS colonne,
  COUNT(*) AS Variable_incomplete
FROM fait_offre_emploi
WHERE entreprise_adaptee IS NULL
HAVING Variable_incomplete > 0
UNION ALL
SELECT
 'date_creation' AS colonne,
 COUNT(*) AS Variable_incomplete
FROM fait_offre_emploi
WHERE date_creation IS NULL
HAVING Variable_incomplete > 0
UNION ALL
SELECT
 'code_rome' AS colonne,
 COUNT(*) AS Variable_incomplete
FROM fait_offre_emploi
WHERE code_rome IS NULL
HAVING Variable_incomplete > 0
UNION ALL
SELECT
 'code_naf' AS colonne,
 COUNT(*) AS Variable_incomplete
FROM fait_offre_emploi
WHERE code_naf IS NULL
HAVING Variable_incomplete > 0
UNION ALL
SELECT
 'alternance' AS colonne,
 COUNT(*) AS Variable_incomplete
FROM fait_offre_emploi
WHERE alternance IS NULL
HAVING Variable_incomplete > 0
UNION ALL
SELECT
 'accessible_th' AS colonne,
 COUNT(*) AS Variable_incomplete
FROM fait_offre_emploi
WHERE accessible_th IS NULL
HAVING Variable_incomplete > 0
ORDER BY Variable_incomplete DESC
```

<DataTable data={valeurs_nulles_par_colonnes}/>

Nous notons qu’il y a de nombreuses offres de poste incomplètes. En date du 1er août, il y avait: 
- 520 000 données manquantes pour qualification_code
- 344 000 pour code_naf, 157 000 pour entreprise_adaptee
- 77 000 pour lieu_travail_code
- 72 000 pour nombre_postes
- et 33 000 pour accessible_th. 

Cela représente un défi significatif pour la qualité des données, étant donné qu’il y a un total de 800 000 offres dans la base de données notamment pour les variables code_naf, lieu_travail_code, nombre_postes qui sont utilisés pour nos calculs et représentations géographiques. Les informations sur le niveau de qualification demandé sont à considérer en sachant que plus de la moitié des offres n'ont pas cette information complétée.

**Sélectionnez une colonne** pour voir le nombre de valeurs incomplètes :
<Dropdown
    data={Nom_des_colonnes} 
    name=name_of_dropdown
    value=column_name
/>

```sql dropdown_valeurs_incompletes
SELECT
 '${inputs.name_of_dropdown.value}' AS colonne,
 COUNT(*) AS Nombre_de_valeurs_nulles
FROM fait_offre_emploi
WHERE ${inputs.name_of_dropdown.value} IS NULL
```
<DataTable
    data={dropdown_valeurs_incompletes}
/>


---
### Nombre d'offres intégralement complétées

Nous identifions le nombre de lignes complètes (dont toutes les informations sont bien renseignées), ainsi que le pourcentage de complétion des offres d'emploi: 

```sql Lignes_completes
SELECT 'Pourcentage de lignes complètes' AS status,
  concat (ROUND(100 * COUNT(*) /(SELECT COUNT(*) AS count FROM fait_offre_emploi)) , '%') AS count
FROM fait_offre_emploi
WHERE type_contrat IS NOT NULL
  AND qualification_code IS NOT NULL
  AND nombre_postes IS NOT NULL
  AND nature_contrat IS NOT NULL
  AND lieu_travail_code IS NOT NULL
  AND id IS NOT NULL
  AND experience_exige IS NOT NULL
  AND entreprise_adaptee IS NOT NULL
  AND date_creation IS NOT NULL
  AND code_rome IS NOT NULL
  AND code_naf IS NOT NULL
  AND alternance IS NOT NULL
  AND accessible_th IS NOT NULL
UNION ALL
SELECT 'Nombre total de lignes' AS status,
  COUNT(*) AS count
FROM fait_offre_emploi
UNION ALL
SELECT 'Pourcentage de lignes incomplètes' AS status,
  concat (ROUND(100 * COUNT(*) /(SELECT COUNT(*) AS count FROM fait_offre_emploi)) , '%') AS count
FROM fait_offre_emploi
WHERE type_contrat IS NULL
  OR qualification_code IS NULL
  OR nombre_postes IS NULL
  OR nature_contrat IS NULL
  OR lieu_travail_code IS NULL
  OR id IS NULL
  OR experience_exige IS NULL
  OR entreprise_adaptee IS NULL
  OR date_creation IS NULL
  OR code_rome IS NULL
  OR code_naf IS NULL
  OR alternance IS NULL
  OR accessible_th IS NULL
```
<DataTable
    data={Lignes_completes}
/>

A date, nous avons 9% des offres d'emploi qui sont complètes dans leur intégralité.

Il est maintenant nécessaire de savoir quel est le pourcentage de complétion des offres qui ne sont pas complètes dans leur intégralité.

### Pourcentage de complétion des offres

```sql Pourcentage_completion
WITH completion_stats AS (
    SELECT
        id,
        (
            SUM(CASE WHEN type_contrat IS NOT NULL THEN 1 ELSE 0 END)
            + SUM(CASE WHEN qualification_code IS NOT NULL THEN 1 ELSE 0 END)
            + SUM(CASE WHEN nombre_postes IS NOT NULL THEN 1 ELSE 0 END)
            + SUM(CASE WHEN nature_contrat IS NOT NULL THEN 1 ELSE 0 END)
            + SUM(CASE WHEN lieu_travail_code IS NOT NULL THEN 1 ELSE 0 END)
            + SUM(CASE WHEN id IS NOT NULL THEN 1 ELSE 0 END)
            + SUM(CASE WHEN experience_exige IS NOT NULL THEN 1 ELSE 0 END)
            + SUM(CASE WHEN entreprise_adaptee IS NOT NULL THEN 1 ELSE 0 END)
            + SUM(CASE WHEN date_creation IS NOT NULL THEN 1 ELSE 0 END)
            + SUM(CASE WHEN code_rome IS NOT NULL THEN 1 ELSE 0 END)
            + SUM(CASE WHEN code_naf IS NOT NULL THEN 1 ELSE 0 END)
            + SUM(CASE WHEN alternance IS NOT NULL THEN 1 ELSE 0 END)
            + SUM(CASE WHEN accessible_th IS NOT NULL THEN 1 ELSE 0 END)
        ) * 100.0
        / 13.0 AS pourcentage_completion
    FROM fait_offre_emploi
    GROUP BY id
)
SELECT
    pourcentage_completion,
    COUNT(*) AS count_of_values
FROM completion_stats
GROUP BY pourcentage_completion
```



<BarChart
    data={Pourcentage_completion} 
    x=pourcentage_completion
    y=count_of_values
/>

Les pourcentages de complétion varient de 69.2 % à 100 %. Les offres sont majoritairement complétées entre entre 84 et 92%, c'est à dire qu'il manque entre une et deux variables. Sachant que qualification code n'est pas présent dans plus de la moitié des offres et que le code naf est également présent que dans 2/3 des offres, cela nous permet de dire que pour le restes des variables, nous avons un très bon score de complétion des offres.

---

### Doublons

Nous comptons le pourcentage d'offres en double dans notre base. Pour cela nous utilisons l'id unique de chaque offre. 

```sql doublons
WITH foe AS (
  SELECT id
  FROM fait_offre_emploi
)
SELECT 1 - (COUNT(DISTINCT id) / (SELECT COUNT(*) FROM foe)) AS 'Pourcentage de doublons'
FROM foe;
```

<DataTable
    data={doublons}
/>
 
Le nombre de doublons est clairement négligeable (inférieur à 0,0001 %)

---

L'utilisation de l'API francetravail nous permet de garantir **la conformité des types de données, d'absence de valeurs incoherentes ou aberrantes, le format**, que les valeurs des colonnes catégorielles appartiennent aux **ensembles de valeurs attendus** ou encore que les colonnes dépendantes d'autres colonnes sont **bien cohérentes**.


