import os
import duckdb
from zipfile import ZipFile

def decompactage(yyyy_mm):

    nom_archive=f"{os.getenv('DESTINATION_SIRENE')}/etablissements_sirene_{yyyy_mm}.zip"

    with ZipFile(nom_archive, 'r') as f:
        f.extractall(path=os.getenv('DESTINATION_SIRENE'))

def chargement(yyyy_mm):

    csv=f"{os.path.join(os.getenv('DESTINATION_SIRENE'),'StockEtablissement_utf8.csv')}"

    with duckdb.connect() as con:

        con.install_extension("postgres")
        con.load_extension("postgres")
        con.sql("ATTACH 'dbname=entrepot user=entrepot password=entrepot host=entrepot' AS entrepot (TYPE POSTGRES);")

        SQL = f"""
            CREATE OR REPLACE TABLE entrepot.sirene_etablissement AS (
                SELECT
                    '{yyyy_mm}' AS version, 
                    e.codeCommuneEtablissement,
                    e.activitePrincipaleEtablissement
                FROM 
                    '{csv}' AS e
                WHERE
                    e.etatAdministratifEtablissement = 'A'
            )
        """

        con.sql(SQL)

        con.execute("SELECT COUNT(*) FROM entrepot.sirene_etablissement")
        print(f"\n\n{con.fetchone()[0]} enregistrements chargés !\n\n")

    os.remove(csv)