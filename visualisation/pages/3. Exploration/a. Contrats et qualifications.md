## Les Contrats

Les contrats de travail en France se déclinent en plusieurs types et natures, chacun répondant à des besoins spécifiques tant pour les employeurs que pour les salariés. Parmi les principaux types de contrats, on retrouve le Contrat à Durée Indéterminée (CDI), le Contrat à Durée Déterminée (CDD) et le contrat de travail temporaire, ou intérim.

En ce qui concerne les natures de contrats, ils se distinguent de la manière suivante:
1. **Contrat de travail** : Inclut le CDI (contrat à durée indéterminée), offrant une stabilité à long terme, et le CDD (contrat à durée déterminée), utilisé pour des missions temporaires.

2. **Contrat d'apprentissage** : Permet aux jeunes de 16 à 29 ans de travailler tout en suivant une formation théorique, visant l'acquisition de compétences professionnelles et un diplôme.

3. **Emploi non salarié** : Regroupe les travailleurs indépendants, tels que les freelances et les professions libérales, qui n’ont pas de lien contractuel avec un employeur spécifique.

4. **Contrat de professionnalisation** : S'adresse aux jeunes et aux demandeurs d'emploi de plus de 26 ans, combinant travail et formation professionnelle pour obtenir une qualification.

5. **Insertion par l’activité économique (IAE)** : Offre des emplois aux personnes en difficulté pour favoriser leur insertion professionnelle, avec un accompagnement spécifique.

Chaque type de contrat répond à des besoins spécifiques en matière d'emploi, de formation et d'insertion professionnelle.

---

### Types de contrat 

La répartition des types de contrats proposés par France Travail est la suivante :

```sql Repartition_des_types_de_contrats

SELECT DISTINCT
    type_contrat AS pie,
    (SELECT COUNT(*) FROM fait_offre_emploi AS sub WHERE sub.type_contrat = fait_offre_emploi.type_contrat) AS count
FROM
    fait_offre_emploi
```



<ECharts config={
    {
        tooltip: {
            formatter: '{b}: {c} ({d}%)'
        },
        series: [
        {
          type: 'pie',
          data: [...Top_5_types_de_contrats],
        }
      ]
      }
    }
/>

Le graphique révèle une prépondérance des Contrats à Durée Indéterminée (CDI), des Missions Intermittentes (MIS) et des Contrats à Durée Déterminée (CDD) par rapport aux autres types de contrats. En comparaison, les autres contrats semblent beaucoup moins fréquents.

### Natures de contrats

La répartition des types de contrats proposés par France Travail est la suivante :

```sql Repartition_des_natures_de_contrats
SELECT DISTINCT
    nature_contrat AS pie,
    (SELECT COUNT(*) FROM fait_offre_emploi AS sub WHERE sub.nature_contrat = fait_offre_emploi.nature_contrat) AS count
FROM
    fait_offre_emploi
```

<BarChart 
    data={premier_nature_contrat}
    x=name
    y=count 
    swapXY=true
/>

<BarChart 
    data={reste_top_5_nature_contrat}
    x=name
    y=value 
    swapXY=true
/>

Les contrats de travail dominent largement le marché de l’emploi, représentant la majorité des constructions professionnelles. Cette situation reflète une concentration significative sur les formes classiques de travail salarié.

### Qualifications

la nomenclature des qualifications est la suivante:

| Numéro | Qualification |
|--------|--------|
| 1      | Manoeuvre      |
| 2      | Ouvrier Spécialisé      |
| 3      | Ouvrier qualifié P1,P2     |
| 4      | Ouvrier qualifié P3,P4      |
| 5      | Employé non qualifié      |
| 6      | Employé qualifié      |
| 7      | Technicien      |
| 8      | Agent de maîtrise      |
| 9      | Cadre      |


```sql Repartition_des_qualification_code

SELECT DISTINCT
    qualification_code AS pie,
    (SELECT COUNT(*) FROM fait_offre_emploi AS sub WHERE sub.qualification_code = fait_offre_emploi.qualification_code) AS count
FROM
    fait_offre_emploi
```

<BarChart 
    data={Repartition_des_qualification_code}
    x=pie
    y=count 
    swapXY=true
/>

On constate qu'en haut du classement on retrouve les employés qualifiés, les employés non qualifiés et les cadres.


# Queries

```sql Top_5_types_de_contrats
select pie as name, count as value
from ${Repartition_des_types_de_contrats}
Limit 5
```

```sql premier_nature_contrat
select
nature_contrat AS name,
count(*) as count
from entrepot_emploi.fait_offre_emploi
where nature_contrat = 'Contrat travail'
group by nature_contrat
```

```sql reste_top_5_nature_contrat
select pie as name, count as value
from (SELECT DISTINCT
    nature_contrat AS pie,
    (SELECT COUNT(*) FROM fait_offre_emploi AS sub WHERE sub.nature_contrat = fait_offre_emploi.nature_contrat) AS count
FROM
    fait_offre_emploi
WHERE nature_contrat <> 'Contrat travail')
Limit 5
```