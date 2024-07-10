import os
import duckdb

def chargement():

    with duckdb.connect() as con:

        con.install_extension("postgres")
        con.load_extension("postgres")
        con.sql("ATTACH 'dbname=entrepot user=entrepot password=entrepot host=entrepot' AS entrepot (TYPE POSTGRES);")

        file_path = os.path.join(os.getenv('DESTINATION_ROME'), 'domaine_professionnel.json')

        SQL = f"""
            CREATE OR REPLACE TABLE entrepot.rome_domaine_professionnel AS (
                SELECT
                    code,
                    libelle
                FROM 
                    '{file_path}'
            )
        """

        con.sql(SQL)

        con.execute("SELECT COUNT(*) FROM entrepot.rome_domaine_professionnel")
        print(f"\n\n{con.fetchone()[0]} enregistrements chargés !\n\n")


        file_path = os.path.join(os.getenv('DESTINATION_ROME'), 'grand_domaine.json')

        SQL = f"""
            CREATE OR REPLACE TABLE entrepot.rome_grand_domaine AS (
                SELECT
                    code,
                    libelle
                FROM 
                    '{file_path}'
            )
        """

        con.sql(SQL)

        con.execute("SELECT COUNT(*) FROM entrepot.rome_grand_domaine")
        print(f"\n\n{con.fetchone()[0]} enregistrements chargés !\n\n")


        file_path = os.path.join(os.getenv('DESTINATION_ROME'), 'metier.json')

        SQL = f"""
            CREATE OR REPLACE TABLE entrepot.rome_metier AS (
                SELECT
                    code,
                    libelle
                FROM 
                    '{file_path}'
            )
        """

        con.sql(SQL)

        con.execute("SELECT COUNT(*) FROM entrepot.rome_metier")
        print(f"\n\n{con.fetchone()[0]} enregistrements chargés !\n\n")