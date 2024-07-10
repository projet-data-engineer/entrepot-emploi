# Aperçu des données

## Table region

### Schéma

```sql schema_region

SELECT 
  column_name, 
  data_type
FROM 
  information_schema.columns
WHERE 
  table_name = 'region';
```

<DataTable data={schema_region}/>

### Aperçu

```sql head_region

SELECT 
  *
FROM 
  region
LIMIT 3
```

<DataTable data={head_region}/>


## Table departement

### Schéma

```sql schema_departement

SELECT 
  column_name, 
  data_type
FROM 
  information_schema.columns
WHERE 
  table_name = 'departement';
```

<DataTable data={schema_departement}/>

### Aperçu

```sql head_departement

SELECT 
  *
FROM 
  departement
LIMIT 3
```

<DataTable data={head_departement}/>