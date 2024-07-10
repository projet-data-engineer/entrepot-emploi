import os
import requests

def telechargement_stock_etablissement(yyyy_mm):
  
    nom_archive=f"{os.getenv('DESTINATION_SIRENE')}/etablissements_sirene_{yyyy_mm}.zip"

    data = requests.get(os.getenv('URI_STOCK_ETABLISSEMENT'))

    with open(nom_archive, 'wb')as file:
        file.write(data.content)