from datetime import datetime, timedelta
import pendulum

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator

from chargement import chargement_offres


local_tz = pendulum.timezone("Europe/Paris")

"""
Chargement et transformation du stock de fichiers brutes d'offres présents dans le dossier donnees_brutes.
"""

@dag(
    dag_id="pipeline_offres_stock",
    description="Chargement et transformation du stock de fichiers brutes d'offres présents dans le dossier donnees_brutes.",
    schedule=None,
    start_date=datetime(2024, 5, 23, tzinfo=local_tz),
    catchup=False
)
def pipeline_offres_stock():

    @task
    def chargement():
        chargement_offres.chargement_offres_stock()

    transformation = BashOperator(

        task_id='transformation',
        bash_command="""
            cd /opt/airflow/modules/transformation
            dbt run --target prod
        """
    )

    chargement() >> transformation

pipeline_offres_stock()