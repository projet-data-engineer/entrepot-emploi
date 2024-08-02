import os
import duckdb

def chargement(version):

    shp_region=f"{os.path.join(os.getenv('DESTINATION_COG_CARTO'),version,'REGION.shp')}"
    shp_departement=f"{os.path.join(os.getenv('DESTINATION_COG_CARTO'),version,'DEPARTEMENT.shp')}"
    shp_commune=f"{os.path.join(os.getenv('DESTINATION_COG_CARTO'),version,'COMMUNE.shp')}"
    shp_arrondissement_municipal=f"{os.path.join(os.getenv('DESTINATION_COG_CARTO'),version,'ARRONDISSEMENT_MUNICIPAL.shp')}"

    with duckdb.connect() as con:

        con.install_extension("postgres")
        con.load_extension("postgres")
        con.sql("ATTACH 'dbname=entrepot user=entrepot password=entrepot host=entrepot' AS entrepot (TYPE POSTGRES);")

        con.install_extension("spatial")
        con.load_extension("spatial")

        geojson_file_path = os.path.join('/visualisation', 'region-metropole.geojson')

        SQL = f"""
        
            COPY (
                SELECT 
                    shp.insee_reg,
                    shp.nom,    
                    shp.geom
                FROM
                    '{shp_region}' AS shp
                WHERE
                    shp.insee_reg NOT IN ('01','02','03','04','06')
            ) 
            TO '{geojson_file_path}' 
            WITH (FORMAT GDAL, DRIVER 'GeoJSON', LAYER_CREATION_OPTIONS 'WRITE_BBOX=YES')

        """
        con.sql(SQL)


        con.sql( f"""
                
            CREATE OR REPLACE TABLE entrepot.cog_carto_region AS (
                SELECT
                    '{version}' AS version,
                    shp.insee_reg,
                    shp.nom,
                    ST_X(ST_Centroid(shp.geom)) AS long,
                    ST_Y(ST_Centroid(shp.geom)) AS lat  
                FROM 
                    '{shp_region}' AS shp
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM entrepot.cog_carto_region")
        print(f"\n\nChargement de {con.fetchone()[0]} regions !\n\n")

        """
        Export de certaines métadonnées et de la géométrie dans un fichier GeoJSON departement-metropole.geojson
        """
        geojson_file_path = os.path.join('/visualisation', 'departement-metropole.geojson')

        SQL = f"""
        
            COPY (
                SELECT 
                    shp.insee_dep,
                    shp.nom,
                    shp.geom
                FROM 
                    '{shp_departement}' AS shp
                WHERE
                    shp.insee_reg NOT IN ('01','02','03','04','06')
            ) 
            TO '{geojson_file_path}' 
            WITH (FORMAT GDAL, DRIVER 'GeoJSON', LAYER_CREATION_OPTIONS 'WRITE_BBOX=YES')

        """
        con.sql(SQL)


        con.sql( f"""
                
            CREATE OR REPLACE TABLE entrepot.cog_carto_departement AS (
                SELECT
                    '{version}' AS version,
                    shp.insee_dep,
                    shp.insee_reg,
                    shp.nom,
                    ST_X(ST_Centroid(shp.geom)) AS long,
                    ST_Y(ST_Centroid(shp.geom)) AS lat
                FROM 
                    '{shp_departement}' AS shp
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM entrepot.cog_carto_departement")
        print(f"\n\nChargement de {con.fetchone()[0]} départements !\n\n")


        file_path = os.path.join('/visualisation', 'commune.geojson')

        SQL = f"""
        
            COPY (
                SELECT 
                    shp.insee_com,
                    shp.nom,
                    shp.geom
                FROM 
                    '{shp_commune}' AS shp
                WHERE
                    shp.insee_reg NOT IN ('01','02','03','04','06')
            ) 
            TO '{file_path}' 
            WITH (FORMAT GDAL, DRIVER 'GeoJSON', LAYER_CREATION_OPTIONS 'WRITE_BBOX=YES')

        """

        con.sql(SQL)



        con.sql( f"""
                
            CREATE OR REPLACE TABLE entrepot.cog_carto_commune AS (
                SELECT
                    '{version}' AS version,
                    shp.insee_com,
                    shp.insee_dep,
                    shp.insee_reg,
                    shp.nom,
                    shp.population,
                    ST_X(ST_Centroid(shp.geom)) AS long,
                    ST_Y(ST_Centroid(shp.geom)) AS lat
                FROM 
                    '{shp_commune}' AS shp
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM entrepot.cog_carto_commune")
        print(f"\n\nChargement de {con.fetchone()[0]} communes !\n\n")


        file_path = os.path.join('/visualisation', 'arrondissement_municipal.geojson')

        SQL = f"""
        
            COPY (
                SELECT 
                    shp.insee_arm,
                    shp.nom,
                    shp.geom
                FROM 
                    '{shp_arrondissement_municipal}' AS shp
            ) 
            TO '{file_path}' 
            WITH (FORMAT GDAL, DRIVER 'GeoJSON', LAYER_CREATION_OPTIONS 'WRITE_BBOX=YES')

        """

        con.sql(SQL)


        con.sql( f"""
                
            CREATE OR REPLACE TABLE entrepot.cog_carto_arrondissement_municipal AS (
                SELECT
                    '{version}' AS version,
                    shp.insee_arm,
                    shp.insee_com,
                    shp.nom,
                    shp.population,
                    ST_X(ST_Centroid(shp.geom)) AS long,
                    ST_Y(ST_Centroid(shp.geom)) AS lat
                FROM 
                    '{shp_arrondissement_municipal}' AS shp
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM entrepot.cog_carto_arrondissement_municipal")
        print(f"\n\nChargement de {con.fetchone()[0]} communes !\n\n")