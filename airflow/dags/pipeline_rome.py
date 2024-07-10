from datetime import datetime
import pendulum

from airflow.decorators import dag, task
from collecte import collecte_rome
from chargement import chargement_rome


local_tz = pendulum.timezone("Europe/Paris")

"""
Collecte et chargement nomenclature 3 niveaux
"""

@dag(
    dag_id='pipeline_rome',
    description='Collecte 3 niveaux nomenclature ROME depuis api francetravail.io',
    schedule=None,
    start_date=datetime(2024, 5, 23, tzinfo=local_tz),
    catchup=False
)
def pipeline_rome():

    @task
    def collecte():
        collecte_rome.collecte()

    @task
    def chargement():
        chargement_rome.chargement()

    collecte() >> chargement()


pipeline_rome()