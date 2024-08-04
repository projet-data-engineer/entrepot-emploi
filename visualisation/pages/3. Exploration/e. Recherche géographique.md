# Sélectionnez les emplois et les régions

Sélectionnez un métier et une région. 

Vous obtenez une première carte montrant deux informations clés pour chaque département de la région :
	1.	La population de chaque département.
	2.	La répartition du nombre de métiers sélectionnés dans chaque département de la région.

Ensuite, vous obtenez une carte montrant les activités des entreprises qui ont publié des offres d’emploi pour ce même métier dans la région sélectionnée. 


<Dropdown
    data={list_jobs}
    name="Métiers"
    value=jobs
    multiple=True
/>
<Dropdown
    data={list_region}
    name="Région"
    value=name
/>


```sql population_departement
select 
    r.nom,code_dep,d.nom,sum(population) as population
from
    dim_lieu dl
JOIN 
    departement d ON dl.code_dep = d.code
JOIN
    region r ON dl.code_reg = r.code
where 
    r.nom = '${inputs.Région.value}'
GROUP BY
    code_dep,d.nom,r.nom
```

```sql city_with_jobs_filtered
SELECT 
    dl.nom AS nom,
    dl.lat AS lat,
    dl.long AS long,
    foe.lieu_travail_code as code, 
    COUNT(DISTINCT foe.id) AS nombre_d_offres
FROM 
    fait_offre_emploi foe
JOIN
    dim_rome dr ON foe.code_rome = dr.code_3
JOIN 
    dim_lieu dl ON foe.lieu_travail_code = dl.code_parent
JOIN 
    region r ON dl.code_reg = r.code
where
    dr.libelle_3  IN ${inputs.Métiers.value}
    and r.nom = '${inputs.Région.value}'
GROUP BY 
    dl.nom,foe.lieu_travail_code, dl.lat, dl.long
ORDER BY 
    nombre_d_offres DESC
LIMIT 10
```

La densité de population et la distribution des emplois spécifiés pour chaque département de la région choisie se présente sur la carte de la manière suivante:

<BaseMap>
  <Areas 
    data={population_departement} 
    areaCol=code_dep
    geoJsonUrl='/departement-metropole.geojson'
    geoId=INSEE_DEP
    value=population
    height=500
    opacity=0.5
    tooltip={[
        {id: 'nom', showColumnName: false, valueClass: 'text-xl font-semibold'},
        {id: 'population', fieldClass: 'text-[grey]', valueClass: 'text-[green]'}
    ]}
  />
  <Bubbles 
    data={city_with_jobs_filtered} 
    lat=lat 
    long=long 
    size=nombre_d_offres
    value=nombre_d_offres 
    pointName=nom
    height=500
    opacity=0.9
    startingZoom=5
    colorPalette={['yellow','orange','red','darkred']}
    tooltip={[
        {id: 'nom', showColumnName: false, valueClass: 'text-xl font-semibold'},
        {id: 'nombre_d_offres', fieldClass: 'text-[grey]', valueClass: 'text-[green]'}
    ]}
  />
</BaseMap>

<DataTable 
data={city_with_jobs_filtered} 
/>

---

```sql activites_departement
SELECT 
    d.nom AS nom,
    d.code as code,
    SUM(dla.total) AS nombre_d_entreprises
FROM 
    dim_lieu_activite dla
JOIN
    fait_offre_emploi foe ON foe.code_naf = dla.code_activite
JOIN
    dim_rome dr ON foe.code_rome = dr.code_3
JOIN
    dim_naf dn ON dla.code_activite = dn.code_5
JOIN 
    dim_lieu dl ON dla.code_commune = dl.code_parent
JOIN 
    departement d ON dl.code_dep = d.code
JOIN 
    region r ON dl.code_reg = r.code
where
    dr.libelle_3 = ${inputs.Métiers.value}
    and r.nom = '${inputs.Région.value}'
GROUP BY 
    d.nom,d.code
```

La densité du nombre d'entreprises et la distribution des emplois spécifiés pour chaque département de la région choisie se présente sur la carte de la manière suivante:

<BaseMap>
  <Areas 
    data={activites_departement} 
    areaCol=code
    geoJsonUrl='/departement-metropole.geojson'
    geoId=INSEE_DEP
    value=nombre_d_entreprises
    height=500
    opacity=0.5
    tooltip={[
        {id: 'nom', showColumnName: false, valueClass: 'text-xl font-semibold'},
        {id: 'nombre_d_entreprises', fieldClass: 'text-[grey]', valueClass: 'text-[green]'}
    ]}
  />
  <Bubbles 
    data={city_with_jobs_filtered} 
    lat=lat 
    long=long 
    size=nombre_d_offres
    value=nombre_d_offres 
    pointName=nom
    height=500
    opacity=0.9
    startingZoom=5
    colorPalette={['yellow','orange','red','darkred']}
    tooltip={[
        {id: 'nom', showColumnName: false, valueClass: 'text-xl font-semibold'},
        {id: 'nombre_d_offres', fieldClass: 'text-[grey]', valueClass: 'text-[green]'}
    ]}
  />
</BaseMap>



Il est important de noter que la carte ne reflète pas toutes les activités de toutes les entreprises potentiellement intéressées par le poste recherché, seulement celles qui ont effectivement posté des offres.

# Queries

<!-- 
```sql list_departements
SELECT 
    distinct nom as "name", 
FROM 
    departement
``` 
-->

```sql list_region
SELECT 
    distinct nom as "name", 
FROM 
    region
```
<!-- 
```sql list_activites
SELECT 
    distinct dn.libelle_5 as "activity", 
FROM 
    dim_naf dn
``` 
-->

```sql list_jobs
SELECT 
    distinct dr.libelle_3 as "jobs", 
FROM 
    dim_rome dr
```

<!-- 
<Dropdown
    data={list_departements}
    name="Département"
    value=name
/>
 -->