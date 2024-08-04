from datetime import datetime, timedelta
import pendulum
import os
import pendulum

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.decorators import dag, task

from chargement import chargement_cog_carto, chargement_naf, chargement_rome, chargement_sirene, chargement_offres
from collecte import collecte_rome, collecte_sirene, collecte_offres, collecte_cog_carto

local_tz = pendulum.timezone("Europe/Paris")

@dag(
    dag_id='initialisation',
    description='Chargement dans entrepôt DuckDB nomenclature NAF',
    schedule=None,
    start_date=datetime(2024, 5, 23, tzinfo=local_tz),
    catchup=False
)
def initialisation():

    @task
    def nomenclature_naf():
        chargement_naf.chargement()

    with TaskGroup("cog_carto") as cog_carto:

        @task
        def telechargement():
            collecte_cog_carto.telechargement()

        @task
        def decompactage():
           collecte_cog_carto.decompactage()

        @task
        def filtrage():
            collecte_cog_carto.filtrage()

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


    with TaskGroup("nomenclature_rome") as nomenclature_rome:
        @task
        def collecte():
            collecte_rome.collecte()

        @task
        def chargement():
            chargement_rome.chargement()

        collecte() >> chargement()

    with TaskGroup("sirene") as sirene:

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

    """     
    debut = EmptyOperator(task_id='debut')
    fin = EmptyOperator(task_id='fin') 
    """

    with TaskGroup("offres_emploi_du_jour") as offres_emploi_du_jour:

        @task
        def date_creation(ds):
            return (datetime.strptime(ds, '%Y-%m-%d') + timedelta(days=-1)).strftime('%Y-%m-%d')

        @task
        def collecte(date_creation):
            collecte_offres.collecte_offres_date(date_creation=date_creation)

        _date_creation = date_creation()
        collecte(date_creation=_date_creation)

    with TaskGroup("stock_offres_chargement") as stock_offres_chargement:

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
    
    [nomenclature_naf(), cog_carto, nomenclature_rome, sirene, offres_emploi_du_jour] >> stock_offres_chargement

initialisation()