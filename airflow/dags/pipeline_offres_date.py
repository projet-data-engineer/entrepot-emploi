from datetime import datetime, timedelta
import pendulum

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator

from collecte import collecte_offres
from chargement import chargement_offres

local_tz = pendulum.timezone("Europe/Paris")

"""
Tous les jours à 01h00, requêtage api des offres créées J-1, puis chargement
"""

@dag(
    dag_id='pipeline_offres_date',
    description='Collecte des offres créées J-1',
    schedule_interval='0 1 * * *',
    start_date=datetime(2024, 5, 23, tzinfo=local_tz),
    catchup=False
)
def pipeline_offres_date():

    @task
    def date_creation(ds):
        return (datetime.strptime(ds, '%Y-%m-%d') + timedelta(days=-1)).strftime('%Y-%m-%d')

    @task
    def collecte(date_creation):
        collecte_offres.collecte_offres_date(date_creation=date_creation)

    @task
    def chargement(date_creation):
        chargement_offres.chargement_offres_date(date_creation=date_creation)

    transformation = BashOperator(

        task_id='transformation',
        bash_command="""
            cd /opt/airflow/modules/transformation
            dbt run --target prod
        """
    )

    _date_creation = date_creation()
    collecte(date_creation=_date_creation) >> chargement(date_creation=_date_creation) >> transformation


pipeline_offres_date()