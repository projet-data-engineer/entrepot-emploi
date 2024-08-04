## Top activités d'entreprise


<DataTable data={Top_code_naf} />

La majeure partie des activités d'entreprise se concentre dans le secteur des activités des agences de travail temporaire, représentant une part très significative par rapport aux autres secteurs. Les autres domaines, bien que variés, présentent un nombre d’offres beaucoup plus restreint, avec des services d'aide à la personne

---

## Top des domaines d'activite


<DataTable data={Top_div_activite} />

On observe que les activités de services administratifs et de soutien dominent largement le marché. Viennent ensuite la santé humaine et l’action sociale, suivies par les activités spécialisées, scientifiques et techniques, le commerce et la réparation automobile, et enfin l’industrie manufacturière. 

---

## Type d'expérience demandé


<DataTable data={Top_experience} />


Les débutants exigés (D) représentent la plus grande part des offres. Les offres requérant une expérience préalable (E) suivent de près. Enfin, les offres où une expérience est souhaitée (S) sont nettement moins nombreuses. Cela indique une forte demande pour les candidats débutants et expérimentés, tandis que les postes préférant une expérience sont rares.

---

## Top 5 des régions avec le plus d'offres


<DataTable data={Top_region} />

<AreaMap 
    data={Top_region} 
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

L’Auvergne-Rhône-Alpes et l’Île-de-France sont les régions offrant le plus grand nombre d’opportunités d’emploi. Pour avoir plus d'informations sur les emplois proposés dans les région, explorez les autres pages.


# Queries

```sql Top_code_naf
SELECT 
    dn.libelle_5 as  description, 
    COUNT(distinct foe.id) AS nombre_offre
FROM 
    fait_offre_emploi foe
JOIN 
    dim_naf dn ON foe.code_naf = dn.code_5
GROUP BY 
    dn.libelle_5, 
ORDER BY 
    nombre_offre DESC
LIMIT 5

```

```sql Top_div_activite
SELECT 
    dn.libelle_1 as "Domaine d'activite", 
    COUNT(distinct foe.id) AS nombre_offre
FROM 
    fait_offre_emploi foe
JOIN 
    dim_naf dn ON foe.code_naf = dn.code_5
GROUP BY 
    dn.libelle_1
ORDER BY 
    nombre_offre DESC
LIMIT 5

```


```sql Top_experience
SELECT 
    foe.experience_exige AS "Expérience exigée", 
    COUNT(DISTINCT foe.id) AS nombre_ids_distincts
FROM 
    fait_offre_emploi foe
GROUP BY 
    foe.experience_exige
ORDER BY 
    nombre_ids_distincts DESC
Limit 3
```

```sql Top_region
SELECT 
    r.nom AS nom,
    r.code as code, 
    COUNT(DISTINCT foe.id) AS nombre_d_offres
FROM 
    fait_offre_emploi foe
JOIN 
    dim_lieu dl ON foe.lieu_travail_code = dl.code_parent
JOIN 
    region r ON dl.code_reg = r.code
GROUP BY 
    r.nom,r.code
ORDER BY 
    nombre_d_offres DESC
Limit 5
```
