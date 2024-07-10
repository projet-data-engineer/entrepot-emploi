import os
import duckdb

def chargement():

    with duckdb.connect() as con:

        con.install_extension("postgres")
        con.load_extension("postgres")

        con.sql("ATTACH 'dbname=entrepot user=entrepot password=entrepot host=entrepot' AS entrepot (TYPE POSTGRES);")

        
        # hierarchie
        con.sql( f"""
                
            CREATE OR REPLACE TABLE entrepot.naf2008_5_niveaux AS (
                SELECT
                    *
                FROM 
                    '{os.getenv('DESTINATION_NAF')}/naf2008_5_niveaux.csv'
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM entrepot.naf2008_5_niveaux")
        print(f"naf2008_5_niveaux: chargement de {con.fetchone()[0]} enregistrements !")

        # Niveau 1
        con.sql( f"""
                
            CREATE OR REPLACE TABLE entrepot.naf2008_liste_n1 AS (
                SELECT
                    *
                FROM 
                    '{os.getenv('DESTINATION_NAF')}/naf2008_liste_n1.csv'
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM entrepot.naf2008_liste_n1")
        print(f"naf2008_liste_n1: chargement de {con.fetchone()[0]} enregistrements !")

        # Niveau 2
        con.sql( f"""
                
            CREATE OR REPLACE TABLE entrepot.naf2008_liste_n2 AS (
                SELECT
                    *
                FROM 
                    '{os.getenv('DESTINATION_NAF')}/naf2008_liste_n2.csv'
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM entrepot.naf2008_liste_n2")
        print(f"naf2008_liste_n2: chargement de {con.fetchone()[0]} enregistrements !")

        # Niveau 3
        con.sql( f"""
                
            CREATE OR REPLACE TABLE entrepot.naf2008_liste_n3 AS (
                SELECT
                    *
                FROM 
                    '{os.getenv('DESTINATION_NAF')}/naf2008_liste_n3.csv'
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM entrepot.naf2008_liste_n3")
        print(f"naf2008_liste_n3: chargement de {con.fetchone()[0]} enregistrements !")

        # Niveau 4
        con.sql( f"""
                
            CREATE OR REPLACE TABLE entrepot.naf2008_liste_n4 AS (
                SELECT
                    *
                FROM 
                    '{os.getenv('DESTINATION_NAF')}/naf2008_liste_n4.csv'
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM entrepot.naf2008_liste_n4")
        print(f"naf2008_liste_n4: chargement de {con.fetchone()[0]} enregistrements !")

        # Niveau 5
        con.sql( f"""
                
            CREATE OR REPLACE TABLE entrepot.naf2008_liste_n5 AS (
                SELECT
                    *
                FROM 
                    '{os.getenv('DESTINATION_NAF')}/naf2008_liste_n5.csv'
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM entrepot.naf2008_liste_n5")
        print(f"naf2008_liste_n5: chargement de {con.fetchone()[0]} enregistrements !")