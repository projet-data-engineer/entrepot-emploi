import json
import os
import time
import requests

"""
# 
# API Rome francetravail.io
# Collecte de la nomenclature ROME: 3 niveaux Grands Domaines > Domaines professionnels > métiers
# Dénormalisation des 3 niveaux dans un fichier rome.json
#
"""


def authenticate(identifiant_client, cle_secrete):

    url = 'https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/partenaire'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}    

    params = {
        'grant_type': 'client_credentials',
        'scope': 'api_rome-metiersv1 nomenclatureRome',
        'client_id': identifiant_client,
        'client_secret': cle_secrete
    }

    response = requests.post(url=url,data=params,headers=headers)
    response = json.loads(response.text)
    return response['access_token']


def get_data(url, access_token):

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url=url, headers=headers)

    while response.status_code == 429:            
            
        retry_after = response.headers['Retry-After']
        time.sleep(int(retry_after))
        response = requests.get(url=url,headers=headers) 

    response.encoding = 'utf-8'
    return response.text



def collecte():
  
    FRANCETRAVAIL_ID_CLIENT = os.getenv("FRANCETRAVAIL_ID_CLIENT")
    FRANCETRAVAIL_CLE_SECRETE = os.getenv("FRANCETRAVAIL_CLE_SECRETE")

    access_token = authenticate(FRANCETRAVAIL_ID_CLIENT, FRANCETRAVAIL_CLE_SECRETE)
    url_rome = f"{os.getenv('FRANCETRAVAIL_HOST')}/partenaire/rome-metiers/v1/metiers"

    grand_domaine = json.loads(get_data(url=f"{url_rome}/grand-domaine", access_token=access_token))
    domaine_professionnel = json.loads(get_data(url=f"{url_rome}/domaine-professionnel", access_token=access_token))
    metier = json.loads(get_data(url=f"{url_rome}/metier", access_token=access_token))

    path = os.getenv('DESTINATION_ROME')
    if not os.path.exists(path):
        os.mkdir(path)
        
    grand_domaine_path = os.path.join(path, 'grand_domaine.json')
    domaine_professionnel_path = os.path.join(path, 'domaine_professionnel.json')
    metier_path = os.path.join(path, 'metier.json')

    with open(grand_domaine_path, 'w') as output_file:
        json.dump(grand_domaine, output_file, indent=2, ensure_ascii=False)

    with open(domaine_professionnel_path, 'w') as output_file:
        json.dump(domaine_professionnel, output_file, indent=2, ensure_ascii=False)

    with open(metier_path, 'w') as output_file:
        json.dump(metier, output_file, indent=2, ensure_ascii=False)