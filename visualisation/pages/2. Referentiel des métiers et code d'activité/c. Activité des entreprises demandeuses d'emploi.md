Cette page permet d’explorer et de comprendre les activités d’entreprise les plus fréquentes parmis les entreprises demandeuses d'emploi dans un département, ainsi que les domaines d’activité les plus représentés. L’objectif est d’obtenir une meilleure vue d’ensemble de l’activité professionnelle dans le département sélectionné, en utilisant le CODE NAF.




## Départements

```sql activite_par_departement
SELECT
    dn.libelle_5 AS name,
    SUM(dla.total) AS value
FROM
    dim_lieu dl
JOIN
    dim_lieu_activite dla ON dl.code = dla.code_commune 
Join
    departement ON dl.code_dep = departement.code
Join
    dim_naf dn ON dla.code_activite = dn.code_5
WHERE
    departement.nom='${inputs.Nom_du_departement.value}'
GROUP BY
    dl.nom, dn.libelle_5
ORDER BY
    value DESC;
```

```sql domaine_activite_par_departement

SELECT
    dn.libelle_1 AS name,
    SUM(dla.total) AS value
FROM
    dim_lieu dl
JOIN
    dim_lieu_activite dla ON dl.code = dla.code_commune 
JOIN
    departement ON dl.code_dep = departement.code
JOIN
    dim_naf dn ON dla.code_activite = dn.code_5
WHERE
    departement.nom = '${inputs.Nom_du_departement.value}'
GROUP BY
    dn.libelle_1
ORDER BY
    value DESC;
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
        text: 'Activités les plus présentes dans le département sélectionné',
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
          data: activite_par_departement.slice(0, 10),
          breadcrumb: {
            show: false
          }
        }
      ]
      }
    }
/>



<ECharts config={
  {
    title: {
      text: 'Domaines d activité les plus présents dans le département sélectionné',
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
        data: domaine_activite_par_departement.slice(0, 10),
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




```sql activite_par_region
SELECT
    dn.libelle_5 AS name,
    SUM(dla.total) AS value
FROM
    dim_lieu dl
JOIN
    dim_lieu_activite dla ON dl.code = dla.code_commune 
Join
    region ON dl.code_reg = region.code
Join
    dim_naf dn ON dla.code_activite = dn.code_5
WHERE
    region.nom='${inputs.Nom_de_la_region.value}'
GROUP BY
    region.nom, dn.libelle_5
ORDER BY
    value DESC;

``` 


```sql domaine_activite_par_region
SELECT
    dn.libelle_1 AS name,
    SUM(dla.total) AS value
FROM
    dim_lieu dl
JOIN
    dim_lieu_activite dla ON dl.code = dla.code_commune 
Join
    region ON dl.code_reg = region.code
Join
    dim_naf dn ON dla.code_activite = dn.code_5
WHERE
    region.nom='${inputs.Nom_de_la_region.value}'
GROUP BY
    dl.code_reg, name
ORDER BY
    value DESC;

```

<Dropdown
    name=Nom_de_la_region
    data={nom_region}
    value=nom_region
/>




<ECharts config={
    {
      title: {
        text: 'Activités les plus présentes dans la région sélectionnée',
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
          data: activite_par_region.slice(0, 10),
          breadcrumb: {
            show: false
          }
        }
      ]
      }
    }
/>





<ECharts config={
    {
      title: {
        text: 'Domaines d activité les plus présents dans la région sélectionnée',
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
          data: domaine_activite_par_region.slice(0, 10),
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

