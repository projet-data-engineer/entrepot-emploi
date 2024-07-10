import os
import duckdb

def chargement(date_creation):

    file_path = os.path.join(os.getenv('DESTINATION_OFFRE_EMPLOI'), f'offres-{date_creation}.json')

    with duckdb.connect() as con:

        con.install_extension("postgres")
        con.load_extension("postgres")

        con.sql("ATTACH 'dbname=entrepot user=entrepot password=entrepot host=entrepot' AS entrepot (TYPE POSTGRES);")

        SQL = f"""
        
            CREATE OR REPLACE TABLE entrepot.offre_emploi AS (
                SELECT 
                id,
                CAST(dateCreation AS DATE) AS date_creation,
                lieuTravail.commune AS lieu_travail_code,
                lieuTravail.latitude AS lieu_travail_latitude,
                lieuTravail.longitude AS lieu_travail_longitude,
                codeNAF AS code_naf,
                romeCode AS code_rome,
                entreprise.entrepriseAdaptee AS entreprise_adaptee,
                typeContrat AS type_contrat,
                natureContrat AS nature_contrat,
                experienceExige AS experience_exige,
                alternance AS alternance,
                nombrePostes AS nombre_postes,
                accessibleTH AS accessible_TH,
                CAST(qualificationCode AS VARCHAR) AS qualification_code 
            FROM 
                '{file_path}'
            )

        """
        con.sql(SQL)

        con.execute("SELECT COUNT(*) FROM entrepot.offre_emploi")    
        print(f"\n\n{con.fetchone()[0]} enregistrements chargés !\n\n")