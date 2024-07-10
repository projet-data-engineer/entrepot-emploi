
--
-- chargement_geojson_visualisation.sql: pour création manuelle des fichiers de contours geojson.
--

install postgres;
load postgres;
install spatial;
load spatial;
ATTACH 'dbname=entrepot user=entrepot password=entrepot host=localhost' AS entrepot (TYPE POSTGRES);


COPY (
  SELECT 
    code,
    nom,    
    ST_GeomFromText(frontiere)
  FROM 
    entrepot.emploi.region
  WHERE
    code NOT IN ('01','02','03','04','06')
) TO 'C:\privé\DE\entrepot-emploi\visualisation\static\region-metropole.geojson' WITH (FORMAT GDAL, DRIVER 'GeoJSON');


COPY (
  SELECT 
    code,
    nom,
    code_reg,
    ST_GeomFromText(frontiere)
  FROM 
    entrepot.emploi.departement
  WHERE
    code_region NOT IN ('01','02','03','04','06')
) TO 'C:\privé\DE\entrepot-emploi\visualisation\static\departement-metropole.geojson' WITH (FORMAT GDAL, DRIVER 'GeoJSON');

COPY (
  SELECT 
    code,
    code_parent,
    code_dep,
    code_reg,
    nom,
    population,
    ST_GeomFromText(frontiere)
  FROM 
    entrepot.emploi.dim_lieu
  WHERE
    code_reg NOT IN ('01','02','03','04','06')
) TO 'C:\privé\DE\entrepot-emploi\visualisation\static\commune_arrondissement-municipal.geojson' WITH (FORMAT GDAL, DRIVER 'GeoJSON');