## Objectif
Cette page interactive vous permet d'explorer les données des offres d'emploi en utilisant les codes NAF fournis par l'INSEE.

### Étapes à suivre

1. **Sélection du Code NAF :**
   - Choisissez le ou les codes NAF correspondant(s) à l'activité recherchée.
   - Vous pouvez sélectionner jusqu'à 10 codes NAF différents.

2. **Sélection de la Région :**
   - Choisissez la région qui vous intéresse pour affiner votre recherche.
   **Pensez à sélectionner sur la carte**

3. **Consultation des Offres :**
   - À la fin de la page, vous trouverez les offres d'emploi correspondant aux critères sélectionnés.
   - Les offres sont accompagnées de leur localisation pour faciliter votre recherche.

---


```sql code_naf
select code_1 , code_2, code_3, code_4, code_5, libelle_1, libelle_2, libelle_3, libelle_4, libelle_5
from dim_naf
```

<DimensionGrid 
    data={code_naf} 
    name="dimensiongrid_code_naf"
    limit=21
/>

```sql filtered_query_code_naf
select code_5
from dim_naf
where ${inputs.dimensiongrid_code_naf}
```

```sql nombre_poste_naf_region
WITH FOE as (
    SELECT nombre_postes, code_naf, lieu_travail_code
    FROM entrepot_emploi.fait_offre_emploi
),
DN as (
    SELECT code_5
    FROM entrepot_emploi.dim_naf
),
DL as (
    SELECT code, code_reg
    FROM entrepot_emploi.dim_lieu 
    WHERE code = code_parent
),
R as (
    SELECT code, nom
    FROM entrepot_emploi.region
)
SELECT
    R.nom as nom,
    R.code as code,
    SUM(FOE.nombre_postes) as nombre
FROM
    FOE
JOIN DN ON FOE.code_naf = DN.code_5
JOIN DL ON FOE.lieu_travail_code = DL.code
JOIN R ON DL.code_reg = R.code
WHERE
    FOE.code_naf = ${filtered_query_code_naf}
GROUP BY
    R.code, R.nom
```
### Représentation géographique

<AreaMap 
    data={nombre_poste_naf_region} 
    areaCol=code
    name=areamap_1
    title="Répartition régionale des domaines d'activité"
    geoJsonUrl='/region-metropole.geojson'
    geoId=INSEE_REG
    value=nombre
    height=500
    opacity=0.5
    tooltip={[
        {id: 'nom', showColumnName: false, valueClass: 'text-xl font-semibold'},
        {id: 'nombre', fieldClass: 'text-[grey]', valueClass: 'text-[green]'}
    ]}
/>

```sql filtered_nombre_poste_naf_region
WITH FOE as (
    SELECT id, lieu_travail_code, code_naf, type_contrat, nature_contrat, experience_exige, qualification_code
    FROM entrepot_emploi.fait_offre_emploi
),
DL as (
    SELECT code, code_reg, lat, long
    FROM entrepot_emploi.dim_lieu 
    WHERE code = code_parent
),
R as (
    SELECT code, nom
    FROM entrepot_emploi.region
)
SELECT
    DL.lat as lat,
    DL.long as long,
    DL.code as code,
    R.nom as nom,
    FOE.id,
    FOE.lieu_travail_code,
    FOE.code_naf,
    FOE.type_contrat,
    FOE.nature_contrat,
    FOE.experience_exige,
    FOE.qualification_code
FROM
    FOE
JOIN DL ON FOE.lieu_travail_code = DL.code
JOIN R ON DL.code_reg = R.code
WHERE
    FOE.code_naf = ${filtered_query_code_naf}
    AND
    R.nom = '${inputs.areamap_1.nom}'
```
### Sélectionner sur la carte

<DataTable data={filtered_nombre_poste_naf_region}/>

<PointMap 
    data={filtered_nombre_poste_naf_region} 
    lat=lat 
    long=long 
    pointName= code
    height=200
/>

<!-- 
```sql poste_naf_region_selected
Select id, lieu_travail_code, type_contrat, experience_exige
from fait_offre_emploi
Where r.code 
```
-->