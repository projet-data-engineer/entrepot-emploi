# Sélectionnez une activité

Pour vous aidez vous avez la liste des activités du code NAF à l'adresse suivante https://blog.easyfichiers.com/wp-content/uploads/2014/08/Liste-code-naf-ape.pdf

<Dropdown
    data={list_activites}
    name="Activités"
    value=activity
    multiple=True
/>

## Les 10 régions les plus dynamiques pour l'activité sélectionnée

```sql Top_region_with_activity_filtered
SELECT 
    r.nom AS nom,
    r.code as code, 
    SUM(dla.total) AS nombre_d_entreprises
FROM 
    dim_lieu_activite dla
JOIN
    dim_naf dn ON dla.code_activite = dn.code_5
JOIN 
    dim_lieu dl ON dla.code_commune = dl.code_parent
JOIN 
    region r ON dl.code_reg = r.code
where
    dn.libelle_5  IN ${inputs.Activités.value}
GROUP BY 
    r.nom,r.code
ORDER BY
    nombre_d_entreprises DESC
Limit 10
```

<DataTable data={Top_region_with_activity_filtered} />

<AreaMap 
    data={Top_region_with_activity_filtered} 
    areaCol=code
    name=areamap_1
    geoJsonUrl='/region-metropole.geojson'
    geoId=INSEE_REG
    value=nombre_d_entreprises
    height=500
    opacity=0.5
    tooltip={[
        {id: 'nom', showColumnName: false, valueClass: 'text-xl font-semibold'},
        {id: 'nombre_d_entreprises', fieldClass: 'text-[grey]', valueClass: 'text-[green]'}
    ]}
/>

---

## Les 10 départements les plus dynamiques pour l'activité sélectionnée

```sql Top_departement_with_activity_filtered
SELECT 
    d.nom AS nom,
    d.code as code, 
    SUM(dla.total) AS nombre_d_entreprises
FROM 
    dim_lieu_activite dla
JOIN
    dim_naf dn ON dla.code_activite = dn.code_5
JOIN 
    dim_lieu dl ON dla.code_commune = dl.code_parent
JOIN 
    departement d ON dl.code_dep = d.code
where
    dn.libelle_5  IN ${inputs.Activités.value}
    and d.code not in ('971','972','973','974','976')
GROUP BY 
    d.nom,d.code
ORDER BY 
    nombre_d_entreprises DESC
Limit 10
```




<DataTable data={Top_departement_with_activity_filtered} />

<AreaMap 
    data={Top_departement_with_activity_filtered} 
    areaCol=code
    name=areamap_1
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


## Les 10 villes les plus dynamiques pour l'activité sélectionnée

```sql Top_ville_with_activity_filtered
SELECT 
    dl.nom AS nom,
    dl.lat AS lat,
    dl.long AS long,
    dla.code_commune as code, 
    SUM(dla.total) AS nombre_d_entreprises
FROM 
    dim_lieu_activite dla
JOIN
    dim_naf dn ON dla.code_activite = dn.code_5
JOIN 
    dim_lieu dl ON dla.code_commune = dl.code_parent
JOIN 
    departement d ON dl.code_dep = d.code
where
    dn.libelle_5  IN ${inputs.Activités.value}
    and d.code not in ('971','972','973','974','976')
GROUP BY 
    dl.nom,dla.code_commune, dl.lat, dl.long
ORDER BY 
    nombre_d_entreprises DESC
Limit 10
```

<DataTable data={Top_ville_with_activity_filtered} />

<BubbleMap 
    data={Top_ville_with_activity_filtered} 
    lat=lat 
    long=long 
    size=nombre_d_entreprises
    value=nombre_d_entreprises 
    pointName=nom
    height=500
    opacity=0.5
    startingZoom=5
    tooltip={[
        {id: 'nom', showColumnName: false, valueClass: 'text-xl font-semibold'},
        {id: 'nombre_d_entreprises', fieldClass: 'text-[grey]', valueClass: 'text-[green]'}
    ]}
/>

# Queries

```sql list_activites
SELECT 
    distinct dn.libelle_5 as "activity", 
FROM 
    dim_naf dn
```

