from datetime import datetime
import os
import glob
import pendulum
import shutil
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
import py7zr
import requests
from chargement import chargement_cog_carto

local_tz = pendulum.timezone("Europe/Paris")

@dag(
    dag_id='pipeline_cog_carto',
    description="Téléchargement limites géographiques COG CARTO 2024",
    schedule=None,
    start_date=datetime(2024, 5, 23, tzinfo=local_tz),
    catchup=False
)
def pipeline_cog_carto():

    @task
    def telechargement():

        nom_archive = os.path.join(os.getenv('DESTINATION_COG_CARTO'), f"{os.getenv('VERSION_COG_CARTO')}.7z")

        if not os.path.exists(nom_archive):

            print(f"Le fichier {nom_archive} absent. Téléchargement cog carto {os.getenv('VERSION_COG_CARTO')}...")
            data = requests.get(os.getenv('URI_COG_CARTO'))
            with open(nom_archive, 'wb') as file:
                file.write(data.content)

        else:
            print(f"Le fichier {nom_archive} est déjà présent")

    @task
    def decompactage():

        nom_archive = os.path.join(os.getenv('DESTINATION_COG_CARTO'), f"{os.getenv('VERSION_COG_CARTO')}.7z")
        with py7zr.SevenZipFile(nom_archive, mode='r') as z:
            z.extractall(os.getenv('DESTINATION_COG_CARTO'))

    @task
    def filtrage():

        termes = ['REGION','DEPARTEMENT', 'COMMUNE', 'ARRONDISSEMENT_MUNICIPAL']
        paths = glob.glob(f"{os.getenv('DESTINATION_COG_CARTO')}/**/*", recursive=True)
        files = [f for f in paths if os.path.isfile(f)]
        shape_files = [f for f in files if f.split(sep='/')[-1].split(sep='.')[0] in termes]

        destination = os.path.join(os.getenv('DESTINATION_COG_CARTO'), os.getenv('VERSION_COG_CARTO'))
        if not os.path.exists(destination):
            os.mkdir(destination)

        for file in shape_files:
            shutil.copy2(file, destination)

    @task
    def chargement_entrepot():
        chargement_cog_carto.chargement(os.getenv('VERSION_COG_CARTO'))

    nettoyage = BashOperator(

        task_id='nettoyage',
        bash_command="""
            rm -rf $DESTINATION_COG_CARTO/$VERSION_COG_CARTO
            rm -rf $DESTINATION_COG_CARTO/ADMIN-EXPRESS*
        """
    )

    telechargement() >> decompactage() >> filtrage() >> chargement_entrepot() >> nettoyage


pipeline_cog_carto()