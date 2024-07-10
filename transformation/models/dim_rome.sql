{{
    config(
        materialized='incremental',
        unique_key='code_3'
    )
}}

WITH
    grand_domaine AS (
        SELECT
            code, 
            libelle
        FROM
            {{ source('collecte_rome', 'rome_grand_domaine') }}
    ),
    domaine_professionnel AS (
        SELECT
            code,
            libelle
        FROM
            {{ source('collecte_rome', 'rome_domaine_professionnel') }}
    ),
    metier AS (
        SELECT
            code,
            libelle
        FROM
            {{ source('collecte_rome', 'rome_metier') }}
    )

SELECT
    metier.code AS code_3,
    metier.libelle AS libelle_3,
    domaine_professionnel.code AS code_2,
    domaine_professionnel.libelle AS libelle_2,
    grand_domaine.code AS code_1,
    grand_domaine.libelle AS libelle_1
FROM
    metier
JOIN
    domaine_professionnel ON domaine_professionnel.code = SUBSTRING(metier.code, 1, 3)
JOIN
    grand_domaine ON grand_domaine.code = SUBSTRING(metier.code, 1, 1)