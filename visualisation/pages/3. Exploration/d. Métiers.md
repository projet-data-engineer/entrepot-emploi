# Sélectionnez une activité

Pour vous aidez vous avez la liste des métiers du code ROME à l'adresse suivante : https://candidat.francetravail.fr/metierscope/metiers

<Dropdown
    data={list_jobs}
    name="métiers"
    value=jobs
    multiple=True
/>

## Les 10 régions les plus demandeuses d'emploi pour le métier sélectionné

```sql Top_region_with_jobs_filtered
SELECT 
    r.nom AS nom,
    r.code as code, 
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
    dr.libelle_3  IN ${inputs.métiers.value}
GROUP BY 
    r.nom,r.code
ORDER BY
    nombre_d_offres DESC
Limit 10
```

<DataTable data={Top_region_with_jobs_filtered} />

<AreaMap 
    data={Top_region_with_jobs_filtered} 
    areaCol=code
    name=areamap_1
    geoJsonUrl='/region-metropole.geojson'
    geoId=INSEE_REG
    value=nombre_d_offres
    height=500
    opacity=0.5
    tooltip={[
        {id: 'nom', showColumnName: false, valueClass: 'text-xl font-semibold'},
        {id: 'nombre_d_offres', fieldClass: 'text-[grey]', valueClass: 'text-[green]'}
    ]}
/>

## Les 10 départements les plus demandeurs d'emploi pour le métier sélectionné

```sql Top_departement_with_jobs_filtered
SELECT 
    d.nom AS nom,
    d.code as code, 
    COUNT(DISTINCT foe.id) AS nombre_d_offres
FROM 
    fait_offre_emploi foe
JOIN
    dim_rome dr ON foe.code_rome = dr.code_3
JOIN 
    dim_lieu dl ON foe.lieu_travail_code = dl.code_parent
JOIN 
    departement d ON dl.code_dep = d.code
where
    dr.libelle_3  IN ${inputs.métiers.value}
    and d.code not in ('971','972','973','974','976')
GROUP BY 
    d.nom,d.code
ORDER BY 
    nombre_d_offres DESC
Limit 10
```




<DataTable data={Top_departement_with_jobs_filtered} />

<AreaMap 
    data={Top_departement_with_jobs_filtered} 
    areaCol=code
    name=areamap_1
    geoJsonUrl='/departement-metropole.geojson'
    geoId=INSEE_DEP
    value=nombre_d_offres
    height=500
    opacity=0.5
    tooltip={[
        {id: 'nom', showColumnName: false, valueClass: 'text-xl font-semibold'},
        {id: 'nombre_d_offres', fieldClass: 'text-[grey]', valueClass: 'text-[green]'}
    ]}
/>

## Les 10 villes les plus demandeuses d'emploi pour le métier sélectionné

```sql Top_ville_with_jobs_filtered
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
    departement d ON dl.code_dep = d.code
where
    dr.libelle_3  IN ${inputs.métiers.value}
    and d.code not in ('971','972','973','974','976')
GROUP BY 
    dl.nom,foe.lieu_travail_code, dl.lat, dl.long
ORDER BY 
    nombre_d_offres DESC
Limit 10
```

<DataTable data={Top_ville_with_jobs_filtered} />

<BubbleMap 
    data={Top_ville_with_jobs_filtered} 
    lat=lat 
    long=long 
    size=nombre_d_offres
    value=nombre_d_offres 
    pointName=nom
    height=500
    opacity=0.5
    startingZoom=5
    tooltip={[
        {id: 'nom', showColumnName: false, valueClass: 'text-xl font-semibold'},
        {id: 'nombre_d_offres', fieldClass: 'text-[grey]', valueClass: 'text-[green]'}
    ]}
/>


# Queries

```sql list_jobs
SELECT 
    distinct dr.libelle_3 as jobs, 
FROM 
    dim_rome dr
```

