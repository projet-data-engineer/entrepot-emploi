from datetime import datetime
import os
import pendulum

from airflow.decorators import dag, task
from collecte import collecte_sirene
from chargement import chargement_sirene

local_tz = pendulum.timezone("Europe/Paris")

@dag(
    dag_id='pipeline_sirene',
    description="Téléchargement fichier stock etablissements Sirene mensuel",
    schedule=None,
    start_date=datetime(2024, 5, 23, tzinfo=local_tz),
    catchup=False
)
def pipeline_sirene():

    @task
    def calcul_mois_annee(ds):
        return datetime.strptime(ds, '%Y-%m-%d').strftime('%Y-%m')    
    
    ## Si zip inexistant
    @task
    def telechargement_stock_etablissement(yyyy_mm):

        nom_archive=f"{os.getenv('DESTINATION_SIRENE')}/etablissements_sirene_{yyyy_mm}.zip"

        if not os.path.exists(nom_archive):
            print(f"Le fichier {nom_archive} absent. Téléchargement stock Sirene {yyyy_mm}...")
            collecte_sirene.telechargement_stock_etablissement(yyyy_mm=yyyy_mm)
        else:
            print(f"Le fichier {nom_archive} est déjà présent")

    @task
    def decompactage_archive(yyyy_mm):
        chargement_sirene.decompactage(yyyy_mm=yyyy_mm)

    @task
    def chargement_entrepot(yyyy_mm):
        chargement_sirene.chargement(yyyy_mm=yyyy_mm)

    _yyyy_mm = calcul_mois_annee()
    telechargement_stock_etablissement(yyyy_mm=_yyyy_mm) >> decompactage_archive(yyyy_mm=_yyyy_mm) >> chargement_entrepot(yyyy_mm=_yyyy_mm)

pipeline_sirene()