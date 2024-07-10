import duckdb
from fastapi.responses import JSONResponse
import pandas as pd
from contextlib import contextmanager
import pandas as pd
from fastapi.encoders import jsonable_encoder

class Db:

    """ Classe en charge de requêter l'entrepôt DuckDB"""

    @contextmanager
    def _connect(self):

        con = None
        try:
            con = duckdb.connect()
            yield con
        finally:
            if con:
                con.close()

    def get_dim_rome(self):

        query = f"""

            SELECT
                *
            FROM
                emploi.dim_rome
            ORDER BY
                code_3

        """

        with self._connect() as con:
            con.execute(query)
            data = con.cursor().execute(query).df().to_dict('records')

        return data
    

    def get_regions_geojson(self):

        with self._connect() as con:
            
            con.install_extension("postgres")
            con.load_extension("postgres")
            con.sql("ATTACH 'dbname=entrepot user=entrepot password=entrepot host=localhost' AS entrepot (TYPE POSTGRES);")

            con.install_extension("spatial")
            con.load_extension("spatial")

            query = """
                COPY (
                    SELECT 
                        code,
                        nom,    
                        ST_GeomFromText(frontiere) AS frontiere
                    FROM 
                        entrepot.emploi.region
                    WHERE
                        code NOT IN ('01','02','03','04','06')
                    ) TO './geojson/regions.geojson' WITH (FORMAT GDAL, DRIVER 'GeoJSON')

                """
            
            con.execute(query)
            
            with open('./geojson/regions.geojson') as f:
                geojson = f.read()

            return JSONResponse(content=jsonable_encoder(geojson))