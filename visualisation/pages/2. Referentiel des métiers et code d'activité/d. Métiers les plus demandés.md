Cette page permet d’explorer et de comprendre les métiers les plus demandés dans les offres d'emplois dans les département et régions sélectionnés. L’objectif est d’obtenir une meilleure vue d’ensemble sur les demandes d'emplois en utilisant le CODE ROME.

---


## Départements



```sql nombre_poste_rome_departement
WITH FOE as (
    SELECT nombre_postes, code_rome, lieu_travail_code
    FROM entrepot_emploi.fait_offre_emploi
),
DR as (
    SELECT code_3,libelle_3
    FROM entrepot_emploi.dim_rome
),
DL as (
    SELECT code, code_dep
    FROM entrepot_emploi.dim_lieu 
    WHERE code = code_parent
),
D as (
    SELECT code, nom
    FROM entrepot_emploi.departement
)
SELECT
    DR.libelle_3 as name,
    SUM(FOE.nombre_postes) as value
FROM
    FOE
JOIN DR ON FOE.code_rome = DR.code_3
JOIN DL ON FOE.lieu_travail_code = DL.code
JOIN D ON DL.code_dep = D.code
WHERE D.nom = '${inputs.Nom_du_departement.value}'
GROUP BY
    D.code, DR.libelle_3
ORDER BY
  value DESC
```

### Sélectionnez un département 

<Dropdown
    name=Nom_du_departement
    data={nom_departement}
    value=nom_departement
/>

<ECharts config={
    {
      title: {
        text: 'Postes les plus proposés dans le département sélectionné',
        left: 'center'
      },
        tooltip: {
            formatter: '{b}: {c}'
        },
      series: [
        {
          type: 'treemap',
          visibleMin: 10,
          label: {
            show: true,
            formatter: '{b}'
          },
          itemStyle: {
            borderColor: '#fff'
          },
          roam: false,
          nodeClick: false,
          data: nombre_poste_rome_departement.slice(0, 10),
          breadcrumb: {
            show: false
          }
        }
      ]
      }
    }
/>

---

## Régions


```sql nombre_poste_rome_region_2
WITH FOE as (
    SELECT nombre_postes, code_rome, lieu_travail_code
    FROM entrepot_emploi.fait_offre_emploi
),
DR as (
    SELECT code_3,libelle_3
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
    DR.libelle_3 as name,
    SUM(FOE.nombre_postes) as value
FROM
    FOE
JOIN DR ON FOE.code_rome = DR.code_3
JOIN DL ON FOE.lieu_travail_code = DL.code
JOIN R ON DL.code_reg = R.code
WHERE 
    R.nom = '${inputs.Nom_de_la_region.value}'
GROUP BY
    R.code, DR.libelle_3
ORDER BY
  value DESC
```

<Dropdown
    name=Nom_de_la_region
    data={nom_region}
    value=nom_region
/>

<ECharts config={
    {
      title: {
        text: 'Postes les plus présents dans la région sélectionnée',
        left: 'center'
      },
        tooltip: {
            formatter: '{b}: {c}'
        },
      series: [
        {
          type: 'treemap',
          visibleMin: 10,
          label: {
            show: true,
            formatter: '{b}'
          },
          itemStyle: {
            borderColor: '#fff'
          },
          roam: false,
          nodeClick: false,
          data: nombre_poste_rome_region_2.slice(0, 10),
          breadcrumb: {
            show: false
          }
        }
      ]
      }
    }
/>

# Queries 

```sql nom_departement
SELECT DISTINCT departement.nom  AS nom_departement
FROM departement
order by departement.nom asc;
```


```sql nom_region
SELECT DISTINCT region.nom  AS nom_region
FROM region
order by region.nom asc;
```

