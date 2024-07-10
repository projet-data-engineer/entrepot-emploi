# Maps


## Population par arrondissement à Lyon

```sql population_lyon

select 
    code,nom,population
from
    entrepot_emploi.dim_lieu
where 
    code_parent = '69123'
```

<DataTable data={population_lyon}/>

<AreaMap 
    data={population_lyon} 
    areaCol=code
    geoJsonUrl='/arrondissement_municipal.geojson'
    geoId=INSEE_ARM
    value=population
    height=500
    opacity=0.5
    tooltip={[
        {id: 'nom', showColumnName: false, valueClass: 'text-xl font-semibold'},
        {id: 'population', fieldClass: 'text-[grey]', valueClass: 'text-[green]'}
    ]}
/>


## Répartition des offres d'emploi de Data Engineer par département

```sql metier_rome_departement
with 
lieu as (
    select code,code_dep,population from entrepot_emploi.dim_lieu where code = code_parent
),
departement as (
    select code,nom,lat,long from entrepot_emploi.departement
)
select
	departement.code,
	departement.nom,
	departement.lat,
	departement.long,
	count(*) as nombre,
    sum(lieu.population) as population
from 
	departement
join
	lieu on departement.code = lieu.code_dep
join
	entrepot_emploi.fait_offre_emploi as fait_offre_emploi on fait_offre_emploi.lieu_travail_code = lieu.code
where
	fait_offre_emploi.code_rome = 'M1811'
    and departement.code not in ('971','972','973','974','976')
group by
	departement.code,departement.nom,departement.lat,departement.long
```

<DataTable data={metier_rome_departement}/>

### AreaMap

<AreaMap 
    data={metier_rome_departement} 
    areaCol=code
    geoJsonUrl='/departement-metropole.geojson'
    geoId=INSEE_DEP
    value=nombre
    height=500
    opacity=0.5
    tooltip={[
        {id: 'nom', showColumnName: false, valueClass: 'text-xl font-semibold'},
        {id: 'nombre', fieldClass: 'text-[grey]', valueClass: 'text-[green]'}
    ]}
/>

### BaseMap pour repésenter plusieurs dimensions. 

- les aires représente la population de chaque département, les bulles le nombre d'offres
- voir pour meilleure palette de couleurs

<BaseMap>
    <Areas 
        data={metier_rome_departement} 
        areaCol=code
        geoJsonUrl='/departement-metropole.geojson'
        geoId=INSEE_DEP
        value=population
        colorPalette={['yellow','orange','red','darkred']}
        tooltip={[
            {id: 'nom', showColumnName: false, valueClass: 'text-xl font-semibold'},
            {id: 'population', fieldClass: 'text-[grey]', valueClass: 'text-[green]'}
        ]}
    />

    <Bubbles
        data={metier_rome_departement} 
        lat=lat 
        long=long 
        size=nombre
        value=nombre 
        pointName=nom
        height=500
    />

</BaseMap>



