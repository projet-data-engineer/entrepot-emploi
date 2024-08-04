## Objectif
Cette page interactive vous permet d'explorer les données des offres d'emploi en utilisant les codes ROME fournis par France Travail.

### Étapes à suivre

1. **Sélection du Code ROME :**
   - Choisissez le ou les codes ROME correspondant(s) aux métiers recherchés.
   - Vous pouvez sélectionner jusqu'à 10 codes ROME différents.

2. **Sélection de la Région :**
   - Choisissez la région qui vous intéresse pour affiner votre recherche.
   **Pensez à sélectionner sur la carte**

3. **Consultation des Offres :**
   - À la fin de la page, vous trouverez les offres d'emploi correspondant aux critères sélectionnés.
   - Les offres sont accompagnées de leur localisation pour faciliter votre recherche.

---


```sql code_rome
select code_1 , code_2, code_3, libelle_1, libelle_2, libelle_3
from dim_rome
```

<DimensionGrid 
    data={code_rome}   
    name="dimensiongrid_code_rome"
    limit=17
/>

```sql filtered_query_code_rome
select code_3
from dim_rome
where ${inputs.dimensiongrid_code_rome}
```

```sql nombre_poste_rome_region
WITH FOE as (
    SELECT nombre_postes, code_rome, lieu_travail_code
    FROM entrepot_emploi.fait_offre_emploi
),
DR as (
    SELECT code_3
    FROM entrepot_emploi.dim_rome
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
JOIN DR ON FOE.code_rome = DR.code_3
JOIN DL ON FOE.lieu_travail_code = DL.code
JOIN R ON DL.code_reg = R.code
WHERE
    FOE.code_rome = ${filtered_query_code_rome}
GROUP BY
    R.code, R.nom
```

### Repartition géographique

<AreaMap 
    data={nombre_poste_rome_region} 
    areaCol=code
    name=areamap_1
    title="Répartition régionale des postes"
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

```sql filtered_nombre_poste_rome_region
WITH FOE as (
    SELECT id, lieu_travail_code, code_rome, type_contrat, nature_contrat, experience_exige, qualification_code
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
    FOE.code_rome,
    FOE.type_contrat,
    FOE.nature_contrat,
    FOE.experience_exige,
    FOE.qualification_code
FROM
    FOE
JOIN DL ON FOE.lieu_travail_code = DL.code
JOIN R ON DL.code_reg = R.code
WHERE
    FOE.code_rome = ${filtered_query_code_rome}
    AND
    R.nom = '${inputs.areamap_1.nom}'
```
### Sélectionner sur la carte

<DataTable data={filtered_nombre_poste_rome_region}/>

<PointMap 
    data={filtered_nombre_poste_rome_region} 
    lat=lat 
    long=long 
    pointName= code
    height=200
/>

<!-- 
```sql poste_rome_region_selected
Select id, lieu_travail_code, type_contrat, experience_exige
from fait_offre_emploi
Where r.code 
```
-->