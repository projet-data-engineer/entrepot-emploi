import glob
import os
import shutil
import py7zr
import requests

def telechargement():

    nom_archive = os.path.join(os.getenv('DESTINATION_COG_CARTO'), f"{os.getenv('VERSION_COG_CARTO')}.7z")

    if not os.path.exists(nom_archive):

        print(f"Le fichier {nom_archive} absent. Téléchargement cog carto {os.getenv('VERSION_COG_CARTO')}...")
        data = requests.get(os.getenv('URI_COG_CARTO'))
        with open(nom_archive, 'wb') as file:
            file.write(data.content)

    else:
        print(f"Le fichier {nom_archive} est déjà présent")

def decompactage():

    nom_archive = os.path.join(os.getenv('DESTINATION_COG_CARTO'), f"{os.getenv('VERSION_COG_CARTO')}.7z")
    with py7zr.SevenZipFile(nom_archive, mode='r') as z:
        z.extractall(os.getenv('DESTINATION_COG_CARTO'))

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